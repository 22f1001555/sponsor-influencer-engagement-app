from flask import Flask,render_template,redirect,request,url_for,flash
from sqlalchemy.exc import IntegrityError
from flask import current_app as app
from .models import *
from .users import *
from .campaigns import *
from .payment import *
from datetime import datetime



    
@app.route('/<username>/<int:id>/new_ad',methods=['GET','POST'])               #create add
def new_ad(id,username):
    camp=Campaign.query.filter_by(campaign_id=id).first()
    niches=Niche.query.filter_by(cat_id=camp.category_id).all()
    infs=Influencer.query.filter_by(category_id=camp.category_id).all()
    
        

    if request.method=='POST':
        name=request.form.get('name')
        content=request.form.get('content')
        campaign_id=request.form.get('campaign_id')
        influencer_id=request.form.get('influencer_id')
        niche_id=request.form.get('niche_id')
        budget=float(request.form.get('budget'))

        camp.budget=float(camp.budget)-budget
        if float(camp.budget)>=0:


            new_ad=Adrequest(name=name,content=content,campaign_id=campaign_id,
                            influencer_id=influencer_id,niche_id=niche_id,budget=budget)
            try:
                db.session.add(new_ad)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash('Ad already exists','error')
            return redirect(url_for('camp_details',id=id,username=username))
        else:
            return 'Insufficient budget,add more budget to the campaign',404

    return render_template('new_ad.html',camp=camp,infs=infs,niches=niches,username=username)
        
@app.route('/<username>/<int:camp_id>/<int:ad_id>/update',methods=['GET','POST'])       #update ad
def update_ad(ad_id,camp_id,username):
    ad=Adrequest.query.filter_by(ad_id=ad_id).first()
    camp=Campaign.query.filter_by(campaign_id=camp_id).first()
    niches=Niche.query.filter_by(cat_id=camp.category_id).all()
    infs=Influencer.query.filter_by(category_id=camp.category_id).all()

    if ad.status=='accepted':
        return 'can not edit ad after getting accepted by an influencer!'
    
    if request.method=='POST':
        prev_budget=ad.budget
        ad.name=request.form.get('name')
        ad.content=request.form.get('content')
        ad.influencer_id=request.form.get('influencer_id')
        ad.niche_id=request.form.get('niche_id')
        ad.budget=float(request.form.get('budget'))
        if float(prev_budget)!=ad.budget:
            camp.budget=float(camp.budget)+float(prev_budget)
            camp.budget=float(camp.budget)-float(ad.budget)

        db.session.commit()
        return redirect(url_for('camp_details',username=username,id=camp_id))
    
    return render_template('update_ad.html',ad=ad,camp=camp,infs=infs,
                               niches=niches,username=username)
    
@app.route('/del_ad/<username>/<int:camp_id>/<int:ad_id>')                            # delete a ad
def del_ad(ad_id,username,camp_id): 
    ad=Adrequest.query.filter_by(ad_id=ad_id).first()
    camp=Campaign.query.filter_by(campaign_id=camp_id).first()
    camp.budget=float(camp.budget)+float(ad.budget)

    db.session.delete(ad)
    db.session.commit()
    return redirect(url_for('camp_details',username=username,id=camp_id))


@app.route('/<username>/<int:camp_id>/ad_details/<int:ad_id>')                       #ad details                 
def ad_details(camp_id,ad_id,username):
    ad=Adrequest.query.filter_by(ad_id=ad_id).first()
    inf=Influencer.query.filter_by(influencer_id=ad.influencer_id).first()
    sponsor=Sponsor.query.filter_by(username=username).first()
    if ad.status=='accepted' and sponsor!=None:
        temp_stat='Pay Now'
        return render_template('ad_details.html',ad=ad,inf=inf,status=temp_stat,camp_id=camp_id,username=username)
    elif ad.status=='pending' and sponsor==None:
        temp_stat='Negotiate'
        return render_template('ad_details.html',ad=ad,inf=inf,camp_id=camp_id,username=username,status=temp_stat)
    else:
        return render_template('ad_details.html',ad=ad,inf=inf,camp_id=camp_id,username=username)

@app.route('/<username>/ads/<int:ad_id>/status',methods=['POST'])                       #ad status change                 
def ad_status(ad_id,username):
    if request.method=='POST':
        ad_status=request.form.get('status')
        ad=Adrequest.query.filter_by(ad_id=ad_id).first()
        if(ad_status=='rejected'):
            ad.status='rejected'
            ad.campaign.budget=float(ad.campaign.budget)+float(ad.budget)
        else:
            ad.status='accepted'
    db.session.commit()
    return redirect(url_for('in_dash',username=username))








