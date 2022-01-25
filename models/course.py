class Course(object):
    def __init__(self, code:str, semester:int, credit:int, course_capacity ,elective:bool = False):
        self.hours = credit
        self.credit = credit
        self.lecturer = None
        self.code = code
        self.course_capacity = course_capacity
        self.semester = semester
        self.elective = elective
        self.group = []
     
    @staticmethod   
    def get_must_courses(semester, course_list):
        if semester % 2 == 0:
            return list(filter(lambda item: (item.semester == semester and item.elective == False), course_list))
        else:
            return list(filter(lambda item: (item.semester == semester and item.elective == False), course_list))
            
    
    @staticmethod
    def get_upper_courses(semester, course_list):
        if semester % 2 == 0:
            return list(filter(lambda item: (item.semester > semester and item.semester % 2 == 0 and item.elective == True), course_list))
        else:
            return list(filter(lambda item: (item.semester > semester and item.semester % 2 != 0 and item.elective == True), course_list))
            
    @staticmethod
    def get_lower_courses(semester, course_list):
        if semester % 2 == 0:
            return list(filter(lambda item: (item.semester < semester and item.semester % 2 == 0), course_list))
        else:
            return list(filter(lambda item: (item.semester < semester and item.semester % 2 != 0), course_list))
            