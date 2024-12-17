import streamlit as st
import pandas as pd
from datetime import datetime

# Function to save complaint data to a CSV file
def save_complaint(name, designation, student_class, description):
    # Create a DataFrame to hold the complaint details
    complaint_data = {
        'Name': [name],
        'Designation': [designation],
        'Class': [student_class if designation == "Student" else "N/A"],
        'Description': [description],
        'Date': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    }
    df = pd.DataFrame(complaint_data)

    # Save or append to a CSV file
    try:
        df.to_csv('complaints.csv', mode='a', header=False, index=False)
    except FileNotFoundError:
        df.to_csv('complaints.csv', mode='w', header=True, index=False)

# Function to load complaints from the CSV file (For viewing)
def load_complaints():
    try:
        df = pd.read_csv('complaints.csv')
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['Name', 'Designation', 'Class', 'Description', 'Date'])

# Initialize session state to store complaints temporarily
if 'complaints' not in st.session_state:
    st.session_state['complaints'] = []

# Streamlit app layout
st.title("School Complaint Submission System")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Submit Complaint", "View Complaints"])

if page == "Submit Complaint":
    st.header("Submit a Complaint")

    # Input fields for the complaint
    name = st.text_input("Enter your Name:")
    designation = st.selectbox("Select your Designation:", ["Student", "Teacher"])
    student_class = ""
    if designation == "Student":
        student_class = st.text_input("Enter your Class:")
    description = st.text_area("Enter your Complaint Description:")

    # File upload (optional)
    uploaded_file = st.file_uploader("Upload any related file (Optional)", type=["jpg", "jpeg", "png", "pdf"])

    # Submit button
    if st.button("Submit Complaint"):
        # Check if the required fields are filled
        if name.strip() and description.strip() and (designation == "Teacher" or student_class.strip()):
            # Save the complaint to CSV
            save_complaint(name, designation, student_class, description)
            
            # Temporarily store the complaint in session state
            complaint = {
                'Name': name.strip(),
                'Designation': designation,
                'Class': student_class.strip() if designation == "Student" else "N/A",
                'Description': description.strip(),
                'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            st.session_state['complaints'].append(complaint)
            
            st.success("Your complaint has been successfully submitted!")
            
            # Optionally show the uploaded file
            if uploaded_file:
                st.image(uploaded_file, caption="Uploaded file", use_column_width=True)
        else:
            st.error("Please fill all the required fields before submitting.")

elif page == "View Complaints":
    st.header("View Complaints")

    # If there are complaints stored in the session state, display them
    if len(st.session_state['complaints']) > 0:
        # Display complaints from session state
        for complaint in st.session_state['complaints']:
            st.subheader(f"Complaint Submitted on {complaint['Date']}")
            st.write(f"**Name**: {complaint['Name']}")
            st.write(f"**Designation**: {complaint['Designation']}")
            st.write(f"**Class**: {complaint['Class']}")
            st.write(f"**Description**: {complaint['Description']}")
            st.write("---")
    else:
        st.write("No complaints submitted yet.")

    # Load complaints from the CSV file and display them (for persistence)
    st.subheader("Complaints from CSV file:")
    complaints_df = load_complaints()

    # If there are complaints in the CSV, display them
    if len(complaints_df) > 0:
        st.write(complaints_df)
    else:
        st.write("No complaints in the CSV file.")
