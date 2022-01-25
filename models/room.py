import random
from typing import Optional

START_TIME=8
FINISH_TIME=18

class Room(object):
    def __init__(self, name:str, capacity:int=50):
        self.name = name
        self.capacity = capacity
        self.reservation = {
            "Monday": {"8-9": "", "9-10": "", "10-11": "", "11-12": "", "12-13": "", "13-14": "", "14-15": "", "15-16": "", "16-17": "", "17-18": ""},
            "Tuesday": {"8-9": "", "9-10": "", "10-11": "", "11-12": "", "12-13": "", "13-14": "", "14-15": "", "15-16": "", "16-17": "", "17-18": ""},
            "Wednesday": {"8-9": "", "9-10": "", "10-11": "", "11-12": "", "12-13": "", "13-14": "", "14-15": "", "15-16": "", "16-17": "", "17-18": ""},
            "Thursday": {"8-9": "", "9-10": "", "10-11": "", "11-12": "", "12-13": "", "13-14": "", "14-15": "", "15-16": "", "16-17": "", "17-18": ""},
            "Friday": {"8-9": "", "9-10": "", "10-11": "", "11-12": "", "12-13": "", "13-14": "", "14-15": "", "15-16": "", "16-17": "", "17-18": ""}
        }
        
    
    def change_day_randomize(self, course_code):
        random_day = random.choice(list(self.reservation.keys()))
        course_days = self.get_course_days(course_code=course_code)
        random_course_day = random.choice(list(course_days.keys()))
        
        while random_day == random_course_day:
            random_day = random.choice(list(self.reservation.keys()))
            random_course_day = random.choice(list(course_days.keys()))

        temp_day = self.reservation.get(random_day)
        self.reservation[random_day] = self.reservation[random_course_day]
        self.reservation[random_course_day] = temp_day
    
    def exchange_course_day(self, other_room, course_one, course_two):
        temp_data = self.reservation.copy()
        room_courses_day = self.get_course_days(course_one)
        other_room_courses_day = other_room.get_course_days(course_two)
        for day, hours in other_room_courses_day.items():
            for hour in hours:
                temp_data[day][hour] = course_two
                
        for day, hours in room_courses_day.items():
            for hour in hours:
                other_room.reservation[day][hour] = course_one
        
        self.reservation = temp_data
            
            
    def __reserve(self, day:str, course_code, start_time:int):
        self.reservation.get(day, {})[f"{start_time}-{start_time + 1}"] = course_code
        
    def random_date(self, course_code:str, hour:int) -> Optional[bool]:
        random_day = self._random_day(hour=hour)
        left_hour = hour
        if random_day is None:
            left_hour = self._random_available(course_code, hour)
            if  left_hour is None:
                return None
            
        limit = 10
        time_limit = 5
        start_time = self.__random_start_time(False, random_day)
        while left_hour > 0:
           
          
            random_day = self._random_day(left_hour)
           
            while random_day is None:
                limit = limit - 1
                random_day = self._random_day(hour=hour)
                if limit == 0:
                    limit = 10
                    break
            if random_day is None:
                left_hour = self._random_available(course_code, left_hour)             
                if left_hour is None:    
                    return None
            else:
                start_time = self.__random_start_time(False, random_day)
                if time_limit == 0:
                    return None
                if start_time is None:
                    time_limit = time_limit - 1
                    continue  
            
                self.__reserve(random_day, course_code, start_time)
                left_hour = left_hour - 1
        
        return True
                
    def get_course_days(self, course_code) -> dict:
        result = {}
        for key, val in self.reservation.items():
            hours = []
            for key2, val2 in val.items():
                if val2 == course_code:
                    hours.append(key2)
            result[key] = hours
        
        return result
    
    def _random_available(self, course_code ,hour:int) -> Optional[str]:
        daylist = []
        day = random.choice(list(self.reservation.keys()))
        left_hours = hour
        prevent_infinitive_loop = 0
        daylist.append(day)
        
        while self.__is_day_full(day=day, hour=hour) is False or left_hours != 0:
            for key, value in self.reservation.get(day, {}).items():
                if value == "":
                   self.reservation[day][key] = course_code
                   left_hours = left_hours - 1
            day = random.choice(list(self.reservation.keys()))
            if day not in daylist:
                daylist.append(day)
                prevent_infinitive_loop = prevent_infinitive_loop + 1
            if prevent_infinitive_loop == 4:

                return None
                
        return left_hours
    
    def __random_start_time(self, first:bool, day:str):
        start_time = random.randint(START_TIME, 17)
        day_hours = self.reservation.get(day, {})
        temp_hours = list(day_hours.keys())
        is_found = False
        while is_found is False:
            if f"{start_time}-{start_time+1}" in temp_hours:
                temp_index = temp_hours.index(f"{start_time}-{start_time+1}")
                temp_hours.pop(temp_index)

            if start_time +1 <= FINISH_TIME and day_hours[f"{start_time}-{start_time+1}"] == "":
                is_found = True
            
            if is_found is False:
                start_time = random.randint(START_TIME, FINISH_TIME)
            
            if len(temp_hours) == 0:
                return None
        
        return start_time
        
    def _random_day(self, hour:int) -> Optional[str]:
        daylist = []
        day = random.choice(list(self.reservation.keys()))
        
        prevent_infinitive_loop = 0
        daylist.append(day)
        
        while self.__is_day_full(day=day, hour=hour) is False:
            
            day = random.choice(list(self.reservation.keys()))
            if day not in daylist:
                daylist.append(day)
                prevent_infinitive_loop = prevent_infinitive_loop + 1
            if prevent_infinitive_loop == 4:

                return None
                
        return day

    def __is_day_full(self, day:str, hour:int) -> bool:
        empty_count = 0
        for value in self.reservation.get(day, {}).values():
            if value == "":
                empty_count = empty_count +1
                
        if empty_count >= hour:
            return empty_count
        return 0
        
    
    