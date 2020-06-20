
from web import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(doctor_id):
    return Doctor.query.get(int(doctor_id))


def load_patient(patient_id):
    return Patient.query.get(int(patient_id))



class Patient(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='padefault.jpeg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return "Patient('{self.username}', '{self.email}', '{self.image_file}')"

class Disease(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    diseasename = db.Column(db.String(20), unique=True, nullable=False)
    chronic = db.Column(db.Boolean, unique=False, nullable =False)
    speciality = db.Column(db.String, unique=False, nullable =False)

    def __repr__(self):
        return "Disease('{self.diseasename}','{self.chronic}','{self.speciality}')"


class Doctor(db.Model,UserMixin):
    __searchable__ = ['username','speciality']
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='static/profile_pics/default.png')
    password = db.Column(db.String(60), nullable=False)
    speciality = db.Column(db.String(60), nullable=False)
    slmcno = db.Column(db.Integer ,unique=True, nullable=False)
    hospital = db.Column(db.String(60), nullable=False)


    def __repr__(self):
        return "Doctor('{self.username}', '{self.email}', '{self.speciality}', '{self.slmcno}','{self.hospital}','{self.image_file}')"

class Doctorpatient(db.Model, UserMixin):
    __searchable__ = ['doctorname', 'patientname']
    id = db.Column(db.Integer, primary_key=True)
    doctorname = db.Column(db.String(20), unique=True, nullable=False)
    patientname = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return "Doctorpatient('{self.doctorname}','{self.patientname}')"