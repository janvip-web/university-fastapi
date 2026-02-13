from pydantic import BaseModel

class CourseCreateRequest(BaseModel):
    name:str
    s_id:int
    f_id:int

class CourseReadResponse(BaseModel):
    c_id:int
    c_name:str
    student_id:int
    faculty_id:int

