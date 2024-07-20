from flask import Flask,render_template,redirect,request,url_for,flash
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_
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
                return redirect(url_for('admin_dash'))
            else:
                return 'incorrect Credentials',404


@app.route('/admin/dashboard')                                  # admin dashboard
def admin_dash():
    sponsors=Sponsor.query.all()
    infs=Influencer.query.all()
    camps=Campaign.query.all()
    return render_template('admin_dashboard.html',sponsors=sponsors,infs=infs,camps=camps)

@app.route('/admin/search',methods=['GET','POST'])                                         # admin search for all
def search_all():

    if request.method=='POST':
        query = request.form.get('query')
        search = "%{}%".format(query)
        campaigns = Campaign.query.filter(
        or_(
            Campaign.name.like(search),
            Campaign.categories.has(Category.name.like(search))
        )
        ).all()

        sponsors= Sponsor.query.filter(
            or_(Sponsor.username.like(search),
                Sponsor.company_name.like(search),
                Sponsor.industry.like(search)
            )
        ).all()

        influencers = Influencer.query.filter(
        or_((Influencer.f_name.like(search)),
        (Influencer.l_name.like(search)),
        (Influencer.username.like(search)),
        (Influencer.category.has(Category.name.like(search)))
        )).all()
        return render_template('search.html',sponsors=sponsors,influencers=influencers,campaigns=campaigns)
    return render_template('search.html')


@app.route('/admin/campaign/<int:camp_id>',methods=['GET','POST'])              #admin views campaign desc
def admin_camp(camp_id):
    camp=Campaign.query.filter_by(campaign_id=camp_id).first()
    if request.method=='POST':
        flag_status=int(request.form.get('flag'))
        camp.flagged=flag_status
        db.session.commit()
        return redirect(url_for('search_all'))
    return render_template("admin_campaign.html",camp=camp)

@app.route('/admin/ads/<int:ad_id>')                                       # admin views ad details
def admin_ad_details(ad_id):
    ad=Adrequest.query.filter_by(ad_id=ad_id).first()
    return render_template('admin_ad_details.html',ad=ad)

@app.route('/admin/sponsors/<int:sponsor_id>',methods=['GET','POST'])                 #admin finds sponsors
def admin_sponsor(sponsor_id):
    sponsor=Sponsor.query.filter_by(sponsor_id=sponsor_id).first()
    if request.method=='POST':
        flag_status=int(request.form.get('flag'))
        sponsor.flagged=flag_status
        db.session.commit()
        return redirect(url_for('admin_sponsor',sponsor_id=sponsor_id))
    return render_template("admin_sponsor.html",sponsor=sponsor)

@app.route('/admin/influencers/<int:inf_id>',methods=['GET','POST'])                 #admin finds influencers
def admin_inf(inf_id):
    inf=Influencer.query.filter_by(influencer_id=inf_id).first()
    ads=Adrequest.query.filter_by(influencer_id=inf_id).all()
    if request.method=='POST':
        flag_status=int(request.form.get('flag'))
        inf.flagged=flag_status
        db.session.commit()
        return redirect(url_for('admin_inf',inf_id=inf_id))
    return render_template("admin_influencer.html",inf=inf,ads=ads)

@app.route("/admin/remove/<name>",methods=['GET','POST'])               #admin removes user/campaign
def remove(name):
    sponsor=Sponsor.query.filter_by(username=name).first()
    inf=Influencer.query.filter_by(username=name).first()
    camp=Campaign.query.filter_by(name=name).first()
        
    if request.method=='POST':
        print('HI about to delete')
        if sponsor:
            db.session.delete(sponsor)
        if inf:
            db.session.delete(inf)
        if camp:
            ads=Adrequest.query.filter_by(campaign_id=camp.campaign_id).all()
            db.session.delete(camp)
            for ad in ads:
                db.session.delete(ad)

        db.session.commit()
        return redirect(url_for("admin_dash"))
    return render_template('remove.html',name=name)




@app.route('/sponsor/register',methods=['GET','POST'])              #sponsor registration
def sp_register():
    
        
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('pwd')
        company_name=request.form.get('company_name')
        budget=request.form.get('budget')
        initial_budget=request.form.get('budget')
        industry=request.form.get('industry')
        new_sponsor=Sponsor(username=username,password=password,company_name=company_name,
                            budget=budget,initial_budget=initial_budget,industry=industry)
        try:
            db.session.add(new_sponsor)
            db.session.commit()
            return redirect(url_for('sp_login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username or company name already exists.', 'error')
            # return redirect(url_for('sp_register'))


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
        rating=request.form.get('rating')

        new_influencer=Influencer(username=u_name,password=pwd,f_name=f_name,l_name=l_name,
                                  category_id=cat_id,niche_id=niche_id,social_media=social,
                                  subs=reach,rating=rating)
        try:
            db.session.add(new_influencer)
            db.session.commit()
            
            return redirect(url_for('in_login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username already exists.', 'error')
            # return redirect(url_for('in_register'))

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

@app.route('/<username>/search_influencers')                                                           # search for influencers
def search_inf(username):
    query = request.args.get('query')
    sponsor=Sponsor.query.filter_by(username=username).first()
    if not query:
        return render_template('search_infs.html', influencers=[],user=sponsor)
    
    search = "%{}%".format(query)
    influencers = Influencer.query.filter(
        or_((Influencer.f_name.like(search)),
        (Influencer.l_name.like(search)),
        (Influencer.username.like(search)),
        (Influencer.niche.has(Niche.name.like(search))),
        (Influencer.category.has(Category.name.like(search))),
        (Influencer.subs.like(search))),
        Influencer.flagged==0
    ).all()
    return render_template('search_infs.html', infs=influencers,user=sponsor)

@app.route('/<username>/search_campaigns') 
def search_campaign(username):
    query = request.args.get('query')
    inf=Influencer.query.filter_by(username=username).first()
    if not query:
        return render_template('search_campaigns.html', campaigns=[],inf=inf)

    search = "%{}%".format(query)
    campaigns = Campaign.query.filter(
        and_(
            or_(
                Campaign.name.like(search),
                Campaign.categories.has(Category.name.ilike(search))
            ),
            Campaign.visibility == 'public',
            Campaign.flagged == 0,
            Campaign.status != 'completed'
        )
    ).all()

    return render_template('search_campaigns.html', camps=campaigns,inf=inf)

@app.route('/<username>/influencer_details/<int:inf_id>',methods=['GET','POST'])
def inf_descriptions(username,inf_id):
    inf=Influencer.query.filter_by(influencer_id=inf_id).first()
    sponsor=Sponsor.query.filter_by(username=username).first()
    if request.method=='POST':
        ad_id=request.form.get('ad_id')

        ad=Adrequest.query.filter_by(ad_id=ad_id).first()
        ad.status='requested to influencer'
        ad.influencer_id=inf_id
        db.session.commit()
        return redirect(url_for('search_inf',username=username))
    return render_template('inf_details.html',inf=inf,user=sponsor)
