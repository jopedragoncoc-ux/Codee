import json
import os
import hashlib
from datetime import datetime

# File paths
USER_FILE = 'user.txt'
ITEMS_FILE = 'lostfound.json'

# Load users from file
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            users = {}
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    users[parts[0]] = parts[1]
            return users
    return {}

# Save users to file
def save_users(users):
    with open(USER_FILE, 'w') as f:
        for username, password in users.items():
            f.write(f"{username}:{password}\n")

# Load items from JSON
def load_items():
    if os.path.exists(ITEMS_FILE):
        with open(ITEMS_FILE, 'r') as f:
            return json.load(f)
    return []

# Save items to JSON
def save_items(items):
    with open(ITEMS_FILE, 'w') as f:
        json.dump(items, f, indent=4)

# Hash password for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Format datetime for display (AM/PM)
def format_datetime(dt_str):
    try:
        # Try parsing as new AM/PM format
        dt = datetime.strptime(dt_str, '%Y-%m-%d %I:%M:%S %p')
    except ValueError:
        try:
            # Try parsing as old ISO format
            dt = datetime.fromisoformat(dt_str)
        except ValueError:
            return dt_str  # If parsing fails, return as is
    return dt.strftime('%Y-%m-%d %I:%M:%S %p')

# User registration or login
def user_menu(users, items):
    while True:
        choice = input("Student Login or Register? (login/register): ").lower()
        if choice == 'register':
            username = input("Enter username: ")
            if username in users:
                print("Username already exists.")
                continue
            password = input("Enter password: ")
            users[username] = hash_password(password)
            save_users(users)
            print("Registration successful.")
            logged_in_user = username
            break
        elif choice == 'login':
            username = input("Enter username: ")
            password = hash_password(input("Enter password: "))
            if users.get(username) == password:
                print("Login successful.")
                logged_in_user = username
                break
            else:
                print("Invalid credentials.")
        else:
            print("Invalid choice.")
    
    # User menu
    while True:
        print("\n[User Menu]")
        print("1. Report Lost Item")
        print("2. Report Found Item")
        print("3. View All Items")
        print("4. Search Item by Name")
        print("5. Mark as Claimed")
        print("6. Logout")
        option = input("Select option: ")
        
        if option == '1':
            name = input("Item name: ")
            description = input("Description: ")
            location = input("Location: ")
            item = {
                'type': 'lost',
                'name': name,
                'description': description,
                'location': location,
                'date_time': datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'),
                'status': 'unclaimed',
                'reporter': logged_in_user
            }
            items.append(item)
            save_items(items)
            print("Lost item reported.")
        
        elif option == '2':
            name = input("Item name: ")
            description = input("Description: ")
            location = input("Location: ")
            item = {
                'type': 'found',
                'name': name,
                'description': description,
                'location': location,
                'date_time': datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'),
                'status': 'unclaimed',
                'reporter': logged_in_user
            }
            items.append(item)
            save_items(items)
            print("Found item reported.")
        
        elif option == '3':
            for item in items:
                formatted_item = item.copy()
                formatted_item['date_time'] = format_datetime(item['date_time'])
                print(formatted_item)
        
        elif option == '4':
            search_name = input("Enter item name to search: ")
            found = [item for item in items if search_name.lower() in item['name'].lower()]
            for item in found:
                formatted_item = item.copy()
                formatted_item['date_time'] = format_datetime(item['date_time'])
                print(formatted_item)
        
        elif option == '5':
            item_name = input("Enter item name to claim: ")
            for item in items:
                if item['name'].lower() == item_name.lower() and item['status'] == 'unclaimed':
                    item['status'] = 'claimed'
                    save_items(items)
                    print("Item marked as claimed.")
                    break
            else:
                print("Item not found or already claimed.")
        
        elif option == '6':
            break
        else:
            print("Invalid option.")

# Admin login
def admin_menu(users, items):
    # Simple admin login (hardcoded for simplicity)
    username = input("Admin username: ")
    password = input("Admin password: ")
    if username == 'admin' and password == 'admin123':  # Change as needed
        print("Admin login successful.")
    else:
        print("Invalid admin credentials.")
        return
    
    while True:
        print("\n[Admin Menu]")
        print("1. View All Reports")
        print("2. Search Item")
        print("3. Delete Old Record")
        print("4. Summary (Total Lost/Found)")
        print("5. Export to Text File")
        print("6. Logout")
        option = input("Select option: ")
        
        if option == '1':
            for item in items:
                formatted_item = item.copy()
                formatted_item['date_time'] = format_datetime(item['date_time'])
                print(formatted_item)
        
        elif option == '2':
            search_name = input("Enter item name to search: ")
            found = [item for item in items if search_name.lower() in item['name'].lower()]
            for item in found:
                formatted_item = item.copy()
                formatted_item['date_time'] = format_datetime(item['date_time'])
                print(formatted_item)
        
        elif option == '3':
            # Delete records older than 30 days (simplified)
            cutoff = datetime.now().timestamp() - 30*24*3600
            items[:] = [item for item in items if datetime.strptime(format_datetime(item['date_time']), '%Y-%m-%d %I:%M:%S %p').timestamp() > cutoff]
            save_items(items)
            print("Old records deleted.")
        
        elif option == '4':
            lost = sum(1 for item in items if item['type'] == 'lost')
            found = sum(1 for item in items if item['type'] == 'found')
            print(f"Total Lost: {lost}, Total Found: {found}")
        
        elif option == '5':
            with open('export.txt', 'w') as f:
                for item in items:
                    formatted_item = item.copy()
                    formatted_item['date_time'] = format_datetime(item['date_time'])
                    f.write(str(formatted_item) + '\n')
            print("Exported to export.txt")
        
        elif option == '6':
            break
        else:
            print("Invalid option.")

while True:
    users = load_users()
    items = load_items()
    
    print("\n[Login Menu]")
    choice = input("Login as User or Admin? (user/admin): ").lower()
    if choice == 'user':
        user_menu(users, items)
    elif choice == 'admin':
        admin_menu(users, items)
    else:
        print("Invalid choice. Try again.")
