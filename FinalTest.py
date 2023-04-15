import csv
import datetime
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt


def create_class_selector(file_path1):
    root = tk.Tk()

    # Set the size of the window
    root.geometry("700x400")

    # Read the options from the CSV file
    with open(file_path1, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        options = [(row[4], row[8], row[9]) for row in reader]

    # Create a StringVar to store the currently selected option
    selected_option = tk.StringVar()

    # Create an Entry widget for user input
    input_entry = tk.Entry(root, textvariable=selected_option, width=30, font=("Helvetica", 14))
    input_entry.pack()

    # Create a listbox to display filtered options
    options_listbox = tk.Listbox(root, width=70, height=13, font=("Helvetica", 14))
    options_listbox.pack()

    # Populate the options listbox with all the classes
    for option in options:
        options_listbox.insert(tk.END, f"{option[0]}-{option[1]}-{option[2]}")

    # Create a function to filter options based on user input
    def filter_options(*args):
        options_listbox.delete(0, tk.END)
        input_text = selected_option.get().lower()
        filtered_options = [f"{row[0]}-{row[1]}-{row[2]}" for row in options if input_text in row[0].lower()]
        for option in filtered_options:
            options_listbox.insert(tk.END, option)

    # Call the filter_options function whenever the input changes
    selected_option.trace('w', filter_options)

    # Create a function to save the selected option
    def save_option():
        selected_option_val = options_listbox.get(tk.ACTIVE)
        selected_option_val = selected_option_val.strip()  # Remove leading/trailing whitespaces
        selected_options.append(selected_option_val)
        print("Selected options:", selected_options)

    save_button = tk.Button(root, text="Save option", command=save_option)
    save_button.pack()

    # Create a list to store the selected options
    selected_options = []

    def open_saved_options_window():
        saved_options_window = tk.Toplevel(root)
        saved_options_window.geometry("700x400")  # Set the size of the window
        saved_options_window.title("Saved Options")

        # Create a listbox to display saved options
        saved_options_listbox = tk.Listbox(saved_options_window, width=70, height=15, font=("Helvetica", 14))
        saved_options_listbox.pack()

        # Populate the saved options listbox with the selected options
        for option in selected_options:
            saved_options_listbox.insert(tk.END, option)

        # Create a function to delete a selected option
        def delete_option():
            selected_index = saved_options_listbox.curselection()
            if selected_index:
                saved_options_listbox.delete(selected_index)
                selected_options.pop(selected_index[0])
                print("Selected options after deletion:", selected_options)

        delete_button = tk.Button(saved_options_window, text="Delete option", command=delete_option)
        delete_button.pack()

    view_saved_options_button = tk.Button(root, text="View Saved Options", command=open_saved_options_window)
    view_saved_options_button.pack()

    root.mainloop()

    for i in range(len(selected_options)):
        # Split the string by "-" character
        parts = selected_options[i].split("-")
        # Take only the first part before the "-" character
        selected_options[i] = parts[0]

    return selected_options

# def create_class_selector(file_path1):
#     root = tk.Tk()

#     # Set the size of the window
#     root.geometry("400x300")

#     # Read the options from the CSV file
#     with open(file_path1, newline='') as csvfile:
#         reader = csv.reader(csvfile)
#         next(reader)
#         options = [row[4] for row in reader]

#     # Create a StringVar to store the currently selected option
#     selected_option = tk.StringVar()

#     # Create an Entry widget for user input
#     input_entry = tk.Entry(root, textvariable=selected_option, width=30, font=("Helvetica", 14))
#     input_entry.pack()

#     # Create a listbox to display filtered options
#     options_listbox = tk.Listbox(root, width=40, height=10, font=("Helvetica", 14))
#     options_listbox.pack()

#     # Create a function to filter options based on user input
#     def filter_options(*args):
#         options_listbox.delete(0, tk.END)
#         input_text = selected_option.get().lower()
#         filtered_options = [option for option in options if input_text in option.lower()]
#         for option in filtered_options:
#             options_listbox.insert(tk.END, option)

#     # Call the filter_options function whenever the input changes
#     selected_option.trace('w', filter_options)

#     # Create a function to save the selected option
#     def save_option():
#         selected_option = options_listbox.get(tk.ACTIVE)
#         selected_options.append(selected_option)
#         print("Selected options:", selected_options)

#     save_button = tk.Button(root, text="Save option", command=save_option)
#     save_button.pack()

#     # Create a list to store the selected options
#     selected_options = []

#     root.mainloop()

#     return selected_options


def filter_csv(file_path1, condition):
    # Open the CSV file for reading
    with open(file_path1, 'r') as csvfile:
        # Create a CSV reader object
        reader = csv.reader(csvfile)
        
        # Initialize an empty list to store the result
        result = []
        
        # Iterate through each row in the CSV file
        for row in reader:
            # Check if the value in row[4] matches the condition
            if row[4] == condition:
                # If it does, append the values from row[1], row[8], and row[9] to the result list
                result.append([row[1], row[8], row[9]])
        
    # Return the filtered list
    desired_list = result[0]
    desired_list[-1] = desired_list[-1].strip()
    
    # Extract the start and end time from the third element of desired_list
    start_time, end_time = desired_list[2].split('-')

    # Convert the start and end time to datetime objects for easier manipulation
    start_time = datetime.datetime.strptime(start_time, '%H:%M')
    end_time = datetime.datetime.strptime(end_time, '%H:%M')

    # Add 10 minutes to the end time
    end_time += datetime.timedelta(minutes=10)

    # Update the third element of desired_list with the updated end time
    desired_list[2] = start_time.strftime('%H:%M') + '-' + end_time.strftime('%H:%M')

    return desired_list



def create_schedule(inputs):
    # Define your classroom schedule data
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    time_slots = ["08:00 - 08:30", "08:30 - 09:00", "09:00 - 09:30", "09:30 - 10:00", "10:00 - 10:30", "10:30 - 11:00","11:00 - 11:30",
                "11:30 - 12:00", "12:00 - 12:30", "12:30 - 13:00", "13:00 - 13:30", "13:30 - 14:00", "14:00 - 14:30", "14:30 - 15:00"]

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Classroom Schedule Board")
    #root.geometry("800x600")

    # Create a treeview widget for the schedule board
    tree = ttk.Treeview(root)
    tree["columns"] = days
    for day in days:
        tree.heading(day, text=day)
    tree.pack()

    # Define the classroom schedule data as a dictionary

    schedule_data = {
        "Monday": ["", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        "Tuesday": ["", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        "Wednesday": ["", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        "Thursday": ["", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        "Friday": ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    }

    for i in range(len(inputs)):

        start_time = "08:00"
        end_time = "15:00"
        time_range = inputs[i][2]  #'10:00-11:00'

        # Split the time range into start and end times
        start_range, end_range = time_range.split("-")

        # Calculate the number of 30-minute intervals from start time to start range
        start_time_hr, start_time_min = map(int, start_time.split(":"))
        start_range_hr, start_range_min = map(int, start_range.split(":"))
        intervals_start = ((start_range_hr * 60 + start_range_min) - (start_time_hr * 60 + start_time_min)) // 30
        #print(intervals_start)

        # Calculate the number of 30-minute intervals from end range to end time
        end_time_hr, end_time_min = map(int, end_time.split(":"))
        end_range_hr, end_range_min = map(int, end_range.split(":"))
        intervals_end = ((end_range_hr * 60 + end_range_min) - (start_time_hr * 60 + start_time_min)) // 30
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]  # List of days
        for x in inputs[i][1]:
            for day in days:
                if x in day:
                    for j in range(intervals_start, intervals_end):
                        schedule_data[day][j] = inputs[i][0]
                        if intervals_end - intervals_start == 3:
                            schedule_data[day][intervals_end - 2] = inputs[i][0]

    # Pad the strings in schedule_data with spaces to match the length of time_slots
    for day in days:
        while len(schedule_data[day]) < len(time_slots):
            schedule_data[day] += " " # Pad with spaces

    # Insert data into the treeview widget based on the schedule data
    for i, time_slot in enumerate(time_slots):
        tree.insert("", "end", text=time_slot, values=[schedule_data[day][i] for day in days])

    # Start the Tkinter event loop
    root.mainloop()



def generate_pie_chart_from_csv(file_path,Class):
    # Read data from CSV file
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        labels = []
        grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]
        counts = {grade: 0 for grade in grades}
        total_size = 0  # Initialize total size counter
        for row in reader:
            grade = row[2]
            if row[1] == Class:
                if grade in counts:
                    counts[grade] += 1
    # values_grades = list(counts.values())
    # print(values_grades)
    
    non_zero_keys = []
    non_zero_values = []
    for key, value in counts.items():
        if value != 0:
            non_zero_keys.append(key)
            non_zero_values.append(value)

    # print("Non-zero keys:", non_zero_keys)
    # print("Non-zero values:", non_zero_values)

    #Create a pie chart
    plt.pie(non_zero_values, labels=non_zero_keys, autopct='%1.1f%%', startangle=0.7)
    plt.title('Pie Chart of {} Grades'.format(Class))  # Title for the pie chart with total size

    #Show the pie chart
    plt.show()


file_path1 = 'Classes2023.csv'
condition = create_class_selector(file_path1)
#condition = ['COSC 240 Data Structures and Algorithms', 'MATH 220 Discrete Mathematics', 'BSAD 231 Business Law']

NewFormat = []
for i in range(len(condition)):
    NewFormat.append(filter_csv(file_path1, condition[i]))
#print(NewFormat)
#NewFormat = [['COSC 240', 'TR', '13:30-15:00'], ['MATH 220', 'MWF', '10:00-11:00'], ['BSAD 231', 'TR', '09:30-11:00']]

print(create_schedule(NewFormat))

file_path = 'OnlyGrades.csv'
#Class = ['EDUC 605 Introduction Education Inquiry', "ANTH 290 Technology and Culture", "BSAD 130 Business and Society"] #this is gonna be variable

result_list = []
for item in condition:
    words = item.split()
    # Take the first two words and join them with a space
    abbreviated = ' '.join(words[:2])
    # Add the abbreviated string to the result list
    result_list.append(abbreviated)

for i in range(len(result_list)):
    generate_pie_chart_from_csv(file_path, result_list[i])
