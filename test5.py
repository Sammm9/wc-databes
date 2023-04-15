import csv
import datetime

def filter_csv(file_path1, condition):
    # Open the CSV file for reading
    with open(file_path1, 'r', encoding='latin-1') as csvfile:
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

# Call the function with the file path and condition
file_path1 = 'Classes2023.csv'
condition = "MATH 141 Calculus & Analytical Geometry I"
answer = filter_csv(file_path1, condition)

# Print the desired list
print(answer)