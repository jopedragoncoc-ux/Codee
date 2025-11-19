from datetime import datetime

users = {}
feedbacks = []

def register_user():
    global users
    username = input("Enter username: ")
    if username in users:
        print("Username already exists.")
        return
    password = input("Enter password: ")
    confirm_password = input("Confirm password: ")
    if password != confirm_password:
        print("Passwords do not match.")
        return
    users[username] = password
    print("Registration successful.")

def login_user():
    global users
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username in users and users[username] == password:
        return username
    print("Invalid credentials.")
    return None

def submit_feedback(user):
    global feedbacks
    category = input("Enter category: ")
    details = input("Enter feedback details: ")
    date = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    status = "Pending"
    feedback = {
        'user': user,
        'category': category,
        'details': details,
        'date': date,
        'status': status
    }
    feedbacks.append(feedback)
    print("Feedback submitted.")

def view_my_feedbacks(user):
    global feedbacks
    my_feedbacks = [f for f in feedbacks if f['user'] == user]
    if not my_feedbacks:
        print("No feedbacks found.")
        return
    for i, fb in enumerate(my_feedbacks, 1):
        print(f"{i}. Category: {fb['category']}, Details: {fb['details']}, Date: {fb['date']}, Status: {fb['status']}")

def edit_feedback(user):
    global feedbacks
    my_feedbacks = [f for f in feedbacks if f['user'] == user]
    if not my_feedbacks:
        print("No feedbacks to edit.")
        return
    view_my_feedbacks(user)
    try:
        idx = int(input("Enter feedback number to edit: ")) - 1
        if 0 <= idx < len(my_feedbacks):
            fb = my_feedbacks[idx]
            category = input(f"Enter new category (current: {fb['category']}): ") or fb['category']
            details = input(f"Enter new details (current: {fb['details']}): ") or fb['details']
            fb['category'] = category
            fb['details'] = details
            print("Feedback updated.")
        else:
            print("Invalid number.")
    except ValueError:
        print("Invalid input.")

def delete_feedback(user):
    global feedbacks
    my_feedbacks = [f for f in feedbacks if f['user'] == user]
    if not my_feedbacks:
        print("No feedbacks to delete.")
        return
    view_my_feedbacks(user)
    try:
        idx = int(input("Enter feedback number to delete: ")) - 1
        if 0 <= idx < len(my_feedbacks):
            feedbacks.remove(my_feedbacks[idx])
            print("Feedback deleted.")
        else:
            print("Invalid number.")
    except ValueError:
        print("Invalid input.")

def user_menu(user):
    while True:
        print("\nUser Menu:")
        print("1. Submit Feedback")
        print("2. View My Feedback")
        print("3. Edit My Feedback")
        print("4. Delete My Feedback")
        print("5. Logout")
        choice = input("Select option: ")
        if choice == '1':
            submit_feedback(user)
        elif choice == '2':
            view_my_feedbacks(user)
        elif choice == '3':
            edit_feedback(user)
        elif choice == '4':
            delete_feedback(user)
        elif choice == '5':
            print("Logging out.......")
            break
        else:
            print("Invalid option.")

def admin_login():
    password = input("Enter admin password: ")
    if password == "admin123":  # Simple hardcoded password
        return True
    print("Invalid admin password.")
    return False

def view_all_feedbacks():
    global feedbacks
    if not feedbacks:
        print("No feedbacks.")
        return
    for fb in feedbacks:
        print(f"User: {fb['user']}, Category: {fb['category']}, Details: {fb['details']}, Date: {fb['date']}, Status: {fb['status']}")

def filter_by_category():
    global feedbacks
    category = input("Enter category to filter: ")
    filtered = [f for f in feedbacks if f['category'].lower() == category.lower()]
    if not filtered:
        print("No feedbacks in this category.")
        return
    for fb in filtered:
        print(f"User: {fb['user']}, Details: {fb['details']}, Date: {fb['date']}, Status: {fb['status']}")

def mark_feedback():
    global feedbacks
    if not feedbacks:
        print("No feedbacks.")
        return
    view_all_feedbacks()
    try:
        idx = int(input("Enter feedback number to mark: ")) - 1
        if 0 <= idx < len(feedbacks):
            status = input("Enter new status (Reviewed/Resolved): ")
            feedbacks[idx]['status'] = status
            print("Status updated.")
        else:
            print("Invalid number.")
    except ValueError:
        print("Invalid input.")

def delete_feedback_admin():
    global feedbacks
    if not feedbacks:
        print("No feedbacks.")
        return
    view_all_feedbacks()
    try:
        idx = int(input("Enter feedback number to delete: ")) - 1
        if 0 <= idx < len(feedbacks):
            feedbacks.pop(idx)
            print("Feedback deleted.")
        else:
            print("Invalid number.")
    except ValueError:
        print("Invalid input.")

def summary_report():
    global feedbacks
    categories = {}
    for fb in feedbacks:
        cat = fb['category']
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1
    print("Summary by Category:")
    for cat, count in categories.items():
        print(f"{cat}: {count} feedbacks")

def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. View All Feedback")
        print("2. Filter by Category")
        print("3. Mark as Reviewed/Resolved")
        print("4. Delete Feedback")
        print("5. Summary Report by Category")
        print("6. Logout")
        choice = input("Select option: ")
        if choice == '1':
            view_all_feedbacks()
        elif choice == '2':
            filter_by_category()
        elif choice == '3':
            mark_feedback()
        elif choice == '4':
            delete_feedback_admin()
        elif choice == '5':
            summary_report()
        elif choice == '6':
            print("Logging out.......")
            break
        else:
            print("Invalid option.")

while True:
    print("\n== Welcome to the Feedback System ==")
    print("1. Login as User")
    print("2. Register as User")
    print("3. Login as Admin")
    print("4. Exit")
    choice = input("Enter choice (1-4): ")
    
    if choice == "1":
        user = login_user()
        if user:
            user_menu(user)
    elif choice == "2":
        register_user()
    elif choice == "3":
        if admin_login():
            admin_menu()
    elif choice == "4":
        print("Exiting the system...")
        exit()
    else:
        print("Invalid choice. Try again.")