# CS50 Study Buddy

**CS50 Study Buddy** is a Python program designed to be your ultimate aide for CS50 courses. When launched with specific flags, the program scrapes the relevant CS50 course websites to gather and download all required lesson plans and problem sets. It automatically creates a structured folder hierarchy for the course, such as:

- `cs50x/week-1`
- `week-1/lecture`
- `week-1/pset-1`
- `pset-1/indoor`
- `week-1/shorts`
- `shorts/functions`
- And similar directories.

The program also downloads the follow-along code discussed in the lectures into a folder named:

- `/week-*/lecture/code_snippets`

or a similar location.

Additionally, within each problem set folder, the program scrapes detailed assignment information and generates structured content to aid your learning process.

## Development Status

CS50 Study Buddy is currently in development. Some features have not been properly implemented, and it is by no means complete. The project has been put on GitHub for the time being to facilitate collaboration and feedback.

## TODO

- **Downloading Course Materials**: The next update will include the ability to download each week's lecture follow-along code, which will be placed in the lecture folders.
- **Short Videos**: The program will be updated to download relevant short video information. If the video/audio flags are selected, these videos will be downloaded alongside example code.

### Recent Fixes

- **Updated CS50X Logic**: Fixed parsing issue with the cs50x course.

### Known Issues

- **Download Files Logic**: The logic for downloading files is yet to be implemented.
- **Course Parsing Logic**: Some courses do not scrape and create all the problem sets correctly.

## How to Contribute

Feel free to fork the repository, open issues, or submit pull requests. Any contributions to help improve the project are welcome.

## Getting Started

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/msimism/cs50-study-buddy.git
cd cs50-study-buddy
```

Run the program:
```bash
python main.py

```


