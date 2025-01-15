import streamlit as st
from supabase import create_client, Client

# Supabase configuration
SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_supabase_anon_key"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Streamlit app
st.title("Streamlit Test App with Supabase")
st.write("Welcome to gettingThroughTheDay!")

# Test connection to Supabase
try:
    st.header("Supabase Connection Test")
    data = supabase.table("tasks").select("*").execute()
    st.write("Data fetched from 'tasks' table:")
    st.dataframe(data.data)
except Exception as e:
    st.error("Error connecting to Supabase")
    st.write(e)

# Add a simple form to insert data into the 'tasks' table
st.header("Add a Test Task")
with st.form("add_task_form"):
    task_name = st.text_input("Task Name", placeholder="Enter task name")
    task_description = st.text_area("Task Description", placeholder="Enter task details")
    task_due_date = st.date_input("Due Date")
    submitted = st.form_submit_button("Add Task")

    if submitted:
        try:
            response = supabase.table("tasks").insert({
                "name": task_name,
                "description": task_description,
                "due_date": task_due_date.isoformat(),
                "status": "pending"
            }).execute()
            st.success("Task added successfully!")
            st.write(response.data)
        except Exception as e:
            st.error("Error adding task to Supabase")
            st.write(e)

# Simple display for all tasks
st.header("All Tasks")
try:
    tasks = supabase.table("tasks").select("*").execute()
    st.write("Fetched tasks from the database:")
    st.dataframe(tasks.data)
except Exception as e:
    st.error("Error fetching tasks")
    st.write(e)

