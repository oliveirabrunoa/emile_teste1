from flask import Blueprint, jsonify, request
from . import models
from backend import db
import datetime


course_type = Blueprint("course_type", __name__)
