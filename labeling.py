#!/usr/bin/python3

import pandas as pd
from os.path import exists

# Define the labels
labels = [
    "1. Conduct engineering design and development tasks",
    "2. Analyze the operation or functional performance of a component or system",
    "3. Perform thermal science or fluid dynamic analysis",
    "4. Perform solid mechanics analysis",
    "5. Perform dynamics or vibrational analysis",
    "6. Perform control analysis",
    "7. Create or revise technical drawings",
    "8. Develop or modify computer codes and/or public software including CAD, CAM, FEA, CFD, Matlab, C++, Python, or related computational tools",
    "9. Conduct experimental programs, including the testing of prototypes, components, hardware, or products",
    "10. Conduct manufacturing activities or processes",
    "11. Conduct quality control activities or troubleshooting a failure of a component or system",
    "12. Create written documentation of procedures, processes, or results",
    "13. Communicate via oral presentations to a variety of audiences",
    "14. Collaborate with or contribute to an engineering group, department, or multi-disciplinary team",
    "15. Participate in on-the-job training and develop new technical skills or abilities",
    "16. Not a job task",
    "17. Other"
]


df = pd.read_excel('/Users/zhangyilin/Documents/UF/Ph.D/ROSF/labeling/final_all_tasks.xlsx')

# Check if 'Task' column exists
if 'Task' not in df.columns:
    print("The column 'Task' was not found in the Excel file.")
    exit()

# Add a 'task_id' column if it doesn't exist
if 'task_id' not in df.columns:
    df['task_id'] = range(1, len(df) + 1)

# Ask the user for the range of tasks they want to work on
start_task = int(input("Enter the start task number: ")) - 1  # Zero-based index
end_task = int(input("Enter the end task number: "))

# Ensure the task numbers are within the range of the df
start_task = max(0, start_task)
end_task = min(len(df), end_task)

# Check if an existing output file is there to append the labels
output_file = 'labeled_tasks.xlsx'
append_data = exists(output_file) and input("An existing label file was found. Do you want to append the new labels to it? (y/n): ").strip().lower() == 'y'

# Load existing data if appending, otherwise initialize a new DataFrame
if append_data:
    existing_df = pd.read_excel(output_file)
else:
    existing_df = pd.DataFrame(columns=['task_id', 'Task'] + labels)  # Ensure structure aligns with new data

label_data_list = []  # Initialize a list to hold the label data dictionaries

# Iterate through the specified range of tasks and ask the user to label each
for index, row in df.iloc[start_task:end_task].iterrows():
    valid_input = False
    print(f"\nTask {index + 1} (ID: {row['task_id']}): {row['Task']}")
    
    while not valid_input:
        label_data = {'task_id': row['task_id'], 'Task': row['Task']}  # Initialize task_id and Task
        label_data.update({label: 0 for label in labels})  # Initialize labels with 0
        user_input = input(f"Enter the labels for this task separated by comma (1-{len(labels)}): ")
        valid_input = True  # Assume the input is valid, look for evidence to the contrary
        
        for label_index in user_input.split(','):
            try:
                label_index = int(label_index.strip()) - 1  # Convert to zero-based index
                if 0 <= label_index < len(labels):
                    label_data[labels[label_index]] = 1
                else:
                    print(f"Label number {label_index + 1} is out of range. Please enter a valid label number.")
                    valid_input = False
                    break  # Exit the for loop, go back to the while loop for new input
            except ValueError:
                print(f"Invalid input: {label_index}. Expected a number. Please enter a valid label number.")
                valid_input = False
                break  # Exit the for loop, go back to the while loop for new input
        
        if valid_input:
            # Add label_data to the list
            label_data_list.append(label_data)

# Create a df from the label_data_list
label_df = pd.DataFrame(label_data_list)

# Merge the existing data with the new data
if append_data:
    combined_df = pd.concat([existing_df, label_df]).drop_duplicates(subset=['task_id'], keep='last').reset_index(drop=True)
else:
    combined_df = label_df

# Export to excel
combined_df.to_excel(output_file, index=False)

print(f"\nLabeled data has been saved to {output_file}.")


