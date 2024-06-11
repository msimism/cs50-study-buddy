import os
import re
 
class CS50FileManager:
    def __init__(self, base_directory):
        self.base_directory = base_directory
 
    def sanitize_filename(self, name):
        # Replace spaces with underscores, convert to lowercase, and remove special characters
        name = re.sub(r'[^\w\s-]', '', name).replace(' ', '_').lower()
        # Truncate to a reasonable length
        return name[:50].strip()
 
    def create_folders(self, course, weeks_data):
        """
        Creates the necessary folder structure.
 
        :param course: Name of the course
        :param weeks_data: Data for each week including lectures, shorts, and problem sets
        """
        # Create base directory for the course
        course_dir = os.path.join(self.base_directory, course)
        os.makedirs(course_dir, exist_ok=True)
 
        for week, data in weeks_data.items():
            # Create week directory
            week_dir = os.path.join(course_dir, f"week-{week}")
            os.makedirs(week_dir, exist_ok=True)
 
            # Create Lecture directory
            lecture_dir = os.path.join(week_dir, "lecture")
            os.makedirs(lecture_dir, exist_ok=True)
 
            # Create Shorts directory
            shorts_dir = os.path.join(week_dir, "shorts")
            os.makedirs(shorts_dir, exist_ok=True)
 
            # Create a single pset directory for the week
            pset_dir = os.path.join(week_dir, "pset")
            os.makedirs(pset_dir, exist_ok=True)
 
            # Create directories for each problem set inside the pset directory
            for pset in data['problem_sets']:
                problem_dir = os.path.join(pset_dir, self.sanitize_filename(pset['title']))
                os.makedirs(problem_dir, exist_ok=True)
 
    def save_data(self, course, weeks_data):
        """
        Saves the scraped data into the corresponding folders.
 
        :param course: Name of the course
        :param weeks_data: Data for each week including lectures, shorts, and problem sets
        """
        # Define paths based on the folder structure
        course_dir = os.path.join(self.base_directory, course)
 
        for week, data in weeks_data.items():
            week_dir = os.path.join(course_dir, f"week-{week}")
 
            # Save lectures data
            lecture_dir = os.path.join(week_dir, "lecture")
            with open(os.path.join(lecture_dir, "lectures.txt"), "w", encoding='utf-8') as file:
                file.write(data['lectures'])
 
            # Save shorts data
            shorts_dir = os.path.join(week_dir, "shorts")
            with open(os.path.join(shorts_dir, "shorts.txt"), "w", encoding='utf-8') as file:
                file.write(data['shorts'])
 
            # Save problem sets data
            pset_dir = os.path.join(week_dir, "pset")
            for pset in data['problem_sets']:
                problem_dir = os.path.join(pset_dir, self.sanitize_filename(pset['title']))
                readme_path = os.path.join(problem_dir, "README.txt")
                with open(readme_path, "w", encoding='utf-8') as file:
                    file.write(pset['data'])
 
# Usage Example:
# fm = CS50FileManager(base_directory="/path/to/save")
# fm.create_folders(course="python", weeks_data=weeks_data)
# fm.save_data(course="python", weeks_data=weeks_data)