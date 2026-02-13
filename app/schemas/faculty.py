from pydantic import BaseModel

class CourseResponse(BaseModel):
    c_id: int
    c_name: str


class FacultyCreateRequest(BaseModel):
    name: str

class FacultyReadResponse(BaseModel):
    f_id:int
    f_name:str

class FacultyWithCoursesesponse(BaseModel):
    f_id: int
    f_name: str
    courses: list[CourseResponse]



class FacultyCourseRow(BaseModel):
    f_id: int
    f_name: str
    c_id: int | None
    c_name: str | None