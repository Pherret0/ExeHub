#ExeHub Web App
The ExeHub project is a web app that aims to re-connect the university student community a promote student engagement online. With the pandemic, the university experience has significantly changed, with dramatically reduced interaction with fellow peers, academics and support networks. ExeHub aims to provide a bridge between these groups and allow students to socialise and engage with each other, promoting a healthy student community. 

#Languages/Frameworks
This project uses the Python framework Django. To run this web app locally, you will need to ensure that you have the Django framework installed. To install Django, execute the following command:

python -m pip install Django

To ensure that the installation was successful, you can run the following command:

python -m django --version

If Django has successfully been installed, you should see the version of Django installed. 

The MySQL server will also need to be running while accessing the web app locally. Ensure that mysql-connector-python is installed using the following command:

pip install mysql-connector-python

#Run the Project:
To start the Django development server and run the web app, run the following command:

python manage.py runserver

The web app will then be accessible at the following location: http://127.0.0.1:8000/