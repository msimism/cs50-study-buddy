from includes.cs50scraper import CS50Scraper
from includes.cs50commandline import CommandLine
from includes.cs50interface import Interface
from includes.cs50 import CS50  # Import CS50
from alive_progress import alive_bar
import sys

def main():
    course_manager = CS50()  # Initialize CS50 without course to access course info methods

    # Check if any command-line arguments are provided
    if len(sys.argv) > 1:
        cli = CommandLine()
        args = cli.parse_arguments()
        scraper = CS50Scraper(course=args.course, base_directory=args.destination)
        scraper.scrape_course()
    else:
        interface = Interface(course_manager)  # Pass CS50 instance to Interface
        interface.display_menu()

if __name__ == "__main__":
    main()
