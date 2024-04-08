import os
import shutil
from datetime import datetime
from time import sleep
import argparse

# Important Notes:
# As requested, the program runs with command line arguments, in the example given on "output_example" folder, 
# The command line argument used was: python C:\Users\tiago\OneDrive\Documentos\Projects\TestTasks\test_task.py C:\Users\tiago\OneDrive\Documentos\Projects\TestTasks\source C:\Users\tiago\OneDrive\Documentos\Projects\TestTasks\replica 10 C:\Users\tiago\OneDrive\Documentos\Projects\TestTasks\log.txt
# As such, the argument given for the program to run is: python path/to/test_task.py /path/to/source /path/to/replica sync_interval(int x) /path/to/logfile.txt
# A source folder needs to be created before the arguments, although, the replica folder will be created automatically if it doesn't exist yet

# The program should then update every x seconds with all log.txt outputs according to the changes made
# The synchronization should be one way, the replica folder should always match the content of the source folder


# Function to display log file updates
def display_log_updates(log_file_path):
    with open(log_file_path, "r") as log_file:
        print(log_file.read())

def main(source_folder, replica_folder, sync_interval, log_file_path):
    # Create replica folder if it doesn't exist
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)

    # Inform the user about the synchronization period
    print(f'Synchronization will be done every {sync_interval} seconds')

    # Main synchronization loop
    while True:
        # Get the current date and time
        current_datetime = datetime.now()

        # Format the current date and time
        current_date_time_str = current_datetime.strftime("%d/%m/%Y %H:%M:%S")

        # Keep track of any file changes
        file_changes = False

        # Iterate through files in the source folder
        for file_name in os.listdir(source_folder):
            source = os.path.join(source_folder, file_name)
            replica = os.path.join(replica_folder, file_name)

            # Check if the item in the source folder is a file
            if os.path.isfile(source):
                # Check if the file exists in the replica folder
                if not os.path.exists(replica):
                    # File is new or has been renamed
                    shutil.copy(source, replica)
                    operation = "created"
                    file_changes = True
                else:
                    # File exists in replica folder
                    # Check if the file has been modified
                    source_modified_time = os.path.getmtime(source)
                    replica_modified_time = os.path.getmtime(replica)
                    if source_modified_time != replica_modified_time:
                        shutil.copy(source, replica)
                        operation = "copied"
                        file_changes = True
                    else:
                        operation = "unchanged"

                # Log the operation to a file
                with open(log_file_path, "a") as log_file:
                    log_file.write(f'{current_date_time_str} - File {file_name} {operation} from: {source_folder} to: {replica_folder}\n')

                # Print to console
                print(f'{current_date_time_str} - File {file_name} {operation} from: {source_folder} to: {replica_folder}')

        # Check for deleted files in replica folder
        for file_name in os.listdir(replica_folder):
            replica = os.path.join(replica_folder, file_name)
            source = os.path.join(source_folder, file_name)

            # Check if the file in replica folder doesn't exist in source folder
            if not os.path.exists(source):
                # File has been deleted
                os.remove(replica)

                # Log the operation to a file
                with open(log_file_path, "a") as log_file:
                    log_file.write(f'{current_date_time_str} - File {file_name} deleted from: {replica_folder}\n')

                # Print to console
                print(f'{current_date_time_str} - File {file_name} deleted from: {replica_folder}')
                file_changes = True

        # Print log file updates if there were any file changes
        if file_changes:
            print("Log file updates:")
            display_log_updates(log_file_path)

        # Print the last updated time to console
        print("Last time updated at:", current_date_time_str)

        # Wait for the specified synchronization interval before the next synchronization
        sleep(sync_interval)

        # Clear the console output
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="File synchronization script")
    parser.add_argument("source_folder", type=str, help="Path to the source folder")
    parser.add_argument("replica_folder", type=str, help="Path to the replica folder")
    parser.add_argument("sync_interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file_path", type=str, help="Path to the log file")
    args = parser.parse_args()

    # Call the main function with provided arguments
    main(args.source_folder, args.replica_folder, args.sync_interval, args.log_file_path)
