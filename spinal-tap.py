import subprocess

file_choice = input("Which Python file do you want to execute? \nEnter 1 for Concert Stage\nEnter 2 for Stage Lights only: \n")

if file_choice == '1':
    file_name = "concert_stage_.py"
elif file_choice == '2':
    file_name = "stage_lights.py"
else:
    print("Invalid choice. Exiting the program.")
    exit()

try:
    subprocess.run(['python', file_name], check=True)
except FileNotFoundError:
    print(f"Python file '{file_name}' not found. Exiting the program.")
except subprocess.CalledProcessError:
    print(f"Error executing Python file '{file_name}'. Exiting the program.")