# # SELECTing from the base class vs. specific sub-classes

# from sqlalchemy.orm import DeclarativeBase,


# class Base(DeclarativeBase):
#     pass

# class Employee(Base):
#     pass

# class Manager(Employee):
#     pass

# from sqlalchemy import select

# stmt = select(Manager).order_by()
# manager = session.scalars(stmt).all() 