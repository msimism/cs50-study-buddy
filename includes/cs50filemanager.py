# includes/cs50filemanager.py

import os
import re
import requests
import zipfile
from bs4 import BeautifulSoup
from alive_progress import alive_bar

class CS50FileManager:
    def __init__(self, base_directory, debug_categories=None):
        self.base_directory = base_directory
        self.debug_categories = debug_categories or []

    def debug_print(self, category, message):
        if category in self.debug_categories:
            print(f"Debug ({category}): {message}")

    def sanitize_filename(self, name):
        # Replace spaces with underscores, convert to lowercase, and remove special characters
        name = re.sub(r'[^\w\s-]', '', name).replace(' ', '_').lower()
        # Truncate to a reasonable length
        return name[:50].strip()

    def get_course_folder_name(self, course):
        # Map course identifiers to folder names
        course_mapping = {
            "x": "cs50x",
            "python": "cs50p",
            "web": "cs50web",
            "ai": "cs50ai",
            "sql": "cs50sql",
            "scratch": "cs50scratch",
        }
        return course_mapping.get(course, course)

    def create_folders(self, course, weeks_data):
        """
        Creates the necessary folder structure.

        :param course: Name of the course
        :param weeks_data: Data for each week including lectures, shorts, and problem sets
        """
        # Determine the course folder name
        course_folder = self.get_course_folder_name(course)
        # Create base directory for the course
        course_dir = os.path.join(self.base_directory, course_folder)
        os.makedirs(course_dir, exist_ok=True)
        self.debug_print("data_saving", f"Created course folder: {course_dir}")

        for week, data in weeks_data.items():
            # Create week directory
            week_dir = os.path.join(course_dir, f"week-{week}")
            os.makedirs(week_dir, exist_ok=True)
            self.debug_print("data_saving", f"Created week folder: {week_dir}")

            # Create Lecture directory
            lecture_dir = os.path.join(week_dir, "lecture")
            os.makedirs(lecture_dir, exist_ok=True)
            self.debug_print("data_saving", f"Created lecture folder: {lecture_dir}")

            # Create Shorts directory
            shorts_dir = os.path.join(week_dir, "shorts")
            os.makedirs(shorts_dir, exist_ok=True)
            self.debug_print("data_saving", f"Created shorts folder: {shorts_dir}")

            # Create problem set directory for the week
            pset_dir = os.path.join(week_dir, f"pset-{week}")
            os.makedirs(pset_dir, exist_ok=True)
            self.debug_print("data_saving", f"Created problem set folder: {pset_dir}")

            # Create directories for each problem set inside the pset directory
            for pset in data['problem_sets']:
                problem_dir = os.path.join(pset_dir, self.sanitize_filename(pset['title']))
                os.makedirs(problem_dir, exist_ok=True)
                self.debug_print("data_saving", f"Created problem set sub-folder: {problem_dir}")

    def save_data(self, course, weeks_data, cs50_instance, download_audio=False, download_video=False, download_code=True):
        """
        Saves the scraped data into the corresponding folders and downloads relevant files.

        :param course: Name of the course
        :param weeks_data: Data for each week including lectures, shorts, and problem sets
        :param cs50_instance: Instance of CS50 class
        :param download_audio: Boolean flag to download audio files
        :param download_video: Boolean flag to download video files
        :param download_code: Boolean flag to download code files (defaults to True)
        """
        # Determine the course folder name
        course_folder = self.get_course_folder_name(course)
        # Define paths based on the folder structure
        course_dir = os.path.join(self.base_directory, course_folder)

        for week, data in weeks_data.items():
            week_dir = os.path.join(course_dir, f"week-{week}")

            # Save lectures data
            lecture_dir = os.path.join(week_dir, "lecture")
            with open(os.path.join(lecture_dir, "lectures.txt"), "w") as file:
                file.write(data['lectures'])
            self.debug_print("data_saving", f"Saved lectures to {os.path.join(lecture_dir, 'lectures.txt')}")

            # Save shorts data
            shorts_dir = os.path.join(week_dir, "shorts")
            with open(os.path.join(shorts_dir, "shorts.txt"), "w") as file:
                file.write(data['shorts'])
            self.debug_print("data_saving", f"Saved shorts to {os.path.join(shorts_dir, 'shorts.txt')}")

            # Download relevant files if flags are set
            media_links = cs50_instance.get_media_links(data['lectures'], download_audio, download_video, download_code)
            self.download_relevant_files(media_links, lecture_dir, week)

            # Save problem sets data
            pset_dir = os.path.join(week_dir, f"pset-{week}")
            for pset in data['problem_sets']:
                if 'data' in pset:
                    problem_dir = os.path.join(pset_dir, self.sanitize_filename(pset['title']))
                    readme_path = os.path.join(problem_dir, "README.md")  # Change extension to .md
                    with open(readme_path, "w") as file:
                        file.write(self.format_problem_set(pset['title'], pset['data']))
                    self.debug_print("data_saving", f"Saved problem set to {readme_path}")

                    # Download problem set files
                    media_links = cs50_instance.get_media_links(pset['data'], download_audio, download_video, download_code)
                    self.download_relevant_files(media_links, problem_dir, week)

    def download_relevant_files(self, media_links, directory, week):
        """
        Downloads relevant files based on the flags provided.

        :param media_links: Dictionary of media links to download
        :param directory: The directory to save the files
        :param week: The week number for naming files
        """
        os.makedirs(directory, exist_ok=True)

        # Download audio files
        for mp3_link in media_links['audio']:
            mp3_url = requests.compat.urljoin(self.base_directory, mp3_link)
            self.download_file(mp3_url, os.path.join(directory, f"week-{week}-lecture.mp3"))

        # Download video files (720p)
        for video_link in media_links['video']:
            video_url = requests.compat.urljoin(self.base_directory, video_link)
            self.download_file(video_url, os.path.join(directory, f"week-{week}-lecture.mp4"))

        # Download code files and extract
        example_code_dir = os.path.join(directory, "example_code")
        os.makedirs(example_code_dir, exist_ok=True)
        for zip_link in media_links['code']:
            zip_url = requests.compat.urljoin(self.base_directory, zip_link)
            zip_path = os.path.join(directory, f"week-{week}-example_code.zip")
            self.download_file(zip_url, zip_path)
            self.extract_zip(zip_path, example_code_dir)

        # Download PDF files
        for pdf_link in media_links['pdf']:
            pdf_url = requests.compat.urljoin(self.base_directory, pdf_link)
            self.download_file(pdf_url, os.path.join(directory, f"week-{week}-lecture.pdf"))

    def download_file(self, file_url, file_name):
        self.debug_print("file_download", f"Downloading {file_url} to {file_name}")
        response = requests.get(file_url)
        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(response.content)
            self.debug_print("file_download", f"{file_name} downloaded")
        else:
            self.debug_print("file_download", f"Failed to download {file_url}, status code: {response.status_code}")

    def extract_zip(self, zip_path, extract_to):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                filename = os.path.basename(member)
                # Skip directories and empty file names
                if not filename:
                    continue
                source = zip_ref.open(member)
                target = open(os.path.join(extract_to, filename), "wb")
                with source, target:
                    target.write(source.read())
        self.debug_print("file_download", f"{zip_path} extracted to {extract_to}")
        os.remove(zip_path)
        self.debug_print("file_download", f"{zip_path} deleted after extraction")

    def format_problem_set(self, title, content):
        """
        Formats the problem set content into a nicely formatted Markdown file.

        :param title: The title of the problem set
        :param content: The content of the problem set
        :return: Formatted Markdown content
        """
        formatted_content = f"# {title}\n\n"
        formatted_content += "## Problem Description\n\n"
        formatted_content += content
        formatted_content += "\n\n"
        formatted_content += "## Submission Instructions\n\n"
        formatted_content += "- Follow the instructions provided in the problem set.\n"
        formatted_content += "- Ensure your code is well-documented and tested.\n"
        formatted_content += "- Submit your solution via the appropriate submission portal.\n"

        return formatted_content
