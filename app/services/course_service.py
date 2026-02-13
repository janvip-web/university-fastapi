from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Student, Course, Association
from app.schemas.course import CourseCreateRequest
from fastapi import HTTPException, status
from sqlalchemy import select

async def create_course_service(course_req: CourseCreateRequest, db: AsyncSession)->Course:
    async with db.begin_nested():
        db_course = Course(c_name = course_req.name, student_id = course_req.s_id, faculty_id = course_req.f_id)
        db.add(db_course)
    return db_course

async def get_courses_service(db: AsyncSession):
    result = await db.execute(select(Course))
    return result.scalars().all()

async def remove_course_service(course_id: int, db:AsyncSession):
    course = await db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FAculty not found")
    await db.delete(course)
    
    # await db.commit()
    return {
        "message": "course deleted successfully",
        "student_id": course_id,
    }