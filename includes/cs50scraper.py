# includes/cs50scraper.py
from includes.cs50 import CS50
from includes.cs50filemanager import CS50FileManager
from alive_progress import alive_bar
import os

class CS50Scraper:
    def __init__(self, course, base_directory, debug_categories=None):
        self.cs50 = CS50(course)
        self.file_manager = CS50FileManager(base_directory, debug_categories)
        self.debug_categories = debug_categories or []

    def debug_print(self, category, message):
        if category in self.debug_categories:
            print(f"Debug ({category}): {message}")

    def scrape_course(self, download_audio=False, download_video=False, download_code=True):
        week = 0
        weeks_data = {}
        total_weeks = 10

        with alive_bar(total_weeks, title="Scraping course data") as bar:
            while True:
                doc = self.cs50.scrape_page(week)
                if doc is None:
                    break

                self.debug_print("scraping", f"Scraped week {week}")

                lectures = self.cs50.get_title() + "\n" + self.cs50.get_description() + "\n" + self.cs50.get_week_tags() + "\n" + self.cs50.get_shorts()
                self.debug_print("scraping", f"Lectures: {lectures}")

                pset_doc = self.cs50.scrape_problem_set_page(week)
                problem_sets = []
                if pset_doc:
                    problem_sets = self.cs50.get_problem_set_lists()
                    for pset in problem_sets:
                        problems = self.cs50.get_problem_set([pset], week)
                        pset['data'] = "\n\n".join([content for title, content in problems.items()])  # Ensure 'data' key exists

                weeks_data[week] = {
                    'lectures': lectures,
                    'shorts': self.cs50.get_shorts(),
                    'problem_sets': problem_sets
                }

                media_links = self.cs50.get_media_links(str(doc), download_audio, download_video, download_code)
                self.debug_print("media_links", f"Extracted Media Links: {media_links}")

                course_folder = self.file_manager.get_course_folder_name(self.cs50.course)
                self.file_manager.download_relevant_files(media_links, os.path.join(self.file_manager.base_directory, course_folder, f"week-{week}", "lecture"), week)

                week = self.cs50.progress(week)
                bar()

        course_folder = self.file_manager.get_course_folder_name(self.cs50.course)
        self.file_manager.create_folders(course_folder, weeks_data)
        self.file_manager.save_data(course_folder, weeks_data, self.cs50, download_audio=download_audio, download_video=download_video, download_code=download_code)
