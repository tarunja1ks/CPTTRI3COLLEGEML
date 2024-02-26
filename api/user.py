import jwt
import logging

from model.users import User
from model.colleges import College
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource
from datetime import datetime
from auth_middleware import token_required
from ast import literal_eval

user_api = Blueprint('user_api', __name__, url_prefix='/api/users')
api = Api(user_api)

class UserAPI:
    class _CRUD(Resource):
        def post(self):  # Removed current_user
            body = request.get_json()

            # Validate inputs
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400

            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400

            password = body.get('password')
            dob = body.get('dob')
            email = body.get('email')

            uo = User(name=name, uid=uid, email=email)

            if password is not None:
                uo.set_password(password)

            if dob is not None:
                try:
                    uo.dob = datetime.strptime(dob, '%Y-%m-%d').date()
                except:
                    return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 400

            # Add user to database
            user = uo.create()

            if user:
                return jsonify(user.read())  # 201 Created status code

            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

        @token_required
        def get(self, current_user):
            users = User.query.all()
            json_ready = [user.read() for user in users]
            return jsonify(json_ready)
        
        @token_required
        def delete(self, current_user):
            body = request.get_json()
            uid = body.get('uid')
            users = User.query.all()
            for user in users:
                if user.uid == uid:
                    user.delete()
            return jsonify(user.read())
    
    class _Edit(Resource):    
        #READ STR college_list AS LIST THEN REPORT SELECTIONS AS JSON
        def post(self):
            body = request.get_json()
            colleges = College.query.all()
            list = literal_eval(body.get('college_list'))
            user_colleges = []
            for college in colleges:
                if college.name() in list:
                    user_colleges.append(college.read())
            return jsonify(user_colleges)
        
        #REPORT WHOLE COLLEGES DATASET AS JSON
        def get(self):
            colleges = College.query.all()
            json_ready = [college.read() for college in colleges]
            return jsonify(json_ready)
        
        #TAKE STR INPUT AND APPEND TO LIST IF NOT MATCHING
        def put(self, item):
            body = request.get_json()
            uid = body.get('uid')
            ulist = literal_eval(body.get('college_list'))
            user = User.query.get(uid)
            if item not in ulist:
                user.college_list = str(ulist.append(item))
            user.update()
            return jsonify(user.read())
            
    class _Security(Resource):
        def post(self):
            try:
                body = request.get_json()
                if not body:
                    return {"message": "Please provide user details", "data": None, "error": "Bad request"}, 400

                uid = body.get('uid')
                if uid is None:
                    return {'message': f'User ID is missing'}, 400

                password = body.get('password')

                user = User.query.filter_by(_uid=uid).first()
                if user is None or not user.is_password(password):
                    return {'message': f"Invalid user id or password"}, 400

                if user:
                    try:
                        token = jwt.encode(
                            {"_uid": user._uid},
                            current_app.config["SECRET_KEY"],
                            algorithm="HS256"
                        )
                        resp = Response(f"Authentication for {user._uid} successful")
                        resp.set_cookie("jwt", token,
                                max_age=3600,
                                secure=True,
                                httponly=True,
                                path='/',
                                samesite='None'
                                )
                        return resp
                    except Exception as e:
                        return {"error": "Something went wrong", "message": str(e)}, 500

                return {"message": "Error fetching auth token!", "data": None, "error": "Unauthorized"}, 404

            except Exception as e:
                return {"message": "Something went wrong!", "error": str(e), "data": None}, 500

    api.add_resource(_CRUD, '/')
    api.add_resource(_Security, '/authenticate')
    api.add_resource(_Edit, '/edit')