from flask import Blueprint
# from flask import Blueprint, render_template, redirect, url_for, flash, request
# from werkzeug.security import generate_password_hash
# from flask_login import login_user, logout_user, login_required
# from models.user import User
# from models.database import db
# from datetime import datetime

auth_bp = Blueprint('auth', __name__)
main_bp = Blueprint('main', __name__)
survey_bp = Blueprint('survey', __name__)

from . import auth
from . import main
from . import survey