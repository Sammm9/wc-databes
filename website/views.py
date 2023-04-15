
from flask import Blueprint, render_template, request, flash, jsonify, url_for, session
from flask_login import login_required, current_user
from . import db
import csv



v = Blueprint('views', __name__)

@v.route('/2023')
def home2023():
    # Read the options from the CSV file
    with open('Classes2023.csv', 'r', encoding='latin-1', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        options = [row[4] for row in reader]

    # Filter options based on user input
    input_text = request.args.get('selected_option', '').lower()
    filtered_options = [option for option in options if input_text in option.lower()]

    # Pass the filtered options to the Jinja template
    return render_template("2023spring.html", options=filtered_options)



@v.route('/')
def home():
    user_id = session.get('user_id')
    return render_template("home.html", user=current_user, user_id=user_id)


