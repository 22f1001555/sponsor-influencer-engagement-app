from flask import Flask,render_template,redirect,request,url_for
from flask import current_app as app
from .models import *
from .users import *
from .campaigns import *
from .payment import *
from datetime import datetime



@app.route('/')                                                     #Index page
def home():
    return render_template('index.html')


@app.route('/admin/login', methods=['GET','POST'])                 #Admin login
def ad_login():
    if request.method=='GET':
        return render_template('admin_login.html')
    else:
        username=request.form.get('username')
        password=request.form.get('pwd')
        user=Admin.query.filter_by(username=username).first()
        if not(user):
            return 'user not found'
        else:
            if password==user.password:
                return render_template('admin_dashboard.html')
            else:
                return 'incorrect password,try again'


@app.route('/sponsor/register',methods=['GET','POST'])              #sponsor registration
def sp_register():
    if request.method=='GET':
        return render_template('sponsor_reg.html')
    else:
        username=request.form.get('username')
        user=Sponsor.query.filter_by(username=username).first()
        if user!=None:
            if user.username:
                return '<h3 style="text-allign:center">user already exists</h3><h3>try using a different user name</h3>'
        password=request.form.get('pwd')
        company_name=request.form.get('company_name')
        budget=request.form.get('budget')
        industry=request.form.get('industry')
        new_sponsor=Sponsor(username=username,password=password,company_name=company_name,budget=budget,industry=industry)
        db.session.add(new_sponsor)
        db.session.commit()
        return redirect('/sponsor/login')



@app.route('/sponsor/login',methods=['GET','POST'])                 # sponsor login
def sp_login():
    if request.method=='GET':
        return render_template('sponsor_login.html')
    else:
        username=request.form.get('username')
        password=request.form.get('pwd')
        user=Sponsor.query.filter_by(username=username).first()
        if not(user):
            return 'user not found'
        else:
            if password==user.password:
                return redirect(url_for('sp_dash',username=user.username))
            else:
                return 'incorrect password,try again',404
    
@app.route('/sponsor/<username>/dashboard',methods=['GET','POST'])              # sponsor dashboard
def sp_dash(username):
    if request.method=='GET':
        user = Sponsor.query.filter_by(username=username).first()
        
        return render_template('sponsor_dash.html',user=user)
