# Shift Planer 

Welcome to our Shift Planer. If you must to create some work schedule you can use our program. The program was created as part of my own project during the course. We decided to use our previous professional experience and try to create something that helps with everyday duties at work.

![Zrzut ekranu 2024-01-02 092108](https://github.com/SidorowiczPaulina/ShiftPlaner/assets/138161293/dc31895e-13c3-4ce1-b996-c6267f362a5c)

# Table of contents

* [Technologies](#Technologies)
* [Instalation process](#Instalation-process)
* [Features](#Features)
* [Accounts app](#Accounts-app)
* [Tests](#Tests)
* [Authors](#Authors)


# Technologies

## Backend - Python and Django
We provided a backend foundation by using Python 3.11.3 and Django 5.0. Python offers the latest features, bug fixes and optimizations, which contributes to effective and modern application development. Django 5.0, as a high-level web framework, provides tools for quickly creating solid web applications.

## Fronted - HTML5, CSS, JavaScript, Bootstrap
In order to create a user-friendly look, we used popular frontend technologies HTML5, CSS, Bootstrap and JavaScript.

# Instalation process

1. Clone the repository to your local computer

       $ git clone 'https://github.com/SidorowiczPaulina/ShiftPlaner.git'


2. Navigate to project directory

       $ cd ShiftPlaner


3. Create virtual environment

       $ python -m venv venv

      activate for windows
        
        $ python venv\Scripts\activate

      activate for Linux

        $ cource venv/bin/activate
     

5. Install the required dependencies

        $ pip install -r requirements.txt

6. Create database 'db.sqlite3' using migration

        $ python manage.py migrate
   

7. Run the Django development server

        $ python manage.py runserver 

    Our server will be available at http://localhost:8000/



# Features
  * Determining the hourly range of changes (I, II)
  * User registration and login
  * Creating work schedules for users (manager - administrator, employee users)
  * Exporting the table with the schedule available on the project website (on a monthly basis)
  * Adding new users to the system
  * Viewing your own schedule
  * Depending on the user's status - additional functionalities
  * Generating schedules and reports in .pdf file format
  * Possibility to enter hourly instructions
    
 #### To do
  * Preparation of a predictive model for part-time positions, etc
  * Additional restrictions related to labor law
  * Manage contracts and assign contract types to users
  * Viewing and modifying user data
  * Viewing working time reports
 
##### Short description
The main idea was to create a program that would speed up the creation of a work schedule. Our program provides different options for an administrator (e.g. manager) and others for an ordinary user. Thanks to this, the administrator has the opportunity to verify changes and accessibility introduced by users. The program is relatively simple, it is possible that it will be expanded with additional functionalities in the future. We created the program as part of a project during the course in "Software Development Academy".

# Accounts app

### Registration

![image](https://github.com/SidorowiczPaulina/ShiftPlaner/assets/138161293/8a9db7af-a976-418f-adfe-55aeddbb918a)

### Log in

![image](https://github.com/SidorowiczPaulina/ShiftPlaner/assets/138161293/0135bac7-15ee-40fc-a464-a91c4cd3e250)


# Tests
To test our code, we used unit tests and functional tests. Unit tests allow you to check individual components, such as forms. Integration tests allow you to check cooperation between larger pieces of code.

### Coverage report

![image](https://github.com/SidorowiczPaulina/ShiftPlaner/assets/138161293/1b225683-2889-4067-91cf-6bcf99197b05)


# Authors

  ## Paulina Sidorowicz

  Find me on LinkedIn: https://www.linkedin.com/in/pausidor/

  ## Filip Rdzanek

  Find me on LinkedIn: 


   





