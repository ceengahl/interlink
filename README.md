# INTERLINK:

interlinking li connections to vc's from master list via your 1st connections

# NON CODERS:

see section 'getting started for non coders' below

# AUTHENTICATION:

After running "controller.py", user will be prompted for their linkedin credentials

# HOW TO:

'controller.py' is the main module that controls the submodules.

USER will be prompted to select the action they'd like to take:

- enter a new list of VCs
- continue parsing existing list of VCs
- export current results to csv after cleaning and organizing the information
- message the 1st connections for warm intros (pending, under development)

After making a selection, user may be asked if he wants to parse the entire list of VCs or limit the amount of results

User will be asked to enter linkedin credentials at the appropriate time.

User will also be asked if they'd like to export the raw scrape data to a consummable CSV format after their list has been parsed. Respond Yes to get both a JSON file with '--final network' in the name with all the results, and an abbreviated decision making CSV called '1st_connections.csv'. In that CSV they will find a column asking if they'd like to reach out to this contact or not. Mark boolean TRUE/FALSE

User will be asked to approve both first degree connections and their connected VCs for outreach - carefully review these CSVs to approve only those you should reach out to.

After approving people and VCs, the final output will be a CSV with your approved first degree connections and a outbound request message with the VCs and the target contact. This message is ready to copy and paste into your linkedin messages or wherever.

# CODE PROCESS:

controller will then attempt to:

1. parse through VC list and scrap info for any VC's that haven't been recorded as scraped from linkedin
2. remove any emoticons and emojis from the results
3. reorganized the data scraped from linked from "by VC" to "by 1st degree mutual connections"
4. create 1 csv for approving your first degree connections you'd like to reach out to, and 1 csv for the VCs to approve for outreach as well
5. combine your approved VCs and first connections and compose a final CSV with a templated message you can copy and paste to message your first degree connections

# GETTING STARTED FOR NON CODERS

## Running a Python Script from Terminal

This guide provides step-by-step instructions on how to run a Python script from the terminal. It also covers setting up a virtual environment (venv) to isolate your project's dependencies.

## Prerequisites

1. Make sure you have Python installed on your computer. You can download it from the official Python website: [python.org](https://www.python.org/downloads/)

## Setup

1. Clone or download this project repository to your computer.

2. Open a terminal or command prompt.

3. Navigate to the project directory using the `cd` command. For example:

   cd /path/to/project-directory

   \*To get your project directory, ask chatGPT for the fastest response, as it varies depending on operating system

4. Create a virtual environment (venv) to isolate your project's dependencies. Enter the following command:

   python3 -m venv venv

5. Activate the virtual environment. Run the appropriate command based on your operating system:

   - For Windows:

     venv\Scripts\activate

   - For macOS/Linux:

     source venv/bin/activate

## Installing Dependencies

1. Once the virtual environment is activated, you can install the required dependencies by running the following command:

   pip3 install -r requirements.txt

2. Wait for the installation process to complete. This will install all the necessary packages for the project.

## Running the Python Script

1. After installing the dependencies, you can run the Python script using the following command:

   python3 controller.py

2. Press Enter to execute the script. The output, if any, will be displayed in the terminal.

3. Follow any on-screen instructions, if provided, to interact with the script.

## Exiting the Script and Virtual Environment

1. To exit the Python script, you can press `Ctrl + C` in the terminal.

2. To deactivate the virtual environment, enter the following command:

   deactivate

contact project owner for questions
