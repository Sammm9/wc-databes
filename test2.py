import tkinter as tk
import csv

root = tk.Tk()

# Set the size of the window
root.geometry("400x300")

# Read the options from the CSV file
with open('Classes2023.csv', 'r', encoding='latin-1', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    options = [row[4] for row in reader]
# Create a StringVar to store the currently selected option
selected_option = tk.StringVar()

# Create an Entry widget for user input
input_entry = tk.Entry(root, textvariable=selected_option, width=30, font=("Helvetica", 14))  # Set desired width, font, and height
input_entry.pack()

# Create a listbox to display filtered options
options_listbox = tk.Listbox(root, width=40, height=10, font=("Helvetica", 14))  # Set desired width, height, and font
options_listbox.pack()

# Create a function to filter options based on user input
def filter_options(*args):
    options_listbox.delete(0, tk.END)
    input_text = selected_option.get().lower()
    filtered_options = [option for option in options if input_text in option.lower()]
    for option in filtered_options:
        options_listbox.insert(tk.END, option)

# Call the filter_options function whenever the input changes
selected_option.trace('w', filter_options)

# Create a function to save the selected option
def save_option():
    selected_option = options_listbox.get(tk.ACTIVE)
    selected_options.append(selected_option)
    #print("Selected options:", selected_options)

save_button = tk.Button(root, text="Save option", command=save_option)
save_button.pack()

# Create a list to store the selected options
selected_options = []

root.mainloop()

#print(selected_options)