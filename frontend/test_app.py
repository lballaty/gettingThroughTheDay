import streamlit as st
from supabase import create_client, Client

# Supabase configuration
SUPABASE_URL = "https://gnyvvmvazbjvhnzhvetv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdueXZ2bXZhemJqdmhuemh2ZXR2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY5MzIwOTcsImV4cCI6MjA1MjUwODA5N30.NSx6aI1v8ou6Sv-qKCtjwsl7FmtG6e1ztIb1bBDPBvE"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# Initialize session state
if "view" not in st.session_state:
    st.session_state["view"] = "login"  # Default view

# Function to change views
def change_view(view_name):
    st.session_state["view"] = view_name
   # st.experimental_rerun()

# Registration view
def registration_view():
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
            # Register user in Supabase
            auth_response = supabase.auth.sign_up(email=email, password=password)
            if "user" in auth_response:
                user_id = auth_response["user"]["id"]
                # Add user profile to the `users` table
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
               # st.button("Go to Login", on_click=lambda: change_view("login"))

                if st.button("Go to Login"):
                    change_view("login")

            else:
                st.error("Registration failed. Check your inputs.")
        except Exception as e:
            st.error("Registration failed.")
            st.write(e)

# Login view
def login_view():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        try:
            # Authenticate user in Supabase
            auth_response = supabase.auth.sign_in(email=email, password=password)
            if "user" in auth_response:
                user_id = auth_response["user"]["id"]
                user_data = supabase.table("users").select("*").eq("id", user_id).execute()
                if user_data.data:
                    user_profile = user_data.data[0]
                    st.success(f"Welcome {user_profile['first_name']} ({user_profile['role']})")
                    # Store user details in session state
                    st.session_state["user_role"] = user_profile["role"]
                    st.session_state["user_id"] = user_profile["id"]
                    change_view("dashboard")
                else:
                    st.error("User profile not found.")
            else:
                st.error("Invalid credentials.")
        except Exception as e:
            st.error("Login failed.")
            st.write(e)

    #st.button("Register New User", on_click=lambda: change_view("register"))

     if st.button("Register New User"):
        change_view("register")


# Role-based dashboard view
def dashboard_view():
    user_role = st.session_state.get("user_role")
    if not user_role:
        st.warning("Unauthorized access. Please log in.")
        change_view("login")
        return

    st.title(f"{user_role.capitalize()} Dashboard")
    if user_role == "Admin":
        admin_dashboard()
    elif user_role == "Client":
        client_dashboard()
    elif user_role == "Social Worker":
        social_worker_dashboard()

    #st.button("Logout", on_click=lambda: st.session_state.clear() or change_view("login"))
    if st.button("Logout"):
        change_view("login")


# Admin-specific dashboard
def admin_dashboard():
    st.header("Admin Dashboard")
    st.subheader("User Management")
    try:
        users = supabase.table("users").select("*").execute()
        for user in users.data:
            st.write(f"{user['email']} - Role: {user['role']}")
    except Exception as e:
        st.error("Error fetching users.")
        st.write(e)

# Client-specific dashboard
def client_dashboard():
    st.header("Client Dashboard")
    st.subheader("My Tasks")
    try:
        tasks = supabase.table("tasks").select("*").eq("user_id", st.session_state["user_id"]).execute()
        if tasks.data:
            for task in tasks.data:
                st.write(f"- **{task['name']}**: {task['description']} (Due: {task['due_date']})")
        else:
            st.info("No tasks found.")
    except Exception as e:
        st.error("Error fetching tasks.")
        st.write(e)

# Social worker-specific dashboard
def social_worker_dashboard():
    st.header("Social Worker Dashboard")
    st.subheader("Assigned Clients")
    try:
        clients = supabase.table("users").select("*").eq("role", "client").execute()
        if clients.data:
            for client in clients.data:
                st.write(f"{client['email']} - {client['first_name']} {client['last_name']}")
        else:
            st.info("No clients found.")
    except Exception as e:
        st.error("Error fetching clients.")
        st.write(e)

# Main app
if st.session_state["view"] == "login":
    login_view()
elif st.session_state["view"] == "register":
    registration_view()
elif st.session_state["view"] == "dashboard":
    dashboard_view()

