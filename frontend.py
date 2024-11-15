import streamlit as st
from backend import register, fetch_topics_by_topic, fetch_flashcards, login, fetch_intermediate_topic, fetch_inter_flashcards


# Define pages outside of main function for clarity
def go_to_page(page_name):
    st.session_state.current_page = page_name  # Update the page to the desired one

# Update progress when a user interacts with an expander
def update_progress(topic_name):
    if 'progress' not in st.session_state:
        st.session_state.progress = 0  # Initialize progress if not already set

    if topic_name not in st.session_state:
        st.session_state[topic_name] = False  # Track whether the topic has been opened

    # If the user opens the expander for the first time, update progress
    if not st.session_state[topic_name]:
        st.session_state[topic_name] = True  # Mark the topic as interacted with
        st.session_state.progress += 6.67  # Increment progress by 6.67% (or any other value)
        # Ensure progress does not exceed 100
    if st.session_state.progress > 100:
        st.session_state.progress = 100
        
def update_progress_intermediate(topic_name):
    if 'intermediate_progress' not in st.session_state:
        st.session_state.intermediate_progress = 0  # Initialize progress if not already set

    if topic_name not in st.session_state:
        st.session_state[topic_name] = False  # Track whether the topic has been opened

    # If the user opens the expander for the first time, update progress
    if not st.session_state[topic_name]:
        st.session_state[topic_name] = True  # Mark the topic as interacted with
        st.session_state.intermediate_progress += 7.14  # Increment progress by 7.14% (or any other value)

    # Ensure progress does not exceed 100
    if st.session_state.intermediate_progress > 100:
        st.session_state.intermediate_progress = 100



# Display topics under the specific section


# Home Page


# Registration Page
def registration_page():
    st.title("Registration Page")
    st.markdown("### Please enter your details below")

    # Input fields for email, username, and password
    email = st.text_input("Email", max_chars=50)
    username = st.text_input("Username", max_chars=20)
    password = st.text_input("Password", type="password", max_chars=20)

    # Register button
    if st.button("Register"):
        if username and password and email:
            register(username, email, password)  # Call your registration function
            st.success(f"User {username} registered successfully!")
            go_to_page('home')  # Go to home page after successful registration
        else:
            st.warning("Please enter a username, email, and password.")
    
    # Option to go back to login page
    if st.button("Go to Login"):
        go_to_page("login_page")

def login_page():
    st.title("Login Page")
    st.markdown("Please enter your username or email and password to log in.")

    # Input fields for username/email and password
    username_or_email = st.text_input("Username or Email")
    password = st.text_input("Password", type="password")

    # Login button
    if st.button("Login"):
        if username_or_email and password:
            # Call the login function and capture the response
            result = login(username_or_email, password)
            
            # Display the result message
            if "successful" in result:
                st.success(result)
                st.session_state.logged_in = True
                st.session_state.user = username_or_email  # Store user info in session
                go_to_page('beginner_page')  # Go directly to beginner page
            else:
                st.error(result)
        else:
            st.warning("Please enter both username/email and password.")
    
    # Option to go to registration page
    if st.button("Register"):
        go_to_page("registration")  # Go to registration page if clicked


def home_page():
    st.title("Home Page")
    st.write("Welcome to the Home Page!")
    if st.button("Logout"):
        go_to_page('registration')  # Redirect to Registration page

    # Main app content
    st.write("Welcome to our App! Use the tutorial below to learn how to use this app.")

    # Step 1: Introduction
    with st.expander("Step 1: Introduction"):
        st.write("""This app is designed to provide you with resources to learn Python faster. You have three stages: Beginner, Intermediate & Advanced.""")

    # Step 2: Setting Up
    with st.expander("Step 2: Setting Up"):
        st.write("""Each Level has different topics under it. Each topic includes resources & a video to help make your learning more focused.""")

    # Step 3: Using the App
    with st.expander("Step 3: Using the App"):
        st.write("""Once you are done with a topic, you are to take a brief quiz to test your knowledge of the course.""")

    if st.button("Finish Tutorial", on_click=beginner_page, key="finish_tutorial"):
        go_to_page('beginner_page')


def display_topics(topics):
    if topics:
        for topic in topics:
            name = topic['name']
            # Display the topic details inside the expander
            st.subheader(topic['name'])  # Display the topic name
            st.write(topic['description'])  # Display the topic description
            if topic['external_link']:
                st.markdown(f"[{name}]({topic['external_link']})")  # Display the external link if exists
    else:
        st.write("No topics available yet.")

# Beginner Page
def beginner_page():
    st.title("Beginner Topics")
    st.write("Welcome to the Beginner Level. Here are the topics you can explore:")

    topics_list = [
        ('Intro', 'Introduction to Python', 1,'https://forms.gle/4e8kR2S6XgxczAUBA'),  # 1 is the topic_id for Intro
        ('Syntax', 'Basic Syntax in Python', 2, 'https://forms.gle/nGMiLii2SpJAiKmX7'),
        ('Data_type', 'Datatype & Type Conversion', 3, 'https://forms.gle/cSSScyTk6DXGf1Q18'),
        ('variables', 'Variables', 4, 'https://forms.gle/BT3h92isiA97uRkBA'),
        ('operators', 'Operators & Expressions', 5, 'https://forms.gle/j1bdd4fgmDHYpZqM8'),
        ('conditionals', 'Conditionals' , 6,'https://forms.gle/DDXpss2WP7mbhqeY8'),
        ('functions', 'Functions', 7, 'https://forms.gle/5QgJnnApfV2Vaz55A'),
        ('formatting', 'String Formating', 8, 'https://forms.gle/nrPRYX8Rh78H3LJ29'),
        ('lists', 'Lists', 9, 'https://forms.gle/b2o9JjByzTzqtxBs6'),
        ('tuples', 'Tuples', 10, 'https://forms.gle/briLCXzq8P8VhzTVA'),
        ('dict', 'Dictionaries', 11, 'https://forms.gle/uBCRhjFronpSPw8A9'),
        ('loops', 'Loops', 12, 'https://forms.gle/YmPVTPw88EUqLVL47'),
        ('libs', 'Modules & Libaries', 13, 'https://forms.gle/z5fwaaiRXydyAE1X7'),
        ('oop','Object-Oriented Programming', 14, 'https://forms.gle/RNo6acc7FY6t3QVAA'),
        ('packages','Working with Packages', 15, 'https://forms.gle/xT2LCxK2GJE4AKBLA')
    ]

    for idx, (topic_key, topic_title, topic_id, question_link) in enumerate(topics_list):
        with st.expander(topic_title):
            # Update progress when the user interacts with the expander
            update_progress(topic_key)

            # Display the topic content
            topics = fetch_topics_by_topic(topic_key)
            display_topics(topics)
            
            # Display current progress
            st.write(f"Your progress: {st.session_state.progress}%")
            
            if st.button(f'Questions', key=f'questions_button_{idx}'):
                st.markdown(f"[Click here to go to quiz]({question_link})", unsafe_allow_html=True)
            
            # Button to go to the flashcards page
            if st.button(f"Flashcard - Learn More", key=f"flashcard_button_{idx}"):
                st.session_state.selected_topic_id = topic_id
                go_to_page('flashcard')
    if st.button('Intermediate'):
        go_to_page('intermediate')

def intermediate_page():
    st.title("Intermediate Topics")
    st.write("Welcome to the Intermediate Level. Here are the topics you can explore:")

    topics_list = [
        ('advfunc', 'Advanced Functions (Higher Order functions, Closure)', 1),
        ('compr', 'List, Dictionary, and Set Comprehensions', 2),
        ('excpt', 'Exception Handling  Custom Exceptions', 3),
        ('file', 'File Handling  Reading and Writing Large Files', 4),
        ('stdlib', 'Python Standard Library (e.g., datetime, collections, itertools)', 5),
        ('oop', 'Introduction to Object-Oriented Programming (Classes, Inheritance)', 6),
        ('polymorphism', 'Polymorphism and Method Overriding', 7),
        ('api', 'Working with External APIs', 8),
        ('gui', 'Introduction to GUI Programming (Tkinter, Kivy)', 9),
        ('data', 'Data Handling with JSON and CSV', 10),
        ('scraping', 'Introduction to Web Scraping (BeautifulSoup, Requests)', 11),
        ('testing', 'Introduction to Unit Testing (unittest, pytest)', 12),
        ('lambda', 'Lambda Functions and Anonymous Functions', 13),
        ('env', 'Introduction to Virtual Environments', 14),
        ('database', 'Working with Databases (SQLite)', 15)
    ]

    for idx, (topic_key, topic_title, topic_id) in enumerate(topics_list):
        with st.expander(topic_title):
            # Update progress when the user interacts with the expander
            update_progress_intermediate(topic_key)
            # Display the topic content
            topics = fetch_intermediate_topic(topic_key)
            display_topics(topics)

            st.write(f"Your progress: {st.session_state.intermediate_progress}%")
            # Button to go to the flashcards page
            if st.button(f"Flashcard - Learn More", key=f"flashcard_button_{idx}"):
                st.session_state.selected_topic_id = topic_id
                go_to_page('flashcard_for_intermediate')


# Flashcard Page
def flashcard():
    st.title("Flashcards")
    
    # Get the selected topic_id from session state
    topic_id = st.session_state.get("selected_topic_id")
    flashcards = fetch_flashcards(topic_id)  # Fetch flashcards by topic_id

    # Check if there are any flashcards for the selected topic
    if not flashcards:
        st.write("No flashcards available for this topic.")
    else:
        # Ensure flashcard_index is within the valid range
        if 'flashcard_index' not in st.session_state or st.session_state.flashcard_index >= len(flashcards):
            st.session_state.flashcard_index = 0  # Start with the first flashcard
        if 'show_answer' not in st.session_state:
            st.session_state.show_answer = False  # Hide answer by default

        def show_flashcard():
            # Retrieve the current flashcard based on the index
            flashcard = flashcards[st.session_state.flashcard_index]
            st.write(f"**Term:** {flashcard[2]}")  # Term is in column 1 (index 2)
            if st.session_state.show_answer:
                st.write(f"**Definition:** {flashcard[3]}")  # Definition is in column 2 (index 3)

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Previous Flashcard"):
                st.session_state.flashcard_index = (st.session_state.flashcard_index - 1) % len(flashcards)
                st.session_state.show_answer = False  # Hide answer when moving

        with col2:
            if st.button("Show Answer"):
                st.session_state.show_answer = True  # Show the answer for the current flashcard

        with col3:
            if st.button("Next Flashcard"):
                st.session_state.flashcard_index = (st.session_state.flashcard_index + 1) % len(flashcards)
                st.session_state.show_answer = False  # Hide answer when moving

        show_flashcard()

        # Add a back button to return to the previous page
        if st.button("Back to Topics"):
            go_to_page('beginner_page')
            
def intermediate_flashcard():
    st.title("Flashcards")
    
    # Get the selected topic_id from session state
    topic_id = st.session_state.get("selected_topic_id")
    flashcards = fetch_inter_flashcards(topic_id)  # Fetch flashcards by topic_id

    # Check if there are any flashcards for the selected topic
    if not flashcards:
        st.write("No flashcards available for this topic.")
    else:
        # Ensure flashcard_index is within the valid range
        if 'flashcard_index' not in st.session_state or st.session_state.flashcard_index >= len(flashcards):
            st.session_state.flashcard_index = 0  # Start with the first flashcard
        if 'show_answer' not in st.session_state:
            st.session_state.show_answer = False  # Hide answer by default

        def show_flashcard():
            # Retrieve the current flashcard based on the index
            flashcard = flashcards[st.session_state.flashcard_index]
            st.write(f"**Term:** {flashcard[2]}")  # Term is in column 1 (index 2)
            if st.session_state.show_answer:
                st.write(f"**Definition:** {flashcard[3]}")  # Definition is in column 2 (index 3)

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Previous Flashcard"):
                st.session_state.flashcard_index = (st.session_state.flashcard_index - 1) % len(flashcards)
                st.session_state.show_answer = False  # Hide answer when moving

        with col2:
            if st.button("Show Answer"):
                st.session_state.show_answer = True  # Show the answer for the current flashcard

        with col3:
            if st.button("Next Flashcard"):
                st.session_state.flashcard_index = (st.session_state.flashcard_index + 1) % len(flashcards)
                st.session_state.show_answer = False  # Hide answer when moving

        show_flashcard()

        # Add a back button to return to the previous page
        if st.button("Back to Topics"):
            go_to_page('intermediate')

# Main function to control page flow
def main():
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'login_page'  # Default page

    # Display the current page based on session state
    if st.session_state.current_page == 'registration':
        registration_page()
    elif st.session_state.current_page == 'login_page':
        login_page()
    elif st.session_state.current_page == 'home':
        home_page()
    elif st.session_state.current_page == 'beginner_page':
        beginner_page()
    elif st.session_state.current_page == 'flashcard':
        flashcard()
    elif st.session_state.current_page == 'flashcard_for_intermediate':
        intermediate_flashcard()
    elif st.session_state.current_page == 'intermediate':
        intermediate_page()

# Run the app
if __name__ == "__main__":
    main()
