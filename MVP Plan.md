**POC/MVP Design Document**

**Project Name:** gettingThroughTheDay  
**Date:** [Insert Date]  
**Version:** Draft 1.0

---

### 1. Core Features for POC/MVP

1. **Task Management** (Client Interface):
   - Create, edit, and delete tasks.
   - Assign tasks to user-defined categories.
   - Categorize tasks as daily, weekly, or other user-defined types.
   - Mark tasks as completed.

2. **Planning and Scheduling**:
   - Daily and weekly task planning with a visual calendar view.
   - Simple drag-and-drop functionality for task rescheduling (optional for POC).

3. **Social Worker Monitoring and Feedback**:
   - View client progress on tasks.
   - Add feedback or suggestions for improvement.
   - Adjust client plans as needed.

4. **Configurable Task Categories**:
   - Allow clients and social workers to define task categories.
   - Group and filter tasks by category.

5. **Backend Database** (Supabase):
   - Store task details, schedules, feedback, and user-defined categories.
   - Manage user authentication and role-based access.
   - Ensure data encryption and compliance with GDPR.

6. **Basic User Roles and Permissions**:
   - Client: Access to their own tasks and feedback.
   - Social Worker: Access to assigned clients’ data and feedback tools.

---

### 2. Simplified Scope for POC

**Client Interface:**
- A functional task list and calendar view.
- Simple interface for adding and categorizing tasks.

**Social Worker Interface:**
- Dashboard to monitor a single client’s tasks and progress.
- Feedback submission interface.

**Backend:**
- Supabase setup with minimal schema to support tasks, categories, and feedback.
- Authentication for clients and social workers.

---

### 3. User Flows for POC

#### Client Task Creation and Categorization:
1. Log in to the Client Interface.
2. Navigate to the "Tasks" section.
3. Click "Add Task" and input task details (e.g., name, description, due date).
4. Assign the task to a category (e.g., Work, Health, Personal).
5. Save the task, which appears in the list and calendar view.

#### Social Worker Feedback:
1. Log in to the Social Worker Interface.
2. Select a client profile.
3. Review tasks and progress.
4. Provide feedback for tasks marked as completed.
5. Submit feedback, visible to the client.

---

### 4. Technical Requirements

1. **Frontend:**
   - Framework: Streamlit for rapid prototyping and simplicity.
   - Use forms for task creation, categorization, and feedback submission.
   - Display task lists and calendar views using libraries like `streamlit-aggrid`.

2. **Backend:**
   - Supabase for database and authentication.
   - Basic schema for users, tasks, categories, and feedback.

3. **Deployment:**
   - Frontend: Hosted on Streamlit Cloud.
   - Backend: Supabase free tier.

4. **Code Repository:**
   - Use GitHub for version control and collaboration.
   - Ensure clear folder structures and commit messages for better management.

5. **Security:**
   - User authentication via Supabase.
   - Basic role-based access controls.

---


### 5. Timeline

**Week 1**:
- Finalize core features and scope.
- Set up Supabase backend.

**Week 2**:
- Develop Client Interface for task management using Streamlit.
- Integrate backend with Streamlit frontend.

**Week 3**:
- Develop Social Worker Interface for feedback.
- Test client and social worker flows.

**Week 4**:
- Conduct internal testing.
- Deploy POC on Streamlit Cloud for stakeholder feedback.

---

Let me know if this aligns with your vision or if additional details are needed for any section!

