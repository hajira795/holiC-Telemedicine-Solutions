import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from web import website, db, bcrypt,dbconn
from web.forms import  LoginForm , PatientRegistration , Registration ,PatientLoginForm ,UpdatePatientProfileForm ,UpdateDoctorProfileForm , UpdateHospitalForm , AnalyzeSymptoms, Diseases, PsychologicalSymptoms, DrList
from web.models import Doctor , Patient, Disease, Doctorpatient
from flask_login import login_user, current_user, logout_user, login_required
from web import socketio
from web.code import DecisionTree, NaiveBayes
#from web.psychocode import PNaiveBayes

pname =''

@website.route('/')
@website.route('/index')
def index():
    return render_template("index.html")


@website.route('/doctor', methods=['GET', 'POST'])
def doctor():
        return render_template('doctor.html')


@website.route('/patient', methods=['GET', 'POST'])
def patient():
        return render_template('patient.html')

@website.route('/requestdoctor', methods=['GET', 'POST'])
def request_doctor():
        return render_template('Doctorrequest.html')





@website.route("/dregdetail", methods=['GET', 'POST'])
def register():
    form = Registration()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        doctor = Doctor(username=form.username.data, email=form.email.data, speciality=form.speciality.data,  slmcno=form.slmcno.data, hospital=form.hospital.data, password=hashed_password)
        db.session.add(doctor)
        db.session.commit()
        flash('Doctor Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('doctorlogin'))
    return render_template('dregdetail.html', title='Register', form=form)



@website.route("/doctorlogin", methods=['GET', 'POST'])
def doctorlogin():
    form = LoginForm()
    if form.validate_on_submit():
        doctor = Doctor.query.filter_by(email=form.email.data).first()
        if doctor and bcrypt.check_password_hash(doctor.password, form.password.data):
            login_user(doctor, remember=form.remember.data)
            return redirect(url_for('doctor_profile'))
        else:
            flash('Login Unsuccessful. Please check Email and Password', 'danger')

    #elif request.method == 'GET':
        #return redirect(url_for('doctor_login'))
    return render_template('doctorlogin.html', title='Login', form=form)

@website.route("/patientReg", methods=['GET', 'POST'])
def register_patient():
    form = PatientRegistration()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        patient = Patient(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(patient)
        db.session.commit()
        flash(' Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('patient_login'))
    return render_template('patientReg.html', title='Registration', form=form)


@website.route("/plogin", methods=['GET', 'POST'])
def patient_login():
    form = PatientLoginForm()
    global pname
    if form.validate_on_submit():
        patient = Patient.query.filter_by(email=form.email.data).first()



        if patient and bcrypt.check_password_hash(patient.password, form.password.data):
            login_user(patient, remember=form.remember.data)
            form.email = patient.email
            print(patient.username)
            #return redirect(url_for('patient_profile'))
            pname = patient.username
            return render_template('PatientProfile.html',form=form)
        else:
            flash('Login Unsuccessful. Please check Email and Password', 'danger')
    return render_template('plogin.html', title='Login', form=form)

@website.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('Patient'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(website.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@website.route("/PatientProfile",methods=['GET', 'POST'])
@login_required
def patient_profile():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('PatientProfile.html', title='PatientProfile',image_file=image_file)


@website.route("/DoctorProfile",methods=['GET', 'POST'])
@login_required
def doctor_profile():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('DoctorProfile.html', title='DoctorProfile',image_file=image_file)

@website.route('/patientaccount', methods=['GET', 'POST'])
def patient_account():
    form = UpdatePatientProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('patient_account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('patientaccount.html', title='PatientAccount', image_file=image_file, form=form)

@website.route('/updatehospital', methods=['GET', 'POST'])
def update_hospital():
    form = UpdateHospitalForm()
    if form.validate_on_submit():
        current_user.hospital = form.hospital.data
        db.session.commit()
        flash('Your Hospital has been updated!', 'success')
        return redirect(url_for('doctor_profile'))
    elif request.method == 'GET':
        form.hospital.data = current_user.hospital
        return render_template('updatehospital.html', title='UpdateHospital', form=form)

@website.route('/doctoraccount', methods=['GET', 'POST'])
def doctor_account():
    form = UpdateDoctorProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('doctor_account'))
    elif request.method == 'GET':
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('doctoraccount.html', title='DoctorAccount', image_file=image_file, form=form)






@website.route('/chat' ,methods=['GET', 'POST'])
def chat_message():
    return render_template('chatmessage.html')


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')



@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

@website.route('/analyzesymptoms',methods=['GET','POST'])
def analyze_symptoms():
    form = AnalyzeSymptoms()
    if request.method == 'POST' and request.form['submit_button']=='Analyze Symptoms':
        #if form.validate() == False:
           # flash('All fields are required.')
            #return render_template('analyzesymptoms.html', form=form)
        #else:
            dis = NaiveBayes(form.symptom1.data,form.symptom2.data,form.symptom3.data,form.symptom4.data,form.symptom5.data)
            print(dis)
            form.prediction.data = dis
            disease = Disease.query.filter_by(diseasename=form.prediction.data).first()
            if dis not in ('Dengue','Common Cold','Allergy','Drug Reaction','Gastroenteritis','Malaria','Chicken pox','Typhoid','Pneumonia'):
                flash('You have a chronic disease if you need psychological support please click on the analyze psychological symptomps button')
                print(disease.speciality)
                return render_template('analyzesymptoms.html', form=form,pname=form.name)
            else:
                return render_template('analyzesymptoms.html', form=form, pname=form.name)
    elif request.method == 'POST' and request.form['submit_button']=='Find Doctor':
        disease = Disease.query.filter_by(diseasename=form.prediction.data).first()
        drlist = Doctor.query.filter_by(speciality=disease.speciality).all()
        for row in drlist:
            print (row.username)
        return render_template('drlist.html',form=drlist,pname=form.name)
    elif request.method == 'POST' and request.form['submit_button'] == 'Analyze Psychological Symptoms':
        form = PsychologicalSymptoms()
        return render_template('psychologicalsymptoms.html',form=form, pname=form.name)
    else:
        return render_template('analyzesymptoms.html', form=form,pname=form.name)

@website.route('/psychologicalsymptoms',methods=['GET','POST'])
def psychological_symptoms():
    form = PsychologicalSymptoms()
    chronicdisease = form.prediction.data
    disease = Disease.query.filter_by(diseasename=chronicdisease).first()
    drlist = Doctor.query.filter_by(speciality='psychological').all()
    drlist1 = Doctor.query.filter_by(speciality=disease.speciality).all()
    if request.method == 'POST' and request.form['submit_button'] == 'Analyze Symptoms':
        if (form.symptom1.data or form.symptom2.data or form.symptom3.data or form.symptom4.data or form.symptom5.data == 'hallucinations auditory') or (form.symptom1.data or form.symptom2.data or form.symptom3.data or form.symptom4.data or form.symptom5.data == 'suicidal') or (form.symptom1.data or form.symptom2.data or form.symptom3.data or form.symptom4.data or form.symptom5.data == 'unconscious state'):
            flash('we recommend you to get  psychological help, you might have disorders like psychosis please see the set of doctors')
            return render_template('psychologicalsymptoms.html',form=form)
        elif (form.symptom1.data or form.symptom2.data or form.symptom3.data or form.symptom4.data or form.symptom5.data == 'Feeling nervous') or (form.symptom1.data or form.symptom2.data or form.symptom3.data or form.symptom4.data or form.symptom5.data == 'Feeling weak') or (form.symptom1.data or form.symptom2.data or form.symptom3.data or form.symptom4.data or form.symptom5.data == 'Feeling nervous') or (form.symptom1.data or form.symptom2.data or form.symptom3.data or form.symptom4.data or form.symptom5.data == 'Loss of energy'):
            flash('You might Have Anxiety and Depression please see the doctor list')
            return render_template('psychologicalsymptoms.html',form=form)
        else:
            flash('Although you might not mentally disturbed with the chronic disease you have please see a psychologist')
            return render_template('psychologicalsymptoms.html',form=form)
    elif request.method == 'POST' and request.form['submit_button']=='Find Doctor':
        return render_template('drlist.html',psychodata=drlist,data=drlist1,disease=chronicdisease)
    else:
        return render_template('psychologicalsymptoms.html',form=form)
@website.route('/diseases',methods=['GET','POST'])
def diseases():
    form = Diseases()
    if request.method == 'POST':
        disease = Disease(diseasename=form.disease.data, chronic=form.chronic.data, speciality=form.speciality.data)
        db.session.add(disease)
        db.session.commit()
        return render_template('diseases.html',form=form)
    else:
        return render_template('diseases.html', form=form)

@website.route('/drlist',methods= ['GET','POST'])
def drlist():
    if request.method == 'POST':
        global pname
        doctorpatient = Doctorpatient(doctorname=request.form['submit_button'], patientname=pname)
        print(request.args.get('speciality'))
        db.session.add(doctorpatient)
        db.session.commit()
        return render_template('drlist.html',pname=pname)
    else:
        return render_template('drlist.html',pname=doctorpatient.patientname)

@website.route('/drcircle',methods=['GET','POST'])
def drcircle():
    if request.method == 'GET':
        global pname
        drcirc = Doctorpatient.query.filter_by(patientname=pname).all()
        print(drcirc)
        return render_template('drcircle.html',drcirc=drcirc)
    else:
        return render_template('drcircle.html',pname=pname)

