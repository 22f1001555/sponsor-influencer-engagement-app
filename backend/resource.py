from flask import make_response
from flask_restful import Resource,Api,fields,marshal_with,reqparse
from .models import *
# import json
from werkzeug.exceptions import HTTPException
from datetime import datetime

api=Api()

# Error handling
class Genericemsg(HTTPException):
    def __init__(self,message,status_code):
        self.response=make_response(message,status_code)

campaigns={
    'sponsor_id':fields.Integer,
    'campaign_id':fields.Integer,
    'name':fields.String,
    'start_date':fields.String,
    'end_date':fields.String,
    'initial_budget':fields.Float,
    'status':fields.String,
    'goals':fields.String,
    'visibility':fields.String,
    'category_id':fields.String
}
def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()  # Convert string to date
    except ValueError:
        raise ValueError(f"Not a valid date: '{s}'. Must be in YYYY-MM-DD format.")
parser=reqparse.RequestParser()
parser.add_argument('sponsor_id')
parser.add_argument('name')
parser.add_argument('category_id')
parser.add_argument('start_date',type=valid_date)
parser.add_argument('end_date',type=valid_date)
parser.add_argument('budget')
parser.add_argument('status')
parser.add_argument('goals')
parser.add_argument('visibility')
parser.add_argument('category_id')


class Sponsorcampaigns(Resource):

    @marshal_with(campaigns)
    def get(self,sponsor_id):
        sponsor=Sponsor.query.filter_by(sponsor_id=sponsor_id).first()
        campaigns_list=[]
        if sponsor:
            if sponsor.campaigns:
                for camp in sponsor.campaigns:
                    campaigns_list.append(camp)
            else:
                raise Genericemsg('campaigns not found',status_code=404)

            return campaigns_list
                
        else:
            raise Genericemsg('user not found',status_code=404)
            
        
    @marshal_with(campaigns)    
    def post(self):
        data=parser.parse_args()
        new_campaign=Campaign(sponsor_id=data['sponsor_id'],name=data['name'],category_id=data['category_id'],
                                start_date=data['start_date'],end_date=data['end_date'],initial_budget=data['budget'],
                                budget=data['budget'],visibility=data['visibility'],goals=data['goals'])
        db.session.add(new_campaign)
        db.session.commit()
        return new_campaign,201
    @marshal_with(campaigns)
    def put(self,campaign_id):
        args=parser.parse_args()
        camp=Campaign.query.filter_by(campaign_id=campaign_id).first()
        if camp:
            camp.campaign_id=campaign_id
            camp.name=args['name']
            camp.category_id=args['category_id']
            camp.start_date=args['start_date']
            camp.end_date=args['end_date']
            camp.budget=args['budget']
            camp.initial_budget=args['budget']
            camp.status=args['status']
            camp.visibility=args['visibility']
            camp.goals=args['goals']
            db.session.commit()
            return camp,200
        else:
            raise Genericemsg('campaign not found',status_code=404)
    
    def delete(self,campaign_id):
        camp=Campaign.query.filter_by(campaign_id=campaign_id).first()
        if camp:
            db.session.delete(camp)
            db.session.commit()
            raise Genericemsg(f'Campaign {campaign_id} deleted successfully',status_code=200)
            
        else:
            raise Genericemsg('campaign not found',status_code=404)
        
api.add_resource(Sponsorcampaigns,'/api/campaigns','/api/sponsors/<int:sponsor_id>','/api/campaigns/update/<int:campaign_id>','/api/campaigns/delete/<int:campaign_id>')

        


    