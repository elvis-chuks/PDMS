from flask import Flask, flash, request,render_template, redirect, url_for, session
from flask_pymongo import PyMongo
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
import random

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'hdbms'
app.config['MONGO_URI'] = 'mongodb://elvis:elvischuks@127.0.0.1:27017/hdbms'
mongo = PyMongo(app)

@app.route('/')
def index():


    return render_template('home.html')


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
            session['regno'] = request.form['regno']
        return redirect(url_for('index'))
    return render_template('reg.html')
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
            patient.insert({'p_id':str(id),
            'First name': request.form['fname'],
            'Last name':request.form['lname'],
            'Blood group':request.form['bldgrp'],
            'Address':request.form['Address'],
            'Next of kin':request.form['nxtkin'],
            'Phone number':request.form['phone'],
            'Genotype':request.form['genotype'],
            'Physical disabilities':request.form['phydis'],
            'Gender':request.form['gender']
            })
            #flash('added patient')
            return  'your p_id is : ' + str(p)
        return render_template('add.html', logg=logg)
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
            find = patient.find_one({'p_id': request.form['p_id']})
            findt = list(treatment.find({'p_id': request.form['p_id']}))
            if find is None:
                return redirect(url_for('view'))

            pat = find['First name']
            lname = find['Last name']
            bg = find['Blood group']
            addy = find['Address']
            nxt = find['Next of kin']
            gen = find['Genotype']
            phy = find['Physical disabilities']

            x = []
            for i in findt:
                x.append(i)
                for b in range(0,1):
                    y = x[b]['treatment']
                    tre = str(y)



            return render_template('view.html', pat=pat, tre=tre, lname=lname, bg=bg, addy=addy, nxt=nxt, gen=gen, phy=phy)
        return render_template('view.html', logg=logg)
    return redirect(url_for('login'))

@app.route('/addtreat', methods=['GET','POST'])
def addtreat():
    if 'regno' in session:
        user = mongo.db.users
        cuur = user.find_one({'regno':session['regno']})
        logg = cuur['fname']

        if request.method == 'POST':
            treatment = mongo.db.treatment
            treatment.insert({'p_id':request.form['p_id'],
            'treatment':request.form['treatm'],
            'remarks':request.form['remarks']})

        return render_template('addtreat.html', logg=logg)
    return redirect(url_for('login'))
@app.route('/logout')
def logout():
    if 'regno' in session:
        session.pop('regno', None)
        return redirect(url_for('login'))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
