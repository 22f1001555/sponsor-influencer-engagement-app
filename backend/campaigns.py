from flask import Flask,render_template,redirect,request,url_for
from flask import current_app as app
from .models import *
from .users import *
from datetime import datetime




@app.route('/<username>/campaigns',methods=['GET','POST'])                  #campaigns list of sponsors
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
        category_id=request.form.get('category')
        start=request.form.get('start')
        end=request.form.get('end')
        budget=float(request.form.get('budget'))
        visibility=request.form.get('visibility')
        goals=request.form.get('goals')
        start_date=datetime.strptime(start, '%Y-%m-%d')
        end_date=datetime.strptime(end, '%Y-%m-%d')
        
        if end_date<=start_date:
            return "End date must be after start date",400
        
        new_campaign=Campaign(name=title,sponsor_id=sponsor_id,category_id=category_id,start_date=start_date.date(),
                              end_date=end_date.date(),budget=budget,visibility=visibility,goals=goals)
        db.session.add(new_campaign)

        user.budget=float(user.budget)-budget
        db.session.commit()
        return redirect(url_for('campaigns',username=username))

@app.route('/update/<username>/<int:id>',methods=['GET','POST'])                    # update a campaign
def update_camp(id,username):
    sponsor=Sponsor.query.filter_by(username=username).first()
    cat=Category.query.all()
    update_camp=Campaign.query.filter_by(campaign_id=id).first()
    
    if request.method=='GET':
        return render_template('update_campaign.html',user=sponsor,camp=update_camp,cat=cat)
    
    if request.method=='POST':
        sponsor.budget=float(sponsor.budget)+float(update_camp.budget)
        update_camp.name=request.form.get('title')
        update_camp.category_id=request.form.get('category')
        update_camp.start=request.form.get('start')
        update_camp.end=request.form.get('end')
        update_camp.visibility=request.form.get('visibility')
        update_camp.goals=request.form.get('goals')
        update_camp.start_date=datetime.strptime(update_camp.start, '%Y-%m-%d')
        update_camp.end_date=datetime.strptime(update_camp.end, '%Y-%m-%d')
        
        update_camp.budget=float(request.form.get('budget'))
        sponsor.budget=float(sponsor.budget)-(update_camp.budget)

        if update_camp.end_date<=update_camp.start_date:
            return "End date must be after start date",400
        
        db.session.commit()
        return redirect(url_for('campaigns',username=username))

@app.route('/del/<username>/<int:id>')                            # delete a campaign
def del_camp(id,username): 
        user=Sponsor.query.filter_by(username=username).first()
        camp=Campaign.query.filter_by(campaign_id=id).first()
        user.budget=float(user.budget)+float(camp.budget)

        db.session.delete(camp)
        db.session.commit()
        return redirect(url_for('campaigns',username=username))

@app.route('/campaign_details/<username>/<int:id>', methods=['GET','POST'])               # campaign details
def camp_details(id,username):
    camp=Campaign.query.filter_by(campaign_id=id).first()
    user=camp.sponsors
    if request.method=='GET':
        return render_template('campaign_details.html',camp=camp,user=user)