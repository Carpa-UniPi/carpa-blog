from flask import Blueprint, render_template, request
from typing import Self
from enum import Flag, auto
from templates import *
from globals import *
from utils import *
from session import UserData

students_bp = Blueprint("students", __name__)

class StudentRole(Flag):
    STUDENT = auto()
    MANTAINER = auto()
    REPRESENTATIVE = auto()

    def serialize(self) -> str:
        if StudentRole.STUDENT | StudentRole.MANTAINER | StudentRole.REPRESENTATIVE in self:
            return "all"
        elif StudentRole.STUDENT in self:
            return "student"
        elif StudentRole.MANTAINER in self:
            return "mantainer"
        elif StudentRole.REPRESENTATIVE in self:
            return "representative"
        
    def deserialize(value: str) -> Self:
        if value == "all":
            return StudentRole.STUDENT | StudentRole.MANTAINER | StudentRole.REPRESENTATIVE
        elif value == "student":
            return StudentRole.STUDENT
        elif value == "mantainer":
            return StudentRole.MANTAINER
        elif value == "representative":
            return StudentRole.REPRESENTATIVE
        else:
            raise RuntimeError("StudentRole deserialization failure")
        
    def try_deserialize(value: str) -> Self:
        try:
            return StudentRole.deserialize(value)
        except:
            return StudentRole.STUDENT | StudentRole.MANTAINER | StudentRole.REPRESENTATIVE

class StudentData:
    def __init__(self, role: StudentRole, name: str, page: str):
        self.role = role
        self.name = name
        self.page = page

    def from_user_data(role: StudentRole, user_data: UserData) -> Self:
        return StudentData(role, camel_case_name(f"{user_data.name} {user_data.surname}"), user_data.personal_page)

    def has_role(self, role: StudentRole):
        return self.role in role
        
    def name_filter(self, name: str):
        if name is None or name == "":
            return True
        return str.lower(name) in str.lower(self.name)
    
    def __repr__(self):
        return f"StudentData for '{self.name}' ({self.role})"

@students_bp.route("/students")
def settings():
    role = request.args.get("role")
    if role is None:
        role = "all"
    role = StudentRole.try_deserialize(role)
    name = request.args.get("name")
    
    students = get_student_data()
    students = filter(lambda x: x.name_filter(name), students)
    students = filter(lambda x: x.has_role(role), students)
    students = sorted(students, key=lambda x: x.name)
    students = ''.join([ render_student(x) for x in students ])

    page = render_template("/students/main.html", users=students)
    return render_skeleton(f"{app_config["blog-name"]} - Students", page)

def render_student(data: StudentData):
    if data.role == StudentRole.MANTAINER:
        icon = render_template("/students/icon_mantainer.html")
    elif data.role == StudentRole.REPRESENTATIVE:
        icon = render_template("/students/icon_representative.html")
    else:
        icon = render_template("/students/icon_student.html")

    return render_template("/students/student_tag.html",
                           icon= icon,
                           student_name= data.name,
                           personal_page= data.page,
                           ppage_class= "hidden" if data.page == "" or data.page is None else "")

def get_student_data():
    import json
    
    with open("/blog/data/students/roles.json", "r") as f:
        roles = json.loads(f.read())

    with open("/blog/data/students/extra.json", "r") as f:
        extra = json.loads(f.read())

    db_users = user_management.get_all_users()
    db_students = [ StudentData.from_user_data(get_student_role(user, roles), user)
                    for user in db_users if user.public ]
    extra_students = [ StudentData(StudentRole.deserialize(user['role']), user['full_name'], user['personal_page'])
                       for user in extra if next(filter(lambda x: user['email'] == x.email and x.public, db_users), None) is None ]
    return db_students + extra_students

def get_student_role(user_data: UserData, roles: dict) -> StudentRole:
    if user_data.email in roles['mantainers']:
        return StudentRole.MANTAINER
    elif user_data.email in roles['representatives']:
        return StudentRole.REPRESENTATIVE
    else:
        return StudentRole.STUDENT