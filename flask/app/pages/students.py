from flask import Blueprint, render_template, request
from templates import *
from globals import *
from utils import *
from session import UserData

students_bp = Blueprint("students", __name__)

class StudentData:
    def __init__(self, role, user_data: UserData):
        self.role = role
        self.name = camel_case_name(f"{user_data.name} {user_data.surname}")
        self.page = user_data.personal_page

    def has_role(self, role: str):
        if role == "all":
            return True
        else:
            return self.role == role
        
    def name_filter(self, name: str):
        if name is None or name == "":
            return True
        return str.lower(name) in str.lower(self.name)

@students_bp.route("/students")
def settings():
    role = request.args.get("role")
    if role is None:
        role = "all"
    name = request.args.get("name")
    
    students = get_student_data()
    students = filter(lambda x: x.name_filter(name), students)
    students = filter(lambda x: x.has_role(role), students)
    students = sorted(students, key=lambda x: x.name)
    students = ''.join([ render_student(x) for x in students ])

    page = render_template("/students/main.html", users=students)
    return render_skeleton(f"{app_config["blog-name"]} - Students", page)

def render_student(data: StudentData):
    if data.role == "mantainer":
        icon = render_template("/students/icon_mantainer.html")
    elif data.role == "representative":
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

    return [ StudentData(get_student_role(user, roles), user) for user in user_management.get_all_users() if user.public ]

def get_student_role(user_data: UserData, roles: dict) -> str:
    if user_data.email in roles['mantainers']:
        return 'mantainer'
    elif user_data.email in roles['representatives']:
        return 'representative'
    else:
        return 'student'