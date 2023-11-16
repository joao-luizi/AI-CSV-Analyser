# CSV Analysis with Artificial Intelligence

# Overview

Welcome to AIJohn, a tool for analyzing CSV files with the assistance of Artificial Intelligence. This application is designed to streamline the process of extracting valuable insights from your CSV data, using AI algorithms, without specific query language (like SQL).

# Features

- **AI-Powered Analysis**: Leverage AI algorithms to extract meaningful patterns and insights from your CSV data.
- **User-Friendly Interface**: Intuitive and easy-to-use interface for users of all levels.
- ~~**Customizable Analysis**: Tailor the analysis to your specific needs with customizable parameters and options.~~ (TODO)
- ~~**Export Results**: Save and export analysis results in various formats for further use or sharing.~~ (TODO)
- ~~**Fast and Scalable**: Handle large CSV files efficiently, ensuring quick and reliable analysis.~~ (TODO)

# Configuration

After cloning you will need to create a virtual enviroment for the app. Reqirements.txt has all necessary packages.

Run pip install -r requirements.txt from the command line.

The application requires users to login. You can create an admin user by running manage.py from the terminal with the command:

python manage.py create_admin

You will be prompted for an email address and a password (2x). If an error occurs you will see "Couldn't create admin user.". If sucessfull no prompt will return.

You can run the application on a development server by running the "flask run" from the command line (you need to activate your virtual enviroment).

After the login you can:

## Register Users

You can create more admin or guest users.
The user you created on the command line can be used here to create a proper user,
You can also delete users.

## Register Keys

This is a bring-your-openAI-key app so here you can register keys. Keys are automatically assign to the user who created them.

## Assign Keys

You can assign keys to users. A user that creates a key has that key assigned by default.

## Upload CSV

You can upload a CSV you want to query. The file is limited to 1 MB.

## Query CSV

You can query an uploaded CSV.
