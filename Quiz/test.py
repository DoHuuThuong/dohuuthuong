import streamlit as st
import sqlite3

from datetime import datetime 
# Link to the external CSS file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# Database connection
conn = sqlite3.connect('quiz_management.db')
c = conn.cursor()

# Create the Quizzes table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS Quizzes (
    quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_name TEXT NOT NULL,
    description TEXT,
    created_by INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

# Function to add a quiz
def add_quiz(quiz_name, description, created_by):
    c.execute('''
        INSERT INTO Quizzes (quiz_name, description, created_by)
        VALUES (?, ?, ?)
    ''', (quiz_name, description, created_by))
    conn.commit()

def delete_quiz_and_rearrange_ids(quiz_id):
    c.execute('DELETE FROM Quizzes WHERE quiz_id = ?', (quiz_id,))
    c.execute('SELECT quiz_id FROM Quizzes ORDER BY quiz_id ASC')
    quizzes = c.fetchall()
    
    for index, (current_id,) in enumerate(quizzes, start=1):
        c.execute('UPDATE Quizzes SET quiz_id = ? WHERE quiz_id = ?', (index, current_id))
    
    c.execute(''' 
    UPDATE sqlite_sequence SET seq = (SELECT MAX(quiz_id) FROM Quizzes) WHERE name = 'Quizzes'
    ''')
    
    conn.commit()

# Function to update a quiz
def update_quiz(quiz_id, quiz_name, description):
    c.execute('''
        UPDATE Quizzes
        SET quiz_name = ?, description = ?
        WHERE quiz_id = ?
    ''', (quiz_name, description, quiz_id))
    conn.commit()


# Function to delete a quiz
def delete_quiz(quiz_id):
    c.execute('DELETE FROM Quizzes WHERE quiz_id = ?', (quiz_id,))
    conn.commit()

# Function to search quizzes
def search_quizzes(search_term):
    c.execute('''
        SELECT * FROM Quizzes
        WHERE quiz_name LIKE ?
    ''', ('%' + search_term + '%',))
    return c.fetchall()

# Streamlit app UI
st.title("Quiz Management System")

menu = ["Add Quiz", "Update Quiz", "Delete Quiz", "Search Quizzes"]
choice = st.sidebar.radio("Menu", menu)

if choice == "Add Quiz":
    st.subheader("Add a New Quiz")
    quiz_name = st.text_input("Quiz Name")
    description = st.text_area("Description")
    created_by = st.number_input("Created By (User ID)", min_value=1)
    if st.button("Add Quiz"):
        if not quiz_name.strip():
            st.warning("Please enter a quiz name.")
        elif not description.strip():
            st.warning("Please enter a description.")
     
        else:
            add_quiz(quiz_name, description, created_by)
            st.success(f"Quiz '{quiz_name}' added successfully.")


elif choice == "Update Quiz":
    st.subheader("Update an Existing Quiz")
    quiz_id = st.number_input("Quiz ID", min_value=1)
    quiz_name = st.text_input("New Quiz Name")
    description = st.text_area("New Description")
    if st.button("Update Quiz"):
        if quiz_id <= 0:
            st.warning("Please enter a valid Quiz ID (greater than 0).")
        elif not quiz_name.strip():
            st.warning("Please enter a new quiz name.")
        elif not description.strip():
            st.warning("Please enter a new description.")
        else:
            update_quiz(quiz_id, quiz_name, description)
            st.success(f"Quiz ID '{quiz_id}' updated successfully.")


elif choice == "Delete Quiz":
    st.subheader("Delete a Quiz")
    quiz_id = st.number_input("Quiz ID to Delete", min_value=1)
    if st.button("Delete Quiz"):
        delete_quiz(quiz_id)
        st.success(f"Quiz ID '{quiz_id}' deleted successfully.")

elif choice == "Search Quizzes":
    st.subheader("Search Quizzes")
    search_term = st.text_input("Search by Quiz Name")
    if st.button("Search"):
        results = search_quizzes(search_term)
        if results:
            for quiz in results:
                st.write(f"ID: {quiz[0]} | Name: {quiz[1]} | Description: {quiz[2]} | Created By: {quiz[3]} | Created At: {quiz[4]}")
        else:
            st.warning("No quizzes found.")

conn.close()

