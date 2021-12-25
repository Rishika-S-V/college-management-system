from __future__ import annotations

from sqlalchemy import Column, Integer, JSON, ForeignKey
from sqlalchemy.orm import relationship

from ..extensions import db

# Type Hints
from flask_sqlalchemy import BaseQuery
from typing import List, Dict, Any, TYPE_CHECKING, Optional, Tuple

if TYPE_CHECKING:
    from . import Department, Staff, Student


"""ASSOCIATION TABLES"""


class ClassCc(db.Model):
    __tablename__ = "class_cc"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    semester = Column(Integer)

    # Foreign Key
    class_id = Column(Integer, ForeignKey("class.id"))
    staff_id = Column(Integer, ForeignKey("staff.id"))

    # Relationships
    class_: Class = relationship("Class", back_populates="cc_s")

    # External Relationships
    cc: Staff = relationship("Staff", back_populates="classes_as_cc")

    def __init__(self, semester: int):
        self.semester = semester


class ClassRep(db.Model):
    __tablename__ = "class_rep"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    semester = Column(Integer)

    # Foreign Key
    class_id = Column(Integer, ForeignKey("class.id"))
    student_id = Column(Integer, ForeignKey("student.id"))

    # Relationships
    class_: Class = relationship("Class", back_populates="reps")

    # External Relationships
    rep: Student = relationship("Student", back_populates="class_as_rep")

    def __init__(self, semester: int):
        self.semester = semester


"""DATA TABLES"""


class Class(db.Model):
    __tablename__ = "class"

    query: BaseQuery

    id = Column(Integer, primary_key=True)

    batch = Column(Integer)
    regulation = Column(Integer)
    current_sem = Column(Integer)
    time_table = Column(JSON)

    # Foreign Keys
    dept_id = Column(Integer, ForeignKey("department.id"))

    # Relationships
    cc_s: List[Staff] = relationship("ClassCc", back_populates="class_")
    reps: List[Student] = relationship("ClassRep", back_populates="class_")

    # External Relationships
    department: Department = relationship("Department", back_populates="classes")
    students: List[Student] = relationship("Student", back_populates="class_")

    def __init__(
        self,
        batch: int,
        regulation: int,
        current_sem: Optional[int] = 1,
        timetable: Optional[Dict[str, Any]] = JSON.NULL,
    ) -> None:
        self.batch = batch
        self.regulation = regulation
        self.current_sem = current_sem
        self.time_table = timetable

    def __repr__(self) -> str:
        return f"<Class: {self.batch} - {self.regulation} Regulation, {self.department.short_name}>"

    @classmethod
    def add_class(
        cls, class_: Class, cc: Staff, rep: Optional[Student]
    ) -> Tuple[ClassCc, ClassRep]:
        association_cc = ClassCc(semester=1)
        association_cc.class_ = class_
        cc.is_cc = True
        cc.classes_as_cc.append(association_cc)

        association_rep = ClassRep(semester=1)
        association_rep.class_ = class_
        rep.is_rep = True
        rep.class_as_rep.append(association_rep)

        return association_cc, association_rep

    @classmethod
    def add_cc(cls, class_: Class, cc: Staff, semester: int) -> ClassCc:
        association = ClassCc(semester=semester)
        association.class_ = class_
        cc.is_cc = True
        cc.classes_as_cc.append(association)

        return association

    @classmethod
    def add_rep(cls, class_: Class, rep: Student, semester: int) -> ClassRep:
        association = ClassRep(semester=semester)
        association.class_ = class_
        rep.is_rep = True
        rep.class_as_rep.append(association)

        return association
