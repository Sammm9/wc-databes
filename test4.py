import tkinter as tk
from tkinter import ttk

def create_schedule(inputs):
    # Define your classroom schedule data
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    time_slots = ["08:00 - 08:30", "08:30 - 09:00", "09:00 - 09:30", "09:30 - 10:00", "10:00 - 10:30", "10:30 - 11:00","11:00 - 11:30",
                "11:30 - 12:00", "12:00 - 12:30", "12:30 - 12:00", "13:00 - 13:30", "13:30 - 14:00", "14:00 - 14:30", "14:30 - 15:00"]

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
        

        for x in inputs[i][1]:
            if intervals_end - intervals_start == 2:
                if x == "M":
                    schedule_data["Monday"][intervals_start] = inputs[i][0]
                    schedule_data["Monday"][intervals_end - 1] = inputs[i][0]
                if x == "T":
                    schedule_data["Tuesday"][intervals_start] = inputs[i][0]
                    schedule_data["Tuesday"][intervals_end - 1] = inputs[i][0]
                if x == "W":
                    schedule_data["Wednesday"][intervals_start] = inputs[i][0]
                    schedule_data["Wednesday"][intervals_end - 1] = inputs[i][0]
                if x == "R":
                    schedule_data["Thursday"][intervals_start] = inputs[i][0]
                    schedule_data["Thursday"][intervals_end - 1] = inputs[i][0]
                if x == "F":
                    schedule_data["Friday"][intervals_start] = inputs[i][0]
                    schedule_data["Friday"][intervals_end - 1] = inputs[i][0]
            
            if intervals_end - intervals_start == 3:
                if x == "M":
                    schedule_data["Monday"][intervals_start] = inputs[i][0]
                    schedule_data["Monday"][intervals_end - 1] = inputs[i][0]
                    schedule_data["Monday"][intervals_end - 2] = inputs[i][0]
                if x == "T":
                    schedule_data["Tuesday"][intervals_start] = inputs[i][0]
                    schedule_data["Tuesday"][intervals_end - 1] = inputs[i][0]
                    schedule_data["Tuesday"][intervals_end - 2] = inputs[i][0]
                if x == "W":
                    schedule_data["Wednesday"][intervals_start] = inputs[i][0]
                    schedule_data["Wednesday"][intervals_end - 1] = inputs[i][0]
                    schedule_data["Wednesday"][intervals_end - 2] = inputs[i][0]
                if x == "R":
                    schedule_data["Thursday"][intervals_start] = inputs[i][0]
                    schedule_data["Thursday"][intervals_end - 1] = inputs[i][0]
                    schedule_data["Thursday"][intervals_end - 2] = inputs[i][0]
                if x == "F":
                    schedule_data["Friday"][intervals_start] = inputs[i][0]
                    schedule_data["Friday"][intervals_end - 1] = inputs[i][0]
                    schedule_data["Friday"][intervals_end - 2] = inputs[i][0]


    # Pad the strings in schedule_data with spaces to match the length of time_slots
    for day in days:
        while len(schedule_data[day]) < len(time_slots):
            schedule_data[day] += " " # Pad with spaces

    # Insert data into the treeview widget based on the schedule data
    for i, time_slot in enumerate(time_slots):
        tree.insert("", "end", text=time_slot, values=[schedule_data[day][i] for day in days])

    # Start the Tkinter event loop
    root.mainloop()


inputs = [['MATH 141', 'MTWF', '10:00-11:00'], ['BIOT 142', 'TR', '11:00-12:00'], ['COSC 143', 'MW', '13:00-14:30']]
print(create_schedule(inputs))    