# CS50 Study Buddy

**CS50 Study Buddy** is a Python program designed to be your ultimate aide for CS50 courses. When launched, the program scrapes the relevant CS50 course websites to gather and download all required lesson plans and problem sets. It automatically creates a structured folder hierarchy for the course, such as:

- `cs50x/week-1`
- `week-1/lecture`
- `week-1/pset-1`
- `pset-1/indoor`
- `week-1/shorts`
- `shorts/functions`
- And similar directories.

The program also downloads the follow-along code discussed in the lectures into a folder named:

- `/week-*/lecture/example_code`

or a similar location.

Additionally, within each problem set folder, the program scrapes detailed assignment information and generates structured content to aid your learning process.

## Development Status

CS50 Study Buddy is currently in development. Some features have not been properly implemented, and it is by no means complete. The project has been put on GitHub for the time being to facilitate collaboration and feedback.

## Recent Updates

- **Added Course Selection and Configuration Options Flow**: Improved the interface to allow users to select courses, configure download options, and run the course aide with a clear and user-friendly flow.
- **Introduced Debug Flag**: Added a debug flag to control debug output, making it easier to diagnose issues.
- **Dynamic Course Folder Naming**: Implemented dynamic naming for course folders (e.g., `cs50x`, `cs50p`, `cs50ai`, etc.).
- **Enhanced File Download and Extraction Logic**: Improved the logic for downloading and extracting files, including removing zip files after extraction.
- **Improved Menu Navigation**: Added "back" and "continue" options in the menu for better navigation.

### Known Issues

- **Course Parsing Logic**: Some courses might not scrape and create all the problem sets properly.

## TODO

- **Short Videos**: Will add the ability to download the short videos' relevant information. If video/audio flags are selected, they will be downloaded accordingly alongside the example codes.

## How to Contribute

Feel free to fork the repository, open issues, or submit pull requests. Any contributions to help improve the project are welcome.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python packages (install via `pip`)

### Installation

1. Clone the repository and navigate to the project directory:

    ```bash
    git clone https://github.com/msimism/cs50-study-buddy.git
    cd cs50-study-buddy
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Program

You can run the program either via the command line or interactively through the menu.

#### Command Line Usage

```bash
python main.py -course [course_name] -destination [output_directory] -audio -video -code -debug 
``` 

#### Interactive Menu

Run the program and follow the prompts to select courses, configure options, and run the course aide.

```bash
python main.py 
```

### Directory Structure

The program creates a structured folder hierarchy for the course content, such as:

```
-cs50p/
    -week-0/
        -lecture/
            -lectures.txt
            -example_code/
            -week-0-lecture.mp3
            -week-0-lecture.mp4
            -week-0-lecture.pdf
        -pset-0/
            -problem-1/
                -README.md
            -problem-2/
                -README.md
        -shorts/
            -shorts.txt
    -week-1/
        -...
```