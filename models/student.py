import random
from models import department
from models.course import Course

class Student(object):
    def __init__(self, id, department ,current_semester:int):
        self.id = id
        self.current_semester = current_semester
        self.department = department
        self.selected_courses = []

    def select_random_course(self, deparment_courses, all_courses):
        must_courses:list[Course] = Course.get_must_courses(self.current_semester, deparment_courses)
        self.selected_courses = self.selected_courses + must_courses
        for val in must_courses:
            val.group.append(self)
        selected_count = len(must_courses)
        
        if self.current_semester > 4:
            choice_upper = bool(random.getrandbits(1)) if self.current_semester < 7 else False
            choice_lower = bool(random.getrandbits(1))
            if choice_upper:
                random_upper = self.__select_random_upper(all_courses)
                self.selected_courses = self.selected_courses + random_upper
                selected_count = selected_count + len(random_upper)        
            elif choice_lower:
                random_lower = self.__select_random_lower(deparment_courses)
                self.selected_courses = self.selected_courses + random_lower
                selected_count = selected_count + len(random_lower)
        
        while selected_count < 6 and self.current_semester < 7:
            #print(self.id)
            self.selected_courses.append(random.choice(Course.get_upper_courses(self.current_semester, all_courses)))
            selected_count = selected_count + 1
       
        
        
    def __select_random_upper(self, courses):
        course_count = random.randint(1, 3)
        upper_courses = Course.get_upper_courses(self.current_semester, courses).copy()
        selected_upper_courses = []
        for _ in range(course_count):
            random_course:Course = random.choice(upper_courses)
            while random_course.course_capacity == len(random_course.group):
                #print(random_course.code)
                random_course_index = upper_courses.index(random_course)
                upper_courses.pop(random_course_index)
                random_course = random.choice(upper_courses)
            random_course.group.append(self)
            random_course_index = upper_courses.index(random_course)
            selected_upper_courses.append(upper_courses.pop(random_course_index))
                
        return selected_upper_courses
    
    def __select_random_lower(self, courses):
        course_count = random.randint(1, 3)
        lower_courses = Course.get_lower_courses(self.current_semester, courses).copy()
        selected_lower_courses = []
        for _ in range(course_count):
            random_course:Course = random.choice(lower_courses)
            while random_course.course_capacity == len(random_course.group):
                #print(random_course.code)
                random_course_index = lower_courses.index(random_course)
                lower_courses.pop(random_course_index)
                random_course = random.choice(lower_courses)
            random_course_index = lower_courses.index(random_course)
            random_course.group.append(self)
            selected_lower_courses.append(lower_courses.pop(random_course_index))
        return selected_lower_courses
                
    

        

        
        
