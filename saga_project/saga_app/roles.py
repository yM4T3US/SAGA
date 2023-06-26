from rolepermissions.roles import AbstractUserRole

class Professor(AbstractUserRole):
    available_permissions = {
        "create_availability": True, 
        "create_schedule": True, 
        "access_courses": True,
        "schedule_an_appointment": True,
    }

class Student(AbstractUserRole):
    available_permissions = {
        "create_availability": False,
        "access_courses": True,
        "schedule_an_appointment": True,
        "create_availability": False, 
        "create_schedule": False, 
    }


