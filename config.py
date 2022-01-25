import json
import random
from models import course, department, lecturer, room, student


student_id_start = {
    "CENG" : 1000,
    "MCE" : 2000,
    "CE" : 3000,
    #"MSE" : 4000,
    #"SENG" : 5000,
    #"EE" : 6000
}

department_course_obj = {
    "CENG": [],
    "MCE": [],
    "CE": [],
    "MSE": [],
    "SENG": [],
    "EE": []
}

students = {
    "CENG": [],
    "MCE": [],
    "CE": [],
    "MSE": [],
    "SENG": [],
    "EE": []
}


all_dict ={
    "courses": [],
    "departments": [],
    "lecturers": [],
    "rooms": [],
    "students": students
}


def read_file(file_path:str) -> dict:
    with open(file=file_path) as f:
        lines = f.read()
    
    return json.loads(lines)


def assign_objects():
    json_data = read_file("./deneme.json")
    
    for key, val in json_data.items():
        if key == "prof":
            for x in val:
                all_dict["lecturers"].append(lecturer.Lecturer(x.get("id")))
        elif key == "course":
            for x in val:
                all_dict["courses"].append(course.Course(
                    x.get("code"), 
                    x.get("semester"), 
                    random.randint(3, 5), 
                    x.get("course_capacity"),
                    x.get("elective"))
                )
        elif key == "room":
            for x in val:
                all_dict["rooms"].append(room.Room(x.get("name")))
        elif key == "department":
            for x in val:
                all_dict["departments"].append(department.Deparment(
                    x.get("name"),
                    x.get("code"),
                    x.get("courses")
                ))
        else:
            pass


def assing_course_obj_to_department():
    for value in all_dict["departments"]:
        for course in value.courses:
            department_course_obj[value.code].append(list(filter(lambda item: item.code == course, all_dict.get("courses")))[0])


def assign_lecturer_to_course():
    lecturers = all_dict["lecturers"]
    for value in all_dict["courses"]:
        random_lecturer = random.choice(lecturers)
        value.lecturer = random_lecturer

def generate_student(is_autumn=True):
    for key, value in student_id_start.items():
        temp_id_start_point = value
        temp_semester = 1 if is_autumn else 2
        for i in range(0, 200):
            if i > 0 and i % 50 == 0:
                temp_semester = temp_semester + 2
            temp_id_start_point = temp_id_start_point + 1
            print(temp_id_start_point)
            s = student.Student(
                temp_id_start_point,
                key,
                temp_semester
            )
            
            s.select_random_course(department_course_obj.get(key) ,all_dict.get("courses"))
            students[key].append(s)

def generate_random_room(count = 5):
    last_room:room.Room = all_dict["rooms"][len(all_dict["rooms"]) - 1]
    split_number = last_room.name.split("R")[1]
    for _ in range(count):
        all_dict["rooms"].append(room.Room(
            name=f"R{int(split_number)+1}"
        ))
    print(len(all_dict["rooms"]))

assign_objects()
assing_course_obj_to_department()
assign_lecturer_to_course()
generate_student()