
import os
import subprocess

def find_project_folder(root_directory):
    for root, dirs, files in os.walk(root_directory):
        if 'settings.py' in files:
            return os.path.basename(root)
    return None

# Specify the root directory to start the search
root_directory = os.getcwd()  # Change this to your desired root directory

project_folder = find_project_folder(root_directory)


git_command = ["git","pull","origin","master"]

try:
    subprocess.run(git_command, check=True)
    print("updated pulled successfully.")
except subprocess.CalledProcessError as e:
    print("Error:", e)

if project_folder:
    print("Project folder found:", project_folder)
    settings_module = __import__(f"{project_folder}.settings", fromlist=['INSTALLED_APPS'])
    INSTALLED_APPS = settings_module.INSTALLED_APPS
    # Extract items without dots to a new list
    apps_without_dots = [app for app in INSTALLED_APPS if '.' not in app]
    # Command to execute
    command = ["python", "manage.py", "makemigrations"]

    # Execute the command
    for i in apps_without_dots:
        command.append(i)
        try:
            subprocess.run(command, check=True)
            print("makemigrations completed successfully.")
        except subprocess.CalledProcessError as e:
            print("Error:", e)

        command.pop()


    migrate_command = ["python","manage.py","migrate"]

    try:
        subprocess.run(migrate_command, check=True)
        print("makemigrations completed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error:", e)


    # create superuser
    db_file_path = root_directory+"\db.sqlite3"
    if not os.path.exists(db_file_path):
        createsuperuser_command = ["python","manage.py","createsuperuser"]

        try:
            subprocess.run(createsuperuser_command, check=True)
            print("superuser created successfully...")
        except subprocess.CalledProcessError as e:
            print("Error:", e)
else:
    print("Project folder not found.")
