from __future__ import annotations

from sqlalchemy import Column, Integer, Text, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship

from ..extensions import db

# Type Hints
from flask_sqlalchemy import BaseQuery
from typing import Iterable, List, Dict, Any, TYPE_CHECKING, Optional, Tuple

if TYPE_CHECKING:
    from . import Department, Staff, Student, Calendar, Subject, Exam
    from datetime import date


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


class ClassCalendar(db.Model):
    __tablename__ = "class_calendar"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    is_working_day = Column(Boolean)
    holiday_rsn = Column(Text)

    # Foreign Keys
    class_id = Column(Integer, ForeignKey("class.id"))
    calendar_id = Column(Integer, ForeignKey("calendar.id"))

    # Relationships
    class_: Class = relationship("Class", back_populates="dates")
    date_: Calendar = relationship("Calendar", back_populates="classes")

    def __init__(
        self, is_working_day: Optional[bool] = True, holiday_rsn: Optional[str] = None
    ) -> None:
        self.is_working_day = is_working_day
        self.holiday_rsn = holiday_rsn


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

class Attendance(db.Model):
    __tablename__ = "attendance"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    is_present = Column(Boolean)
    is_od = Column(Boolean)
    note = Column(Text)

    # Foreign Keys
    log_id = Column(Integer, ForeignKey("log.id"))
    student_id = Column(Integer, ForeignKey("student.id"))

    # Relationships
    log: Log = relationship("Log", back_populates="students")
    student: Student = relationship("Student", back_populates="attendance")

    def __init__(
        self,
        is_present: bool,
        is_od: Optional[bool] = False,
        note: Optional[str] = None,
    ) -> None:
        self.is_present = is_present
        self.is_od = is_od
        self.note = note

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
    dates: List[Calendar] = relationship("ClassCalendar", back_populates="class_")
    logs:List[Log] = relationship("Log", back_populates="class_")

    # External Relationships
    departments: List[Department] = relationship(
        "Department", secondary="class_dept", back_populates="classes"
    )
    students: List[Student] = relationship("Student", back_populates="class_")
    exams: List[Exam] = relationship("Exam", secondary="exam_class", back_populates="classes")

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

    def add_date(
        self,
        date_: Calendar,
        is_working_day: Optional[bool] = None,
        holiday_rsn: Optional[str] = None,
    ):
        is_working_day = (
            not (date_.is_govt_holiday) if is_working_day == None else is_working_day
        )
        holiday_rsn = date_.holiday_rsn if holiday_rsn == None else holiday_rsn

        association = ClassCalendar(is_working_day, holiday_rsn)
        association.date_ = date_
        self.dates.append(association)

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


class Log(db.Model):
    __tablename__ = "log"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    period_no = Column(Integer)
    note = Column(Text)

    # Foreign Keys
    calendar_id = Column(Integer, ForeignKey("calendar.id"))
    subject_id = Column(Integer, ForeignKey("subject.id"))
    staff_id = Column(Integer, ForeignKey("staff.id"))
    class_id = Column(Integer, ForeignKey("class.id"))

    # Relationships
    date_: Calendar = relationship("Calendar", back_populates="logs")
    subject: Subject = relationship("Subject", back_populates="logs")
    staff: Staff = relationship("Staff", back_populates="logs")
    class_: Class = relationship("Class", back_populates="logs")
    
    students:List[Student] = relationship("Attendance", back_populates="log")

    def __init__(self, date_:Calendar, subject:Subject, staff:Staff, class_: Class, period_no: int, note: str) -> None:
        self.date_ = date_
        self.subject = subject
        self.staff = staff
        self.class_ = class_
        self.period_no = period_no
        self.note = note

    def add_attendance(self, present: Iterable[Student], od:Optional[Dict[str, Iterable[Student]]]=dict()):

        is_present, is_od, note = None, None, None
        
        for stud in self.class_.students:
            if stud in present:
                is_present, is_od, note = True, False, None
            elif stud in [stud for i in od.values() for stud in i]: # Checking if the student is in any of the od groups
                for key, val in od.items():
                    if stud in val:
                        is_present, is_od, note = False, True, key 
            else:
                is_present, is_od, note = False, False, None

            association = Attendance(is_present=is_present, is_od=is_od, note=note)
            association.student = stud
            self.students.append(association)
