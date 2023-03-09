from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

db = "flex_program"
number_regex = re.compile(r'^[0-9]\d*(\.\d+)?$')

class Meal:
    def __init__(self, data):
        self.id = data["id"]
        self.meal_type = data["meal_type"]
        self.details = data["details"]
        self.proteins = data["proteins"]
        self.fats = data["fats"]
        self.fruits = data["fruits"]
        self.vegetables = data["vegetables"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.daily_log_id = data["daily_log_id"]

    @staticmethod
    def validate_meal(data):
        is_valid = True

        #proteins validation
        if not number_regex.match(str(data["proteins"])):
            flash("Invalid proteins", data["meal_type"])
            is_valid = False
        elif float(data["proteins"]) > 100:
            flash("Invalid proteins, cannot exceed 100 oz", data["meal_type"])
            is_valid = False

        #fats validation
        if not number_regex.match(str(data["fats"])):
            flash("Invalid fats", data["meal_type"])
            is_valid = False
        elif float(data["fats"]) > 100:
            flash("Invalid fats, cannot exceed 100 servings", data["meal_type"])
            is_valid = False

        #fruits validation
        if not number_regex.match(str(data["fruits"])):
            flash("Invalid fruits", data["meal_type"])
            is_valid = False
        elif float(data["fruits"]) > 50:
            flash("Invalid fruits, cannot exceed qty of 50", data["meal_type"])
            is_valid = False

        #vegetables validation
        if not number_regex.match(str(data["vegetables"])):
            flash("Invalid vegetables", data["meal_type"])
            is_valid = False
        elif float(data["vegetables"]) > 50:
            flash("Invalid vegetables, cannot exceed qty of 50", data["meal_type"])
            is_valid = False
        
        return is_valid
    
    @classmethod
    def insert_meal_details(cls, data):
        query = '''
            INSERT INTO meals (daily_log_id, meal_type, details, proteins, fats, fruits, vegetables)
            VALUES (%(daily_log_id)s, %(meal_type)s, %(details)s, %(proteins)s, %(fats)s, %(fruits)s, %(vegetables)s);
        '''
        connectToMySQL(db).query_db(query, data)

    @classmethod
    def update_meal_details(cls, data):
        query = '''
            UPDATE meals
            SET details = %(details)s,
                proteins = %(proteins)s,
                fats = %(fats)s,
                fruits = %(fruits)s,
                vegetables = %(vegetables)s
            WHERE daily_log_id = %(daily_log_id)s
                AND meal_type = %(meal_type)s;
        '''
        connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_daily_summary(cls, data):
        query = '''
            SELECT SUM(proteins) as total_proteins,
                SUM(fats) as total_fats,
                SUM(fruits) as total_fruits,
                SUM(vegetables) as total_vegetables
            FROM meals
            WHERE daily_log_id = %(daily_log_id)s;
        '''
        results = connectToMySQL(db).query_db(query, data)
        if results[0]["total_proteins"] == None and results[0]["total_fats"] == None and results[0]["total_fruits"] == None and results[0]["total_vegetables"] == None:
            return False
        return results
