from pydantic import BaseModel


class CourseResponse(BaseModel):
    c_id: int
    c_name: str

class StudentCreateRequest(BaseModel):
    name: str
    email: str

class StudentBulkCreateRequest(BaseModel):
    students: list[StudentCreateRequest]

class StudentReadResponse(BaseModel):
    s_id: int 
    s_name: str
    s_email: str

class StudentWithCoursesResponse(BaseModel):
    s_id: int
    s_name: str
    s_email: str 
    courses: list[CourseResponse]

class FacultyReadResponse(BaseModel):
    f_id:int
    f_name:str

class StudentWithFacultiesResponse(BaseModel):
    s_id: int
    s_name: str
    s_email: str
    faculties: list[FacultyReadResponse]