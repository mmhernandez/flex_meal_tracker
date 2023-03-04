from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, meal
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re

db = "flex_program"
num_regex = re.compile(r'^[0-9]\d*$')
number_regex = re.compile(r'^[0-9]\d*(\.\d+)?$')

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
        self.is_breakfast = True
        self.is_lunch = True
        self.is_dinner = True
        self.is_snacks = True
        self.is_daily_checks = True
        self.is_weight_measurements = True

    @staticmethod
    def validate_daily_checks(data):
        is_valid = True

        #water validation
        if "water" in data:
            if not num_regex.match(str(data["water"])):
                flash("Invalid hydration entry", "water")
                is_valid = False
            if int(data["water"]) > 30:
                flash("Invalid hydration entry, cannot exceed 30 glasses of water", "water")
                is_valid = False

        return is_valid
    
    @staticmethod
    def validate_daily_weights_measurements(data):
        is_valid = True

        #weight validation
        if len(data["weight"]) > 1:
            if not number_regex.match(data["weight"]):
                flash("Invalid weight", "weight")
                is_valid = False
            elif float(data["weight"]) > 700:
                flash("Invalid weight, cannot exceed 700lbs", "weight")
                is_valid = False

        #bust validation
        if len(data["bust"]) > 1:
            if not number_regex.match(data["bust"]):
                flash("Invalid bust measurement", "bust")
                is_valid = False
            if float(data["bust"]) > 70:
                flash("Invalid bust measurement, cannot exceed 70 inches", "bust")
                is_valid = False

        #waist validation
        if len(data["waist"]) > 1:
            if not number_regex.match(data["waist"]):
                flash("Invalid waist measurement", "waist")
                is_valid = False
            if float(data["waist"]) > 100:
                flash("Invalid waist measurement, cannot exceed 100 inches", "waist")
                is_valid = False

        #abdomen validation
        if len(data["abdomen"]) > 1:
            if not number_regex.match(data["abdomen"]):
                flash("Invalid abdomen measurement", "abdomen")
                is_valid = False
            if float(data["abdomen"]) > 100:
                flash("Invalid abdomen measurement, cannot exceed 100 inches", "abdomen")
                is_valid = False

        #hips validation
        if len(data["hips"]) > 1:
            if not number_regex.match(data["hips"]):
                flash("Invalid hip measurement", "hips")
                is_valid = False
            if float(data["hips"]) > 100:
                flash("Invalid hip measurement, cannot exceed 100 inches", "hips")
                is_valid = False
        
        #right arm validation
        if len(data["right_arm"]) > 1:
            if not number_regex.match(data["right_arm"]):
                flash("Invalid arm measurement", "right_arm")
                is_valid = False
            if float(data["right_arm"]) > 30:
                flash("Invalid arm measurement, cannot exceed 30 inches", "right_arm")
                is_valid = False

        #left arm validation
        if len(data["left_arm"]) > 1:
            if not number_regex.match(data["left_arm"]):
                flash("Invalid arm measurement", "left_arm")
                is_valid = False
            if float(data["left_arm"]) > 30:
                flash("Invalid arm measurement, cannot exceed 30 inches", "left_arm")
                is_valid = False

        #right thigh validation
        if len(data["right_thigh"]) > 1:
            if not number_regex.match(data["right_thigh"]):
                flash("Invalid thigh measurement", "right_thigh")
                is_valid = False
            if float(data["right_thigh"]) > 40:
                flash("Invalid thigh measurement, cannot exceed 40 inches", "right_thigh")
                is_valid = False

        #left thigh validation
        if len(data["left_thigh"]) > 1:
            if not number_regex.match(data["left_thigh"]):
                flash("Invalid thigh measurement", "left_thigh")
                is_valid = False
            if float(data["left_thigh"]) > 40:
                flash("Invalid thigh measurement, cannot exceed 40 inches", "left_thigh")
                is_valid = False

        #right calf validation
        if len(data["right_calf"]) > 1:
            if not number_regex.match(data["right_calf"]):
                flash("Invalid calf measurement", "right_calf")
                is_valid = False
            if float(data["right_calf"]) > 40:
                flash("Invalid calf measurement, cannot exceed 40 inches", "right_calf")
                is_valid = False

        #left calf validation
        if len(data["left_calf"]) > 1:
            if not number_regex.match(data["left_calf"]):
                flash("Invalid calf measurement", "left_calf")
                is_valid = False
            if float(data["left_calf"]) > 40:
                flash("Invalid calf measurement, cannot exceed 40 inches", "left_calf")
                is_valid = False

        return is_valid
    
    @classmethod 
    def get_id_by_date(cls, data):
        query = '''
            SELECT id 
            FROM daily_logs
            WHERE date = %(date)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return results[0]["id"]
    
    @classmethod
    def get_all_by_id(cls, data):
        query = '''
            SELECT *,
                CASE
                    WHEN flex_daily_bonus IS NOT NULL or exercise IS NOT NULL or water IS NOT NULL
                        THEN 'True'
                    ELSE 'False'
                END AS is_daily_checks,
                CASE
                    WHEN weight IS NOT NULL or 
                        bust IS NOT NULL or waist IS NOT NULL or 
                        abdomen IS NOT NULL or hips IS NOT NULL or 
                        right_arm IS NOT NULL or left_arm IS NOT NULL or 
                        right_thigh IS NOT NULL or left_thigh IS NOT NULL or 
                        right_calf IS NOT NULL or left_calf IS NOT NULL
                        THEN 'true'
                    ELSE 'False'
                    END AS is_weight_measurements
            FROM daily_logs
            WHERE id = %(id)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        log = cls(results[0])
        log.is_daily_checks = results[0]["is_daily_checks"]
        log.is_weight_measurements = results[0]["is_weight_measurements"]
        return log

    @classmethod
    def insert_daily_checks(cls, data):
        query = '''
            INSERT INTO daily_logs (date, flex_daily_bonus, exercise, water, user_id)
            VALUES (%(date)s, %(flex_daily_bonus)s, %(exercise)s, %(water)s, %(user_id)s);
        '''
        connectToMySQL(db).query_db(query, data)

    @classmethod
    def update_daily_checks(cls, data):
        query = '''
            UPDATE daily_logs
            SET water = %(water)s,
                flex_daily_bonus = %(flex_daily_bonus)s,
                exercise = %(exercise)s
            WHERE id = %(id)s
                and user_id = %(user_id)s;
        '''
        connectToMySQL(db).query_db(query, data)

    @classmethod
    def insert_weights_measurements(cls, data):
        query = '''
            INSERT INTO daily_logs (date, user_id, weight, bust, waist, abdomen, hips, right_arm, left_arm, right_thigh, left_thigh, right_calf, left_calf)
            VALUES (%(date)s, %(user_id)s, %(weight)s, %(bust)s, %(waist)s, %(abdomen)s, %(hips)s, %(right_arm)s, %(left_arm)s, %(right_thigh)s, %(left_thigh)s, %(right_calf)s, %(left_calf)s);
        '''
        connectToMySQL(db).query_db(query, data)