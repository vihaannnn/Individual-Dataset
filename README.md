# Individual Dataset
This Repository is for the Individual Dataset for the AIPI course 510, created by Vihaan Swapneshkumar Nama.
Make sure you are on the 'master' branch of the project. Other branches are provided to see commits and history.

NOTE  - EDA CODE INCLUDED WITH THE PIPELINE CODE IN THE pipeline.py FILE IN THE DIRECTORY - workingDir

# Indian-Supreme-Court-Judgements-Chunked

## Introduction
This project aims to create the Indian-Supreme-Court-Judgements-Chunked dataset via a pipeline and the chunked contents from the PDF files have been uploaded to HuggingFace.

## About the Dataset
Dataset published on - https://huggingface.co/datasets/vihaannnn/Indian-Supreme-Court-Judgements-Chunked


## Prerequisites
This project requires the use of a Python virtual environment to manage dependencies and ensure consistent behavior across different systems. This guide provides step-by-step instructions for setting up a virtual environment on both Windows and Mac, as well as installing dependencies via a `requirements.txt` file.
- Python 3.x installed on your system.
- Git installed on your machine
- Basic knowledge of command-line operations.

## Cloning the Project
- Open the Command Shell or Terminal on your machine and execute the following command
   ```sh
   git clone https://github.com/vihaannnn/Individual-Dataset.git
   ```


## Setting Up a Virtual Environment

### Windows

1. **Open Command Prompt or PowerShell**:
   - Search for `cmd` or `PowerShell` in the start menu and open it.

2. **Navigate to your project directory**:
   cd (move) into your specific project path (where you have saved it on your computer), for example - 
   ```sh
   cd /Individual-Dataset
   ```

3. **Create a virtual environment**:
   ```sh
   python -m venv venv
   ```
   This creates a directory named `venv` that contains the virtual environment.

4. **Activate the virtual environment**:
   ```sh
   .\venv\Scripts\activate
   ```
   After activation, your command prompt will show `(venv)` indicating the virtual environment is active.

### Mac

1. **Open Terminal**:
   - You can find Terminal in your Applications > Utilities folder.

2. **Navigate to your project directory**:
   cd (move) into your specific project path (where you have saved it on your computer), for example - 
   ```sh
   cd /Individual-Dataset
   ```

3. **Create a virtual environment**:
   ```sh
   python3 -m venv venv
   ```
   This creates a directory named `venv` that contains the virtual environment.

4. **Activate the virtual environment**:
   ```sh
   source venv/bin/activate
   ```
   After activation, your terminal prompt will show `(venv)` indicating the virtual environment is active.

## Installing Dependencies

1. **Ensure your virtual environment is activated**:
   - Verify that `(venv)` is present in your terminal/command prompt.

2. **Install the dependencies from `requirements.txt`**:
   ```sh
   pip install -r requirements.txt
   ```
   This command installs all the packages listed in the `requirements.txt` file into your virtual environment.

   **Install the dependencies using setup.py**:
   Make sure you have setuptools installed on your machine
   ```sh
   pip install setuptools
   ```
   Next just run - 
   ```sh
   python setup.py install
   ```
   Either of these methods should have all your dependencies downloaded

## Deactivating the Virtual Environment

Once you're done working, you can deactivate the virtual environment by running:
  ```sh
  deactivate
  ```
  After deactivation, the `(venv)` prefix will disappear from your terminal/command prompt.

## Creating the Project Structure
On your local, once the project is cloned and the virtual environment is created, create several folders in the root directory of the project titled 'Semantic', 'Recursive', 'TokenWise', 'output', 'metadata', and 'output_normal'

These files are where your data will go once the pipeline has run.

## Obtain Data
 - Original PDF documents for this chunking can be obtained here - https://www.sci.gov.in/judgements-judgement-date/
Fill out the form and specify the date ranges to obtain the data
 - Once you obtain the PDF documents - label them with a number for example - '1.pdf' No number should repeat.
 - Delete the already existing 2 documents in the 'data' folder
 - Place your new documents in the folder

## Creating the ENV file
Go into the workingDir directory. Create a file name '.env'

Go to openai platform - https://platform.openai.com/docs/overview and create an API Key

Place the API key in your .env file - 
```sh
  OPENAI_API_KEY=<your-API-key>
```
## To run the project
Go into the workingDir directory and run the pipeline.py file.

Please make sure the ENV file was created and in the working directory before running the pipeline

The code to do so is - 
```sh
  cd Individual-Dataset/workingDir
  python pipeline.py
```

## To run the test cases of the project
Go into the main directory and run the testing commands.

4 test cases should execute and pass.
If the tests all show up as green -> all tests are running fine

Please make sure the ENV file was created and in the working directory before running tests
```sh
  cd Individual-Dataset
  pytest -v
```

## Credits
- Part of this README.md file was generated using the Artificial Intelligence agent - ChatGPT
- Original data sourced from - https://www.sci.gov.in/judgements-judgement-date/
