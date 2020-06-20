from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField ,IntegerField ,SelectField , TextField ,validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from web.models import Doctor , Patient




class Registration(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    speciality = StringField('Speciality',
                           validators=[DataRequired(), Length(min=2, max=50)])
    slmcno = StringField('SLMC/Registration NO',
                           validators=[DataRequired(), Length(min=2, max=20)])
    hospital = StringField('Practising Hospital',
                         validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        doctor = Doctor.query.filter_by(username=username.data).first()
        if doctor:
            raise ValidationError('the entered username is already in use . Please choose a different one.')

    def validate_email(self, email):
        doctor = Doctor.query.filter_by(email=email.data).first()
        if doctor:
            raise ValidationError('The entered email is taken already in use . Please choose a different one.')

    def validate_slmcno(self, slmcno):
        doctor = Doctor.query.filter_by(email=slmcno.data).first()
        if doctor:
            raise ValidationError('The entered SLMC NO is  incorrect . Please  enter the Valid SLMC NO.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PatientRegistration(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        patient = Patient.query.filter_by(username=username.data).first()
        if patient:
            raise ValidationError('the entered username is already in use . Please choose a different one.')

    def validate_email(self, email):
        patient = Patient.query.filter_by(email=email.data).first()
        if patient:
            raise ValidationError('The entered email is taken already in use . Please choose a different one.')


class PatientLoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdatePatientProfileForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        patient = Patient.query.filter_by(username=username.data).first()
        if patient:
            raise ValidationError('the entered username is already in use . Please choose a different one.')

    def validate_email(self, email):
        patient = Patient.query.filter_by(email=email.data).first()
        if patient:
            raise ValidationError('The entered email is taken already in use . Please choose a different one.')

class UpdateDoctorProfileForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Update')


class UpdateHospitalForm(FlaskForm):
    hospital = StringField('Practising Hospital',
                           validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Update Hospital')

#class AnalyzeSymptoms(FlaskForm):
 #   name = TextField("Name Of Student", [validators.Required('Please enter your name.')])
 #   symptom1 = SelectField('Symptom1', choices=[('back_pain', 'Back Pain'), ('constipation', 'Constipation')])


class AnalyzeSymptoms(FlaskForm):
    l1 = ['back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine',
          'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
          'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation',
          'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
          'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
          'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
          'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
          'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips',
          'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
          'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
          'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine',
          'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
          'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain',
          'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria',
          'family_history', 'mucoid_sputum',
          'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion',
          'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen',
          'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum', 'prominent_veins_on_calf',
          'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling',
          'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose',
          'yellow_crust_ooze']
    name = TextField('Your Name', [validators.Required('Please enter your name.')])
    list1 = []
    for i in l1:
        list1.append((i,i))

    symptom1 = SelectField('Symptom1', choices=list1,)
    symptom2 = SelectField('Symptom2', choices=list1,)
    symptom3 = SelectField('Symptom3', choices=list1,)
    symptom4 = SelectField('Symptom4', choices=list1,)
    symptom5 = SelectField('Symptom5', choices=list1,)

    prediction = TextField('Disease')
    #submit = SubmitField('Analyze symptoms')
    #submit1 = SubmitField('Find Doctors')

class DrList(FlaskForm):
    text = TextField('Dr List')

class PsychologicalSymptoms(FlaskForm):
    l1 = ['hallucinations auditory', 'sleeplessness', 'suicidal','motor retardation','motor retardation','unable to concentrate','todd paralysis',
          'worry','tremor','alcoholic withdrawl symptoms','agitation','unresponsiveness','blackout','withdraw','difficulty','irritable mood', 'sensory discomfort',
          'drowsiness','formication','unconscious state','fever','cough','Feeling nervous','Having a sense of impending danger','Sweating','Trembling','Feeling weak'
          ,'Sleep Changes','Feeling of Helplessness','Loss of interest in daily activities','Appetite of weight changes','Anger','Loss of energy','Strong feelings of worthlessness',
          'racing Heart','chest pain','Breathing difficulties','Feeling loss of control','Low Self esteem','Fear of abandonment', 'Unstable relationships','Extreme emotional swings',
          'Feeling suspicious or out of touch with reality','disorganized speech such as switching topics erratically','Appetite of weight changes','alcoholic withdrawl symptoms']
    name = TextField('Your Name', [validators.Required('Please enter your name.')])
    list1 = []
    for i in l1:
        list1.append((i, i))

    symptom1 = SelectField('Symptom1', choices=list1, )
    symptom2 = SelectField('Symptom2', choices=list1, )
    symptom3 = SelectField('Symptom3', choices=list1, )
    symptom4 = SelectField('Symptom4', choices=list1, )
    symptom5 = SelectField('Symptom5', choices=list1, )

    prediction = TextField('Disease')
    submit = SubmitField('Analyze symptoms')

class Diseases(FlaskForm):
    disease = ['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction',
               'Peptic ulcer diseae', 'AIDS', 'Diabetes', 'Gastroenteritis', 'Bronchial Asthma', 'Hypertension',
               ' Migraine', 'Cervical spondylosis',
               'Paralysis (brain hemorrhage)', 'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'hepatitis A',
               'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E', 'Alcoholic hepatitis', 'Tuberculosis',
               'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
               'Heartattack', 'Varicoseveins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis',
               'Arthritis', '(vertigo) Paroymsal  Positional Vertigo', 'Acne', 'Urinary tract infection', 'Psoriasis',
               'Impetigo']
    list1 = []
    j=0
    for i in disease:
        ++j
        list1.append((i,i))

    disease = SelectField('Disease', choices=list1, )
    #chronic = SelectField('Chronic', choices=[('True', 'True'),('False', 'False')])
    chronic = BooleanField('Chronic', default=True)
    speciality = SelectField('Speciality', choices=[('general','General Physician'),('primary','Primary Care Physician'),('dermatologist','Dermotologist')
    ,('gastroenterologist','Gastroenterologist'),('allergist','Allergist'),('neurologist','Neurologist'),('neuro_surgeon','Neuro Surgeon'),('cardiologist','Cardiologist'),
                                                    ('rheumatologists','Rheumatologists'),('endocrinologist','Endocrinologist'),('nephrologist','Nephrologist'),('psychology','Psychology')])


    submit = SubmitField('Add Disease')
