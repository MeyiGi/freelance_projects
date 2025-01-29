import os
import re
from datetime import datetime
from collections import deque

class FileManager:
    def __init__(self, directory, max_history=100):
        self.directory = directory
        self.processed_files = deque(maxlen=max_history)
        self.pattern = re.compile(r"^(?!.*(google\.com|facebook\.com|bing\.com)).*\.html$")
        self.pending_deletion_files = []

    def delete_html_files(self):
        while self.pending_deletion_files:
            file = self.pending_deletion_files.pop()  # Pops the last file in the list
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Error deleting {file}: {e}")

    def process_new_files(self):
        # delete previous html files
        self.delete_html_files()

        new_files = []  # List to store paths of new files

        for filename in os.listdir(self.directory):
            if filename in self.processed_files:
                continue  # Skip already processed files

            match = self.pattern.match(filename)
            if match:
                filepath = os.path.join(self.directory, filename)

                # Add the file to the list of new files
                new_files.append(filepath)

                # Delete the file after processing
                try:
                    self.pending_deletion_files.append(filepath)
                except OSError as e:
                    pass  # Handle errors if file deletion fails

                # Add the file to the processed list
                self.processed_files.append(filename)

        return new_files
    
    def delete_audio_files(self, folder_path='./audio'):
        """
        Deletes all audio files in the specified folder.

        Args:
            folder_path (str): Path to the folder containing audio files. Default is './audio'.
        """
        # Common audio file extensions
        audio_extensions = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'}
        
        if not os.path.exists(folder_path):
            print(f"Folder '{folder_path}' does not exist.")
            return
        
        # Iterate through all files in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            # Check if the file has an audio extension
            if os.path.isfile(file_path) and os.path.splitext(filename)[1].lower() in audio_extensions:
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
        
        print("Audio file deletion complete.")