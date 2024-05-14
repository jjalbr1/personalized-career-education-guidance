from ResumeModel import Resume
from resume_parser import ResumeParser

class MyResumeParser:
    def __init__(self, file_path):
        # Initialize the MyResumeParser object with the provided file path
        self.file_path = file_path
        # Create an instance of the ResumeModel class to store parsed resume data
        self.resume = Resume()
        # Extract resume data
        self.data = self.extract_data_using_resumeparse()

    def extract_data_using_resumeparse(self):
        # Use ResumeParser class to extract resume data and return the parsed data
        return ResumeParser(self.file_path).parse()

    # Parse the extracted data and populate the Resume object
    def parse(self):
        if self.data.skills:
            self.resume.add_skills(self.data.skills)
        if self.data.experience:
            self.resume.add_experience('\n'.join(self.data.experience))
        if self.data.education:
            self.resume.add_education('\n'.join(self.data.education))
        if self.data.achievements:
            self.resume.add_achievements('\n'.join(self.data.achievements))
        if hasattr(self.data, 'first_name'):
            self.resume.first_name = self.data.first_name
        if hasattr(self.data, 'last_name'):
            self.resume.last_name = self.data.last_name
        if hasattr(self.data, 'gpa'):
            self.resume.gpa = self.data.gpa

        return self.resume
    
#file_path = 'Basic_Resume.docx'
#parser = MyResumeParser(file_path)
#parsed_resume = parser.parse()

# Print the parsed resume
#print(parsed_resume)
