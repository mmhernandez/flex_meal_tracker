from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, meal
from flask import flash

db = "flex_program"

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

