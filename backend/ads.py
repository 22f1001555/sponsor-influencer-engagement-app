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
        niche_id=request.form.get('niche_id')
        budget=float(request.form.get('budget'))
        influencer_id=request.form.get('influencer_id')
        camp.budget=float(camp.budget)-budget
        if influencer_id=="":
            influencer_id=-1
            if float(camp.budget)>=0:
                new_ad=Adrequest(name=name,content=content,campaign_id=campaign_id,
                        influencer_id=influencer_id,niche_id=niche_id,budget=budget)
            else:
                return 'Insufficient budget,add more budget to the campaign',404
        else:
            if float(camp.budget)>=0:
                status='requested to influencer'
                new_ad=Adrequest(name=name,content=content,campaign_id=campaign_id,
                            influencer_id=influencer_id,niche_id=niche_id,budget=budget,status=status)
            else:
                return 'Insufficient budget,add more budget to the campaign',404

        
        try:
            db.session.add(new_ad)
            db.session.commit()
            return redirect(url_for('camp_details',id=id,username=username))
        except IntegrityError:
            db.session.rollback()
            flash('Ad already exists','error')
        

    return render_template('new_ad.html',camp=camp,infs=infs,niches=niches,username=username)
        
@app.route('/<username>/<int:camp_id>/<int:ad_id>/update',methods=['GET','POST'])       #update ad
def update_ad(ad_id,camp_id,username):
    ad=Adrequest.query.filter_by(ad_id=ad_id).first()
    camp=Campaign.query.filter_by(campaign_id=camp_id).first()
    niches=Niche.query.filter_by(cat_id=camp.category_id).all()
    infs=Influencer.query.filter_by(category_id=camp.category_id).all()

    if ad.status=='accepted by influencer':
        return 'can not edit ad after getting accepted by an influencer!'
    
    if request.method=='POST':
        prev_budget=ad.budget
        ad.name=request.form.get('name')
        ad.content=request.form.get('content')
        
        ad.niche_id=request.form.get('niche_id')
        ad.budget=float(request.form.get('budget'))
        influencer_id=request.form.get('influencer_id')
        if influencer_id=='':
            ad.influencer_id=-1
            ad.status='pending'
        else:
           ad.influencer_id= influencer_id
           ad.status='requested to influencer'
        
        if float(prev_budget)!=ad.budget:
            camp.budget=float(camp.budget)+float(prev_budget)
            camp.budget=float(camp.budget)-float(ad.budget)
            if camp.budget<0:
                return 'Insufficient budget'

        db.session.commit()
        return redirect(url_for('camp_details',username=username,id=camp_id))
    
    return render_template('update_ad.html',ad=ad,camp=camp,infs=infs,
                               niches=niches,username=username)
    
@app.route('/del_ad/<username>/<int:camp_id>/<int:ad_id>')                            # delete a ad
def del_ad(ad_id,username,camp_id): 
    ad=Adrequest.query.filter_by(ad_id=ad_id).first()
    camp=Campaign.query.filter_by(campaign_id=camp_id).first()
    camp.budget=float(camp.budget)+float(ad.budget)
    if ad.status=='completed' or ad.status=='accepted by influencer' or ad.status=='accepted by sponsor':
        return 'ad is accepted or completed, can not delete'
    else:
        db.session.delete(ad)
        db.session.commit()
    return redirect(url_for('camp_details',username=username,id=camp_id))

# add details only for sponsors
@app.route('/<username>/campaigns/<int:camp_id>/ad_details/<int:ad_id>')
def ad_details(username,camp_id,ad_id):
    ad=Adrequest.query.filter_by(ad_id=ad_id).first()
    inf=Influencer.query.filter_by(influencer_id=ad.influencer_id).first()
    if ad.status=='completed' :
        return render_template('ad_details.html',ad=ad,camp_id=camp_id,username=username,inf=inf,status='ad req fulfilled')
    else:
        return render_template('ad_details.html',ad=ad,camp_id=camp_id,username=username,inf=inf)

# add details only for influencer
@app.route('/<username>/ad_details/<int:ad_id>',methods=['GET','POST'])
def inf_ad_details(username,ad_id):
    ad=Adrequest.query.filter_by(ad_id=ad_id).first()
    inf=Influencer.query.filter_by(influencer_id=ad.influencer_id).first()
    if request.method=='POST':
        ad.status=request.form.get('status')
        db.session.commit()
        return redirect(url_for('in_dash',username=username))
    else:
        if ad.status=='pending':
            return render_template('inf_ad_details.html',ad=ad,username=username,inf=inf,status='Negotiate')

        return render_template('inf_ad_details.html',ad=ad,username=username,inf=inf)


# add status
@app.route('/<username>/<int:ad_id>',methods=['post'])
def ad_status(username,ad_id):
    ad=Adrequest.query.filter_by(ad_id=ad_id).first()
    inf=Influencer.query.filter_by(username=username).first()
    sponsor=Sponsor.query.filter_by(username=username).first()
    
    ad_status=request.form.get('status')
    inf_id=Influencer.query.filter_by(influencer_id=ad_status).first()
    if not(sponsor) and (inf):
    
        if ad_status=='accepted by influencer':
            ad.influencer_id=inf.influencer_id
            ad.status='accepted by influencer'
        if ad_status=='rejected by influencer':
            ad.status='pending'
            ad.influencer_id=-1
        db.session.commit()
        return redirect(url_for('in_dash',username=username))
    if sponsor and not(inf):
    
        if inf_id:
            if ad.negotiate_budget>ad.budget:
                if ad.campaign.budget>=ad.negotiate_budget:
                    ad.status='accepted by sponsor'
                    ad.influencer_id=inf_id.influencer_id
                else:
                    return 'Insufficient campaign budget'

        if ad_status=='rejected by sponsor':
            ad.status='pending'
            ad.influencer_id=-1
            ad.negotiate_budget=0
        db.session.commit()
        return redirect(url_for('sp_dash',username=username))

    
#negotiation for influencers
@app.route('/<username>/negotiate/<int:ad_id>',methods=['GET','POST'])
def negotiate(username,ad_id):
    ad=Adrequest.query.filter_by(ad_id=ad_id).first()
    inf=Influencer.query.filter_by(username=username).first()
    if request.method=='POST':
        negotiate=float(request.form.get('negotiate'))
        if negotiate>float(ad.budget):
            ad.negotiate_budget=negotiate
            ad.status='requested by influencer'
            ad.influencer_id=inf.influencer_id
        else:
            return 'put a greater negotiation value or click on accept'
        
        
        db.session.commit()
        return redirect(url_for('in_dash',username=username))
    
    return redirect(url_for('inf_ad_details',ad_id=ad_id,username=username))
     
