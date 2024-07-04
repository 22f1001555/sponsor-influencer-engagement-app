from flask import Flask,render_template,redirect,request,url_for
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
    if request.method=='GET':
        return render_template('new_ad.html',camp=camp,infs=infs,niches=niches,username=username)

    else:
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
            
            db.session.add(new_ad)
            db.session.commit()
            return redirect(url_for('camp_details',id=id,username=username))
        else:
            return 'Insufficient budget,add more budget to the campaign',404
        
@app.route('/<username>/<int:camp_id>/<int:ad_id>/update',methods=['GET','POST'])       #update ad
def update_ad(ad_id,camp_id,username):
    ad=Adrequest.query.filter_by(ad_id=ad_id).first()
    camp=Campaign.query.filter_by(campaign_id=camp_id).first()
    niches=Niche.query.filter_by(cat_id=camp.category_id).all()
    infs=Influencer.query.filter_by(category_id=camp.category_id).all()
    if request.method=='GET':
        return render_template('update_ad.html',ad=ad,camp=camp,infs=infs,
                               niches=niches,username=username)
    else:
        ad.name=request.form.get('name')
        ad.content=request.form.get('content')
        ad.influencer_id=request.form.get('influencer_id')
        ad.niche_id=request.form.get('niche_id')
        camp.budget=float(camp.budget)+float(ad.budget)
        ad.budget=float(request.form.get('budget'))
        camp.budget=float(camp.budget)-float(ad.budget)

        db.session.commit()

        return redirect(url_for('camp_details',username=username,id=camp_id))
    
@app.route('/del_ad/<username>/<int:camp_id>/<int:ad_id>')                            # delete a campaign
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
    #ad.status='accepted'
    if ad.status=='accepted':
        temp_stat='Pay Now'
        return render_template('ad_details.html',ad=ad,inf=inf,status=temp_stat,camp_id=camp_id,username=username)

    return render_template('ad_details.html',ad=ad,inf=inf,username=username,camp_id=camp_id)







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


