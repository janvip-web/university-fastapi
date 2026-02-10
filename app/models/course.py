from app.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey
from typing import TYPE_CHECKING
# from app.models.student import Student

if TYPE_CHECKING:
    from app.models.student import Student
    from app.models.faculty import Faculty

class Course(Base):
    __tablename__="courses"

    c_id: Mapped[int] = mapped_column(primary_key=True)
    c_name: Mapped[str] = mapped_column(String(50))
    student_id: Mapped[int] = mapped_column(ForeignKey("students.s_id"))
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.f_id"))

    student:Mapped["Student"] = relationship("Student", back_populates="courses" )
    faculty: Mapped["Faculty"] = relationship("Faculty", back_populates="courses")