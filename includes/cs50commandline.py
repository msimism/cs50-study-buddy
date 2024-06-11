import argparse

class CommandLine:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="A script to scrape courses and download media")
        self.parser.add_argument("-course", help="the course to scrape", required=True)
        self.parser.add_argument("-audio", help="download audio files", action='store_true')
        self.parser.add_argument("-video", help="download video files", action='store_true')
        self.parser.add_argument("-code", help="download code files", action='store_true')
        self.parser.add_argument("-destination", help="destination folder to save files", default='saved')

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

        print(f"Course: {course}")
        print(f"Download audio: {audio}")
        print(f"Download video: {video}")
        print(f"Download code: {code}")
        print(f"Destination: {destination}")
        
        return course, audio, video, code, destination

    def help(self):
        """ Write useful help information for cli usage """

if __name__ == "__main__":
    cli = CommandLine()
    cli.flags()

