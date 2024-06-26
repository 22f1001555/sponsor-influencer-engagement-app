from .database import db   #. given for database to search db in current folder otherwise it looks in the root folder

class User(db.Model):

    admin_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(),nullable=False,unique=True)
    password=db.Column(db.String(),nullable=False)
    role=db.Column(db.String(),nullable=False)

class Admin(db.Model):

    admin_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(),nullable=False,unique=True)
    password=db.Column(db.String(),nullable=False)
    sponsors=db.relationship('Campaign',back_populates='admin')
    influencers=db.relationship('Influencer',back_populates='admin')
    campaigns=db.relationship('Campaign',back_populates='admin')




class Sponsor(db.Model):

    sponsor_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(),nullable=False,unique=True)
    password=db.Column(db.String(),nullable=False)
    company_name=db.Column(db.String(),nullable=False,unique=True)
    industry=db.Column(db.String(),nullable=False)
    budget=db.Column(db.Numeric(10, 2),nullable=False)
    campaigns=db.relationship('Campaign',back_populates='sponsors')

class Influencer(db.Model):

    influencer_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(),nullable=False,unique=True)
    password=db.Column(db.String(),nullable=False)
    f_name=db.Column(db.String(),nullable=False)
    l_name=db.Column(db.String(),nullable=False)
    category_id=db.Column(db.String(),db.ForeignKey("category.cat_id"),nullable=False)
    niche_id=db.Column(db.String(),db.ForeignKey("niche.niche_id"),nullable=False)
    social_media=db.Column(db.String(),nullable=False)
    subs=db.Column(db.Integer,nullable=False)
    category=db.relationship('Category', back_populates='influencers')
    niche = db.relationship('Niche', back_populates='influencers')

class Campaign(db.Model):

    campaign_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    sponsor_id=db.Column(db.Integer,db.ForeignKey('sponsor.sponsor_id'),nullable=False)
    name=db.Column(db.String(),nullable=False)
    category_id=db.Column(db.String(),db.ForeignKey("category.cat_id"),nullable=False)
    start_date=db.Column(db.Date,nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    budget = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(), nullable=False)
    visibility=status = db.Column(db.String(50), dafault="public")
    goals=db.Column(db.String())
    categories=db.relationship('Category',back_populates='campaigns')
    sponsors=db.relationship('Sponsor',back_populates='campaigns')

class Adrequest(db.Model):
    ad_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    campaign_id=db.column(db.Integer,db.ForeignKey("campaign.campaign_id"),nullable=False)
    influencer_id=db.column(db.Integer,db.ForeignKey("influencer.influencer_id"),nullable=False)
    content=db.Column(db.String(), nullable=False)
    niche_id=db.Column(db.String(),db.ForeignKey("niche.niche_id"),nullable=False)
    status=db.Column(db.String(), nullable=False)
    budget = db.Column(db.Numeric(10, 2), nullable=False)
    niche=db.relationship('Niche',back_populates='adrequests')

class Category(db.Model):

    cat_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(), nullable=False,unique=True)
    campaigns=db.relationship('Campaign',back_populates='categories')
    influencers = db.relationship('Influencer', back_populates='category')

class Niche(db.Model):

    niche_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(), nullable=False,unique=True)
    cat_id=db.Column(db.Integer,db.ForeignKey("category.cat_id"),nullable=False)
    influencers = db.relationship('Influencer', back_populates='niche')
    adrequests=db.relationship('Adrequest',back_populates='niche')
    
