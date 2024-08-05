from flask import Flask,render_template,redirect,request,url_for,flash
from flask import current_app as app
from sqlalchemy.exc import IntegrityError
from .models import *
from .users import *
from datetime import datetime




@app.route('/<username>/campaigns',methods=['GET','POST'])                  #campaigns list for sponsors
def campaigns(username):
    
    campaign_user=Sponsor.query.filter_by(username=username).first()
    cat=Category.query.all()
    if request.method=='GET':
        return render_template('campaigns_page.html',user=campaign_user,cat=cat)

@app.route('/<username>/new_campaign',methods=['GET','POST'])               #create new campaign
def new_campaign(username):
    user=Sponsor.query.filter_by(username=username).first()
    if request.method=='POST':
        title=request.form.get('title')
        sponsor_id=request.form.get('sponsor_id')
        category_id=request.form.get('category')
        start=request.form.get('start')
        end=request.form.get('end')
        budget=float(request.form.get('budget'))
        initial_budget=budget
        visibility=request.form.get('visibility')
        goals=request.form.get('goals')
        start_date=datetime.strptime(start, '%Y-%m-%d')
        end_date=datetime.strptime(end, '%Y-%m-%d')
        
        if end_date<=start_date:
            return "End date must be after start date",400
        
        new_campaign=Campaign(name=title,sponsor_id=sponsor_id,category_id=category_id,start_date=start_date.date(),
                              end_date=end_date.date(),budget=budget,initial_budget=initial_budget,
                              visibility=visibility,goals=goals)
        
        
#deduct the budget for the campaign,from sponsor
        if user.budget<budget:
            return 'Insufficient budget',400
        user.budget=float(user.budget)-budget
        try:
            db.session.add(new_campaign)
            db.session.commit()
            return redirect(url_for('campaigns',username=username))
        except IntegrityError :
            db.session.rollback()
            return ('Campaign already exists')
            # return render_template('new_campaign.html',user=user,cat=cat)


@app.route('/<username>/update/<int:id>',methods=['GET','POST'])                    # update a campaign
def update_camp(id,username):
    sponsor=Sponsor.query.filter_by(username=username).first()
    update_camp=Campaign.query.filter_by(campaign_id=id).first()
    ads=update_camp.ads
    
    if request.method=='POST':
        new_name=request.form.get('title')
        if new_name!=update_camp.name:
            if Campaign.query.filter_by(name=new_name).first():
                return 'campaign already exists'
        update_camp.name=new_name
        update_camp.category_id=request.form.get('category')
        update_camp.start=request.form.get('start')
        update_camp.end=request.form.get('end')
        update_camp.visibility=request.form.get('visibility')
        update_camp.goals=request.form.get('goals')
        update_camp.start_date=datetime.strptime(update_camp.start, '%Y-%m-%d')
        update_camp.end_date=datetime.strptime(update_camp.end, '%Y-%m-%d')
        update_camp.status=request.form.get('status')
# update a campaign completed,only when all its adds are completed and 
# there is atleast one completed add in the campaign
        if update_camp.status=='completed':
            if not(ads):
                return "Please create an Ad before marking the campaign closed",404
            else:
                for ad in ads:
                    if ad.status!='Paid':
                        return 'Action not possbile,one or more Active Ads',404
            sponsor.budget=float(sponsor.budget)+float(update_camp.budget)
            update_camp.budget=0
            db.session.commit()
            return redirect(url_for('campaigns',username=username))
# if campaign budget is changed,add back the old budget to sponsor.       
        sponsor.budget=float(sponsor.budget)+float(update_camp.budget)
        update_camp.budget=float(request.form.get('budget'))
        update_camp.initial_budget=update_camp.budget
# then deduct the new budget.
# if unchanged,same amount added and then deducted.
        if sponsor.budget<update_camp.budget:
            return 'Insufficient budget',400
        sponsor.budget=float(sponsor.budget)-(update_camp.budget)

        if update_camp.end_date<=update_camp.start_date:
            return "End date must be after start date",400
        
        db.session.commit()
        return redirect(url_for('campaigns',username=username))


@app.route('/<username>/del_camp/<int:id>')                            # delete a campaign
def del_camp(id,username): 
        user=Sponsor.query.filter_by(username=username).first()
        camp=Campaign.query.filter_by(campaign_id=id).first()
        ads=camp.ads
# deleting a campaign,deletes all the ads in the campaign.
# if the campaign is incomplete(active), it adds back the budget of 
# all incomplete ad requests to the campaign budget.
# unspent campaign budget adds back to the sponsor budget.
        if camp.status=='active':
            for ad in ads:      
                if ad.status=='pending' or ad.status=='requested to influencer' :
                    camp.budget=float(camp.budget)+float(ad.budget)
                    db.session.delete(ad)
                elif ad.status=='Paid':
                    db.session.delete(ad)
                else:
                    return 'can not delete campaign while there are active ads'
                
            user.budget=float(user.budget)+float(camp.budget)

        db.session.delete(camp)
        db.session.commit()
        return redirect(url_for('campaigns',username=username))

@app.route('/<username>/campaign_details/<int:id>', methods=['GET','POST'])               # campaign details
def camp_details(id,username):
    camp=Campaign.query.filter_by(campaign_id=id).first()
    user=camp.sponsors
    niches=Niche.query.filter_by(cat_id=camp.category_id).all()
    infs=Influencer.query.filter_by(category_id=camp.category_id).all()
    if request.method=='GET':
        return render_template('campaign_details.html',camp=camp,user=user,niches=niches,infs=infs)
    

@app.route('/<username>/campaign_descriptions/<int:id>')                # all the active campaigns shown to the influencer
def camp_descriptions(username,id):
    camp=Campaign.query.filter_by(campaign_id=id).first()
    return render_template('camp_descriptions.html',camp=camp,username=username)

