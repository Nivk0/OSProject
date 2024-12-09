from index_manager import IndexManager

def print_menu():
    print("\nB-Tree Index File Manager")
    print("Commands:")
    print("create - Create a new index file")
    print("open   - Open an existing index file")
    print("insert - Insert a key-value pair")
    print("search - Search for a key")
    print("load   - Load key-value pairs from a CSV file")
    print("print  - Print all key-value pairs")
    print("extract- Extract key-value pairs to a CSV file")
    print("quit   - Exit the program")

def main():
    index_manager = IndexManager()
    
    while True:
        print_menu()
        command = input("Enter command: ").lower().strip()

        try:
            if command == 'create':
                filename = input("Enter filename for new index: ")
                index_manager.create_index_file(filename)
                print(f"Created index file: {filename}")

            elif command == 'open':
                filename = input("Enter filename to open: ")
                if index_manager.open_index_file(filename):
                    print(f"Opened index file: {filename}")

            elif command == 'insert':
                try:
                    key = int(input("Enter key (unsigned integer): "))
                    value = int(input("Enter value (unsigned integer): "))
                    index_manager.insert(key, value)
                    print("Inserted successfully.")
                except ValueError:
                    print("Invalid input. Please enter unsigned integers.")

            elif command == 'search':
                try:
                    key = int(input("Enter key to search: "))
                    result = index_manager.search(key)
                    if result:
                        print(f"Found: Key={result[0]}, Value={result[1]}")
                except ValueError:
                    print("Invalid input. Please enter an unsigned integer.")

            elif command == 'load':
                filename = input("Enter CSV filename to load: ")
                index_manager.load_from_csv(filename)
                print("Loaded data from CSV.")

            elif command == 'print':
                index_manager.print_index()

            elif command == 'extract':
                filename = input("Enter CSV filename to extract to: ")
                index_manager.extract_to_csv(filename)
                print("Extracted data to CSV.")

            elif command == 'quit':
                print("Exiting...")
                break

            else:
                print("Invalid command. Please try again.")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()