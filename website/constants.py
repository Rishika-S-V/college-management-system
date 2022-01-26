from flask import Flask

from website.models.data import NotificationCategory

from .models import Role, BloodGroup, Department, Designation, NotificationCategory
from dataclasses import dataclass


@dataclass
class role_:
    ADMIN: Role
    STAFF: Role
    STUDENT: Role
    PARENT: Role


@dataclass
class blood_group_:
    O_POSITIVE: BloodGroup
    O_NEGATIVE: BloodGroup
    A_POSITIVE: BloodGroup
    A_NEGATIVE: BloodGroup
    B_POSITIVE: BloodGroup
    B_NEGATIVE: BloodGroup
    AB_POSITIVE: BloodGroup
    AB_NEGATIVE: BloodGroup


@dataclass
class department_:
    CSE: Department
    IT: Department
    AERO: Department
    CIVIL: Department
    ECE: Department
    EEE: Department
    EIE: Department
    MECH: Department


@dataclass
class designation_:
    PRINCIPAL: Designation
    HOD: Designation
    PROF: Designation
    AP: Designation


@dataclass
class notification_category_:
    NONE: NotificationCategory
    INFO: NotificationCategory
    ALERT: NotificationCategory
    REMAINDER: NotificationCategory


ROLE: role_
BLOOD_GROUP: blood_group_
DEPARTMENT: department_
DESIGNATION: designation_
NOTIFICATION_CATEGORY: notification_category_


def query_constants(app: Flask):

    global ROLE, BLOOD_GROUP, DEPARTMENT, DESIGNATION, NOTIFICATION_CATEGORY

    with app.app_context():
        # Roles
        role_admin = Role.query.filter(Role.role_name == "Admin").first()
        role_staff = Role.query.filter(Role.role_name == "Staff").first()
        role_student = Role.query.filter(Role.role_name == "Student").first()
        role_parent = Role.query.filter(Role.role_name == "Parent").first()
        ROLE = role_(role_admin, role_staff, role_student, role_parent)

        # Blood groups
        bg_o_positive = BloodGroup.query.filter(BloodGroup.blood_group == "O+").first()
        bg_o_negative = BloodGroup.query.filter(BloodGroup.blood_group == "O-").first()
        bg_a_positive = BloodGroup.query.filter(BloodGroup.blood_group == "A+").first()
        bg_a_negative = BloodGroup.query.filter(BloodGroup.blood_group == "A-").first()
        bg_b_positive = BloodGroup.query.filter(BloodGroup.blood_group == "B+").first()
        bg_b_negative = BloodGroup.query.filter(BloodGroup.blood_group == "B-").first()
        bg_ab_positive = BloodGroup.query.filter(
            BloodGroup.blood_group == "AB+"
        ).first()
        bg_ab_negative = BloodGroup.query.filter(
            BloodGroup.blood_group == "AB-"
        ).first()
        BLOOD_GROUP = blood_group_(
            bg_o_positive,
            bg_o_negative,
            bg_a_positive,
            bg_a_negative,
            bg_b_positive,
            bg_b_negative,
            bg_ab_positive,
            bg_ab_negative,
        )

        # Departments
        dept_cse = Department.query.filter(Department.short_name == "CSE").first()
        dept_it = Department.query.filter(Department.short_name == "IT").first()
        dept_civil = Department.query.filter(Department.short_name == "CIVIL").first()
        dept_mech = Department.query.filter(Department.short_name == "MECH").first()
        dept_eee = Department.query.filter(Department.short_name == "EEE").first()
        dept_ece = Department.query.filter(Department.short_name == "ECE").first()
        dept_eie = Department.query.filter(Department.short_name == "EIE").first()
        dept_aero = Department.query.filter(Department.short_name == "AERO").first()
        DEPARTMENT = department_(
            dept_cse,
            dept_it,
            dept_aero,
            dept_civil,
            dept_ece,
            dept_eee,
            dept_eie,
            dept_mech,
        )

        # Designation
        desig_principal = Designation.query.filter(
            Designation.short_name == "PRINCIPAL"
        ).first()
        desig_hod = Designation.query.filter(Designation.short_name == "HOD").first()
        desig_prof = Designation.query.filter(Designation.short_name == "PROF").first()
        desig_ap = Designation.query.filter(Designation.short_name == "AP").first()
        DESIGNATION = designation_(desig_principal, desig_hod, desig_prof, desig_ap)

        # Notification Category
        not_cat_none = NotificationCategory.query.filter(
            NotificationCategory.category == "NONE"
        ).first()
        not_cat_info = NotificationCategory.query.filter(
            NotificationCategory.category == "INFO"
        ).first()
        not_cat_alert = NotificationCategory.query.filter(
            NotificationCategory.category == "ALERT"
        ).first()
        not_cat_remainder = NotificationCategory.query.filter(
            NotificationCategory.category == "REMAINDER"
        ).first()
        NOTIFICATION_CATEGORY = notification_category_(
            not_cat_none, not_cat_info, not_cat_alert, not_cat_remainder
        )
