from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email

class StudentInfoForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    student_name = StringField("Student's Name", validators=[DataRequired()])
    date_of_birth = StringField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
                         validators=[DataRequired()])
    nationality = StringField('Nationality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    parent_guardian_name = StringField("Guardian's Full Name", validators=[DataRequired()])
    relationship_to_student = StringField('Relationship to Student', validators=[DataRequired()])
    contact_number = StringField("Guardian's Contact Number", validators=[DataRequired()])
    email_gp = StringField("Guardian's Email", validators=[DataRequired(), Email()])
    emergency_contact_name = StringField("Emergency Contact's Name", validators=[DataRequired()])
    emergency_relationship = StringField("Emergency Relationship to Student", validators=[DataRequired()])
    emergency_contact_number = StringField("Emergency Contact's Number", validators=[DataRequired()])
    submit = SubmitField('Submit')
