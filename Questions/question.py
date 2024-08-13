import streamlit as st
import sqlite3

# Link to the external CSS file
def local_css(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style.css")

# Database connection
conn = sqlite3.connect('question.db')
c = conn.cursor()

# Create the Questions table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS question (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER,
    question_text TEXT NOT NULL,
    question_type TEXT NOT NULL,
    FOREIGN KEY (quiz_id) REFERENCES Quizzes(quiz_id)
);
''')
conn.commit()


# Function to add a question
def add_question(quiz_id, question_text, question_type):
    c.execute('''
        INSERT INTO Questions (quiz_id, question_text, question_type)
        VALUES (?, ?, ?)
    ''', (quiz_id, question_text, question_type))
    conn.commit()

# Function to update a question
def update_question(question_id, quiz_id, question_text, question_type):
    c.execute('''
        UPDATE Questions
        SET quiz_id = ?, question_text = ?, question_type = ?
        WHERE question_id = ?
    ''', (quiz_id, question_text, question_type, question_id))
    conn.commit()


# Function to delete a question
def delete_question(question_id):
    c.execute('DELETE FROM Questions WHERE question_id = ?', (question_id,))
    conn.commit()

# Function to search questions
def search_questions(search_term):
    c.execute('''
        SELECT * FROM Questions
        WHERE question_text LIKE ?
    ''', ('%' + search_term + '%',))
    return c.fetchall()

# Streamlit app UI
st.title("Question Management System")

menu = ["Add Question", "Update Question", "Delete Question", "Search Questions"]
choice = st.sidebar.radio("Menu", menu)

if choice == "Add Question":
    st.subheader("Add a New Question")
    quiz_id = st.number_input("Quiz ID", min_value=1)
    question_text = st.text_area("Question Text")
    question_type = st.selectbox("Question Type", ["Multiple Choice", "True/False", "Short Answer"])
    if st.button("Add Question"):
        if not question_text.strip():
            st.warning("Please enter a question text.")
        else:
            add_question(quiz_id, question_text, question_type)
            st.success("Question added successfully.")

if choice == "Update Question":
    st.subheader("Update an Existing Question")
    question_id = st.number_input("Question ID", min_value=1)
    quiz_id = st.number_input("Quiz ID", min_value=1)
    question_text = st.text_area("Question Text")
    question_type = st.selectbox("Question Type", ["Multiple Choice", "True/False", "Short Answer"])
    if st.button("Update Question"):
        if not question_text.strip():
            st.warning("Please enter a question text.")
        else:
            update_question(question_id, quiz_id, question_text, question_type)
            st.success("Question updated successfully.")
            
elif choice == "Delete Question":
    st.subheader("Delete a Question")
    question_id = st.number_input("Question ID to Delete", min_value=1)
    if st.button("Delete Question"):
        delete_question(question_id)
        st.success(f"Question ID '{question_id}' deleted successfully.")

elif choice == "Search Questions":
    st.subheader("Search Questions")
    search_term = st.text_input("Search by Question Text")
    if st.button("Search"):
        results = search_questions(search_term)
        if results:
            for question in results:
                st.write(f"ID: {question[0]} | Quiz ID: {question[1]} | Text: {question[2]} | Type: {question[3]}")
        else:
            st.warning("No questions found.")

conn.close()
