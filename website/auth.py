from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Major, MajorClass, ClassPercentage, SelectedOption
import csv
from flask import session
import hashlib
import matplotlib.pyplot as plt
import tkinter as tk

ath = Blueprint('auth', __name__)


@ath.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.student', user_id=user.id))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@ath.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@ath.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    major = {
        "Anthropology": "ANTH",
        "Art & Visual Studies": "ART",
        "Biochemistry": "BCHM",
        "Biology": "BIOL",
        "Business Administration": "BUS",
        "Chemistry": "CHEM",
        "Child Development": "CD",
        "Chinese": "CHIN",
        "Economics": "ECON",
        "Engineering 3-2": "ENGR",
        "English": "ENG",
        "Environmental Science": "ENV",
        "French": "FR",
        "Global & Cultural Studies": "GCS",
        "History": "HIST",
        "Integrated Computer Science/Mathematics": "CS/MATH",
        "Integrated Computer Science/Physics": "CS/PHYS",
        "Integrated Computer Science/Economics": "CS/ECON",
        "Kinesiology": "KIN",
        "Mathematics": "MATH",
        "Mathematics-Business": "MATH/BUS",
        "Mathematics-Economics": "MATH/ECON",
        "Music": "MUS",
        "Philosophy": "PHIL",
        "Applied Philosophy": "APHIL",
        "Physics": "PHYS",
        "Political Science": "POLI",
        "Pre-Professional": "PRE-PRO",
        "Psychological Sciences": "PSYC",
        "Religious Studies": "REL",
        "Social Work": "SW",
        "Sociology": "SOC",
        "Spanish": "SPAN",
        "Theatre & Communication Arts": "TCA"
    }

    major_classes = {
        "Anthropology": ["ANTH 101", "ANTH 201", "ANTH 301"],
        "Art & Visual Studies": ["ARTS 101", "ARTS 201", "ARTS 301"],
        "Biochemistry": ["BIOC 101", "BIOC 201", "BIOC 301"],
        "Biology": ["BIOL 101", "BIOL 201", "BIOL 301"],
        "Business Administration": ["BUSI 101", "BUSI 201", "BUSI 301"],
        "Chemistry": ["CHEM 101", "CHEM 201", "CHEM 301"],
        "Child Development": ["CHDV 101", "CHDV 201", "CHDV 301"],
        "Chinese": ["CHIN 101", "CHIN 201", "CHIN 301"],
        "Economics": ["ECON 101", "ECON 201", "ECON 301"],
        "Engineering 3-2": ["ENGR 101", "ENGR 201", "ENGR 301"],
        "English": ["ENGL 101", "ENGL 201", "ENGL 301"],
        "Environmental Science": ["ENVS 101", "ENVS 201", "ENVS 301"],
        "French": ["FREN 101", "FREN 201", "FREN 301"],
        "Global & Cultural Studies": ["GCS 101", "GCS 201", "GCS 301"],
        "History": ["HIST 101", "HIST 201", "HIST 301"],
        "Integrated Computer Science/Mathematics": ["ICS/MATH 101", "ICS/MATH 201", "ICS/MATH 301"],
        "Integrated Computer Science/Physics": ["ICS/PHYS 101", "ICS/PHYS 201", "ICS/PHYS 301"],
        "Integrated Computer Science/Economics": ["ICS/ECON 101", "ICS/ECON 201", "ICS/ECON 301"],
        "Kinesiology": ["KINS 101", "KINS 201", "KINS 301"],
        "Mathematics": ["MATH 101", "MATH 201", "MATH 301"],
        "Mathematics-Business": ["MATH/BUSI 101", "MATH/BUSI 201", "MATH/BUSI 301"]
    }

    if request.method == 'POST':

        # Retrieve the form data
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        major_id = request.form.get('major')
        major_class_ids = request.form.getlist('major_classes')
        class_percents = {}
        for class_id in major_class_ids:
            percent = request.form.get(f"class_percent_{class_id}")
            if percent:
                class_percents[int(class_id)] = float(percent)
        academic_year = request.form.get('academic_year')
        print(class_percents)
        user = User.query.filter_by(major_id=major_id, email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            class_percent = request.form.get('class_percent', 0.0)
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'), major_id=major_id, academic_year=academic_year, class_percent=class_percent)

            major = Major.query.filter_by(name=major_id).first()
            if not major:
                major = Major(name=major_id)
                db.session.add(major)
        # Add major classes and class percentages to the new user
            for major_id in major_class_ids:
                class_obj = MajorClass.query.get(int(class_id))
                if class_obj and class_obj.major_id == int(major_id):
                    class_percent = class_percents.get(int(class_id), 0.0)
                    new_user.major_classes.append(class_obj)
                    new_user.class_percentages.append(ClassPercentage(
                        major_class_id=int(class_id), percent=class_percent))

            for major_class_id, percent in class_percents.items():
                class_percent = ClassPercentage(
                    major_class_id=major_class_id, user=new_user, percent=percent)
                db.session.add(class_percent)

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user, majors=major, major_classes=major_classes)


@ath.route('/student/<int:user_id>', methods=['GET', 'POST'])
@login_required
def student(user_id):


    def generate_pie_chart_from_csv(file_path, class_name):
    # Read data from CSV file
        with open(file_path, 'r', encoding='latin-1') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            labels = []
            grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]
            counts = {grade: 0 for grade in grades}
            total_size = 0  # Initialize total size counter
            for row in reader:
                grade = row[2]
                if row[1] == class_name:
                    if grade in counts:
                        counts[grade] += 1

            non_zero_keys = []
            non_zero_values = []
            for key, value in counts.items():
                if value != 0:
                    non_zero_keys.append(key)
                    non_zero_values.append(value)

        # Check if the class_name is in the onlygrades.csv file
            with open('OnlyGrades.csv', 'r', encoding='latin-1') as g:
                onlygrades_reader = csv.reader(g)
                next(onlygrades_reader)  # Skip the header row
                class_names = [row[1] for row in onlygrades_reader]
                if class_name in class_names:
                # Create a pie chart
                    plt.pie(non_zero_values, labels=non_zero_keys,
                            autopct='%1.1f%%', startangle=90)
                # Equal aspect ratio ensures that pie is drawn as a circle
                    plt.axis('equal')
                    plt.title(f"{class_name} Grades")
                    plt.show()
                else:
                    print(f"{class_name} is not in the OnlyGrades.csv file")


    user = User.query.get(user_id)

# Create a list of dictionaries containing major class name and percentage for the user
    user_major_classes = []
    class_percentages = ClassPercentage.query.filter_by(
        major_class_id=user_id).all()
    for class_percent in class_percentages:
        major_class = MajorClass.query.get(class_percent.major_class_id)
        user_major_classes.append(
         {'name': major_class.name, 'percent': class_percent.percent})

    major = user.major
    classes = user.classes
    class_percent = user.class_percent
    session['user_id'] = user_id

# Read the CSV file and filter options based on major identifier
    options = []
    with open('Classes2023.csv', 'r', encoding='latin-1', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        options = [row[4] for row in reader if row[4]]

# Get the selected option from the form
    selected_option = request.form.get('option')

# If an option is selected, generate a pie chart for that class
    if selected_option:
        file_path = 'OnlyGrades.csv'
        image_path = generate_pie_chart_from_csv(file_path, selected_option)
    else:
        image_path = None

    # Define your classroom schedule data
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    time_slots = ["08:00 - 08:30", "08:30 - 09:00", "09:00 - 09:30", "09:30 - 10:00", "10:00 - 10:30", "10:30 - 11:00", "11:00 - 11:30",
                  "11:30 - 12:00", "12:00 - 12:30", "12:30 - 12:00", "13:00 - 13:30", "13:30 - 14:00", "14:00 - 14:30", "14:30 - 15:00"]

    # Define the classroom schedule data as a dictionary
    schedule_data = {
        "Monday": ["", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        "Tuesday": ["", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        "Wednesday": ["", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        "Thursday": ["", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        "Friday": ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    }

    # Populate schedule_data with your data
    print(user_major_classes)

    return render_template('student.html', user=user, class_percent=class_percent, major=major, options=options, days=days, classes=classes, time_slots=time_slots, schedule_data=schedule_data, user_id=user_id, user_major_classes=user_major_classes, image_path=image_path)


@ath.route('/add2023/<int:user_id>', methods=['GET', 'POST'])
@login_required
def add(user_id):
    user = User.query.get(user_id)
    file_path1 = 'Classes2023.csv'

    with open(file_path1, encoding='latin-1', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        options = [(row[4], row[8], row[9]) for row in reader]

    if user.selected_options is None:
        user.selected_options = []

    # Create a function to filter options based on user input
    def filter_options():
        input_text = request.json['input_text'].lower()
        filtered_options = [f"{row[0]}-{row[1]}-{row[2]}" for row in options if input_text in row[0].lower()]
        return jsonify(filtered_options)

    # Create a function to save selected option for the user
    def save_option():
        selected_option_val = request.json['selected_option']
        selected_option_val = selected_option_val.strip()  # Remove leading/trailing whitespaces
        class_name, day, time_slot = selected_option_val.split('-')
        
        # Store the selected class schedule in the database
        #user_class_schedule = UserClassSchedule(user_id=user_id, class_name=class_name, day=day, time_slot=time_slot)
        #db.session.add(user_class_schedule)
        #db.session.commit()

        return jsonify({'status': 'success'})

    
    def get_saved_options(user_id):
        user = User.query.get(user_id)
        saved_options = user.selected_options
        return jsonify(saved_options=saved_options)

    return render_template('addclasses.html', user=current_user, options=options)