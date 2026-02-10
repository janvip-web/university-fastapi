from app.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.student import Student
    from app.models.association import Association


class Faculty(Base):
    __tablename__="faculties"

    f_id: Mapped[int] = mapped_column(primary_key=True)
    f_name: Mapped[str] = mapped_column(String(50))

#  BACK_POPULATES = to establish a bidirectional relationship between two mapped classes
# one to many between faculty and course
    courses: Mapped[list["Course"]] = relationship("Course", back_populates="faculty")

       #many to many between student and faculty
    students: Mapped[list["Student"]] = relationship(secondary="association_table", back_populates="faculties", viewonly=True)

    # association between student -> association -> faculty
    student_associations: Mapped[list["Association"]] = relationship(back_populates="faculty")