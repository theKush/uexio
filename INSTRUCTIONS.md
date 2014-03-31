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
Currently you can visit http://localhost:8000/admin (after you have started the server) to access the admin dashboard for the application.

### Functionality
In the admin panel you can create products, associate products with categories, create addtional categories, create url slugs, etc. You can also create users.

### Login credentials
You can create a local superadmin user by running the command: django-admin.py createsuperuser in the console, you will then be prompted to enter your login crentials. After you have created the superadmin you can access the admin dashboard with full authorization. If the command: django-admin.py createsuperuser does not work automatically, you will need to run the following commands:

* python manage.py syncdb
* python manage.py migrate
* python manage.py createsuperuser

### Indentation
Since the application is being built with Python, indentation is vital for the program to function properly, you will see spacing is consistent throughout the program.

### Comments
We went through the application multiple times, adding extremely detailed comments describing each piece of functionality so it should be easy to navigate through the application code and understand the features of the current iteration.

### Key files
Since the applicaiton utilizes the Django framework, the system utilizes a strict MVC structure, and key files are: uexio/settings.py, products/admin.py, products/views.py, products/models.py, and uexio/urls.py. An important note, Django utilizes regular expressions for the url view calls.

Regards,

Team Uexio

