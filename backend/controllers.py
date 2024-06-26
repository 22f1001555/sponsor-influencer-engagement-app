from flask import Flask,render_template,redirect,request
from flask import current_app as app

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin/login')
def ad_login():
    return render_template('admin_login.html')

@app.route('/sponsor/login',methods=['GET','POST'])
def sp_login():
    if request.method=='GET':
        return render_template('sponsor_login.html')
    #else:
        #verify use=sponsor in database
        #return render_template('sp_dash.html',user=user)

@app.route('/influencer/login')
def in_login():
    return render_template('influencer_login.html')

@app.route('/sponsor/register')
def sp_register():
    return render_template('sponsor_reg.html')

@app.route('/influencer/register')
def in_register():
    return render_template('influencer_reg.html')