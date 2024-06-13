# includes/cs50interface.py

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
            "Debug": False,
            "Debug Categories": [],
        }

    def display_menu(self):
        while True:
            main_menu = [
                inquirer.List(
                    'action',
                    message="Select an action",
                    choices=['Select courses', 'Exit'],
                ),
            ]

            answers = inquirer.prompt(main_menu)
            action = answers['action']

            if action == 'Select courses':
                self.select_courses()
            elif action == 'Exit':
                break

    def select_courses(self):
        while True:
            dynamic_choices = self.get_course_choices()
            course_question = [
                inquirer.Checkbox(
                    'selected_courses',
                    message="Please select which CS50* course you're studying!",
                    choices=dynamic_choices,
                ),
                inquirer.List(
                    'action',
                    message="Continue or go back?",
                    choices=['Continue', 'Back'],
                ),
            ]
            course_answers = inquirer.prompt(course_question)

            if course_answers['action'] == 'Back':
                return

            self.selected_courses = [self.course_manager.get_course_key_from_choice(choice) for choice in course_answers['selected_courses']]
            pprint({'selected_courses': self.selected_courses})

            if course_answers['action'] == 'Continue':
                self.select_options()
                break

    def select_options(self):
        while True:
            settings_questions = [
                inquirer.Checkbox(
                    'settings',
                    message="Select settings to enable",
                    choices=[
                        'Download lecture audio',
                        'Download lecture videos',
                        'Download example code',
                        'Set root directory of courses',
                        'Enable debugging',
                    ],
                ),
                inquirer.List(
                    'action',
                    message="Continue or go back?",
                    choices=['Continue', 'Back'],
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
                if 'debugging' in setting.lower():
                    self.program_settings['Debug'] = True
                    debug_categories_question = [
                        inquirer.Checkbox(
                            'debug_categories',
                            message="Select debug categories to enable",
                            choices=[
                                'scraping',
                                'problem_sets',
                                'media_links',
                                'folder_creation',
                                'file_download',
                                'data_saving',
                            ],
                        ),
                    ]
                    debug_categories_answer = inquirer.prompt(debug_categories_question)
                    self.program_settings['Debug Categories'] = debug_categories_answer['debug_categories']

            if answers['action'] == 'Back':
                self.select_courses()
                return
            elif answers['action'] == 'Continue':
                pprint(self.program_settings)
                self.run_course_aide()
                break

    def get_course_choices(self):
        return self.course_manager.get_course_choices()

    def run_course_aide(self):
        if not self.selected_courses:
            print("No courses selected. Please select courses first.")
            return

        print(f"Running course aide for {', '.join(self.selected_courses)}...")
        print(f"Download audio: {self.program_settings['Audio']}")
        print(f"Download video: {self.program_settings['Video']}")
        print(f"Download code: {self.program_settings['Code']}")
        print(f"Destination folder: {self.program_settings['Course Folder']}")
        print(f"Debugging: {self.program_settings['Debug']}")
        print(f"Debug Categories: {', '.join(self.program_settings['Debug Categories'])}")

        for course in self.selected_courses:
            # Instantiate the CS50Scraper and run it with the selected options
            scraper = CS50Scraper(course, self.program_settings['Course Folder'], self.program_settings['Debug Categories'])
            
            # Scrape course data and save it using the file manager
            scraper.scrape_course(
                download_audio=self.program_settings['Audio'],
                download_video=self.program_settings['Video'],
                download_code=self.program_settings['Code']
            )

            print(f"Completed running aide for {course}")

# Assuming the course_manager is already defined somewhere
# interface = Interface(course_manager)
# interface.display_menu()
