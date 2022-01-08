from __future__ import annotations

from sqlalchemy import Column, Integer, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship

from ..extensions import db

# Type Hints
from flask_sqlalchemy import BaseQuery
from typing import List, Dict, Any, TYPE_CHECKING, Optional, Tuple

if TYPE_CHECKING:
    from . import Department, Staff, Student


"""ASSOCIATION TABLES"""


class ClassDept(db.Model):
    __tablename__ = "class_dept"

    query: BaseQuery

    id = Column(Integer, primary_key=True)

    class_id = Column(Integer, ForeignKey("class.id"))
    dept_id = Column(Integer, ForeignKey("department.id"))


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


class ClassInherit(db.Model):
    __tablename__ = "class_inherit"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    semester = Column(Integer)

    # Foreign Key
    child_class_id = Column(Integer, ForeignKey("class.id"))
    parent_class_id = Column(Integer, ForeignKey("class.id"))

    # Relationships
    child_class: Class = relationship(
        "Class", back_populates="parents", foreign_keys=[parent_class_id]
    )
    parent: Class = relationship(
        "Class", back_populates="child_classes", foreign_keys=[child_class_id]
    )

    def __init__(self, semester: int) -> None:
        self.semester = semester


"""DATA TABLES"""


class Class(db.Model):
    __tablename__ = "class"

    query: BaseQuery

    id = Column(Integer, primary_key=True)

    batch = Column(Integer)
    regulation = Column(Integer)
    current_sem = Column(Integer)
    is_archived = Column(Boolean)
    time_table = Column(JSON)

    # Relationships
    cc_s: List[Staff] = relationship("ClassCc", back_populates="class_")
    reps: List[Student] = relationship("ClassRep", back_populates="class_")
    parents: List[Class] = relationship(
        "ClassInherit",
        back_populates="child_class",
        foreign_keys="[ClassInherit.child_class_id]",
        overlaps="parent",
    )
    child_classes: List[Class] = relationship(
        "ClassInherit",
        back_populates="parent",
        foreign_keys="[ClassInherit.parent_class_id]",
        overlaps="child_class",
    )

    # External Relationships
    departments: List[Department] = relationship(
        "Department", secondary="class_dept", back_populates="classes"
    )
    students: List[Student] = relationship("Student", back_populates="class_")

    def __init__(
        self,
        batch: int,
        regulation: int,
        current_sem: Optional[int] = 1,
        is_archived: Optional[bool] = False,
        timetable: Optional[Dict[str, Any]] = JSON.NULL,
    ) -> None:
        self.batch = batch
        self.regulation = regulation
        self.current_sem = current_sem
        self.is_archived = is_archived
        self.time_table = timetable

    def __repr__(self) -> str:
        return f"<Class: {self.batch} - {self.regulation} Regulation, {'/'.join([dept.short_name for dept in self.departments])}>"

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

    @classmethod
    def split_classes(
        cls, base_cls: Class, semester: int, *children: Class
    ) -> Tuple[ClassInherit, ...]:
        association: List[ClassInherit] = list()
        base_cls.is_archived = True

        for cls in children:
            asso = ClassInherit(semester)
            asso.parent = base_cls
            cls.parents.append(asso)

            association.append(asso)

        return tuple(association)
