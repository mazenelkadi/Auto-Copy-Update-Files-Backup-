# For setting up the file system observer
from watchdog.observers import Observer
# For handling file system events
from watchdog.events import FileSystemEventHandler
import time  # For time-related functions
import os  # Provides functions for interacting with the operating system
import shutil  # High-level file operations


class Handler(FileSystemEventHandler):
    def process(self, event):
        # Ignore directories and temporary files
        if os.path.isdir(event.src_path) or event.src_path.endswith('.tmp'):
            return

        file_name = os.path.basename(event.src_path)
        src = os.path.join(watched_folder, file_name)
        dst = os.path.join(destination_folder, file_name)

        try:
            # Copy if the file is new/updated or doesn't exist in the destination
            if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
                print(f"Copying {src} to {dst}")
                shutil.copy2(src, dst)  # copy2 preserves metadata
            else:
                print(f"No change in {src}, not copying.")
        except FileNotFoundError:
            print(f"File not found: {src}")
        except Exception as e:
            print(f"Error copying file: {e}")

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


if __name__ == "__main__":
    watched_folder = input("Enter the path of the folder to watch: ")
    destination_folder = input("Enter the path of the destination folder: ")

    # Check if the folders exist
    if not os.path.exists(watched_folder):
        print(f"The watched folder '{watched_folder}' does not exist.")
        exit()
    if not os.path.exists(destination_folder):
        print(f"The destination folder '{destination_folder}' does not exist.")
        exit()

    # Set up the file observer and handler
    handler = Handler()
    observer = Observer()
    observer.schedule(event_handler=handler,
                      path=watched_folder, recursive=True)
    observer.start()

    # Run the observer
    print(f"Monitoring {watched_folder} for changes. To stop, press Ctrl+C.")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        print("File monitoring stopped.")
