class Resume:
    def __init__(self, first_name=None, last_name=None, skills=None, experience=None, education=None, achievements=None, gpa=None):
        self.first_name = first_name
        self.last_name = last_name
        self.skills = skills or []
        self.experience = experience or []
        self.education = education or []
        self.achievements = achievements or []
        self.gpa = gpa

    def add_skills(self, skills):
        self.skills.extend(skills)

    def add_experience(self, experience):
        self.experience.append(experience)

    def add_education(self, education):
        self.education.append(education)

    def add_achievements(self, achievements):
        self.achievements.append(achievements)

    def __str__(self):
        return (f"Name: {self.first_name} {self.last_name}\n"
                f"Skills: {self.skills}\n"
                f"Experience: {self.experience}\n"
                f"Education: {self.education}\n"
                f"Achievements: {self.achievements}\n"
                f"GPA: {self.gpa}")




