from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func, update
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.faculty import FacultyCourseRow, FacultyWithCoursesesponse, FacultyCreateRequest, FacultyReadResponse
from app.services.faculty_service import *

router = APIRouter(tags=["faculty"])

@router.get("/faculties/")
async def get_faculties(db: AsyncSession = Depends(get_db)):
    # result = await db.execute(select(Faculty))
    # return result.scalars().all()
    return await get_faculties_service(db)

@router.get("/faculty-course/joins")
async def faculties_with_courses(db: AsyncSession = Depends(get_db))-> list[FacultyCourseRow]:
    # result = await db.execute(
    #     select(Faculty.f_id,
    #            Faculty.f_name,
    #            Course.c_id,
    #            Course.c_name
    #     ).join(Course, Course.faculty_id == Faculty.f_id, isouter=True)
    # )
    # return result.all()
    return await faculties_with_courses_service(db)


@router.get("/faculty-course/orm")
async def faculties_with_courses_orm(db: AsyncSession = Depends(get_db)) -> list[FacultyWithCoursesesponse]:
    # result = await db.execute(
    #     select(Faculty).options(selectinload(Faculty.courses))
    # )
    # return result.scalars().all()
    return await faculties_with_courses_orm_service(db)


@router.post("/faculties/", status_code=201)
async def create_faculties(faculty_req: FacultyCreateRequest, db: AsyncSession = Depends(get_db))->FacultyReadResponse :
    # db_faculty = Faculty(f_name = faculty_req.name)
    # db.add(db_faculty)
    # return db_faculty
    faculty =  await create_faculties_service(faculty_req, db)
    return faculty

@router.delete("/faculties/{faculty_id}")
async def remove_faculty(faculty_id: int, db:AsyncSession=Depends(get_db)):
#     faculty = await db.get(Faculty, faculty_id)
#     if not faculty:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FAculty not found")
#     await db.delete(faculty)
#     # await db.commit()
#     return {
#         "message": "Student deleted successfully",
#         "student_id": faculty_id,
#     }
    return await remove_faculty_service(faculty_id, db)