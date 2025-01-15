
**User Interface Design Document**

**Project Name:** gettingThroughTheDay  
**Date:** [Insert Date]  
**Version:** Draft 1.0

---

### 1. Overview

This document outlines the design and layout of the user interfaces for the *gettingThroughTheDay* application. The interfaces are divided into two main components: the **Client Interface** and the **Social Worker Interface**.

---

### 2. Client Interface

#### **2.1 Navigation Bar**
- **Components:**
  - Links to:
    - Tasks
    - Calendar View
    - Profile

#### **2.2 Task Management Section**
- **Task List:**
  - Display tasks grouped by categories (e.g., Work, Health).
  - Filters for categories and status (`pending`, `completed`).
- **Task Creation Form:**
  - Input Fields:
    - Task Name (Text)
    - Task Description (Textarea)
    - Due Date (Date Picker)
    - Category (Dropdown or Text Input)
  - Submit Button to save the task.

#### **2.3 Calendar View**
- **Features:**
  - Visual representation of tasks by date.
  - Clickable tasks for quick editing.

---

### 3. Social Worker Interface

#### **3.1 Navigation Bar**
- **Components:**
  - Links to:
    - Client Dashboard
    - Feedback Section
    - Profile

#### **3.2 Client Dashboard**
- **Client List:**
  - Display a list of assigned clients.
  - Select a client to open their **Task Overview**:
    - Group tasks by completion status and category.
    - Progress indicators (e.g., percentage completed).

#### **3.3 Feedback Section**
- **Features:**
  - List of completed tasks with a feedback form.
  - Input Fields:
    - Select a completed task.
    - Feedback Text.
  - Submit Button to save feedback for the client.

---

### 4. Implementation Plan

#### **4.1 Client Interface - Layout Skeleton**
```python
import streamlit as st

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Tasks", "Calendar", "Profile"])

if page == "Tasks":
    st.header("My Tasks")
    # Task List
    st.subheader("Task List")
    st.write("Work: Task 1, Task 2")
    st.write("Health: Task 3")
    
    # Task Creation Form
    st.subheader("Add New Task")
    with st.form("task_form"):
        task_name = st.text_input("Task Name")
        task_description = st.text_area("Task Description")
        task_due_date = st.date_input("Due Date")
        task_category = st.text_input("Category")
        submitted = st.form_submit_button("Add Task")
        if submitted:
            st.success(f"Task '{task_name}' added successfully!")

elif page == "Calendar":
    st.header("Calendar View")
    st.write("This will show tasks on a calendar (future enhancement).")
```

#### **4.2 Social Worker Interface - Layout Skeleton**
```python
# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Client Dashboard", "Feedback", "Profile"])

if page == "Client Dashboard":
    st.header("Client Dashboard")
    client_list = ["Client 1", "Client 2"]  # Example clients
    selected_client = st.selectbox("Select a client", client_list)
    st.write(f"Showing tasks for {selected_client}")
    # Display tasks and progress

elif page == "Feedback":
    st.header("Feedback Section")
    st.subheader("Completed Tasks")
    with st.form("feedback_form"):
        task_to_feedback = st.selectbox("Select a completed task", ["Task 1", "Task 2"])
        feedback_text = st.text_area("Provide Feedback")
        submitted = st.form_submit_button("Submit Feedback")
        if submitted:
            st.success(f"Feedback for '{task_to_feedback}' submitted!")
```

---

### 5. Enhancements
- **Client Interface:**
  - Add a search bar for tasks.
  - Enable drag-and-drop for calendar view (future enhancement).
- **Social Worker Interface:**
  - Display aggregated client statistics on the dashboard.
  - Allow task reassignment to other categories.

---



