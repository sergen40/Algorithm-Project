import random
from models.course import Course
from models.room import Room
from population import Chromosome, Population



class GeneticAlgorithm(object):
    def __init__(self, generation:Population):
        self.generation = generation
        self.generation.fitness = self.calculate_fitness()
    
    def generate(self):
        new_generation = Population(self.generation.population_data, [])
        for _ in range(len(self.generation.schedules)):
            parent_one = random.choice(self.generation.schedules)
            parent_two = random.choice(self.generation.schedules)
            new_generation.schedules.append(self.crossover_population(parent_one, parent_two))
        self.generation = new_generation
        self.generation.fitness = self.calculate_fitness()
    
    def crossover_population(self, parent_one:Chromosome, parent_two:Chromosome):
        prob = random.random()
        
        if prob < 0.90:
            child_chromosome = Chromosome(
                room_id=parent_one.room_id,
                course_id=parent_two.course_id
            )
           
            room_one:Room = list(filter(lambda item: item.name == parent_one.room_id, self.generation.population_data["rooms"]))[0]
            room_two:Room = list(filter(lambda item: item.name == parent_two.room_id, self.generation.population_data["rooms"]))[0]
           
            room_one.exchange_course_day(room_two, parent_one.course_id, parent_two.course_id)
           
            return child_chromosome
            
        else:
            return self.mutate_population(random.choice([parent_one, parent_two]))
            

    def mutate_population(self,parent_one:Chromosome):
        parent_room:Room = list(filter(lambda item: item.name == parent_one.room_id, self.generation.population_data['rooms']))[0]
    
        parent_room.change_day_randomize(parent_one.course_id)
        
        return Chromosome(
            room_id=parent_room.name,
            course_id=parent_one.course_id
        )
    
    def calculate_fitness(self):
        calculate_fitness = 0
        for room_one in self.generation.population_data["rooms"]:
            for room_two in self.generation.population_data["rooms"]:
                if room_one == room_two:
                    continue
                calculate_fitness = calculate_fitness + (self.__compare_room_day(room_one, room_two) / len(self.generation.population_data["rooms"]))
        return 1 / ((1.0 * calculate_fitness + 1))
    
    def __compare_student_schedule(self, course_one:Course, course_two:Course):
        check_student = False
        for val in course_one.group:
            if val in course_two.group:
                check_student = True
                break
        
        return check_student
          
    def __compare_room_day(self ,room_one:Room, room_two:Room):
        conflict = 0
        for key, value in room_one.reservation.items():
            for hours, course in room_two.reservation[key].items():
                if course != "":
                    course_obj:Course = list(filter(lambda item: item.code == course, self.generation.population_data["courses"]))
                    if len(course_obj):
                        course_obj = course_obj[0]
                        must_courses = course_obj.get_must_courses(course_obj.semester, self.generation.population_data["courses"])
                        if value[hours] == course:
                            conflict = conflict + 0.001
                            if course in must_courses:
                                conflict = conflict + 1
                    if course != "":
                        course_obj_two:Course = list(filter(lambda item: item.code == value[hours], self.generation.population_data["courses"]))
                        if len(course_obj_two):
                            course_obj_two = course_obj_two[0]
                            if course_obj_two.lecturer == course_obj.lecturer:
                                conflict = conflict + 1
                            if self.__compare_student_schedule(course_obj_two, course_obj):
                                conflict = conflict + 0.001
        return conflict