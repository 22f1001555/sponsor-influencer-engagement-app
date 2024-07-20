from .database import db   #. given for database to search db in current folder otherwise it looks in the root folder

# class User(db.Model):

#     admin_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
#     username=db.Column(db.String(),nullable=False,unique=True)
#     password=db.Column(db.String(),nullable=False)
#     role=db.Column(db.String(),nullable=False)
    

class Admin(db.Model):

    admin_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(),nullable=False,unique=True)
    password=db.Column(db.String(),nullable=False)
    influencers=db.relationship('Influencer',back_populates='admin')
    sponsors=db.relationship('Sponsor',back_populates='admin')
    campaigns=db.relationship('Campaign',back_populates='admin')




class Sponsor(db.Model):

    sponsor_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(),nullable=False,unique=True)
    password=db.Column(db.String(),nullable=False)
    company_name=db.Column(db.String(),nullable=False,unique=True)
    industry=db.Column(db.String(),nullable=False)
    initial_budget=db.Column(db.Numeric(10, 2),nullable=False,default=0)
    budget=db.Column(db.Numeric(10, 2),nullable=False)
    flagged=db.Column(db.Integer,nullable=False,default=0)
    admin_id=db.Column(db.Integer,db.ForeignKey('admin.admin_id'),nullable=False,default=1)
    campaigns=db.relationship('Campaign',back_populates='sponsors')
    admin=db.relationship('Admin',back_populates='sponsors')

class Influencer(db.Model):

    influencer_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(),nullable=False,unique=True)
    password=db.Column(db.String(),nullable=False)
    f_name=db.Column(db.String(),nullable=False)
    l_name=db.Column(db.String(),nullable=False)
    earnings=db.Column(db.Numeric(10, 2),nullable=False,default=0)
    rating=db.Column(db.Numeric(3, 2),nullable=False,default=None)
    flagged=db.Column(db.Integer,nullable=False,default=0)
    admin_id=db.Column(db.Integer,db.ForeignKey('admin.admin_id'),nullable=False,default=1)
    category_id=db.Column(db.String(),db.ForeignKey("category.cat_id"),nullable=False)
    niche_id=db.Column(db.String(),db.ForeignKey("niche.niche_id"),nullable=False)
    social_media=db.Column(db.String(),nullable=False)
    subs=db.Column(db.Integer,nullable=False)
    category=db.relationship('Category', back_populates='influencers')
    niche = db.relationship('Niche', back_populates='influencers')
    admin=db.relationship('Admin', back_populates='influencers')
    #campaigns=db.relationship('Campaign',back_populates='influencers')

    

class Campaign(db.Model):

    campaign_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    sponsor_id=db.Column(db.Integer,db.ForeignKey('sponsor.sponsor_id'),nullable=False)
    admin_id=db.Column(db.Integer,db.ForeignKey('admin.admin_id'),nullable=False,default=1)
    name=db.Column(db.String(),nullable=False,unique=True)
    category_id=db.Column(db.String(),db.ForeignKey("category.cat_id"),nullable=False)
    start_date=db.Column(db.Date,nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    initial_budget=db.Column(db.Numeric(10, 2),nullable=False,default=0)
    budget = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(), nullable=False,default='active')
    visibility= db.Column(db.String(50),nullable=False)
    goals=db.Column(db.String(),nullable=False)
    flagged=db.Column(db.Integer,nullable=False,default=0)
    categories=db.relationship('Category',back_populates='campaigns')
    sponsors=db.relationship('Sponsor',back_populates='campaigns')
    #influencers=db.relationship('Influencer',back_populates='campaigns')
    admin=db.relationship('Admin',back_populates='campaigns')
    ads=db.relationship('Adrequest',back_populates='campaign')
    
class Adrequest(db.Model):
    ad_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    campaign_id=db.Column(db.Integer,db.ForeignKey("campaign.campaign_id"),nullable=False)
    influencer_id=db.Column(db.Integer,db.ForeignKey("influencer.influencer_id"),nullable=False)
    name=db.Column(db.String(), nullable=False,unique=True)
    content=db.Column(db.String(), nullable=False)
    niche_id=db.Column(db.String(),db.ForeignKey("niche.niche_id"),nullable=False)
    status=db.Column(db.String(), nullable=False,default='pending')
    budget = db.Column(db.Numeric(10, 2), nullable=False)
    negotiate_budget=db.Column(db.Numeric(10, 2), nullable=False,default=0)
    niche=db.relationship('Niche',back_populates='adrequests')
    campaign=db.relationship('Campaign',back_populates='ads')

class Category(db.Model):
    cat_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(), nullable=False,unique=True)
    campaigns=db.relationship('Campaign',back_populates='categories')
    influencers = db.relationship('Influencer', back_populates='category')
    niches= db.relationship('Niche', back_populates='category')

class Niche(db.Model):

    niche_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(), nullable=False,unique=True)
    cat_id=db.Column(db.Integer,db.ForeignKey("category.cat_id"),nullable=False)
    influencers = db.relationship('Influencer', back_populates='niche')
    adrequests=db.relationship('Adrequest',back_populates='niche')
    category=db.relationship('Category', back_populates='niches')
