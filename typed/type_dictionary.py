from typing import TypedDict

class School(TypedDict):

    name:str
    age:int

new_school:School = {'name':'Rao Sahab','age':25}

print(new_school)