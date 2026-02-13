from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Student, Course, Association
from sqlalchemy.orm import load_only,with_expression,selectinload, contains_eager, joinedload
from sqlalchemy import func, update, select
from app.schemas.student import StudentCreateRequest, StudentBulkCreateRequest, StudentReadResponse
from fastapi import HTTPException, status

async def get_students_service(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Student).offset(skip).limit(limit))
    return result.scalars().all()

async def get_students_basic_service(db: AsyncSession):
    result = await db.execute(
        select(Student).options(
            load_only(Student.s_id), 
            with_expression(Student.s_name,func.upper(Student.s_name)),
            selectinload(Student.courses).defer(Course.faculty_id)
        )
    )
    return result.scalars().all()

async def students_with_courses_joins_service(db: AsyncSession):
    result = await db.execute(
        select(Student).join(Student.courses).options(contains_eager(Student.courses).defer(Course.faculty_id))
    )
    return result.unique().scalars().all()


async def students_with_courses_orm_service(db: AsyncSession):
    result = await db.execute(
        select(Student).options(selectinload(Student.courses))
    )
    return result.scalars().all()


async def get_students_joined_service(db: AsyncSession):
    stmt = (
        select(Student)
        .options(
            joinedload(Student.courses)
            .joinedload(Course.faculty)
        )
    )
    result = await db.execute(stmt)
    return result.scalars().unique().all()


async def students_with_faculties_service(db: AsyncSession):
    result = await db.execute(
        select(Student).options(load_only(Student.s_id, Student.s_name),selectinload(Student.faculty_associations)
                                .selectinload(Association.faculty)
                                )  # student.faculty_association -> association.faculty
    )
    return result.scalars().all()


async def get_student_service(student_id: int, db:AsyncSession):
    student = await db.execute(select(Student).where(Student.s_id==student_id))
    return student.scalar()


async def create_student_service(student_req: StudentCreateRequest, db: AsyncSession)->Student:
    async with db.begin_nested():
        db_student = Student(s_name = student_req.name, s_email=student_req.email)
        db.add(db_student)
    return db_student

async def create_bulk_student_service(student_data: StudentBulkCreateRequest, db: AsyncSession) -> list[Student]:
    db_students = [Student(s_name = s.name, s_email = s.email) for s in student_data.students]
    db.add_all(db_students)
    return db_students

async def update_student_service(student_id: int,student_req: StudentCreateRequest,db: AsyncSession):
    stmt = (update(Student)
        .where(Student.s_id == student_id)
        .values(s_name=student_req.name,s_email=student_req.email)
    )
    result = await db.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student updated successfully"}


async def remove_student_cascade_service(student_id: int, db:AsyncSession):
    student = await db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    await db.delete(student)
    # await db.commit()
    return {
        "message": "Student deleted successfully",
        "student_id": student_id,
    }