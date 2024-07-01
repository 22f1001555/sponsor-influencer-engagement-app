from flask import Flask,render_template,redirect,request,url_for
from flask import current_app as app
from .models import *
from datetime import datetime

@app.route('/')                                                 #Index page
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

@app.route('/<username>/campaigns',methods=['GET','POST'])                  #campagns list of sponsors
def campaigns(username):
    
    campaign_user=Sponsor.query.filter_by(username=username).first()
    if request.method=='GET':
        return render_template('campaigns_page.html',user=campaign_user)

@app.route('/<username>/new_campaign',methods=['GET','POST'])               #create new campaign
def new_campaign(username):
    user=Sponsor.query.filter_by(username=username).first()
    cat=Category.query.all()
    if request.method=='GET':
        return render_template('new_campaign.html',user=user,cat=cat)
    else:
        title=request.form.get('title')
        sponsor_id=request.form.get('sponsor_id')
        category=request.form.get('category')
        start=request.form.get('start')
        end=request.form.get('end')
        budget=request.form.get('budget')
        visibility=request.form.get('visibility')
        goals=request.form.get('goals')
        start_date=datetime.strptime(start, '%Y-%m-%d')
        end_date=datetime.strptime(end, '%Y-%m-%d')

        if end_date<=start_date:
            return "End date must be after start date", 400
        
        new_campaign=Campaign(name=title,sponsor_id=sponsor_id,category_id=category,start_date=start_date.date(),
                              end_date=end_date.date(),budget=budget,visibility=visibility,goals=goals)
        db.session.add(new_campaign)
        db.session.commit()
        return redirect(url_for('campaigns',username=username))

@app.route('/del/<int:id><username>',methods=['POST'])                              # delete a campaign
def del_camp(id,username): 
    if request.method=='POST':
        camp=Campaign.query.filter_by(campaign_id=id).first()
        db.session.delete(camp)
        db.session.commit()
        return redirect(url_for('campaigns',username=username))

@app.route('/campaign_details/<int:id>')                                           # campaign details
def camp_details(id):
    camp=Campaign.query.filter_by(campaign_id=id).first()
    return render_template('campaign_details.html',campaign=camp)








@app.route('/influencer/register', methods=['GET','POST'])                  # influencer registration
def in_register():
    if request.method=='GET':
        cat=Category.query.all()
        return render_template('influencer_reg.html',category=cat)
    else:
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
        
        db.session.add(new_influencer)
        db.session.commit()
        return redirect('/influencer/login')

@app.route('/influencer/login',methods=['GET','POST'])                          # influencer login
def in_login():
    if request.method=='GET':
        return render_template('influencer_login.html')
    else:
        username=request.form.get('username')
        password=request.form.get('pwd')
        user=Influencer.query.filter_by(username=username).first()
        if not(user):
            return 'user not found'
        else:
            if password==user.password:
                return render_template('inf_dashboard.html')
            else:
                return 'incorrect password,try again'


