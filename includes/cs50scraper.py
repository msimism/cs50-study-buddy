from includes.cs50 import CS50
from includes.cs50filemanager import CS50FileManager
from alive_progress import alive_bar

class CS50Scraper:
    def __init__(self, course, base_directory):
        self.cs50 = CS50(course)
        self.file_manager = CS50FileManager(base_directory)

    def scrape_course(self):
        week = 0
        weeks_data = {}
        total_weeks = 10  # Assuming a maximum of 10 weeks, adjust as needed

        with alive_bar(total_weeks, title="Scraping course data") as bar:
            while True:
                doc = self.cs50.scrape_page(week)
                if doc is None:
                    break
                lectures = self.cs50.get_title() + "\n" + self.cs50.get_description() + "\n" + self.cs50.get_week_tags() + "\n" + self.cs50.get_shorts()
                pset_doc = self.cs50.scrape_problem_set_page(week)
                problem_sets = []
                if pset_doc:
                    problem_sets = self.cs50.get_problem_set_lists()
                    for pset in problem_sets:
                        problems = self.cs50.get_problem_set([pset], week)
                        pset['data'] = "\n\n".join([content for title, content in problems.items()])  # Ensure 'data' key exists
                    self._print_problem_sets(problem_sets, week)

                weeks_data[week] = {
                    'lectures': lectures,
                    'shorts': self.cs50.get_shorts(),
                    'problem_sets': problem_sets
                }
                week = self.cs50.progress(week)
                bar()  # Update the progress bar

        # Create folders and save data
        self.file_manager.create_folders(self.cs50.course, weeks_data)
        self.file_manager.save_data(self.cs50.course, weeks_data)

    def _print_problem_sets(self, problem_sets, week):
        if isinstance(problem_sets, list):
            for problem_set in problem_sets:
                return(f"Week {week} - Title: {problem_set['title']}, URL: {problem_set['url']}")
            problem_set_page = self.cs50.get_problem_set(problem_sets, week)
            for title, content in problem_set_page.items():
                return(f"Title: {title}\nContent: {content}\n")
        else:
            print(problem_sets)
