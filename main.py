from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from enum import Enum
from app.models import Student, Course, Faculty
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import aliased

app = FastAPI()

class Tags(Enum):
    students = "students"
    faculties = "faculties"
    courses = "courses" 

class CourseCreateRequest(BaseModel):
    name:str
    s_id:int
    f_id:int

class CourseReadResponse(BaseModel):
    c_id:int
    c_name:str
    student_id:int
    faculty_id:int

class StudentCreateRequest(BaseModel):
    name: str
    email: str

class StudentReadResponse(BaseModel):
    s_id: int
    s_name: str
    s_email: str

class FacultyCreateRequest(BaseModel):
    name: str

class FacultyReadResponse(BaseModel):
    f_id:int
    f_name:str


# async def get_students(db: AsyncSession):
#     result = await db.execute()


@app.get("/")
async def home():
    return {"message" : "welcome to university"}

#  students

@app.get("/students/", tags=[Tags.students])
async def get_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student))
    return result.scalars().all()

@app.get("/student-course/", tags=[Tags.students])
async def students_with_courses(db: AsyncSession = Depends(get_db)):
    stu = aliased(Student, name="stu")
    cou = aliased(Course, name="cou")
    result = await db.execute(
        select(stu.s_id,
               stu.s_name,
               stu.s_email,
               cou.c_id,
               cou.c_name
        ).join(cou, cou.student_id == stu.s_id, isouter=True)
    )
    rows = result.all()
    data = {}

    # for row in rows:
    #     if row.s_id not in data:
    #         data[row.s_id] = {
    #             "s_id": row.s_id,
    #             "s_name": row.s_name,
    #             "s_email": row.s_email,
    #             "courses": [],
    #         }
    #     if row.c_id:
    #         data[row.s_id]["courses"].append({
    #             "c_id": row.c_id,
    #             "c_name": row.c_name,
    #         })

    return list(data.values())


@app.get("/students/{student_id}", response_model=StudentReadResponse, tags=[Tags.students], deprecated=True)
async def get_student(student_id: int, db:AsyncSession = Depends(get_db)):
    student = await db.execute(select(Student).where(Student.s_id==student_id))
    return student.scalar()
    # student = result.scalar_one_or_none() - better altrnative


@app.post("/students/", tags=[Tags.students], response_model =StudentReadResponse, status_code=201)
async def create_student(student_req: StudentCreateRequest, db: AsyncSession = Depends(get_db)):
    db_student = Student(s_name = student_req.name, s_email=student_req.email)
    db.add(db_student)
    try:
        await db.commit()
        await db.refresh(db_student)
        return db_student
    
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email must be unique")
    

    
@app.delete("/students/{student_id}", tags=[Tags.students])
async def remove_student(student_id: int, db:AsyncSession=Depends(get_db)):
    result = await db.execute(select(Student).where(Student.s_id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    await db.delete(student)
    await db.commit()
    return {
        "message": "Student deleted successfully",
        "student_id": student_id,
    }

# ? faculties

@app.get("/faculties/", tags=[Tags.faculties])
async def get_faculties(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Faculty))
    return result.scalars().all()

@app.get("/faculty-course/", tags=[Tags.faculties])
async def faculties_with_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Faculty.f_id,
               Faculty.f_name,
               Course.c_id,
               Course.c_name
        ).join(Course, Course.faculty_id == Faculty.f_id, isouter=True)
    )
    rows = result.all()
    data = {}

    # for row in rows:
    #     if row.f_id not in data:
    #         data[row.f_id] = {
    #             "f_id": row.f_id,
    #             "f_name": row.f_name,
    #             "courses": [],
    #         }
    #     if row.c_id:
    #         data[row.f_id]["courses"].append({
    #             "c_id": row.c_id,
    #             "c_name": row.c_name,
    #         })

    return list(data.values())



@app.get("/faculty/{faculty_id}", response_model=FacultyReadResponse, tags=[Tags.faculties], deprecated=True)
async def get_faculty(faculty_id: int, db:AsyncSession = Depends(get_db)):
    faculty = await db.execute(select(Faculty).where(Faculty.f_id==faculty_id))
    return faculty.scalars().first()


@app.post("/faculties/", tags=[Tags.faculties], response_model =FacultyReadResponse, status_code=201)
async def create_faculties(faculty_req: FacultyCreateRequest, db: AsyncSession = Depends(get_db)):
    db_faculty = Faculty(f_name = faculty_req.name)
    db.add(db_faculty)
    await db.commit()
    await db.refresh(db_faculty)
    return db_faculty

@app.delete("/faculty/{faculty_id}", tags=[Tags.faculties])
async def remove_facuty(faculty_id: int, db:AsyncSession=Depends(get_db)):
    result = await db.execute(select(Faculty).where(Faculty.f_id == faculty_id))
    faculty = result.scalar_one_or_none()
    if not faculty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty not found")
    await db.delete(faculty)
    await db.commit()
    return {
        "message": "faculty deleted successfully",
        "student_id": faculty_id,
    }


# courses

@app.post("/courses/", tags=[Tags.courses], response_model =CourseReadResponse, status_code=201)
async def create_course(course_req: CourseCreateRequest, db: AsyncSession = Depends(get_db)):
    db_course = Course(c_name = course_req.name, student_id = course_req.s_id, faculty_id = course_req.f_id)
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course

@app.get("/courses/", tags=[Tags.courses])
async def get_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course))
    return result.scalars().all()

@app.delete("/course/{course_id}", tags=[Tags.courses])
async def remove_course(course_id: int, db:AsyncSession=Depends(get_db)):
    result = await db.execute(select(Course).where(Course.c_id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="course not found")
    await db.delete(course)
    await db.commit()
    return {
        "message": "course deleted successfully",
        "student_id": course_id,
    }







    

    
    
    