from flask_restful import Resource, Api
from flask import request, jsonify
from models.database import*
from datetime import datetime

api=Api()


class SubjectApi(Resource):

    def get_subject(self):
        subjects=Subjects.query.all()
        return jsonify(subjects)


    def post(self):
        name=request.json.get("name")
        

    def put_subject(self,id):
        subjects=Subjects.query.filter_by(id=id).first()
