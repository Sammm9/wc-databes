import csv
import matplotlib.pyplot as plt

def generate_pie_chart_from_csv(file_path,Class):
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

file_path = 'OnlyGrades.csv'
Class = ['EDUC 605 Introduction Education Inquiry', "ANTH 290 Technology and Culture", "BSAD 130 Business and Society"] #this is gonna be variable
for i in range(3):
    generate_pie_chart_from_csv(file_path, Class[i])