from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import daily_log
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
            flash("Invalid proteins")
            is_valid = False
        if len(data["proteins"]) > 1:
            if float(data["proteins"]) > 100:
                flash("Invalid entry, proteins cannot exceed 100 oz")
                is_valid = False

        #fats validation
        if not number_regex.match(data["fats"]):
            flash("Invalid fats")
            is_valid = False
        if len(data["fats"]) > 1:
            if float(data["fats"]) > 100:
                flash("Invalid entry, fats cannot exceed 100 servings")
                is_valid = False

        #fruits validation
        if not number_regex.match(data["fruits"]):
            flash("Invalid fruits")
            is_valid = False
        if len(data["fruits"]) > 1:
            if float(data["fruits"]) > 50:
                flash("Invalid entry, cannot exceed qty of 50 fruits")
                is_valid = False

        #vegetables validation
        if not number_regex.match(data["vegetables"]):
            flash("Invalid vegetables")
            is_valid = False
        if len(data["vegetables"]) > 1:
            if float(data["vegetables"]) > 50:
                flash("Invalid entry, cannot exceed qty of 50 vegetables")
                is_valid = False
        
        return is_valid
    
    