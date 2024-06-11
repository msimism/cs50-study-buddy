import inquirer
from pprint import pprint
from includes.cs50scraper import CS50Scraper  # Import CS50Scraper from the new module
from includes.cs50filemanager import CS50FileManager

class Interface:
    def __init__(self, course_manager):
        self.course_manager = course_manager
        self.selected_courses = []
        self.program_settings = {
            "Audio": False,
            "Video": False,
            "Code": False,
            "Course Folder": "saved",
        }

    def display_menu(self):
        while True:
            questions = [
                inquirer.List(
                    'action',
                    message="Select an action",
                    choices=['Select courses', 'Run course aide', 'Settings', 'Exit'],
                ),
            ]

            answers = inquirer.prompt(questions)
            action = answers['action']

            if action == 'Select courses':
                self.select_courses()
            elif action == 'Run course aide':
                self.run_course_aide()
            elif action == 'Settings':
                self.settings()
            elif action == 'Exit':
                break

    def select_courses(self):
        # Retrieve dynamic choices for courses
        dynamic_choices = self.get_course_choices()
        course_question = [
            inquirer.Checkbox(
                'selected_courses',
                message="Please select which CS50* course you're studying!",
                choices=dynamic_choices,
            ),
        ]
        course_answers = inquirer.prompt(course_question)
        
        # Extract only the course keys
        self.selected_courses = [self.course_manager.get_course_key_from_choice(choice) for choice in course_answers['selected_courses']]
        pprint({'selected_courses': self.selected_courses})

    def get_course_choices(self):
        return self.course_manager.get_course_choices()

    def settings(self):
        settings_questions = [
            inquirer.Checkbox(
                'settings',
                message="Select settings to enable",
                choices=[
                    'Download lecture audio',
                    'Download lecture videos',
                    'Download example code',
                    'Set root directory of courses',
                ],
            ),
        ]
        answers = inquirer.prompt(settings_questions)
        for setting in answers['settings']:
            if 'audio' in setting.lower():
                self.program_settings['Audio'] = True
            if 'video' in setting.lower():
                self.program_settings['Video'] = True
            if 'code' in setting.lower():
                self.program_settings['Code'] = True
            if 'directory' in setting.lower():
                directory_question = [
                    inquirer.Text('directory', message="Enter root directory of courses")
                ]
                directory_answer = inquirer.prompt(directory_question)
                self.program_settings['Course Folder'] = directory_answer['directory']
        pprint(self.program_settings)

    def run_course_aide(self):
        if not self.selected_courses:
            print("No courses selected. Please select courses first.")
            return

        for course in self.selected_courses:
            print(f"Running course aide for {course}...")
            print(f"Download audio: {self.program_settings['Audio']}")
            print(f"Download video: {self.program_settings['Video']}")
            print(f"Download code: {self.program_settings['Code']}")
            print(f"Destination folder: {self.program_settings['Course Folder']}")

            # Instantiate the CS50Scraper and run it with the selected options
            scraper = CS50Scraper(course, self.program_settings['Course Folder'])
            
            # Scrape course data and save it using the file manager
            scraper.scrape_course()
            # Here you can implement logic to handle downloading audio, video, and code if needed

            print(f"Completed running aide for {course}")

# Assuming the course_manager is already defined somewhere
# interface = Interface(course_manager)
# interface.display_menu()
