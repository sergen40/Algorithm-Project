import random
from config import all_dict, department_course_obj
from models.room import Room
from models.course import Course
from models.department import Deparment

def initialize(population_data, is_autumn=True):
    chromosomes = []
    dept:list[Deparment] = population_data.get("departments")
    temp_semester = 1 if is_autumn else 2
    for dep in range(0, len(dept)):
        courses = list(filter(lambda item: item.semester % 2 != 0, department_course_obj[dept[dep].code]))
        for course in range(0, len(courses)):
            random_room:Room = random.choice(population_data.get("rooms"))
            course_obj:Course = list(filter(lambda item: item.code == courses[course].code, population_data.get("courses")))[0]
            
            result = random_room.random_date(
                course_code=course_obj.code,
                hour=course_obj.hours
            )
            
            if result is not None:
                chromosome = Chromosome(
                    random_room.name,
                    course_obj.code,
                )
                chromosomes.append(chromosome)
            else:
                temp_room = population_data.get("rooms").copy()
                while result is None:
                    if len(temp_room) > 0:
                        random_room:Room = random.choice(temp_room)
                        room_index = temp_room.index(random_room)
                        temp_room.pop(room_index)
                        result = random_room.random_date(
                            course_code=course_obj.code,
                            hour=course_obj.hours
                        )
                    else:
                        print("Not enough room")
                        return None
                    
                                        
                if result is not None:
                    chromosome = Chromosome(
                        random_room.name,
                        course_obj.code,
                    )
                    chromosomes.append(chromosome)
    
    return chromosomes        
    
              
              
class Chromosome(object):
    def __init__(self, room_id, course_id):
        self.room_id = room_id
        self.course_id = course_id
        

class Population(object):
    def __init__(self, pop_date = None, schedule_data = None):
        self.fitness = -1 
        self.population_data = all_dict.copy() if pop_date is None else pop_date
        self.schedules = self.init_schedule() if schedule_data is None else schedule_data
    
    
    def init_schedule(self):
        schedule_result = initialize(self.population_data)
        return schedule_result
            