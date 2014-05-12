Uex.io
======

Thank you for reviewing the Uexio project, below is a brief summary of the project's organizational structure, login information, etc.

### Files
The uexio-master directory and uexio-master.zip directory and zip file contain all of the code for the current sprint.

### Language
The application using Python for the programming language.

### Framework
Uexio utilizes the Django framework.

### Views
Currently you can visit http://localhost:5000/admin (after you have started the server) to access the admin dashboard for the application.
You can visit the user side by visiting http://localhost:5000/

### Functionality
In the admin panel you can create products, associate products with categories, create addtional categories, create url slugs, etc. You can also create users.

Following links can be used to navigate through uexio products:
* /products/ # shows the product index
* /products/<slug>/edit/ # allows the user to edit the product
* /products/<slug>/images/ # allows the user to manage their product

### Installation
You can follow the installation guides below:
*  make sure pip is installed, if not follow guide here: http://www.pip-installer.org/en/latest/quickstart.html
*  If you’re using Linux, Mac OS X or some other flavor of Unix, enter the command ```sudo pip install -r requirements.txt```at the shell prompt. If you’re using Windows, start a command shell with administrator privileges and run the command ```pip install -r requirements.txt```. This will install all project dependencies in your Python installation’s site-packages directory.
* Next, unzip the uexio-master zip file and then navigate to that folder through commandline.
* Copy uexio.sqlite3.sample file to uexio.sqlite3
* Next, Follow the Login credentials instructions bellow  

### Login credentials
You can create a local superadmin user by running the command: ```django-admin.py createsuperuser``` in the console, you will then be prompted to enter your login crentials. After you have created the superadmin you can access the admin dashboard with full authorization. If the command: django-admin.py createsuperuser does not work automatically, you will need to run the following commands:

* python manage.py syncdb
* python manage.py migrate
* python manage.py createsuperuser

To test the paypal checkout process, use the following sandbox account
* username/email: kush.patel@ttu.edu
* password: kushpatel

### Running the application
You can test our application on http://uexio.herokuapp.com/ . 
If you would like to install a local copy follow this instructions (note that paypal wont work in local copy)
* Create an amazon S3 account (if not already).
* Create a bucket in amazon S3
* Get the required credentials from your amazon S3
* Copy `.env.sample` file to `.env` and fill in the S3 credentials. 
* Download Redis from redis.io (if not already). On a Mac you can install it with brew using following command in your terminal ```brew install redis```
* Once redis is installed, run the redis server with following command ```redis-server```
* Once that's done you can start the uexio server with ```foreman start```. 

### Indentation
Since the application is being built with Python, indentation is vital for the program to function properly, you will see spacing is consistent throughout the program.

### Comments
We went through the application multiple times, adding extremely detailed comments describing each piece of functionality so it should be easy to navigate through the application code and understand the features of the current iteration.

### Key files
Since the applicaiton utilizes the Django framework, the system utilizes a strict MVC structure, and key files are: uexio/settings.py, products/admin.py, products/views.py, products/models.py, and uexio/urls.py. An important note, Django utilizes regular expressions for the url view calls.

Regards,

Team Uexio

