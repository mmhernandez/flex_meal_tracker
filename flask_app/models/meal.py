from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

db = "flex_program"
number_regex = re.compile(r'^[0-9]*$')

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
        if not number_regex.match(data["proteins"]):
            flash("Invalid proteins", data["meal_type"])
            is_valid = False
        if len(data["proteins"]) > 1:
            if float(data["proteins"]) > 100:
                flash("Invalid entry, proteins cannot exceed 100 oz", data["meal_type"])
                is_valid = False

        #fats validation
        if not number_regex.match(data["fats"]):
            flash("Invalid fats", data["meal_type"])
            is_valid = False
        elif len(data["fats"]) > 1:
            if float(data["fats"]) > 100:
                flash("Invalid entry, fats cannot exceed 100 servings", data["meal_type"])
                is_valid = False

        #fruits validation
        if not number_regex.match(data["fruits"]):
            flash("Invalid fruits", data["meal_type"])
            is_valid = False
        if len(data["fruits"]) > 1:
            if float(data["fruits"]) > 50:
                flash("Invalid entry, cannot exceed qty of 50 fruits", data["meal_type"])
                is_valid = False

        #vegetables validation
        if not number_regex.match(data["vegetables"]):
            flash("Invalid vegetables", data["meal_type"])
            is_valid = False
        if len(data["vegetables"]) > 1:
            if float(data["vegetables"]) > 50:
                flash("Invalid entry, cannot exceed qty of 50 vegetables", data["meal_type"])
                is_valid = False
        
        return is_valid
    
    @classmethod
    def insert_meal_details(cls, data):
        query = '''
            INSERT INTO meals (daily_log_id, meal_type, details, proteins, fats, fruits, vegetables)
            VALUES (%(daily_log_id)s, %(meal_type)s, %(details)s, %(proteins)s, %(fats)s, %(fruits)s, %(vegetables)s);
        '''
        connectToMySQL(db).query_db(query, data)