from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func, update
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Student, Course, Association
from sqlalchemy.orm import load_only, with_expression, selectinload, contains_eager, joinedload
from app.schemas.student import StudentWithCoursesResponse, StudentReadResponse, StudentCreateRequest, StudentBulkCreateRequest
from app.services.student_service import *

router = APIRouter()

@router.get("/students/", tags=["student"])
async def get_students(db: AsyncSession = Depends(get_db)):
    # result = await db.execute(select(Student))
    # return result.scalars().all()
    return await get_students_service(db)

@router.get("/students/basic-loading-demo", tags=["student"])
async def get_students_basic(db: AsyncSession = Depends(get_db)):
    # result = await db.execute(
    #     select(Student).options(
    #         load_only(Student.s_id), 
    #         with_expression(Student.s_name,func.upper(Student.s_name)),
    #         selectinload(Student.courses).defer(Course.faculty_id)
    #     )
    # )
    # return result.scalars().all()
    return await get_students_basic_service(db)


@router.get("/student-course/joins", tags=["student"])
# async def students_with_courses_joins(db: AsyncSession = Depends(get_db)) -> list[StudentCourseRow]:
async def students_with_courses_joins(db: AsyncSession = Depends(get_db)):
    # result = await db.execute(
    #     select(Student).join(Student.courses).options(contains_eager(Student.courses).defer(Course.faculty_id))
    # )
    # return result.unique().scalars().all()
    return await students_with_courses_joins_service(db)


@router.get("/student-course/orm",tags=["student"])
async def students_with_courses_orm(db: AsyncSession = Depends(get_db)) -> list[StudentWithCoursesResponse]:
    # result = await db.execute(
    #     select(Student).options(selectinload(Student.courses))
    # )
    # return result.scalars().all()
    return await students_with_courses_orm_service(db)



@router.get("/students-course/joined", tags=["student"])
async def get_students_joined(db: AsyncSession = Depends(get_db)):
    # stmt = (
    #     select(Student)
    #     .options(
    #         joinedload(Student.courses)
    #         .joinedload(Course.faculty)
    #     )
    # )
    # result = await db.execute(stmt)
    # return result.scalars().unique().all()
    return await get_students_joined_service(db)


# @app.get("/student-faculty/orm", tags=[Tags.students])
# async def students_with_faculties(db: AsyncSession = Depends(get_db)):
#     result = await db.execute(
#         select(Student).options(load_only(Student.s_id, Student.s_name),selectinload(Student.faculties)
#                                 )  # student.faculty_association -> association.faculty
#     )
#     return result.scalars().all()


@router.get("/student-faculty/orm", tags=["student"])
async def students_with_faculties(db: AsyncSession = Depends(get_db)):
    # result = await db.execute(
    #     select(Student).options(load_only(Student.s_id, Student.s_name),selectinload(Student.faculty_associations)
    #                             .selectinload(Association.faculty)
    #                             )  # student.faculty_association -> association.faculty
    # )
    # return result.scalars().all()
    return await students_with_faculties_service(db)

@router.get("/students/{student_id}", tags=["student"],)
async def get_student(student_id: int, db:AsyncSession = Depends(get_db))->StudentReadResponse:
    # student = await db.execute(select(Student).where(Student.s_id==student_id))
    # return student.scalar()
    student = await get_student_service(student_id, db)
    if not student:
        raise HTTPException(status_code=404, detail="student not found")
    return student


@router.post("/students/", tags=["student"], status_code=201)
async def create_student(student_req: StudentCreateRequest, db: AsyncSession = Depends(get_db))->StudentReadResponse:
    # async with db.begin_nested():
    #     db_student = Student(s_name = student_req.name, s_email=student_req.email)
    #     db.add(db_student)
    # return db_student
    student = await create_student_service(student_req, db)
    return student


@router.post("/students/bulk", tags=["student"], status_code=201)
async def create_bulk_student(students: StudentBulkCreateRequest, db: AsyncSession = Depends(get_db)):
    # db_students = [Student(s_name = s.name, s_email = s.email) for s in student.students]
    # db.add_all(db_students)
    # return db_students
    return await create_bulk_student_service(students, db)


@router.put("/students/{student_id}", tags=["student"])
async def update_student(student_id: int,student_req: StudentCreateRequest,db: AsyncSession = Depends(get_db)):
    # stmt = (update(Student)
    #     .where(Student.s_id == student_id)
    #     .values(s_name=student_req.name,s_email=student_req.email)
    # )
    # result = await db.execute(stmt)
    # if result.rowcount == 0:
    #     raise HTTPException(status_code=404, detail="Student not found")
    # return {"message": "Student updated successfully"}
    return await update_student_service(student_id,student_req, db)


@router.delete("/students/{student_id}", tags=["student"])
async def remove_student_cascade(student_id: int, db:AsyncSession=Depends(get_db)):
    # student = await db.get(Student, student_id)
    # if not student:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    # await db.delete(student)
    # # await db.commit()
    # return {
    #     "message": "Student deleted successfully",
    #     "student_id": student_id,
    # }
    return await remove_student_cascade_service(student_id, db)