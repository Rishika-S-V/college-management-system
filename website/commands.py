import click
from flask.cli import with_appcontext

from .extensions import db
from . import models
from . import constants

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
    
@click.command(name="create-admin")
@with_appcontext
def create_admin():
    click.echo("\n1.Create new Admin")
    click.echo("2.Create Admin from Staff\n:  ",nl=False)
    type = int(input(""))
    click.echo()
    
    if type == 1:
        f_name = input("Enter first name: ").strip()
        m_name = input("Enter middle name(*if none): ").strip()
        l_name = input("Enter last name: ").strip()
        
        print(f_name, m_name, l_name)
        click.echo()
    
    else:
        staff_user_name = input("Enter Staff Username: ")
        staff_user:models.User = models.User.query.filter(models.User.u_name==staff_user_name).filter(models.User.role==constants.ROLE.STAFF).first()
        
        if staff_user:
            staff:models.Staff = staff_user.get_data()
            print("The selected Staff Details:")
            print(f"  Name: {staff.f_name}{ f' {staff.m_name}' if staff.m_name else ''} {staff.l_name}")
            print(f"  Staff Id: {staff.staff_id}")
            print(f"  Department: {staff.dept.short_name}")
            print(f"  Designation: {staff.designation.short_name}")
            
            confirmation = int(input("Enter 1 to confirm and 0 to abort: "))
            if confirmation:
                pass # Add logic to create new user.
            else:
                print("Aborted")
                return
        else:
            print("Staff not found.")
        