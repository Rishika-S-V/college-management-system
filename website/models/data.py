from __future__ import annotations

from flask_login import UserMixin

from sqlalchemy import Column, Integer, Text, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relation, relationship

from ..extensions import db

# TypeHints
from typing import List, Optional, Union, overload
from flask_sqlalchemy import BaseQuery
from datetime import date


"""ASSOCIATION TABLES"""


class UserRoles(db.Model):
    __tablename__ = "user_roles"

    query: BaseQuery

    id = Column(Integer, primary_key=True)

    # Foreign Key
    user_id = Column(Integer, ForeignKey("user.id"))
    role_id = Column(Integer, ForeignKey("role.id"))


class ParentStudents(db.Model):
    __tablename__ = "parent_students"

    query: BaseQuery

    id = Column(Integer, primary_key=True)

    # Foreign Key
    parent_id = Column(Integer, ForeignKey("parent.id"))
    student_id = Column(Integer, ForeignKey("student.id"))


"""CONSTANT TABLES"""


class Department(db.Model):
    __tablename__ = "department"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    full_name = Column(Text, unique=True)
    short_name = Column(Text, unique=True)

    # Relationships
    students: List[Student] = relationship("Student", back_populates="dept")
    staffs: List[Staff] = relationship("Staff", back_populates="dept")

    def __init__(self, full_name: str, short_name: str) -> None:
        self.full_name = full_name
        self.short_name = short_name

    def __repr__(self) -> str:
        return f"<Department: {self.short_name}>"


class Designation(db.Model):
    __tablename__ = "designation"

    query: BaseException

    id = Column(Integer, primary_key=True)
    full_name = Column(Text, unique=True)
    short_name = Column(Text, unique=True)

    # Relationships
    staffs: List[Staff] = relationship("Staff", back_populates="designation")

    def __init__(self, full_name: str, short_name: str) -> None:
        self.full_name = full_name
        self.short_name = short_name

    def __repr__(self) -> str:
        return f"<Designation: {self.full_name}>"


class BloodGroup(db.Model):
    __tablename__ = "blood_group"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    blood_group = Column(Text, unique=True)

    # Relationships
    students: List[Student] = relationship("Student", back_populates="blood_grp")
    staffs: List[Staff] = relationship("Staff", back_populates="blood_grp")

    def __init__(self, blood_group: str) -> None:
        self.blood_group = blood_group

    def __repr__(self) -> str:
        return f"<BloodGroup: {self.blood_group}>"


class Role(db.Model):
    __tablename__ = "role"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    role_name = Column(Text, unique=True)

    # Relationships
    users: List[User] = relationship(
        "User", secondary="user_roles", back_populates="roles"
    )

    def __init__(self, role_name: str) -> None:
        self.role_name = role_name

    def __repr__(self) -> str:
        return f"<Role: {self.role_name}>"


"""PERSON TABLES"""


class Admin(db.Model):
    __tablename__ = "admin"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    is_staff = Column(Boolean)
    f_name = Column(Text)
    m_name = Column(Text, nullable=True)
    l_name = Column(Text)

    # Foreign Key
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=True)

    # Relationships
    staff: Staff = relationship("Staff", back_populates="admin")

    @overload
    def __init__(self, staff: Staff) -> None:
        ...

    @overload
    def __init__(self, f_name: str, l_name: str, m_name: Optional[str]) -> None:
        ...

    def __init__(self, **kwargs: Union[str, Staff]) -> None:
        self.f_name = kwargs.get("f_name")
        self.m_name = kwargs.get("m_name")
        self.l_name = kwargs.get("l_name")
        self.staff = kwargs.get("staff")
        self.is_staff = False if kwargs.get("staff") == None else True

    def __repr__(self) -> str:
        if self.is_staff is True:
            return f"<Admin: {self.staff}>"
        else:
            return f"<Admin: {self.f_name} {self.l_name}>"


class Staff(db.Model):
    __tablename__ = "staff"

    query: BaseQuery

    id = Column(Integer, primary_key=True)

    # Data Fields
    f_name = Column(Text)
    m_name = Column(Text, nullable=True)
    l_name = Column(Text)
    staff_id = Column(Text)
    date_of_joining = Column(Date)
    is_admin = Column(Boolean)
    is_active_staff = Column(Boolean)

    # Foreign Keys
    dept_id = Column(Integer, ForeignKey("department.id"))
    desig_id = Column(Integer, ForeignKey("designation.id"))
    blood_grp_id = Column(Integer, ForeignKey("blood_group.id"))

    # Relationships
    dept: Department = relationship("Department", back_populates="staffs")
    designation: Designation = relationship("Designation", back_populates="staffs")
    blood_grp: BloodGroup = relationship("BloodGroup", back_populates="staffs")
    admin: Admin = relationship("Admin", back_populates="staff", uselist=False)

    def __init__(
        self,
        f_name: str,
        l_name: str,
        staff_id: str,
        date_of_joining: date,
        is_active_staff: Optional[bool] = True,
        is_admin: Optional[bool] = False,
        m_name: Optional[str] = None,
    ) -> None:
        self.f_name = f_name
        self.m_name = m_name
        self.l_name = l_name
        self.staff_id = staff_id
        self.date_of_joining = date_of_joining
        self.is_admin = is_admin
        self.is_active_staff = is_active_staff

    def __repr__(self) -> str:
        return f"<Staff: {self.f_name} {self.l_name}, {self.dept.short_name} - {self.designation.short_name}>"


class Student(db.Model):
    __tablename__ = "student"

    query: BaseQuery

    id = Column(Integer, primary_key=True)

    # Data Fields
    f_name = Column(Text)
    m_name = Column(Text, nullable=True)
    l_name = Column(Text)
    roll_no = Column(Integer, unique=True, nullable=True)
    batch = Column(Integer)
    library_id = Column(Text, unique=True, nullable=True)
    dob = Column(Date)
    regulation = Column(Integer)
    is_active_stud = Column(Boolean)
    is_lateral_entry = Column(Boolean)
    is_alumni = Column(Boolean)

    # Foreign Keys
    dept_id = Column(Integer, ForeignKey("department.id"))
    blood_grp_id = Column(Integer, ForeignKey("blood_group.id"))

    # Relationships
    dept: Department = relationship("Department", back_populates="students")
    blood_grp: BloodGroup = relationship("BloodGroup", back_populates="students")
    parents: List[Parent] = relationship(
        "Parent", secondary="parent_students", back_populates="children"
    )

    def __init__(
        self,
        f_name: str,
        l_name: str,
        batch: int,
        dob: date,
        regulation: int,
        is_active_stud: Optional[bool] = True,
        is_lateral_entry: Optional[bool] = False,
        is_alumni: Optional[bool] = False,
        m_name: Optional[str] = None,
        roll_no: Optional[int] = None,
        library_id: Optional[str] = None,
    ):
        self.f_name = f_name
        self.m_name = m_name
        self.l_name = l_name
        self.roll_no = roll_no
        self.batch = batch
        self.library_id = library_id
        self.dob = dob
        self.regulation = regulation
        self.is_active_stud = is_active_stud
        self.is_lateral_entry = is_lateral_entry
        self.is_alumni = is_alumni

    def __repr__(self) -> str:
        return f"<Student: {self.f_name} {self.l_name}, {self.dept.short_name}>"


class Parent(db.Model):
    __tablename__ = "parent"

    query: BaseQuery

    id = Column(Integer, primary_key=True)

    f_name = Column(Text)
    l_name = Column(Text)

    # Relationships
    children: List[Student] = relationship(
        "Student", secondary="parent_students", back_populates="parents"
    )

    def __init__(self, f_name: str, l_name: str) -> None:
        self.f_name = f_name
        self.l_name = l_name

    def __repr__(self) -> str:
        return f"<Parent: {self.f_name} {self.l_name}>"


"""USER TABLES"""


class User(db.Model, UserMixin):
    __tablename__ = "user"

    query: BaseQuery

    id = Column(Integer, primary_key=True)

    u_name = Column(Text, unique=True)
    email = Column(Text, unique=True)
    password = Column(Text)
    last_active = Column(DateTime)

    # Foreign Keys
    data_id = Column(Integer)  # refers to the data

    # Relationship
    roles: List[Role] = relationship(
        "Role", secondary="user_roles", back_populates="users"
    )

    def __init__(self, u_name: str, email: str, password: str) -> None:
        self.u_name = u_name
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return f"<User: {self.u_name} [{[role.role_name for role in self.roles]}]>"
