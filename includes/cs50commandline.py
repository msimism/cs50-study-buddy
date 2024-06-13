# includes/cs50commandline.py

import argparse

class CommandLine:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="A script to scrape courses and download media")
        self.parser.add_argument("-course", help="the course to scrape", required=True)
        self.parser.add_argument("-audio", help="download audio files", action='store_true')
        self.parser.add_argument("-video", help="download video files", action='store_true')
        self.parser.add_argument("-code", help="download code files", action='store_true')
        self.parser.add_argument("-destination", help="destination folder to save files", default='saved')
        self.parser.add_argument("-debug", help="enable debug output", action='store_true')
        self.parser.add_argument("-debug_categories", help="comma-separated list of debug categories", default="")

    def parse_arguments(self):
        self.args = self.parser.parse_args()
        return self.args

    def flags(self):
        args = self.parse_arguments()
        course = args.course
        audio = args.audio
        video = args.video
        code = args.code
        destination = args.destination
        debug = args.debug
        debug_categories = args.debug_categories.split(',') if args.debug_categories else []

        print(f"Course: {course}")
        print(f"Download audio: {audio}")
        print(f"Download video: {video}")
        print(f"Download code: {code}")
        print(f"Destination: {destination}")
        print(f"Debug: {debug}")
        print(f"Debug Categories: {debug_categories}")

        return course, audio, video, code, destination, debug, debug_categories

    def help(self):
        """ Write useful help information for cli usage """

if __name__ == "__main__":
    cli = CommandLine()
    cli.flags()
