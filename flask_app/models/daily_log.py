from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, meal
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re

db = "flex_program"
number_regex = re.compile(r'^[1-9]\d*(\.\d+)?$')

class DailyLog:
    def __init__(self, data):
        self.id = data["id"]
        self.date = data["date"]
        self.flex_daily_bonus = data["flex_daily_bonus"]
        self.exercise = data["exercise"]
        self.water = data["water"]
        self.notes = data["notes"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.weight = data["weight"]
        self.bust = data["bust"]
        self.waist = data["waist"]
        self.abdomen = data["abdomen"]
        self.hips = data["hips"]
        self.right_arm = data["right_arm"]
        self.left_arm = data["left_arm"]
        self.right_thigh = data["right_thigh"]
        self.left_thigh = data["left_thigh"]
        self.right_calf = data["right_calf"]
        self.left_calf = data["left_calf"]
        self.user_id = data["user_id"]
        self.user = None
        self.meals = []

    @staticmethod
    def validate_daily_checks(data):
        is_valid = True

        #water validation
        if not number_regex.match(data["water"]):
            flash("Invalid hydration entry", "water")
            is_valid = False
        if len(data["water"]) > 1:
            if float(data["water"]) > 30:
                flash("Invalid hydration entry, cannot exceed 30 glasses of water", "water")
                is_valid = False

        return is_valid
    
    @staticmethod
    def validate_daily_weights_measurements(data):
        is_valid = True

        #weight validation
        if not number_regex.match(data["weight"]):
            flash("Invalid weight", "weight")
            is_valid = False
        if len(data["weight"]) > 1:
            if float(data["weight"]) > 700:
                flash("Invalid weight, cannot exceed 700lbs", "weight")
                is_valid = False

        #bust validation
        if not number_regex.match(data["bust"]):
            flash("Invalid bust measurement", "bust")
            is_valid = False
        if len(data["bust"]) > 1:
            if float(data["bust"]) > 70:
                flash("Invalid bust measurement, cannot exceed 70 inches", "bust")
                is_valid = False

        #waist validation
        if not number_regex.match(data["waist"]):
            flash("Invalid waist measurement", "waist")
            is_valid = False
        if len(data["waist"]) > 1:
            if float(data["waist"]) > 100:
                flash("Invalid waist measurement, cannot exceed 100 inches", "waist")
                is_valid = False

        #abdomen validation
        if not number_regex.match(data["abdomen"]):
            flash("Invalid abdomen measurement", "abdomen")
            is_valid = False
        if len(data["abdomen"]) > 1:
            if float(data["abdomen"]) > 100:
                flash("Invalid abdomen measurement, cannot exceed 100 inches", "abdomen")
                is_valid = False

        #hips validation
        if not number_regex.match(data["hips"]):
            flash("Invalid hip measurement", "hips")
            is_valid = False
        if len(data["hips"]) > 1:
            if float(data["hips"]) > 100:
                flash("Invalid hip measurement, cannot exceed 100 inches", "hips")
                is_valid = False
        
        #right arm validation
        if not number_regex.match(data["right_arm"]):
            flash("Invalid arm measurement", "right_arm")
            is_valid = False
        if len(data["right_arm"]) > 1:
            if float(data["right_arm"]) > 30:
                flash("Invalid arm measurement, cannot exceed 30 inches", "right_arm")
                is_valid = False

        #left arm validation
        if not number_regex.match(data["left_arm"]):
            flash("Invalid arm measurement", "left_arm")
            is_valid = False
        if len(data["left_arm"]) > 1:
            if float(data["left_arm"]) > 30:
                flash("Invalid arm measurement, cannot exceed 30 inches", "left_arm")
                is_valid = False

        #right thigh validation
        if not number_regex.match(data["right_thigh"]):
            flash("Invalid thigh measurement", "right_thigh")
            is_valid = False
        if len(data["right_thigh"]) > 1:
            if float(data["right_thigh"]) > 40:
                flash("Invalid thigh measurement, cannot exceed 40 inches", "right_thigh")
                is_valid = False

        #left thigh validation
        if not number_regex.match(data["left_thigh"]):
            flash("Invalid thigh measurement", "left_thigh")
            is_valid = False
        if len(data["left_thigh"]) > 1:
            if float(data["left_thigh"]) > 40:
                flash("Invalid thigh measurement, cannot exceed 40 inches", "left_thigh")
                is_valid = False

        #right calf validation
        if not number_regex.match(data["right_calf"]):
            flash("Invalid calf measurement", "right_calf")
            is_valid = False
        if len(data["right_calf"]) > 1:
            if float(data["right_calf"]) > 40:
                flash("Invalid calf measurement, cannot exceed 40 inches", "right_calf")
                is_valid = False

        #left calf validation
        if not number_regex.match(data["left_calf"]):
            flash("Invalid calf measurement", "left_calf")
            is_valid = False
        if len(data["left_calf"]) > 1:
            if float(data["left_calf"]) > 40:
                flash("Invalid calf measurement, cannot exceed 40 inches", "left_calf")
                is_valid = False

        return is_valid
    
    @classmethod
    def get_all_by_date(cls, data):
        query = '''
            SELECT * 
            FROM daily_logs
            WHERE date = %()s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])