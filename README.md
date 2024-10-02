# Keepit Technical Assignment

A program that receives the URL to a web site as a command line argument, retrieves the HTML web page content, finds the HTML unordered list with the most direct children, and returns the number of items in that list.

## Prerequisites

- Python 3.12
- Git

## Usage

### 1. Clone the repository
```bash
git clone https://github.com/yh-0/KeepitTask.git
```

### 2. Navigate to project directory
```bash
cd KeepitTask
```

### 3. Run the script

### Windows
```bash
py task.py <URL>
```

If you have multiple Python versions installed, you can specify the version explicitly:
```bash
py -3 task.py <URL>
```

### Linux/MacOS
```bash
python3 task.py <URL>
```

If your system defaults to Python 3 when using `python`, you can run it as:
```bash
python task.py <URL>
```