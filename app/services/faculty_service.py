from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Faculty, Course, Association
from sqlalchemy.orm import load_only,with_expression,selectinload, contains_eager, joinedload
from sqlalchemy import func, update, select
from app.schemas.faculty import FacultyCreateRequest
from fastapi import HTTPException, status

async def get_faculties_service(db: AsyncSession):
    result = await db.execute(select(Faculty))
    return result.scalars().all()

async def faculties_with_courses_service(db: AsyncSession):
    result = await db.execute(
        select(Faculty.f_id,
               Faculty.f_name,
               Course.c_id,
               Course.c_name
        ).join(Course, Course.faculty_id == Faculty.f_id, isouter=True)
    )
    return result.all()

async def faculties_with_courses_orm_service(db: AsyncSession):
    result = await db.execute(
        select(Faculty).options(selectinload(Faculty.courses))
    )
    return result.scalars().all()

async def create_faculties_service(faculty_req: FacultyCreateRequest, db: AsyncSession) -> Faculty :
    async with db.begin_nested():
        db_faculty = Faculty(f_name = faculty_req.name)
        db.add(db_faculty)
    return db_faculty

async def remove_faculty_service(faculty_id: int, db:AsyncSession):
    faculty = await db.get(Faculty, faculty_id)
    if not faculty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FAculty not found")
    await db.delete(faculty)
    # await db.commit()
    return {
        "message": "Student deleted successfully",
        "student_id": faculty_id,
    }