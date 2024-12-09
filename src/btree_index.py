import os
import csv
from file_handler import FileHandler
from btree import BTree

class BTreeIndexApp:
    def __init__(self):
        self.btree = BTree(FileHandler)
        self.current_file = None

    def display_menu(self):
        """Display the interactive menu"""
        print("\n--- B-Tree Index File Manager ---")
        print("1. create  - Create a new index file")
        print("2. open    - Open an existing index file")
        print("3. insert  - Insert a key/value pair")
        print("4. search  - Search for a key")
        print("5. load    - Load key/value pairs from a CSV")
        print("6. print   - Print all key/value pairs")
        print("7. extract - Save key/value pairs to a CSV")
        print("8. quit    - Exit the program")

    def create_index_file(self):
        """Create a new index file"""
        filename = input("Enter filename for new index file: ").strip()
        
        # Check if file exists
        if os.path.exists(filename):
            overwrite = input(f"File {filename} already exists. Overwrite? (yes/no): ").lower()
            if overwrite != 'yes':
                print("Operation cancelled.")
                return

        if self.btree.create(filename):
            self.current_file = filename
            print(f"Created and opened index file: {filename}")
        else:
            print("Failed to create index file.")

    def open_index_file(self):
        """Open an existing index file"""
        filename = input("Enter filename of index file to open: ").strip()
        
        if self.btree.open(filename):
            self.current_file = filename
            print(f"Opened index file: {filename}")
        else:
            print("Failed to open index file.")

    def insert_key_value(self):
        """Insert a key/value pair"""
        if not self.current_file:
            print("Error: No index file is currently open.")
            return

        try:
            key = int(input("Enter key (unsigned integer): "))
            value = int(input("Enter value (unsigned integer): "))

            if self.btree.insert(key, value):
                print(f"Inserted key {key} with value {value}")
            else:
                print("Failed to insert key/value pair.")
        except ValueError:
            print("Error: Please enter valid unsigned integers.")

    def search_key(self):
        """Search for a key in the index"""
        if not self.current_file:
            print("Error: No index file is currently open.")
            return

        try:
            key = int(input("Enter key to search (unsigned integer): "))
            result = self.btree.search(key)

            if result is not None:
                print(f"Key {key} found. Value: {result}")
            else:
                print(f"Key {key} not found.")
        except ValueError:
            print("Error: Please enter a valid unsigned integer.")

    def load_from_csv(self):
        """Load key/value pairs from a CSV file"""
        if not self.current_file:
            print("Error: No index file is currently open.")
            return

        filename = input("Enter CSV filename to load: ").strip()

        try:
            with open(filename, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                success_count = 0
                error_count = 0

                for row in csv_reader:
                    if len(row) != 2:
                        print(f"Skipping invalid row: {row}")
                        error_count += 1
                        continue

                    try:
                        key = int(row[0])
                        value = int(row[1])
                        if self.btree.insert(key, value):
                            success_count += 1
                        else:
                            error_count += 1
                    except ValueError:
                        print(f"Skipping invalid row (not integers): {row}")
                        error_count += 1

                print(f"Load complete. Successful insertions: {success_count}, Errors: {error_count}")
        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
        except Exception as e:
            print(f"Error loading CSV: {e}")

    def print_all_entries(self):
        """Print all entries in the index"""
        if not self.current_file:
            print("Error: No index file is currently open.")
            return

        try:
            entries = self.btree.get_all_entries()
            
            if not entries:
                print("No entries in the index.")
                return

            print("Current Index Entries:")
            for key, value in entries:
                print(f"Key: {key}, Value: {value}")
        except Exception as e:
            print(f"Error retrieving entries: {e}")

    def extract_to_csv(self):
        """Extract all entries to a CSV file"""
        if not self.current_file:
            print("Error: No index file is currently open.")
            return

        filename = input("Enter CSV filename to extract entries: ").strip()

        # Check if file exists
        if os.path.exists(filename):
            overwrite = input(f"File {filename} already exists. Overwrite? (yes/no): ").lower()
            if overwrite != 'yes':
                print("Operation cancelled.")
                return

        try:
            # Get all entries
            entries = self.btree.get_all_entries()
            
            with open(filename, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                
                # Write entries
                for key, value in entries:
                    csv_writer.writerow([key, value])

                print(f"Entries extracted to {filename}")
        except Exception as e:
            print(f"Error extracting to CSV: {e}")

    def run(self):
        """Run the interactive application"""
        while True:
            self.display_menu()
            
            try:
                choice = input("Enter command: ").lower().strip()

                if choice in ['create', '1']:
                    self.create_index_file()
                elif choice in ['open', '2']:
                    self.open_index_file()
                elif choice in ['insert', '3']:
                    self.insert_key_value()
                elif choice in ['search', '4']:
                    self.search_key()
                elif choice in ['load', '5']:
                    self.load_from_csv()
                elif choice in ['print', '6']:
                    self.print_all_entries()
                elif choice in ['extract', '7']:
                    self.extract_to_csv()
                elif choice in ['quit', '8', 'q']:
                    print("Exiting B-Tree Index Manager. Goodbye!")
                    break
                else:
                    print("Invalid command. Please try again.")
            except Exception as e:
                print(f"An error occurred: {e}")

def main():
    app = BTreeIndexApp()
    app.run()

if __name__ == "__main__":
    main()