from fastapi import FastAPI, HTTPException, status, Depends, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from enum import Enum
from app.models import Student, Course, Faculty, Association
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import aliased, selectinload, load_only, with_expression, contains_eager,joinedload
from fastapi.responses import JSONResponse


app = FastAPI()

# globally exception handler
@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": "Email already exists"
        },
    )

class Tags(Enum):
    students = "students"
    faculties = "faculties"
    courses = "courses" 
    associations = "associations"

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

class StudentBulkCreateRequest(BaseModel):
    students: list[StudentCreateRequest]

class StudentReadResponse(BaseModel):
    s_id: int
    s_name: str
    s_email: str

class FacultyCreateRequest(BaseModel):
    name: str

class FacultyReadResponse(BaseModel):
    f_id:int
    f_name:str

class CourseResponse(BaseModel):
    c_id: int
    c_name: str

class StudentWithCoursesResponse(BaseModel):
    s_id: int
    s_name: str
    s_email: str 
    courses: list[CourseResponse]

class FacultyWithCoursesesponse(BaseModel):
    f_id: int
    f_name: str
    courses: list[CourseResponse]


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

#  column loading options
@app.get("/students/basic", tags=[Tags.students])
async def get_students_basic(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Student).options(
            load_only(Student.s_id), 
            with_expression(Student.s_name,func.upper(Student.s_name)),
            selectinload(Student.courses).defer(Course.faculty_id)
        )
    )
    return result.scalars().all()


class StudentCourseRow(BaseModel):
    s_id: int
    s_name: str
    s_email: str
    c_id: int | None
    c_name: str | None

# contain
@app.get("/student-course/joins", tags=[Tags.students])
# async def students_with_courses_joins(db: AsyncSession = Depends(get_db)) -> list[StudentCourseRow]:
async def students_with_courses_joins(db: AsyncSession = Depends(get_db)):
    # stu = aliased(Student, name="stu")
    # cou = aliased(Course, name="cou")
    # result = await db.execute(
    #     select(stu.s_id,
    #            stu.s_name,
    #            stu.s_email,
    #            cou.c_id,
    #            cou.c_name
    #     ).join(cou, cou.student_id == stu.s_id, isouter=True)
        # ).join(cou.student, isouter=True)
        # )

    result = await db.execute(
        select(Student).join(Student.courses).options(contains_eager(Student.courses).defer(Course.faculty_id))
    )
    return result.unique().scalars().all()



@app.get("/student-course/orm",tags=[Tags.students])
async def students_with_courses_orm(db: AsyncSession = Depends(get_db)) -> list[StudentWithCoursesResponse]:
    result = await db.execute(
        select(Student).options(selectinload(Student.courses))
    )
    return result.scalars().all()



@app.get("/students/joined")
async def get_students_joined(db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Student)
        .options(
            joinedload(Student.courses)
            .joinedload(Course.faculty)
        )
    )
    result = await db.execute(stmt)
    return result.scalars().unique().all()

class StudentWithFacultiesResponse(BaseModel):
    s_id: int
    s_name: str
    s_email: str
    faculties: list[FacultyReadResponse]


# @app.get("/student-faculty/orm", tags=[Tags.students])
# async def students_with_faculties(db: AsyncSession = Depends(get_db)):
#     result = await db.execute(
#         select(Student).options(load_only(Student.s_id, Student.s_name),selectinload(Student.faculties)
#                                 )  # student.faculty_association -> association.faculty
#     )
#     return result.scalars().all()


@app.get("/student-faculty/orm", tags=[Tags.students])
async def students_with_faculties(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Student).options(load_only(Student.s_id, Student.s_name),selectinload(Student.faculty_associations)
                                .selectinload(Association.faculty)
                                )  # student.faculty_association -> association.faculty
    )
    return result.scalars().all()



@app.get("/students/{student_id}", tags=[Tags.students], deprecated=True)
async def get_student(student_id: int, db:AsyncSession = Depends(get_db))->StudentReadResponse:
    student = await db.execute(select(Student).where(Student.s_id==student_id))
    return student.scalar()
    # student = result.scalar_one_or_none() - better altrnative


@app.post("/students/", tags=[Tags.students], status_code=201)
async def create_student(student_req: StudentCreateRequest, db: AsyncSession = Depends(get_db)) -> StudentReadResponse:
    db_student = Student(s_name = student_req.name, s_email=student_req.email)
    db.add(db_student)
    # try:
    #     await db.commit()
    await db.flush()
    await db.refresh(db_student)
    return db_student
    
    # except IntegrityError:
    #     await db.rollback()
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email must be unique")
    
    
    
@app.post("/students/bulk", tags=[Tags.students], status_code=201)
async def create_bulk_student(student: StudentBulkCreateRequest, db: AsyncSession = Depends(get_db)) -> list[StudentReadResponse]:
    db_students = [Student(s_name = s.name, s_email = s.email) for s in student.students]
    db.add_all(db_students)
    # try:
    #     await db.commit()
        # await db.refresh(db_students)
    await db.flush()
    return db_students
    # except IntegrityError:
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail="One or more emails already exist",
    #     )

    
@app.delete("/students/{student_id}", tags=[Tags.students])
async def remove_student(student_id: int, db:AsyncSession=Depends(get_db)):
    result = await db.execute(select(Student).where(Student.s_id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    await db.delete(student)
    # await db.commit()
    return {
        "message": "Student deleted successfully",
        "student_id": student_id,
    }

# ? faculties

@app.get("/faculties/", tags=[Tags.faculties])
async def get_faculties(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Faculty))
    return result.scalars().all()

class FacultyCourseRow(BaseModel):
    f_id: int
    f_name: str
    c_id: int | None
    c_name: str | None

@app.get("/faculty-course/joins", tags=[Tags.faculties])
async def faculties_with_courses(db: AsyncSession = Depends(get_db))-> list[FacultyCourseRow]:
    result = await db.execute(
        select(Faculty.f_id,
               Faculty.f_name,
               Course.c_id,
               Course.c_name
        ).join(Course, Course.faculty_id == Faculty.f_id, isouter=True)
    )
    return result.all()
    # data = {}
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
    # return list(data.values())

@app.get("/faculty-course/orm",tags=[Tags.faculties])
async def faculties_with_courses_orm(db: AsyncSession = Depends(get_db)) -> list[FacultyWithCoursesesponse]:
    result = await db.execute(
        select(Faculty).options(selectinload(Faculty.courses))
    )
    return result.scalars().all()



@app.get("/faculty/{faculty_id}", tags=[Tags.faculties], deprecated=True)
async def get_faculty(faculty_id: int, db:AsyncSession = Depends(get_db)) -> FacultyReadResponse:
    faculty = await db.execute(select(Faculty).where(Faculty.f_id==faculty_id))
    return faculty.scalar()


@app.post("/faculties/", tags=[Tags.faculties], status_code=201)
async def create_faculties(faculty_req: FacultyCreateRequest, db: AsyncSession = Depends(get_db)) -> FacultyReadResponse:
    db_faculty = Faculty(f_name = faculty_req.name)
    db.add(db_faculty)
    await db.flush()
    await db.refresh(db_faculty)
    return db_faculty

@app.delete("/faculty/{faculty_id}", tags=[Tags.faculties])
async def remove_facuty(faculty_id: int, db:AsyncSession=Depends(get_db)):
    result = await db.execute(select(Faculty).where(Faculty.f_id == faculty_id))
    faculty = result.scalar_one_or_none()
    if not faculty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty not found")
    await db.delete(faculty)
    # await db.commit()
    return {
        "message": "faculty deleted successfully",
        "student_id": faculty_id,
    }


# courses

@app.post("/courses/", tags=[Tags.courses],  status_code=201)
async def create_course(course_req: CourseCreateRequest, db: AsyncSession = Depends(get_db)) -> CourseReadResponse:
    db_course = Course(c_name = course_req.name, student_id = course_req.s_id, faculty_id = course_req.f_id)
    db.add(db_course)
    # await db.commit()
    await db.flush()
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
    # await db.commit()
    return {
        "message": "course deleted successfully",
        "student_id": course_id,
    }


class AssociationCreateRequest(BaseModel):
    s_id:int
    f_id:int

class AssociationReadResponse(BaseModel):
    association_id:int
    student_id:int
    faculty_id:int

@app.post("/association/", tags=[Tags.associations],  status_code=201)
async def create_course(asso_req: AssociationCreateRequest, db: AsyncSession = Depends(get_db)) -> AssociationReadResponse:
    db_asso = Association(student_id = asso_req.s_id, faculty_id = asso_req.f_id)
    db.add(db_asso)
    # await db.commit()
    await db.flush()
    await db.refresh(db_asso)
    return db_asso




    

    
    
    