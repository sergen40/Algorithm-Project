import random
from models.course import Course
from population import Population
from genetic_algorithm import GeneticAlgorithm
from config import generate_random_room
POPULATION_SIZE = 1000
GENES = '01'



found = False
pop = Population()
while pop.schedules is None:
    generate_random_room()
    del pop
    print("new room")
    pop = Population()

algorithm = GeneticAlgorithm(pop)
generation_count = 0
while not found:
    
    if algorithm.generation.fitness > 0.90:
        found = True
        break
    print(f"Generation-{generation_count} fitness : {algorithm.generation.fitness}")
    algorithm.generate() # generate new generation
    generation_count = generation_count + 1
    
    print(f"Generation : {generation_count}")
    

for v in algorithm.generation.schedules:
    rooms = list(filter(lambda item: item.name == v.room_id, algorithm.generation.population_data.get("rooms")))
    for room in rooms:
        course_obj:Course = list(filter(lambda item: item.code == v.course_id, algorithm.generation.population_data.get("courses")))[0]
        print(f"{room.name}-{course_obj.code}-{course_obj.hours}" )
        string = [f"{key} - {value}\n" for key, value in room.get_course_days(v.course_id).items()]
        print(string)