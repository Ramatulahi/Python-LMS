from peewee import *
import sqlite3

# Initialize the database
database = SqliteDatabase('management3.db')

# Define the base model for shared database settings
class BaseModel(Model):
    class Meta:
        database = database

# User model (stores user information)
class User(BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()  # Store plaintext password

# Topic model (stores the learning topics)
class Topic(BaseModel):
    name = CharField(unique=True)
    description = CharField()
    external_link = CharField(null=True)
    level = CharField(null = True)
    topic = CharField(null = True)
    task_done = BooleanField(default=False)
    
class intermediate(BaseModel):
    name = CharField(unique=True)
    description = CharField()
    external_link = CharField(null=True)
    level = CharField(null = True)
    topic = CharField(null = True)
    task_done = BooleanField(default=False)
    
    

# UserTopicProgress model (stores user progress on each topic)
class UserTopicProgress(BaseModel):
    user = ForeignKeyField(User, backref='topic_progress')
    topic = ForeignKeyField(Topic, backref='user_progress')
    completed = BooleanField(default=False)

# Flashcard model (stores flashcards related to topics)
class Flashcard(BaseModel):
    topic = ForeignKeyField(Topic, backref='flashcards')
    term = CharField()
    definition = TextField()

# Note model (stores notes for users on topics)
class Note(BaseModel):
    topic = ForeignKeyField(Topic, backref='notes')
    content = TextField()
    user = ForeignKeyField(User, backref='user_notes')

# Initialize the database and create tables
def init_db():
    database.connect()
    database.create_tables([User, Topic, UserTopicProgress, Flashcard, Note], safe=True)
    database.close()

# Register a new user
def register(username, email, password):
    try:
        # Check if username or email already exists
        User.get((User.username == username) | (User.email == email))
        return "Username or email already exists."
    except User.DoesNotExist:
        # Create user with plaintext password
        user = User.create(username=username, email=email, password=password)
        user.save()
        return f"User {username} registered successfully."

# Login function (directly compares plaintext passwords)
def login(username_or_email, password):
    try:
        user = User.get((User.username == username_or_email) | (User.email == username_or_email))
        
        # Check if the password matches
        if user.password == password:
            return f"Login successful for {user.username}"
        else:
            return "Invalid password"
    except User.DoesNotExist:
        return "User not found"

# Fetch all topics
def fetch_topics_by_topic(parent_topic):
    return Topic.select().where(Topic.topic == parent_topic).dicts()

def fetch_intermediate_topic(parent_topic):
    return intermediate.select().where(intermediate.topic==parent_topic).dicts()

# Update task status
def update_task_status(topic_id, task_done):
    task = Topic.get(Topic.id == topic_id)
    task.task_done = task_done
    task.save()
    return f"Task '{task.name}' marked as {'done' if task_done else 'not done'}."

def fetch_flashcards(topic_id=None):
    conn = sqlite3.connect('management3.db')
    cursor = conn.cursor()
    
    # Fetch flashcards for the specific topic_id
    if topic_id:
        cursor.execute('SELECT * FROM flashcard WHERE topic_id = ?', (topic_id,))
    else:
        cursor.execute('SELECT * FROM flashcard')
        
    flashcards = cursor.fetchall()
    conn.close()
    return flashcards

def fetch_inter_flashcards(topic_id = None):
    conn = sqlite3.connect('management3.db')
    cursor = conn.cursor()
    
    # Fetch flashcards for the specific topic_id
    if topic_id:
        cursor.execute('SELECT * FROM intermid_flashcards WHERE topic_id = ?', (topic_id,))
    else:
        cursor.execute('SELECT * FROM intermid_flashcards')
        
    flashcards = cursor.fetchall()
    conn.close()
    return flashcards
    
# Example Usage
if __name__ == "__main__":
    init_db()  # Initialize database and create tables
    #input_topic()
    
    # Example: Register a user
    print(register("testuser", "test@example.com", "securepassword"))

    # Example: Try to login with correct credentials
    print(login("testuser", "securepassword"))

    
