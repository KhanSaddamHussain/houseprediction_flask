from flask import Flask, render_template,request, flash,redirect,session
from joblib import dump,load
import numpy as np
import os
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail



with open('config.json','r')  as c:

    params = json.load(c)["params"]


app = Flask(__name__)
app.secret_key= 'secret-key'
app.config.update(
    MAIL_SERVER= 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail_user'],
    MAIL_PASSWORD = params['gmail_pwd']
)


model=load('model.joblib')



local_server = True;

if( local_server ):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']


db = SQLAlchemy(app)

class Contact( db.Model ):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(20), nullable=True)
    phone_no = db.Column(db.String(12),  nullable=False)
    msg = db.Column(db.String(200),  nullable=False)
    date = db.Column(db.String(12),  nullable=True)

class Signup(db.Model):
    sno = db.Column(db.Integer,primary_key=True,nullable=False)
    name = db.Column(db.String(30))
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    email = db.Column(db.String(30))
    city = db.Column(db.String(30))
    phone_no = db.Column(db.String(30))
    # gender = db.Column(db.String(10))
    # age = db.Column(db.Integer)
    address = db.Column(db.String(50))
  


@app.route('/')
@app.route('/home')

def home():
    if 'myuser' in session:
        return render_template('index.html', params=params)
    else:
        return redirect('/login')

    return render_template('index.html', params=params)


@app.route('/predict', methods=['POST'])
def predict():
    d1 = float(request.form['income'])
    d2 = float(request.form['houseage'])
    d3 = float(request.form['noofroom'])
    d4 = float(request.form['noofbedroom'])
    d5 = float(request.form['population'])
    arr = np.array([[d1,d2,d3,d4,d5]])
    predicted_price = model.predict(arr)
    int_price=int(predicted_price)
    price=str(int_price)
    return render_template('index.html', data=price + '$', params=params)

mail=Mail(app)
@app.route("/contact",methods=['GET','POST'])
def contact():
    if(request.method == 'POST'):
        name = request.form.get("name")
        emailAdd = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("msg")

        entry = Contact(name=name,email=emailAdd,phone_no=phone,msg=message,date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from  '+ name,
                          sender=emailAdd,
                          recipients = [params['gmail_user']],
                          body=message +"\n" + phone,
                          )
        flash("Massaage sent!!! Successfully","success")

    return render_template('contact.html', params=params)

@app.route('/about')
def about():
    return render_template('about.html', params=params)

@app.route('/report')
def report():
    return render_template('report.html')
@app.route('/login',methods=['GET','POST'])
def userLogin():
    if request.method=="POST":
        user_name=request.form['username']
        password=request.form['pass']
        
        row = Signup.query.filter_by(username=user_name).count()
        validating = Signup.query.filter_by(username=user_name).first()
        if row>0:
            if validating.username==user_name and validating.password==password:
                session['myuser']=user_name
                # value = Userinfo.query.filter_by(username = user_name).first()
                
                # users_name = value.name
                flash('successfully login',"success")
                return redirect('/home') 
            else:
                flash("please enter your correct password","warning")
                return redirect('/login')  
                
        else:
            flash("username not found","danger")
            return redirect('/login')   
    return render_template("login.html",params=params)
@app.route('/Signup',methods=['GET','POST'])
def SignUp():
    if request.method=="POST":
        userdetail=request.form
        name=userdetail['name']
        user_name=userdetail['username']
        mypass=userdetail['pass']
        email=userdetail['email']
        city=userdetail['city']
        phoneno=userdetail['phoneno']
        
        address=userdetail['address']
        
        entry = Signup(name=name,username=user_name,password=mypass,email=email,city=city,phone_no=phoneno,address=address)
        db.session.add(entry)
        db.session.commit()
        flash('You have registered Successfully,Now you can login')
        return redirect('/about')
    return render_template("signup.html",params=params)
@app.route('/Logout')
def admin_logout():
    if 'myuser' in session:
        session.pop('myuser')
    flash(' Successfully logout')
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)



