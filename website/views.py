import email
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
# from .forms import StudentInfoForm
from .models import StudentInfo, User, Announcement, CreatingClass, Grade, Schedule

views = Blueprint('views', __name__)


@views.route('/student-dashboard', methods=['GET', 'POST'])
@login_required
def student_dashboard():
    # Retrieve the student information for the current logged-in user
    student_info = StudentInfo.query.filter_by(user_id=current_user.id).first()
    announcements = Announcement.query.all()
    
    # Render the student dashboard template with the student information
    return render_template('student_dashboard.html', student=student_info, announcements=announcements, title='Student Dashboard')

   
@views.route('/teacher-dashboard', methods=['GET', 'POST'])
@login_required
def teacher_dashboard():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        if title and description:
            new_announcement = Announcement(title=title, description=description, created_by=current_user.id)
            db.session.add(new_announcement)
            db.session.commit()
            flash('Announcement added successfully!', category='success')

        elif 'announcement_id' in request.form:
            announcement_id = request.form.get('announcement_id')
            announcement = Announcement.query.get(announcement_id)

            if announcement:
                db.session.delete(announcement)
                db.session.commit()
                flash('Announcement deleted successfully!', category='success')
            else:
                flash('Announcement not found!', category='error')


    announcements = Announcement.query.all()
    curriculums = CreatingClass.query.all()
    
    return render_template('teacher_dashboard.html', user=current_user, announcements=announcements, curriculums=curriculums, title='Teacher Dashboard')


@views.route('/admin-dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if request.method == 'POST':
        if 'email' in request.form:
            # Handle student info form submission (unchanged)
            email = request.form.get('email')
            student_name = request.form.get('student_name')
            date_of_birth = request.form.get('date_of_birth')
            gender = request.form.get('gender')
            nationality = request.form.get('nationality')
            address = request.form.get('address')
            parent_guardian_name = request.form.get('parent_guardian_name')
            relationship_to_student = request.form.get('relationship_to_student')
            contact_number = request.form.get('contact_number')
            email_gp = request.form.get('email_gp')
            emergency_contact_name = request.form.get('emergency_contact_name')
            emergency_relationship = request.form.get('emergency_relationship')
            emergency_contact_number = request.form.get('emergency_contact_number')

            user = User.query.filter_by(email=email).first()
            if user:
                student_info = StudentInfo.query.filter_by(email=email).first()
                if student_info:
                    student_info.student_name = student_name
                    student_info.date_of_birth = date_of_birth
                    student_info.gender = gender
                    student_info.nationality = nationality
                    student_info.address = address
                    student_info.parent_guardian_name = parent_guardian_name
                    student_info.relationship_to_student = relationship_to_student
                    student_info.contact_number = contact_number
                    student_info.email_gp = email_gp
                    student_info.emergency_contact_name = emergency_contact_name
                    student_info.emergency_relationship = emergency_relationship
                    student_info.emergency_contact_number = emergency_contact_number
                else:
                    student_info = StudentInfo(
                        email=email,
                        student_name=student_name,
                        date_of_birth=date_of_birth,
                        gender=gender,
                        nationality=nationality,
                        address=address,
                        parent_guardian_name=parent_guardian_name,
                        relationship_to_student=relationship_to_student,
                        contact_number=contact_number,
                        email_gp=email_gp,
                        emergency_contact_name=emergency_contact_name,
                        emergency_relationship=emergency_relationship,
                        emergency_contact_number=emergency_contact_number,
                        user_id=user.id
                    )
                    db.session.add(student_info)
                
                db.session.commit()
                flash('Student information has been saved successfully!', category='success')
            else:
                flash('No user found with this email address.', category='error')
        
        elif 'title' in request.form:
            # Handle announcement form submission (unchanged)
            title = request.form.get('title')
            description = request.form.get('description')
            if title and description:
                new_announcement = Announcement(title=title, description=description, created_by=current_user.id)
                db.session.add(new_announcement)
                db.session.commit()
                flash('Announcement added successfully!', category='success')
        
        elif 'announcement_id' in request.form:
            # Handle announcement deletion
            announcement_id = request.form.get('announcement_id')
            announcement = Announcement.query.get(announcement_id)
            if announcement:
                db.session.delete(announcement)
                db.session.commit()
                flash('Announcement deleted successfully!', category='success')


    return render_template('admin_dashboard.html', grades = Grade.query.all(), schedules = Schedule.query.all(), announcements=Announcement.query.all())
'''
@views.route('/add_announcement', methods=['POST'], endpoint='add_announcement')
@login_required
def add_announcement():
    title = request.form.get('title')
    description = request.form.get('description')
    if title and description:
        new_announcement = Announcement(title=title, description=description, created_by=current_user.id)
        db.session.add(new_announcement)
        db.session.commit()
        flash('Announcement added successfully!', category='success')
    return redirect(url_for('views.teacher_dashboard'))

@views.route('/delete-announcement/<int:announcement_id>', methods=['POST'])

@login_required
def delete_announcement(announcement_id):
    announcement = Announcement.query.get(announcement_id)
    if announcement and (current_user.role == 'teacher' or current_user.role == 'admin'):
        db.session.delete(announcement)
        db.session.commit()
        flash('Announcement deleted successfully!', category='success')
    else:
        flash('Announcement not found or you are not authorized to delete it.', category='error')
    return redirect(url_for('views.teacher_dashboard'))
'''
@views.route('/create_curriculum', methods=['POST'])
@login_required
def create_curriculum():
    grade_id = request.form['grade_id']
    schedule_id = request.form['schedule_id']
    subjects = request.form['subjects']
    teacher = request.form['teacher']

    grade = Grade.query.get(grade_id)
    schedule = Schedule.query.get(schedule_id)

    if grade and schedule:
        new_curriculum = CreatingClass(
            grade=grade,
            schedule=schedule,
            subjects=subjects,
            teacher=teacher
        )
        db.session.add(new_curriculum)
        db.session.commit()
        flash('Curriculum created successfully!', 'success')
    else:
        flash('Invalid grade or schedule selected!', 'danger')

    return redirect(url_for('views.admin_dashboard'))


@views.route('/', methods=['GET', 'POST'])
@login_required
def index():

    if current_user.is_authenticated:
        # Redirect authenticated users to their respective dashboards
        if current_user.role == 'admin':
            return redirect(url_for('views.admin_dashboard'))
        elif current_user.role == 'teacher':
            return redirect(url_for('views.teacher_dashboard'))
        elif current_user.role == 'student':
            return redirect(url_for('views.student_dashboard'))
    # Render a base page or login page for unauthenticated users
    return render_template('base.html')