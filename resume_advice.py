import openai
import hashlib
import os
import hashlib
import os
import time
from docx import Document  # Import the Document class for working with .docx files
 
# Get OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_SECRET_KEY")
print("OpenAI API Key:", openai_api_key)

# Set OpenAI API key
openai.api_key = openai_api_key

# Function to read a file and return its content as plain text
def read_file(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()  # Get the file extension

    if file_extension == ".docx":
        # Handle .docx file using the python-docx library
        document = Document(file_path)
        resume_text = []
        for paragraph in document.paragraphs:
            resume_text.append(paragraph.text)
        return "\n".join(resume_text)
    elif file_extension == ".txt":
        # Handle plain text file
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print(f"File not found at path: {file_path}")
            exit()
    else:
        print("Unsupported file format. Please provide a .docx or .txt file.")
        exit()

# Define a function to generate a hash for the resume content
def generate_resume_hash(resume_content):
    return hashlib.sha256(resume_content.encode()).hexdigest()

# Define a function to truncate resume content
def truncate_resume_content(resume_content_str, max_tokens=16000):
    # Truncate the content to approximately max_tokens characters
    return resume_content_str[:max_tokens]

# Function to make API requests with backoff strategy using OpenAI chat completion endpoint
def make_api_request_with_backoff(messages):
    delay = 1  # Initial delay (in seconds)
    max_delay = 32  # Maximum delay (in seconds)

    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            return response.choices[0].message.content.strip()
        except openai.error.RateLimitError as e:
            print(f"Rate limit error occurred, retrying in {delay} seconds...")
            time.sleep(delay)
            delay = min(delay * 2, max_delay)
        except openai.error.InvalidRequestError as e:
            print(f"Invalid request error: {e}")
            exit()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            exit()

# Get the path to the resume file from the user
resume_path = input("Enter the path to your resume file (.docx or .txt): ")

# Read the content of the resume file
resume_content_str = read_file(resume_path)

# Generate a hash for the resume content
resume_hash = generate_resume_hash(resume_content_str)

# Define the system prompt for the Chat API
system_prompt = (
    "You are a career advisor reviewing the provided resume. "
    "Based on the resume, give specific advice on the following questions: "
    "1. What should the user's next role be based on their experience, skills, and interests? "
    "2. What skills or gaps does the user have that they can address to be more competitive when applying for the next role? "
    "Please provide detailed recommendations and specific guidance."
)

# Prepare the messages for the Chat API
truncated_resume_content = truncate_resume_content(resume_content_str)
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": truncated_resume_content}
]

# Make the API request with backoff strategy
advice = make_api_request_with_backoff(messages)

# Display the advice to the user
print("AI-Generated Advice:")
print(advice)

import time
from docx import Document  # Import the Document class for working with .docx files

# Set OpenAI API key securely
openai.api_key = "sk-proj-fgPjhtpbpZ0vOSbiv8GyT3BlbkFJAMMqFwrshOX7pMGGPAkR"

# Function to read a file and return its content as plain text
def read_file(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()  # Get the file extension

    if file_extension == ".docx":
        # Handle .docx file using the python-docx library
        document = Document(file_path)
        resume_text = []
        for paragraph in document.paragraphs:
            resume_text.append(paragraph.text)
        return "\n".join(resume_text)
    elif file_extension == ".txt":
        # Handle plain text file
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print(f"File not found at path: {file_path}")
            exit()
    else:
        print("Unsupported file format. Please provide a .docx or .txt file.")
        exit()

# Define a function to generate a hash for the resume content
def generate_resume_hash(resume_content):
    return hashlib.sha256(resume_content.encode()).hexdigest()

# Define a function to truncate resume content
def truncate_resume_content(resume_content_str, max_tokens=16000):
    # Truncate the content to approximately max_tokens characters
    return resume_content_str[:max_tokens]

# Function to make API requests with backoff strategy using OpenAI chat completion endpoint
def make_api_request_with_backoff(messages):
    delay = 1  # Initial delay (in seconds)
    max_delay = 32  # Maximum delay (in seconds)

    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            return response.choices[0].message.content.strip()
        except openai.error.RateLimitError as e:
            print(f"Rate limit error occurred, retrying in {delay} seconds...")
            time.sleep(delay)
            delay = min(delay * 2, max_delay)
        except openai.error.InvalidRequestError as e:
            print(f"Invalid request error: {e}")
            exit()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            exit()

# Get the path to the resume file from the user
resume_path = input("Enter the path to your resume file (.docx or .txt): ")

# Read the content of the resume file
resume_content_str = read_file(resume_path)

# Generate a hash for the resume content
resume_hash = generate_resume_hash(resume_content_str)

# Define the system prompt for the Chat API
system_prompt = (
    "You are a career advisor reviewing the provided resume. "
    "Based on the resume, give specific advice on the following questions: "
    "1. What should the user's next role be based on their experience, skills, and interests? "
    "2. What skills or gaps does the user have that they can address to be more competitive when applying for the next role? "
    "Please provide detailed recommendations and specific guidance."
)

# Prepare the messages for the Chat API
truncated_resume_content = truncate_resume_content(resume_content_str)
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": truncated_resume_content}
]

# Make the API request with backoff strategy
advice = make_api_request_with_backoff(messages)

# Display the advice to the user
print("AI-Generated Advice:")
print(advice)
