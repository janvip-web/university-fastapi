# relationship configuration

from typing import List, Optional
from sqlalchemy import ForeignKey, Integer, Column,Table
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

# one to many
# A one to many relationship places a foreign key on the child table referencing the parent. 
# relationship() is then specified on the parent, as referencing a collection of items represented by the child:

class Parent(Base):
    __tablename__ ="parent_table"

    id : Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Child"]] = relationship(back_populates="parent")

class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
    # to establish bidirctional relationship in 1 to many
    parent: Mapped["Parent"] = relationship(back_populates="children") 


# many to one
# Many to one places a foreign key in the parent table referencing the child. relationship() is declared on the parent,
class Parent1(Base):
    __tablename__ = "parent1"

    id: Mapped[int] = mapped_column(primary_key=True)
    child_id: Mapped[int] = mapped_column(ForeignKey("Child1.id"))
    child: Mapped["Child1"] = relationship(back_populates="parents")
    # # nullable many to one
    # child_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Child1.id"))
    # child: Mapped[Optional["Child1"]] = relationship(back_populates="parents")

class Child1(Base):
    __tablename__ = "child1"

    id: Mapped[int] = mapped_column(primary_key=True)
    parents: Mapped[List["Parent1"]] = relationship(back_populates="child")


# ONE TO ONE - One To One is essentially a One To Many relationship from a foreign key perspective,
class Parent2(Base):
    __tablename__ ="parent_table2"

    id : Mapped[int] = mapped_column(primary_key=True)
    child: Mapped["Child2"] = relationship(back_populates="parent")

class Child2(Base):
    __tablename__ = "child_table2"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table2.id"))
    # to establish bidirctional relationship in 1 to many
    parent: Mapped["Parent2"] = relationship(back_populates="child") 


# MANY TO MANY - Many to Many adds an association table between two classes. 

# associatition_table = Table(
#     "association_table",
#     Base.metadata,
#     Column("left_id", ForeignKey("left_table.id"), primary_key=True),
#     Column("right_id", ForeignKey("right_table.id"), primary_key=True)
# )

class Association(Base):
    __tablename__ = "association_table"

    left_id: Mapped[int] = mapped_column(ForeignKey("left_table.id"), primary_key=True)
    right_id: Mapped[int] = mapped_column(ForeignKey("right_table.id"), primary_key=True)
    extra_data: Mapped[Optional[str]]
    # association between Association -> Child
    child: Mapped["Child3"] = relationship(back_populates="parent_associations")

    parent: Mapped["Parent3"] = relationship(back_populates="child_associations")


class Parent3(Base):
    __tablename__ = "left_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    # many-to-many relationship to Child, bypassing the `Association` class
    children: Mapped[List["Child3"]] = relationship(secondary="association_table", back_populates="parents")

    # children: Mapped[List["Child3"]] = relationship(secondary=association_table, back_populates="parents")
    # association between Parent -> Association -> Child
    child_associations: Mapped[List["Association"]] = relationship(back_populates="parent")

class Child3(Base):
    __tablename__ = "right_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    parents: Mapped[List["Parent3"]] = relationship(secondary="association_table",back_populates="children")

    # parents: Mapped[List["Parent3"]] = relationship(secondary=association_table, back_populates="children")
    parent_association: Mapped[List["Association"]] = relationship(back_populates="child")


