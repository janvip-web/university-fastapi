from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func, update
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Student, Course, Association, Faculty
from sqlalchemy.orm import load_only, with_expression, selectinload, contains_eager, joinedload
from app.schemas.course import CourseCreateRequest
from app.services.course_service import *

router = APIRouter(tags=["courses"])

@router.post("/courses/",  status_code=201)
async def create_course(course_req: CourseCreateRequest, db: AsyncSession = Depends(get_db)):
    # db_course = Course(c_name = course_req.name, student_id = course_req.s_id, faculty_id = course_req.f_id)
    # db.add(db_course)
    # return db_course
    course = await create_course_service(course_req, db)
    return course

@router.get("/courses/")
async def get_courses(db: AsyncSession = Depends(get_db)):
    # result = await db.execute(select(Course))
    # return result.scalars().all()'
    return await get_courses_service(db)

@router.delete("/course/{course_id}")
async def remove_course(course_id: int, db:AsyncSession=Depends(get_db)):
    # course = await db.get(Course, course_id)
    # if not course:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FAculty not found")
    # await db.delete(course)
    
    # # await db.commit()
    # return {
    #     "message": "course deleted successfully",
    #     "student_id": course_id,
    # }
    return await remove_course_service(course_id, db)