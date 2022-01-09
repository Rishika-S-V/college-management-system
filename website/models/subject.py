from __future__ import annotations

from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from ..extensions import db

# Type Hints
from flask_sqlalchemy import BaseQuery
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from . import Staff, Department, Log

"""Association Tables"""


class SubjectDepartment(db.Model):
    __tablename__ = "subject_department"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    semester = Column(Integer)

    # Foreign Key
    sub_id = Column(Integer, ForeignKey("subject.id"))
    dept_id = Column(Integer, ForeignKey("department.id"))

    # Relationships
    subject: Subject = relationship("Subject", back_populates="departments")

    # External Relationships
    department: Department = relationship("Department", back_populates="subjects")

    def __init__(self, semester: int) -> None:
        self.semester = semester


class SubjectStaff(db.Model):
    __tablename__ = "subject_staff"

    query: BaseQuery

    id = Column(Integer, primary_key=True)

    sub_id = Column(Integer, ForeignKey("subject.id"))
    staff_id = Column(Integer, ForeignKey("staff.id"))


"""DATA TABLES"""

class Subject(db.Model):
    __tablename__ = "subject"

    query: BaseQuery

    id = Column(Integer, primary_key=True)

    sub_code = Column(Text, unique=True)
    full_name = Column(Text, unique=True)
    short_name = Column(Text)
    regulation = Column(Integer)

    # Relationships
    departments: List[Department] = relationship(
        "SubjectDepartment", back_populates="subject"
    )
    staffs: List[Staff] = relationship(
        "Staff", secondary="subject_staff", back_populates="subjects_handling"
    )
    logs:List[Log] = relationship("Log", back_populates="subject")

    def __init__(
        self, sub_code: str, full_name: str, short_name: str, regulation: int
    ) -> None:
        self.sub_code = sub_code
        self.full_name = full_name
        self.short_name = short_name
        self.regulation = regulation

    def __repr__(self) -> str:
        return f"<Subject: {self.sub_code} - {self.fullname if len(self.full_name) < 5 else self.short_name}>"

    @classmethod
    def add_sub(cls, sub: Subject, department: Department, semester: int):
        association = SubjectDepartment(semester=semester)
        association.subject = sub
        department.subjects.append(association)

        return association
