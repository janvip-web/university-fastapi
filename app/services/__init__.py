from app.services.student_service import (get_students_service, get_students_basic_service, students_with_courses_joins_service,
                                          students_with_courses_orm_service,get_students_joined_service,
                                          students_with_faculties_service, get_student_service, create_student_service,
                                          create_bulk_student_service, update_student_service, remove_student_cascade_service)

from app.services.faculty_service import (get_faculties_service, faculties_with_courses_service, faculties_with_courses_orm_service, create_faculties_service,
                                          remove_faculty_service)

from app.services.course_service import create_course_service, get_courses_service, remove_course_service