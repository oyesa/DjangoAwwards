# CROWNE AWWARDS
#### By Oyesa Mercy Oluchina
#### 10/06/2022

### Description
This is a website application: a clone for Awwwards website. Users can sign-up, login, create projects to be voted on by their peers as well as view and rate other users projects. 

### Behaviour Driven Development (BDD)

| Behaviour                            |     Input                       |                                                                                                       Output |
| :---                                 |     :---:                       |                                                                                                         ---: |
|On clicking on the application link   |       None                                          |      Crowne Awards website loads a landing page with a login button ---Users with existing accounts login---New users can register  |
|Click Login                           |   Input email and password                           |                       App loads with sumbmit project, profile and logout buttons.            |
|Click Submit project                  |Enter project title, description, url and screenshot  |    New project is created and displayed on home page       |
|Click Profile  button                 |   Enter profile details as desired                  |Profile details updated as populated and displayed on profile page.|
|Click on project title                |   None                                                |     Project page loads with its description and average rating it has been voted on|
|Click on rate project                 |    Enter vote on project design, usability and content|             Page displays the votes and average of the vote for the project|
|Delete project                        |   None                                                |                                     Logged in user is nolonger able to see the deleted project  |
|Logout                                |   None                                                |                   User exits application          |


### Setup/Installation Requirements
The application requires the following installations to operate:
* Python3.8
* Django
* Pip 
* PostgreSQL
* Cloudinary
With the above installations proceed to:
* git clone https://github.com/oyesa/DjangoAwwards.git
* cd DjangoAwwards
* code . (if using Visual Studio Code) 

### Running Application
To run the application, open the cloned files in your terminal and run the following commands:
* $ python3.8 -m venv --without-pip virtual
* $ source virtual/bin/activate
* $ curl https://bootstrap.pypa.io/get-pip.py | python
* $ pip install -r requirements.txt
* $ python manage.py runserver

### Testing the Application
To run the tests:
* $ python3.8 manage.py test profile
* $ python3.8 manage.py test project
* $ python3.8 manage.py test vote

### Technologies Used
* Python
* Django
* PostgreSQL
* HTML
* CSS
* Bootstrap3

### Bugs
The

## Contact
To make contributions to the code or offer any suggestions you can contact me via email:
  Email: mercy.oluchina@student.moringaschool.com

### Licence
 MIT Licence
 Copyright (c) 2022 Oyesa Mercy Oluchina