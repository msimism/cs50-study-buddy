from bs4 import BeautifulSoup
import requests
import urllib.parse

class CS50:
    def __init__(self, course=None):
        self.course_urls = {
            "x": "https://cs50.harvard.edu/x/2024/weeks/",
            "python": "https://cs50.harvard.edu/python/2022/weeks/",
            "web": "https://cs50.harvard.edu/web/2020/weeks/",
            "ai": "https://cs50.harvard.edu/ai/2024/weeks/",
            "sql": "https://cs50.harvard.edu/sql/2024/weeks/",
            "scratch": "https://cs50.harvard.edu/scratch/2024/weeks/",
            # Add more courses as needed
        }

        self.problem_set_urls = {
            "x": "https://cs50.harvard.edu/x/2024/psets/",
            "python": "https://cs50.harvard.edu/python/2022/psets/",
            "web": "https://cs50.harvard.edu/web/2020/projects/",
            "ai": "https://cs50.harvard.edu/ai/2024/projects/",
            "sql": "https://cs50.harvard.edu/sql/2024/psets/",
            "scratch": "https://cs50.harvard.edu/scratch/2024/projects/",
            # Add more courses as needed
        }

        self.course_information = {
            "x": {"name": "CS50x", "description": "Harvard University's introduction to the intellectual enterprises of computer science and the art of programming."},
            "python": {"name": "CS50 Python", "description": "An introduction to programming using Python, a popular language for general-purpose programming, data analysis, and web development."},
            "web": {"name": "CS50 Web", "description": "Learn how to build and deploy web applications with Python and JavaScript."},
            "ai": {"name": "CS50 A.I", "description": "An introduction to the concepts and algorithms at the foundation of modern artificial intelligence, with a focus on implementing AI techniques in Python."},
            "sql": {"name": "CS50 SQL", "description": "A comprehensive introduction to database management and SQL, the standard language for interacting with databases."},
            "scratch": {"name": "CS50 Scratch", "description": "An introduction to programming using Scratch, a visual programming language."},
            # Add more courses as needed
        }

        self.course = course
        if course:
            self.base_url = self.course_urls.get(course)
            self.pset_url = self.problem_set_urls.get(course)

            if self.base_url is None or self.pset_url is None:
                raise ValueError(f"Unknown course: {course}")

    def get_course_choices(self):
        choices = []
        for key, info in self.course_information.items():
            choices.append(f"{info['name']}: {info['description']}")
        return choices

    def get_course_key_from_choice(self, choice):
        for key, info in self.course_information.items():
            if choice.startswith(info['name']):
                return key
        return None

    def scrape_page(self, week):
        url = self.base_url + str(week) + "/"
        result = requests.get(url)
        if result.status_code == 404:
            return None
        self.doc = BeautifulSoup(result.text, "html.parser")
        self.col = self.doc.find('main', class_='col-lg')
        return self.doc

    def scrape_problem_set_page(self, week):
        url = self.pset_url + str(week) + "/"
        result = requests.get(url)
        if result.status_code == 404:
            return None
        self.pset_doc = BeautifulSoup(result.text, "html.parser")
        self.pset_col = self.pset_doc.find('main', class_='col-lg')
        return self.pset_doc

    def progress(self, week):
        week += 1
        return week

    def get_title(self):
        self.meta_tag = self.doc.find('meta', property='og:title')
        self.title = self.meta_tag['content'] if self.meta_tag else 'No title found'
        return f"Title: {self.title}"

    def get_description(self):
        self.meta_tag = self.doc.find('meta', property='og:description')
        self.description = self.meta_tag['content'] if self.meta_tag else 'No description found'
        return f"Desc: {self.description}"

    def get_week_tags(self):
        self.h1_text = self.col.find('h1').get_text() if self.col.find('h1') else 'No h1 found'
        self.tags_text = self.col.find('p').get_text() if self.col.find('p') else 'No tags found'
        return f"Tags: {self.tags_text}"

    def get_shorts(self):
        self.shorts_string = self.doc.find(string="Shorts")
        if self.shorts_string:
            self.ordered_list = self.shorts_string.find_next('ol')
            self.links = self.ordered_list.find_all('a') if self.ordered_list else []
            self.video_titles = [self.link.text for self.link in self.links]
            return(f"Short Videos: {self.video_titles}")
        else:
            return("No shorts found")

    def get_problem_set_lists(self):
        if self.pset_col:
            problem_sets = []

            if self.course == 'python':
                self.main_content = self.pset_col.find('ul')
                if self.main_content:
                    for item in self.main_content.find_all('li'):
                        link = item.find('a')
                        title = item.text.strip()
                        url = link['href'] if link else 'No URL'
                        problem_sets.append({'title': title, 'url': url})
                else:
                    return "No problem sets found"

            elif self.course == 'x':
                self.main_content = self.pset_col.find('ul')
                if self.main_content:
                    for item in self.main_content.find_all('li'):
                        link = item.find('a')
                        title = item.text.strip()
                        url = link['href'] if link else 'No URL'
                        problem_sets.append({'title': title, 'url': url})
                else:
                    return "No problem sets found"

            elif self.course in ['web', 'ai', 'scratch']:
                self.main_content = self.pset_col.find('ul')
                if self.main_content:
                    for item in self.main_content.find_all('li'):
                        link = item.find('a')
                        title = item.text.strip()
                        url = link['href'] if link else 'No URL'
                        problem_sets.append({'title': title, 'url': url})
                else:
                    return "No projects found"

            else:
                self.main_content = self.pset_col.find('ul')
                if self.main_content:
                    for item in self.main_content.find_all('li'):
                        link = item.find('a')
                        title = item.text.strip()
                        url = link['href'] if link else 'No URL'
                        problem_sets.append({'title': title, 'url': url})
                else:
                    return "No problem sets found"

            return problem_sets
        else:
            return "No problem set column found"

    def get_problem_set(self, problem_sets, week):
        data = {}
        for problem_set in problem_sets:
            url = problem_set['url']
            if not url.startswith('http'):
                url = urllib.parse.urljoin(f"{self.pset_url}{week}/", url)
            result = requests.get(url)
            if result.status_code == 200:
                pset_doc = BeautifulSoup(result.text, "html.parser")
                # Extract the required data from pset_doc
                content = pset_doc.find('main', class_='col-lg').text.strip() if pset_doc.find('main', class_='col-lg') else 'No content found'
                data[problem_set['title']] = content
            else:
                data[problem_set['title']] = 'Failed to retrieve'
                print(url)
        return data

    def scrape_and_save(self, week):
        # Scrape data
        self.scrape_page(week)
        problem_sets = self.get_problem_set_lists()

        # Initialize file manager
        file_manager = CS50FileManager(base_directory="/path/to/save")

        # Create folders
        file_manager.create_folders(course=self.course, week=week, lectures=lecture_list, shorts=shorts_list, problem_sets=problem_sets)

        # Scrape detailed problem set data
        problem_sets_data = self.get_problem_set(problem_sets, week)

        # Save data
        file_manager.save_data(course=self.course, week=week, lectures=lecture_data, shorts=shorts_data, problem_sets_data=problem_sets_data)
