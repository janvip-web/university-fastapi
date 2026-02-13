from app.database import engine, AsyncSessionLocal, Base
from app.models import Student, Course, Faculty, Association
from app.controller import students, faculty, courses