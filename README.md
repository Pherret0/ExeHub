#ExeHub Web App
The ExeHub project is a web app that aims to re-connect the university student community and promote student engagement online. Due to the pandemic, the university experience has significantly changed, with dramatically reduced interaction with fellow students, academics and support networks. ExeHub aims to provide a bridge between these groups and allow students to socialise and engage with each other, promoting a healthy student community. 

ExeHub encapsulates student groups, named communities, and gamification to provide a fun and engaging environment. Students can register to join or create their own communities, before being able to create posts, discussions and events for their community. Users are able to compete against one another, promoting student engagement, by claiming achievements and collecting points, all displayed on the ExeHub leaderboard.

#Languages/Frameworks
This project uses the Python framework Django. To run this web app locally, you will need to ensure that you have the Django framework installed. To install Django, execute the following command:

python -m pip install django

To ensure that the installation was successful, you can run the following command:

python -m django --version

If Django has successfully been installed, you should see the version of Django installed. 

The MySQL server will also need to be running while accessing the web app locally. Ensure that mysql-connector-python is installed using the following command:

pip install mysql-connector-python

#Run the Project:
To set up the migrations and start the Django development server to run the web app, run the following commands:

python manage.py migrate

python manage.py runserver

The web app will then be accessible at the following location: http://127.0.0.1:8000/


#Live Website
The website can be viewed at the following address: www.exehub.uk