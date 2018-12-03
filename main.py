from flask import Flask, flash, request,render_template, redirect, url_for, session
from flask_pymongo import PyMongo
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
import random
import webview
import datetime
app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'heroku_8cscwvjn'
app.config['MONGO_URI'] = 'mongodb://elvis:123elvischuks@dbh54.mlab.com:27547/heroku_8cscwvjn'
app.secret_key = 'mysecretkeyisakey'
mongo = PyMongo(app)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def index():


    return render_template('home.html')

#user login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = mongo.db.users
        check_user = user.find_one({"regno":request.form['regno']})

        #check_pass = user.find_one({})
        if check_user:
            if check_user['password'] == request.form['password']:
                session['regno'] = request.form['regno']
                return redirect(url_for('create'))

        return 'user doesnt exist'
    return render_template('login.html')
#admin login route
@app.route('/admin-login', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        user = mongo.db.adminusers
        check_user = user.find_one({"adminid":request.form['regno']})

        #check_pass = user.find_one({})
        if check_user:
            if check_user['password'] == request.form['password']:
                session['adminid'] = request.form['regno']
                return redirect(url_for('adminpage'))

        return 'user doesnt exist'
    return render_template('login.html')

#route for admin page
@app.route('/adminpage')
def adminpage():
    return render_template('admin.html')

#route for user registration accessed through the admin dashboard
@app.route('/register', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        user = mongo.db.users
        existing_user = user.find_one({'regno': request.form['regno']})
        if existing_user is None:
            user.insert({'regno':request.form['regno'],
            'password':request.form['password'],
            'fname':request.form['fname'],
            'lname':request.form['lname'],
            'office':request.form['office']})
            session['adminid'] = request.form['regno']
        return redirect(url_for('adminpage'))
    return render_template('reg.html')


#route for administrator registration
@app.route('/adminregister', methods=['GET', 'POST'])
def adminreg():
    if 'adminid' in session:

        if request.method == 'POST':
            user = mongo.db.adminusers
            existing_user = user.find_one({'adminid': request.form['regno']})
            if existing_user is None:
                user.insert({'adminid':request.form['regno'],
                'password':request.form['password'],
                'fname':request.form['fname'],
                'lname':request.form['lname'],
                'office':request.form['office']})
                session['regno'] = request.form['regno']
                return redirect(url_for('adminpage'))
        return render_template('adminreg.html')
    return redirect(url_for('login'))
#route for user management accessed through the admin dashboard
@app.route('/manageusers')
def manageusers():
    return render_template('manageusers.html')

#ROUTE FOR USER CREATION
@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'regno' in session:
        user = mongo.db.users
        cuur = user.find_one({'regno':session['regno']})
        logg = cuur['fname']
        if request.method == 'POST':

            id = random.randint(100,600)
            p = id
            patient = mongo.db.patientdata
            patient.insert({
            'User': session['regno'],
            'p_id':str(id),
            'First name': request.form['fname'],
            'Last name':request.form['lname'],
            'date of birth':request.form['date'],
            'Phone number':request.form['phone'],
            'Address':request.form['Address'],
            'Next of kin':request.form['nxtkin'],
            'Kin number':request.form['nxtkinphone'],
            'Relation to kin':request.form['relakin'],
            'Kin address':request.form['relaAddress'],
            'Occupation':request.form['occupation'],
            'Relations':request.form['relations'],
            'Gender':request.form['gender']
            })
            #flash('added patient')
            return  'your p_id is : ' + str(p)
        return render_template('add.html', logg=logg)
    return redirect(url_for('login'))
#ROUTE FOR ANTENATAL
@app.route('/ante', methods=['GET', 'POST'])
def ante():
    if 'regno' in session:
        user = mongo.db.users
        cuur = user.find_one({'regno':session['regno']})
        logg = cuur['fname']

        if request.method == 'POST':
            anten = mongo.db.antenatal
            id = random.randint(100,600)
            anten.insert({
            'User': session['regno'],
            'p_id':str(id),
            'surname': request.form['lname'],
            'other names':request.form['fname'],
            'Address':request.form['addy'],
            'home town':request.form['hmtn'],
            'age':request.form['age'],
            'marital status':request.form['mst'],
            'Religion':request.form['religion'],
            'occupation':request.form['occu'],
            'husbands name':request.form['hname'],
            'husbands occupation':request.form['hoccu'],
            'heart disease':request.form['hdis'],
            'kidney disease':request.form['kdis'],
            'yaws or Syphilis':request.form['yrs'],
            'Hypertension':request.form['hyp'],
            'Diabetes':request.form['dib'],
            'Previous operations':request.form['po'],
            'other':request.form['oth'],
            'twins':request.form['twins'],
            'Malformations':request.form['mal'],
            'tuberculosis':request.form['tub'],
            'date of booking':request.form['dofb'],
            'LMP':request.form['lmp'],
            'EDD':request.form['edd'],
            'bleeding':request.form['bleeding'],
            'duration of pregnancy':request.form['dup'],
            'FMF':request.form['fmf'],
            'headache':request.form['headache'],
            'Vomiting':request.form['vom'],
            'Oedema':request.form['oedema'],
            'Constipation':request.form['const'],
            'Urinary Symptoms':request.form['usymp'],
            'Jaundice':request.form['jaund'],
            'other symptoms':request.form['osymp'],
            'Vaginal discharge ':request.form['Vadis'],
            'taken by':request.form['taby'],
            'made by':request.form['mdby'],
            'pdate':request.form['pdate'],
            'height':request.form['height'],
            'weight':request.form['weight'],
            'BP':request.form['bp'],
            'sb':request.form['sb'],
            'General condition':request.form['gc'],
            'Malnutrition':request.form['mal'],
            'clinical anaemia':request.form['clia'],
            'CVS':request.form['cvs'],
            'RS':request.form['rs'],
            'Liver':request.form['liv'],
            'spleen':request.form['spleen'],
            'Breasts':request.form['breasts'],
            'Heigth of funds':request.form['hof'],
            'Abnormalities':request.form['abnor'],
            'Vaginal Examination':request.form['vage'],
            'Urine protien':request.form['up'],
            'Glucose':request.form['glu'],
            'pelvic assesment scan':request.form['pas'],
            'ndate':request.form['dap'],
            'inlet':request.form['inlet'],
            'Promontory reached at':request.form['pra'],
            'not reached':request.form['nr'],
            'Cavity':request.form['cav'],
            'outlet':request.form['outlet'],
            'Soft tissues':request.form['st'],
            'accessed by':request.form['asb']


            })
        return render_template('ante.html')


    return redirect(url_for('login'))



#ROUTE FOR VIEW User
#I HAVEN'T COMPLETED THE LOGIC
@app.route('/viewante', methods=['GET', 'POST'])
def viewante():
    if 'regno' in session:
        user = mongo.db.users
        cuur = user.find_one({'regno':session['regno']})
        logg = cuur['fname']
        if request.method == 'POST':
            antep =mongo.db.antenatal
            antexe = mongo.db.antenatalexam
            finde = antexe.find({'p_id':request.form['p_id']})
            y = (egg for egg in finde)
            find = antep.find_one({'p_id': request.form['p_id']})
            if find is None:
                return redirect(url_for('viewante'))
            pat = find['surname']
            lname = find['other names']
            addy = find['Address']
            hmtwn = find['home town']
            age = find['age']
            marstat = find['marital status']
            religion = find['Religion']
            occu = find['occupation']
            husnme = find['husbands name']
            husocc = find['husbands occupation']
            return render_template('viewante.html', y=y,pat=pat,lname=lname,addy=addy,hmtwn=hmtwn,age=age,marstat=marstat,religion=religion,husocc=husocc,occu=occu,husnme=husnme)
        return render_template('viewante.html')
    return redirect(url_for('login'))
@app.route('/view', methods=['GET', 'POST'])
def view():
    if 'regno' in session:
        user = mongo.db.users
        cuur = user.find_one({'regno':session['regno']})
        logg = cuur['fname']

        if request.method == 'POST':
            patient = mongo.db.patientdata
            treatment = mongo.db.treatment
            exam = mongo.db.antenatalexam
            find = patient.find_one({'p_id': request.form['p_id']})
            findt = treatment.find({'p_id': request.form['p_id']})

            #.forEach(function(doc)(print(doc.treatment)))
            x = ('Date' + ' : ' + doc['date'] + '  '+ 'Treatment' + ' : ' + doc['treatment'] for doc in findt)



            if find is None:
                return redirect(url_for('view'))

            pat = find['First name']
            lname = find['Last name']
            dob = find['date of birth']
            phone = find['Phone number']
            addy = find['Address']
            nxt = find['Next of kin']
            nxtno = find['Kin number']
            relakin = find['Relation to kin']
            kinaddy = find['Kin address']
            occ = find['Occupation']
            rela = find['Relations']


            tre = x

            #[{"text":"first"}, {"text":"second"}]



            return render_template('view.html',  occ=occ, rela=rela,nxtno=nxtno,relakin=relakin, kinaddy=kinaddy,dob=dob,phone=phone,addy=addy,nxt=nxt, pat=pat, tre=tre, lname=lname)
        return render_template('view.html', logg=logg)
    return redirect(url_for('login'))


#ROUTE FOR ADD TREATMENT AS YOU CAN SEE
@app.route('/addtreat', methods=['GET','POST'])
def addtreat():
    if 'regno' in session:
        user = mongo.db.users
        cuur = user.find_one({'regno':session['regno']})
        logg = cuur['fname']

        if request.method == 'POST':
            treatment = mongo.db.treatment
            treatment.insert({
            'date':request.form['date'],
            'p_id':request.form['p_id'],
            'treatment':request.form['treatm'],
            'remarks':request.form['remarks']})

        return render_template('addtreat.html', logg=logg)
    return redirect(url_for('login'))
@app.route('/anteexe', methods=['GET', 'POST'])
def anteexe():
    if 'regno' in session:
        user = mongo.db.users

        if request.method == 'POST':
            exam = mongo.db.antenatalexam
            x = datetime.datetime.now()

            exam.insert({
            "regno": session['regno'],
            "p_id":request.form['p_id'],
            "date":x,
            "haf":request.form['haf'],
            "presentation and lie":request.form['pal'],
            "Relation of PP to Brim":request.form['rpp'],
            "Feotal heart":request.form['fh'],
            "Urine":request.form['urine'],
            "Weight":request.form['weight'],
            "BP":request.form['bp'],
            "HB":request.form['hb'],
            "Oedema":request.form['oed'],
            "remarks":request.form['rem'],
            "treatment":request.form['treat'],
            "next visit":request.form['nxtv']

            })
            return redirect(url_for('anteexe'))
        return render_template('anteexe.html')
    return redirect(url_for('login'))

#ROUTE FOR REMOVING USERS
@app.route('/remove', methods=['GET', 'POST'])
def remove():
    if 'adminid' in session :
        if request.method == 'POST':
            user = mongo.db.users
            curr = user.find_one({'regno':request.form['user_id']})
            if curr :
                user.remove({'regno':request.form['user_id']})
            return redirect(url_for('adminpage'))
        return render_template('remove.html')
    return redirect(url_for('login'))
@app.route('/<path:pat>')
def patients(pat):
    if 'adminid' in session:
        patient = mongo.db.patientdata
        treatment = mongo.db.treatment
        findp = patient.find_one({"p_id":pat})
        name = findp['First name']
        return render_template('patients.html', name=name)
    return redirect(url_for('login'))
@app.route("/view_users")
def view_users():
    if 'adminid' in session:
        user = mongo.db.patientdata
        findu = user.find()
        patients = (doc['p_id'] + '  '+ doc['First name'] for doc in findu)

        return render_template('viewusers.html', patients=patients)

    return redirect(url_for('login'))
#USER LOGOUT, DESTROYS USER SESSION ID
@app.route('/logout')
def logout():
    if 'regno' in session:
        session.pop('regno', None)
        return redirect(url_for('login'))
    return redirect(url_for('index'))

#I KNOW I COULD HAVE JUST USED ANIF STATEMENT TO MANAGE THE TWO LOGOUTS BUT I WAS LAZY LOL AND I WANTED TO BE A LITTLE EXTRA.
@app.route('/adminlogout')
def adminlogout():
    if 'adminid' in session:
        session.pop('adminid', None)
        return redirect(url_for('login'))
    return redirect(url_for('adminpage'))

#RUNS THE APP.
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
