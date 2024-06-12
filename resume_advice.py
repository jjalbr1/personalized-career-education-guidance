import openai
import hashlib
import os
import sys
import time
from docx import Document  # Import the Document class for working with .docx files

# Get OpenAI API key from environment variable
#todo uncomment this line
openai_api_key = os.getenv('OPENAI_API_KEY')


if not openai_api_key:
    print("Error: OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    sys.exit(1)

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
            sys.exit(1)
    else:
        print("Unsupported file format. Please provide a .docx or .txt file.")
        sys.exit(1)

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
        except openai.error.RateLimitError:
            print(f"Rate limit error occurred, retrying in {delay} seconds...")
            time.sleep(delay)
            delay = min(delay * 2, max_delay)
        except openai.error.InvalidRequestError as e:
            print(f"Invalid request error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)

def get_recommendation(resume_content, prompt):
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": resume_content}
    ]
    return make_api_request_with_backoff(messages)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python resume_advice.py <resume_path> <action>")
        sys.exit(1)
    
    resume_path = sys.argv[1]
    action = sys.argv[2]
    resume_content_str = read_file(resume_path)
    resume_content_str = truncate_resume_content(resume_content_str)

    if action == "salary":
        prompt = "Based on the provided resume, give a salary expectation for the next potential role. Provide in the format of 'Salary range: xxx - xxx'."
        result = get_recommendation(resume_content_str, prompt)
    elif action == "role":
        prompt = "Based on the provided resume, what should the user's next role be? Provide a description with a 'Next Role' header. Include the role title as a header with a three sentence description."
        result = get_recommendation(resume_content_str, prompt)
    elif action == "skills":
        prompt = "Identify three technical skills that the user does not have on their resume but would benefit them in their career. Provide a description two sentence description of these skills."
        result = get_recommendation(resume_content_str, prompt)
    elif action == "future":
        prompt = "Based on the provided resume, list some 3 job titles or roles that the user could aspire to achieve within the next 5 years. Put data in the format of 'X years: Title, Description'"
        result = get_recommendation(resume_content_str, prompt)
    elif action == "similar-roles":
        prompt = "Based on the provided resume, suggest three potential jobs that are similar to the user's current role. Provide each suggestion with a job title and a two-sentence description."
        result = get_recommendation(resume_content_str, prompt)
    elif action == "interview-prep":
        prompt = "Based on the provided resume, provide common interview questions and tips for preparing for job interviews."
        result = get_recommendation(resume_content_str, prompt)
    elif action == "certifications":
        prompt = "Based on the provided resume, suggest professional certifications that could benefit the user's career. Provide a brief description of each certification."
        result = get_recommendation(resume_content_str, prompt)
    elif action == "further-education":
        prompt = "Based on the provided resume, recommend further education options that could benefit the user's career. Provide a brief description of each option."
        result = get_recommendation(resume_content_str, prompt)
    else:
        prompt = "Provide general career advice based on the user's resume."
        result = get_recommendation(resume_content_str, prompt)
    
    print(result)

