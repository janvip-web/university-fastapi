from app.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

class Faculty(Base):
    __tablename__="faculties"

    f_id: Mapped[int] = mapped_column(primary_key=True)
    f_name: Mapped[str] = mapped_column(String(50))