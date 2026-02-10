from app.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.student import Student
    from app.models.faculty import Faculty

class Association(Base):
    __tablename__ = "association_table"

    association_id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.s_id"))
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.f_id"))

    student: Mapped["Student"] = relationship("Student", back_populates="faculty_associations")
    faculty: Mapped["Faculty"] = relationship("Faculty", back_populates="student_associations")