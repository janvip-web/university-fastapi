from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from sqlalchemy import String
from typing import TYPE_CHECKING
# from app.models.course import Course

if TYPE_CHECKING:
    from app.models.course import Course

class Student(Base):
    __tablename__="students"

    s_id: Mapped[int] = mapped_column(primary_key=True)
    s_name: Mapped[str] = mapped_column(String(30))
    s_email: Mapped[str] = mapped_column(String(15), unique=True)

# “A Student is related to many Course rows, and this attribute (courses) should behave like a Python list of Course objects.”
    """
    This does NOT create a foreign key
    This does NOT create a column
    This does NOT hit the database immediately   
    """
    courses: Mapped[list["Course"]] = relationship("Course", back_populates="student")