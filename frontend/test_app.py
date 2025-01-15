import streamlit as st
import re  # Import for regex validation
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
    """Change the current view."""
    st.session_state["view"] = view_name

# Function to validate email
def is_valid_email(email):
    """Validate email format."""
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None
    
# Function to validate passwords
def is_valid_password(password):
    """Validate password strength."""
    return len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isalpha() for char in password)

# Registration view
def registration_view():
    st.title("User Registration")

    # Email input with real-time validation
    email = st.text_input("Email")
    if email and not is_valid_email(email):
        st.warning("Please enter a valid email address.")

    # Password input with validation
    password = st.text_input("Password", type="password")
    if password and not is_valid_password(password):
        st.warning("Password must be at least 8 characters long, with a mix of letters and numbers.")

    # Role selection
    role = st.selectbox("Role", ["Client", "Social Worker", "Admin"])

    # First name and last name inputs
    first_name = st.text_input("First Name (optional)")
    last_name = st.text_input("Last Name (optional)")

    # Phone number input with validation
    country_code = st.selectbox("Country Code", ["+1 (US)", "+44 (UK)", "+91 (India)", "+420 (Czech Republic)", "+351 (Portugal)", "+61 (Australia)"])
    phone_number = st.text_input("Phone Number (optional)")
    phone_valid = re.match(r"^\d{7,15}$", phone_number) is not None if phone_number else True
    if phone_number and not phone_valid:
        st.warning("Phone number should only contain digits and be 7-15 characters long.")

    # Submit button
    register_button = st.button("Register")

    if register_button:
        # Validate all inputs
        if not is_valid_email(email):
            st.error("Invalid email address. Please correct it.")
            return
        if not is_valid_password(password):
            st.error("Password must be at least 8 characters long, with a mix of letters and numbers.")
            return
        if phone_number and not phone_valid:
            st.error("Invalid phone number format.")
            return

        # Attempt to register the user
        try:
            auth_response = supabase.auth.sign_up({"email": email, "password": password})
            if "user" in auth_response:
                user_id = auth_response["user"]["id"]
                supabase.table("users").insert({
                    "id": user_id,
                    "email": email,
                    "role": role,
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone_number": f"{country_code} {phone_number}" if phone_number else None,
                }).execute()
                st.success(f"User {email} registered successfully!")
                if st.button("Go to Login"):
                    change_view("login")
            else:
                st.error("Registration failed. Please verify your input.")
        except Exception as e:
            error_message = str(e).lower()
            if "already registered" in error_message:
                st.error("This email is already registered. Try logging in.")
            else:
                st.error(f"An unexpected error occurred: {error_message}")


# Login view
def login_view():
    st.title("Login")

    # Input fields
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        # Validate inputs
        if not is_valid_email(email):
            st.error("Invalid email address format. Please correct it.")
            return
        if not password:
            st.error("Password cannot be empty.")
            return

        # Attempt to authenticate
        try:
            auth_response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if "user" in auth_response:
                user_id = auth_response["user"]["id"]

                # Fetch user details
                user_data = supabase.table("users").select("*").eq("id", user_id).execute()
                if user_data.data:
                    user_profile = user_data.data[0]
                    st.success(f"Welcome {user_profile['first_name']} ({user_profile['role']})")
                    st.session_state["user_role"] = user_profile["role"]
                    st.session_state["user_id"] = user_profile["id"]
                    change_view("dashboard")
                else:
                    st.error("Account exists but profile not found. Please contact support.")
            else:
                st.error("Invalid credentials. Please try again.")
        except Exception as e:
            error_message = str(e).lower()
            if "email not confirmed" in error_message:
                st.error("Your email is not confirmed. Please check your inbox.")
            elif "email or password is invalid" in error_message:
                st.error("Incorrect email or password.")
            elif "invalid login credentials" in error_message:
                st.error("This account does not exist. Please register below.")
                st.markdown(
                    "<p style='color: red; font-weight: bold;'>Click the Register Now button below to create an account!</p>",
                    unsafe_allow_html=True,
                )
            else:
                st.error("An unexpected error occurred during login.")
                st.write(f"Details: {error_message}")

    # Add a "Register Now" button at the bottom of the login form
    st.markdown("---")
    st.write("Don't have an account?")
    register_button = st.button("Register Now")
    if register_button:
        change_view("register")




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

