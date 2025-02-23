import streamlit as st
from supabase import create_client, Client

# Supabase configuration
SUPABASE_URL = "https://gnyvvmvazbjvhnzhvetv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdueXZ2bXZhemJqdmhuemh2ZXR2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY5MzIwOTcsImV4cCI6MjA1MjUwODA5N30.NSx6aI1v8ou6Sv-qKCtjwsl7FmtG6e1ztIb1bBDPBvE"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# Registration form
st.title("User Registration")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
role = st.selectbox("Role", ["Client", "Social Worker", "Admin"])
first_name = st.text_input("First Name (optional)")
last_name = st.text_input("Last Name (optional)")
phone_number = st.text_input("Phone Number (optional)")
register_button = st.button("Register")

if register_button:
    try:
        # Create user authentication record in Supabase
        auth_response = supabase.auth.sign_up(email=email, password=password)
        if "user" in auth_response:
            user_id = auth_response["user"]["id"]
            # Add user profile to `users` table
            supabase.table("users").insert({
                "id": user_id,
                "email": email,
                "role": role,
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": phone_number,
                "created_at": "NOW()",
                "updated_at": "NOW()"
            }).execute()
            st.success(f"User {email} registered successfully!")
        else:
            st.error("Registration failed. Check your inputs.")
    except Exception as e:
        st.error("Registration failed.")
        st.write(e)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Tasks", "Calendar", "Feedback"])
user_role = st.sidebar.radio("Select Role", ["Client", "Social Worker", "Admin"])

#Admin Interface

if user_role == "Admin":
    st.header("Admin Dashboard")

    if page == "Users":
        st.subheader("User Management")
        # Fetch and display all users
        try:
            users = supabase.table("users").select("*").execute()
            if users.data:
                for user in users.data:
                    st.write(f"- **{user['email']}**: Role - {user['role']}")
            else:
                st.info("No users found.")
        except Exception as e:
            st.error("Error fetching users.")
            st.write(e)

    elif page == "Tasks":
        st.subheader("Task Management")
        # Fetch and display all tasks
        try:
            tasks = supabase.table("tasks").select("*").execute()
            if tasks.data:
                for task in tasks.data:
                    st.write(f"- **{task['name']}**: Assigned to User ID - {task['user_id']}")
            else:
                st.info("No tasks found.")
        except Exception as e:
            st.error("Error fetching tasks.")
            st.write(e)



# Client Interface
elif user_role == "Client":
    if page == "Tasks":
        st.header("My Tasks")
        
        # Display Task List
        st.subheader("Task List")
        try:
            tasks = supabase.table("tasks").select("*").eq("user_role", "client").execute()
            if tasks.data:
                for task in tasks.data:
                    st.write(f"- **{task['name']}**: {task['description']} (Due: {task['due_date']})")
            else:
                st.info("No tasks found.")
        except Exception as e:
            st.error("Error fetching tasks.")
            st.write(e)
        
        # Add New Task
        st.subheader("Add New Task")
        with st.form("add_task_form"):
            task_name = st.text_input("Task Name")
            task_description = st.text_area("Task Description")
            task_due_date = st.date_input("Due Date")
            task_category = st.text_input("Category")
            submitted = st.form_submit_button("Add Task")
            
            if submitted:
                try:
                    response = supabase.table("tasks").insert({
                        "name": task_name,
                        "description": task_description,
                        "due_date": task_due_date.isoformat(),
                        "category": task_category,
                        "status": "pending",
                        "user_role": "client"
                    }).execute()
                    st.success("Task added successfully!")
                except Exception as e:
                    st.error("Error adding task.")
                    st.write(e)
    
    elif page == "Calendar":
        st.header("Calendar View")
        st.write("This will show tasks on a calendar (future enhancement).")

# Social Worker Interface
elif user_role == "Social Worker":
    if page == "Tasks":
        st.header("Client Dashboard")
        
        # Select Client
        st.subheader("Clients")
        try:
            clients = supabase.table("users").select("*").eq("role", "client").execute()
            client_names = [client["email"] for client in clients.data]
            selected_client = st.selectbox("Select a Client", client_names)
        except Exception as e:
            st.error("Error fetching clients.")
            st.write(e)
        
        # Display Client Tasks
        if selected_client:
            st.subheader(f"Tasks for {selected_client}")
            try:
                tasks = supabase.table("tasks").select("*").eq("client_email", selected_client).execute()
                for task in tasks.data:
                    st.write(f"- **{task['name']}**: {task['description']} (Due: {task['due_date']}, Status: {task['status']})")
            except Exception as e:
                st.error("Error fetching tasks.")
                st.write(e)
    
    elif page == "Feedback":
        st.header("Provide Feedback")
        
        # Provide Feedback Form
        try:
            tasks = supabase.table("tasks").select("*").eq("status", "completed").execute()
            task_names = [task["name"] for task in tasks.data]
            selected_task = st.selectbox("Select a Completed Task", task_names)
            with st.form("feedback_form"):
                feedback = st.text_area("Feedback")
                submitted = st.form_submit_button("Submit Feedback")
                
                if submitted:
                    try:
                        supabase.table("feedback").insert({
                            "task_name": selected_task,
                            "feedback": feedback,
                            "social_worker": "example_worker"
                        }).execute()
                        st.success("Feedback submitted successfully!")
                    except Exception as e:
                        st.error("Error submitting feedback.")
                        st.write(e)
        except Exception as e:
            st.error("Error fetching completed tasks.")
            st.write(e)
