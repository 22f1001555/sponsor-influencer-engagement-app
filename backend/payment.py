from flask import Flask,render_template,redirect,request,url_for
from flask import current_app as app
from .models import *
from .users import *
from .campaigns import *
from .ads import *

@app.route('/<username>/<int:camp_id>/<int:ad_id>/payment_gateway/<status>',methods=['GET','POST'])
def payment(username,camp_id,ad_id,status):
    ad=Adrequest.query.filter_by(ad_id=ad_id).first()
    camp=Campaign.query.filter_by(campaign_id=camp_id).first()
    niches=Niche.query.filter_by(cat_id=camp.category_id).all()
    inf=Influencer.query.filter_by(influencer_id=ad.influencer_id).first()
    if request.method=='GET':
        
        return render_template('payment_page.html',ad=ad,inf=inf,username=username,status=status)
        
    else:
        if status=='Pay Now':
            
            if ad.negotiate_budget>0:
                camp.budget=float(camp.budget)+float(ad.budget)
                if ad.negotiate_budget<=camp.budget:
                    camp.budget=float(camp.budget)-float(ad.negotiate_budget)
                    inf.earnings=float(inf.earnings)+float(ad.negotiate_budget)
                    ad.status='completed'
                    db.session.commit()
                else:
                    db.session.rollback()
                    return 'requested amount is more than campaign budget'

            else:
                inf.earnings=float(inf.earnings)+float(ad.budget)
                ad.status='completed'
                db.session.commit()
            return redirect(url_for('camp_details',username=username,id=camp_id))
        else:
            ad.status='requested'
            ad.negotiate_budget=(request.form.get('negotiate'))
            
            db.session.commit()
            return redirect(url_for('in_dash',username=username))
            
            ##fill this correctly##

    
