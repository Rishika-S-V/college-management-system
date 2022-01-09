from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer, Boolean, VARCHAR
from sqlalchemy.orm import relation, relationship
from sqlalchemy.sql.base import NO_ARG

from ..extensions import db

from typing import TYPE_CHECKING, Iterable, List, Tuple, Union, overload

if TYPE_CHECKING:
    from typing import Optional
    from flask_sqlalchemy import BaseQuery
    from . import Subject, Student, Class, Calendar


"""Association Tables"""


class ExamClass(db.Model):
    __tablename__ = "exam_class"

    query: BaseQuery

    id = Column(Integer, primary_key=True)

    # Foreign Keys
    class_id = Column(Integer, ForeignKey("class.id"))
    exam_id = Column(Integer, ForeignKey("exam.id"))

class ExamStudent(db.Model):
    __tablename__ = "exam_student"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    is_attended = Column(Boolean)
    is_passed = Column(Boolean)
    marks = Column(Integer)
    grade = Column(VARCHAR(3))

    #Foreign Keys
    student_id = Column(Integer, ForeignKey("student.id"))
    exam_id = Column(Integer, ForeignKey("exam.id"))
    
    #Relationships
    student: Student = relationship("Student", back_populates="exams") 
    exam: Exam = relationship("Exam", back_populates="students")
    
    def __init__(self, is_attended: bool, is_passed: bool, grade: str, marks:int) -> None:
        self.is_attended = is_attended
        self.marks = marks
        self.grade = grade
        self.is_passed = is_passed
        

"""Data Tables"""


class Exam(db.Model):
    __tablename__ = "exam"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(50))
    is_semester = Column(Boolean)
    max_score = Column(Integer)
    pass_score = Column(Integer)

    # Foreign Keys
    calendar_id = Column(Integer, ForeignKey("calendar.id"))
    subject_id = Column(Integer, ForeignKey("subject.id"))

    # Relationships
    date_: Calendar = relationship("Calendar", back_populates="exams")
    subject: Subject = relationship("Subject", back_populates="exams")
    classes: List[Class] = relationship("Class", secondary="exam_class", back_populates="exams")
    
    students: List[Student] = relationship("ExamStudent", back_populates="exam")
    
    def __init__(self, name: str, date_:Calendar, subject:Subject, max_score: int, pass_score: int, classes:Iterable[Class], is_semester: Optional[bool]=False) -> None:
        self.name = name
        self.date_ = date_
        self.subject = subject
        self.max_score = max_score
        self.pass_score = pass_score
        self.is_semester = is_semester
        self.classes.extend(classes)
        
    def enter_marks(self, cls:Class, data: Iterable[Tuple[Student, int, str]], failures:Iterable[students]):
        
        def _add_marks(stud, is_attended, is_passed, marks, grade):
            association = ExamStudent(is_attended, is_passed, marks, grade)
            association.student = stud
            self.students.append(association)
        
        is_attended, is_passed, marks, grade = None, None, None, None
        
        students_not_attended = list(set(cls.students) - set([i[0] for i in data]))
        
        for stud in students_not_attended:
            is_attended, is_passed, marks, grade = False, None, None, None
            _add_marks(stud, is_attended, is_passed, marks, grade)

        for stud, m, g in data:
            is_attended = True
            is_passed = True if stud not in failures else False
            marks, grade = m, g
            _add_marks(stud, is_attended, is_passed, marks, grade)
            