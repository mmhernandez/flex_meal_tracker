from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)
db = "flex_program"
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z ,.\'-]+$')
password_regex = re.compile(r'^(^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$)?(^(?=.*\d)(?=.*[a-z])(?=.*[@#$%^&+=]).*$)?(^(?=.*\d)(?=.*[A-Z])(?=.*[@#$%^&+=]).*$)?(^(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$)?$')
number_regex = re.compile(r'^[0-9]*$')

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.sex = data["sex"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.starting_weight = data["starting_weight"]
        self.starting_bust = data["starting_bust"]
        self.starting_waist = data["starting_waist"]
        self.starting_abdomen = data["starting_abdomen"]
        self.starting_hips = data["starting_hips"]
        self.starting_right_arm = data["starting_right_arm"]
        self.starting_left_arm = data["starting_left_arm"]
        self.starting_right_thigh = data["starting_right_thigh"]
        self.starting_left_thigh = data["starting_left_thigh"]
        self.starting_right_calf = data["starting_right_calf"]
        self.starting_left_calf = data["starting_left_calf"]
        self.daily_log = None

    @staticmethod
    def validate_user(data):
        is_valid = True

        #first name validation
        if len(data["first_name"]) < 1:
            flash("First name required", "first_name")
            is_valid = False
        elif len(data["first_name"]) < 2:
            flash("First name must be at least 2 characters", "first_name")
            is_valid = False
        elif not name_regex.match(data["first_name"]):
            flash("Invalid first name", "first_name")
            is_valid = False

        #last name validation
        if len(data["last_name"]) < 1:
            flash("Last name required", "last_name")
            is_valid = False
        elif len(data["last_name"]) < 2:
            flash("Last name must be at least 2 characters", "last_name")
            is_valid = False
        elif not name_regex.match(data["last_name"]):
            flash("Invalid last name", "last_name")
            is_valid = False

        #email validation
        if "email" in data:
            if len(data["email"]) < 1:
                flash("Email required", "email")
                is_valid = False
            elif not email_regex.match(data["email"]):
                flash("Invalid email", "email")
                is_valid = False
            elif User.get_by_email(data):
                flash("Email already in use", "email")
                is_valid = False
        
        #password validation
        if "password" in data:
            if len(data["password"]) < 1:
                flash("Password required", "password")
                is_valid = False
            elif len(data["password"]) < 8:
                flash("Password must be at least 8 characters", "password")
                is_valid = False
            elif not password_regex.match(data["password"]):
                flash("Invalid password - must include a lowercase and uppercase letter, number, and special character.", "password")
                is_valid = False

            # password confirmation validation
            elif data["password"] != data["confirm_password"]:
                flash("Passwords do not match", "confirm_password")
                is_valid = False

        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True
        user_info = User.get_by_email(data)

        if not user_info:
            flash("Email and/or password incorrect", "login")
            is_valid = False
        elif not bcrypt.check_password_hash(user_info.password, data['password']):
            flash("Email and/or password incorrect", "login")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_account_info(data):
        is_valid = True

        #validate user info
        if not User.validate_user(data):
            is_valid = False

        #weight validation
        if not number_regex.match(data["weight"]):
            flash("Invalid weight", "weight")
            is_valid = False
        if len(data["weight"]) > 1:
            if int(data["weight"]) > 700:
                flash("Invalid weight, cannot exceed 700lbs", "weight")
                is_valid = False

        #bust validation
        if not number_regex.match(data["bust"]):
            flash("Invalid bust measurement", "bust")
            is_valid = False
        if len(data["bust"]) > 1:
            if int(data["bust"]) > 70:
                flash("Invalid bust measurement, cannot exceed 70 inches", "bust")
                is_valid = False

        #waist validation
        if not number_regex.match(data["waist"]):
            flash("Invalid waist measurement", "waist")
            is_valid = False
        if len(data["waist"]) > 1:
            if int(data["waist"]) > 100:
                flash("Invalid waist measurement, cannot exceed 100 inches", "waist")
                is_valid = False

        #abdomen validation
        if not number_regex.match(data["abdomen"]):
            flash("Invalid abdomen measurement", "abdomen")
            is_valid = False
        if len(data["abdomen"]) > 1:
            if int(data["abdomen"]) > 100:
                flash("Invalid abdomen measurement, cannot exceed 100 inches", "abdomen")
                is_valid = False

        #hips validation
        if not number_regex.match(data["hips"]):
            flash("Invalid hip measurement", "hips")
            is_valid = False
        if len(data["hips"]) > 1:
            if int(data["hips"]) > 100:
                flash("Invalid hip measurement, cannot exceed 100 inches", "hips")
                is_valid = False
        
        #right arm validation
        if not number_regex.match(data["right_arm"]):
            flash("Invalid arm measurement", "right_arm")
            is_valid = False
        if len(data["right_arm"]) > 1:
            if int(data["right_arm"]) > 30:
                flash("Invalid arm measurement, cannot exceed 30 inches", "right_arm")
                is_valid = False

        #left arm validation
        if not number_regex.match(data["left_arm"]):
            flash("Invalid arm measurement", "left_arm")
            is_valid = False
        if len(data["left_arm"]) > 1:
            if int(data["left_arm"]) > 30:
                flash("Invalid arm measurement, cannot exceed 30 inches", "left_arm")
                is_valid = False

        #right thigh validation
        if not number_regex.match(data["right_thigh"]):
            flash("Invalid thigh measurement", "right_thigh")
            is_valid = False
        if len(data["right_thigh"]) > 1:
            if int(data["right_thigh"]) > 40:
                flash("Invalid thigh measurement, cannot exceed 40 inches", "right_thigh")
                is_valid = False

        #left thigh validation
        if not number_regex.match(data["left_thigh"]):
            flash("Invalid thigh measurement", "left_thigh")
            is_valid = False
        if len(data["left_thigh"]) > 1:
            if int(data["left_thigh"]) > 40:
                flash("Invalid thigh measurement, cannot exceed 40 inches", "left_thigh")
                is_valid = False

        #right calf validation
        if not number_regex.match(data["right_calf"]):
            flash("Invalid calf measurement", "right_calf")
            is_valid = False
        if len(data["right_calf"]) > 1:
            if int(data["right_calf"]) > 40:
                flash("Invalid calf measurement, cannot exceed 40 inches", "right_calf")
                is_valid = False

        #left calf validation
        if not number_regex.match(data["left_calf"]):
            flash("Invalid calf measurement", "left_calf")
            is_valid = False
        if len(data["left_calf"]) > 1:
            if int(data["left_calf"]) > 40:
                flash("Invalid calf measurement, cannot exceed 40 inches", "left_calf")
                is_valid = False
        
        return is_valid
    
    @classmethod
    def get_by_email(cls, data):
        query = '''
            SELECT *
            FROM users
            WHERE email = %(email)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = '''
            SELECT * 
            FROM users
            WHERE id = %(id)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def insert(cls, data):
        query = '''
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        '''
        hashed_password = bcrypt.generate_password_hash(data["password"])
        data.update({"password": hashed_password})
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = '''
            UPDATE users
            SET first_name = %(first_name)s,
                last_name = %(last_name)s,
                email = %(email)s,
                sex = %(sex)s,
                starting_weight = %(starting_weight)s,
                starting_bust = %(starting_bust)s,
                starting_waist = %(starting_waist)s,
                starting_abdomen = %(starting_abdomen)s,
                starting_hips = %(starting_hips)s,
                starting_right_arm = %(starting_right_arm)s,
                starting_left_arm = %(starting_left_arm)s,
                starting_right_thigh = %(starting_right_thigh)s,
                starting_left_thigh = %(starting_left_thigh)s,
                starting_right_calf = %(starting_right_calf)s,
                starting_left_calf = %(starting_left_calf)s
            WHERE id = %(id)s;
        '''
