from flask import Flask,render_template,redirect,request,url_for,flash
from sqlalchemy.exc import IntegrityError
from flask import current_app as app
from .models import *
from .users import *
from .campaigns import *
from .payment import *
from .ads import *
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
            return 'user not found',404
        else:
            if password==user.password:
                return render_template('admin_dashboard.html')
            else:
                return 'incorrect Credentials',404


@app.route('/sponsor/register',methods=['GET','POST'])              #sponsor registration
def sp_register():
    
        
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('pwd')
        company_name=request.form.get('company_name')
        budget=request.form.get('budget')
        industry=request.form.get('industry')
        new_sponsor=Sponsor(username=username,password=password,company_name=company_name,budget=budget,industry=industry)
        try:
            db.session.add(new_sponsor)
            db.session.commit()
            return redirect(url_for('sp_login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username or company name already exists.', 'error')
            return redirect(url_for('sp_register'))


    return render_template('sponsor_reg.html')


@app.route('/sponsor/login',methods=['GET','POST'])                 # sponsor login
def sp_login():
    if request.method=='GET':
        return render_template('sponsor_login.html')
    else:
        username=request.form.get('username')
        password=request.form.get('pwd')
        user=Sponsor.query.filter_by(username=username).first()
        if not(user):
            return 'user not found',404
        else:
            if password==user.password:
                return redirect(url_for('sp_dash',username=user.username))
            else:
                return 'incorrect Credentials',404
    
@app.route('/sponsor/<username>/dashboard',methods=['GET','POST'])              # sponsor dashboard
def sp_dash(username):
    #if request.method=='GET':
    user = Sponsor.query.filter_by(username=username).first()
    print(user.flagged)
    if int(user.flagged)==1:
        return 'You have been flagged, Contact Admin !',400 
    return render_template('sponsor_dash.html',user=user)


@app.route('/influencer/register', methods=['GET','POST'])                  # influencer registration
def in_register():
    
    cat=Category.query.all()
    if request.method=='POST':
        f_name=request.form.get('f_name')
        l_name=request.form.get('l_name')
        u_name=request.form.get('username')
        pwd=request.form.get('pwd')
        cat_id=request.form.get('category')
        niche_id=request.form.get('niche')
        social=request.form.get('social')
        reach=request.form.get('reach')

        new_influencer=Influencer(username=u_name,password=pwd,f_name=f_name,l_name=l_name,
                                  category_id=cat_id,niche_id=niche_id,social_media=social,subs=reach)
        try:
            db.session.add(new_influencer)
            db.session.commit()
            flash('sponsor registered successfully','success')
            return redirect(url_for('in_login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect(url_for('in_register'))

    return render_template('influencer_reg.html',category=cat)

@app.route('/influencer/login',methods=['GET','POST'])                          # influencer login
def in_login():
    if request.method=='GET':
        return render_template('influencer_login.html')
    else:
        username=request.form.get('username')
        password=request.form.get('pwd')
        user=Influencer.query.filter_by(username=username).first()
        if not(user):
            return 'user not found',404
        else:
            if password==user.password:
                return redirect(url_for('in_dash',username=username))
            else:
                return 'incorrect Credentials',404

@app.route('/influencer/<username>/dashboard',methods=['GET','POST'])                          # influencer dashboard
def in_dash(username):
    inf=Influencer.query.filter_by(username=username).first()
    inf_ads=Adrequest.query.filter_by(influencer_id=inf.influencer_id).all()
    if int(inf.flagged)==1:
        return 'You have been flagged, Contact Admin !',400 
            
    
    return render_template('influencer_dash.html',inf=inf,ads=inf_ads)