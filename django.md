# How to install Django on Windows

## Install Python & Verify
  - [https://www.python.org/downloads/]

  - Check Version: `py --version`

---

## Setup Virtual Environment & Activate
  - `py -m venv project_name`

  - `project_name\Scripts\activate.bat`
      *`$ source project_name/Scripts/activate`*

---

## Install Django & Verify
  - `py -m pip install Django`

    *This will download and install the latest Django release*

    *After the installation has completed, you can verify your Django installation by executing*
  - `django-admin --version`

    *Update*
  - `py -m django --version`

---

## Create a project

  cd into dir that will hold project

  - `django-admin startproject project_name`

  *Update*
  - `py -m django startproject project_name`

---

## Create app
  cd into dir that holds manage.py

  - `cd project_name`

  - `py manage.py startapp app_name`

  *Runserver*
  - `py manage.py runserver 8080`

---  

## Installing Packages
  - `python -m pip install <package_name>`

---

## Register App
  `project_name/settings.py`:

  ```
  INSTALLED_APPS = [
    #...
    'my_app',
    #...
  ]
  ```

  Give Django access to where templates are stored:

  ```
  import os

  # Build paths inside the project like this: BASE_DIR / 'subdir'.
  TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

  TEMPLATES = [
    {
      'DIRS': [TEMPLATE_DIR,],
    }
  ]
  ```

  Give Django access to where static files are stored:

  ```
  import os

  # Static files (CSS, JavaScript, Images)
  # https://docs.djangoproject.com/en/4.1/howto/static-files/
  STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
  ```

---

## Templates
  Create a base template to be rendered by view:
  
  `app_name/templates/app_name/base.html`:

  ```
  <!DOCTYPE html>
  <html lang="en">
    <head>
      <title>Project Title</title>
    </head>
    <body>
      <h2>Base Template</h2>
    </body>
  </html>
  ```
---

## Views
  Create a view that renders the base.html template: 

  `project_name/app_name/views.py`:

  ```
  from django.shortcuts import render

  # Create your views here.
  def home(request):
    return render(request, 'base.html')
  ```

---

## Url's
  Map url to view: `app_name/views`

  ```
  from django.urls import path

  from . import views

  urlpatterns = [
    path('', views.home, name='home'),
  ]
  ```

---

## Database
  Make migrations for database: which is responsible for creating new migrations based on the changes you have made to your models.
  
  - `py manage.py makemigrations`

  ```
  ←[36;1mMigrations for 'my_app':←[0m
  ←[1mmy_app\migrations\0001_initial.py←[0m
    - Create model Search
  (xaviers_venv) 
  ```
   
  Migrate all for database: migrate, which is responsible for applying migrations, as well as unapplying and listing their status.

  - `py manage.py migrate`
  
  ```
  ←[36;1mOperations to perform:←[0m
  ←[1m  Apply all migrations: ←[0madmin, auth, contenttypes, my_app, sessions
  ←[36;1mRunning migrations:←[0m
    Applying my_app.0001_initial...←[32;1m OK←[0m
  (xaviers_venv) 
  ```
  Create a superuser which is the admin of the site / database

  - `py manage.py createsuperuser`
    - Username: admin
    - Email address: admin@email.com
    - Password: ****
    - Password (again): ****
      This password is too common. This password is entirely numeric. ←[0mBypass password validation and create user anyway? [y/N]: y

---

## Models
  Generally, each model maps to a single database table:

  `app_name/models.py`:

  ```
  from django.db import models

  # Create your models here.
  class Search(models.Model):
    class Meta:
      verbose_name_plural = 'Searches'

    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
      return '{}'.format(self.search)
  ```

  Register model:

  `app_name/admin.py`:

  ```
  from django.contrib import admin

  # Register your models here.
  from .models import Search

  admin.site.register(Search)
  ```

---

##
## Models and Databases

  ### MODELS
  - A model is the single, definitive source of information about your data. It contains the essential fields and behaviors of the data you’re storing
  - Generally, each model maps to a single database table
    
    - The Basics:
      - Each model is a Python class that subclasses `django.db.models.Model`.
      - Each attribute of the model represents a database field.
      - With all of this, Django gives you an automatically-generated database-access API; see Making queries.

  #### Quick example:

  This example model defines a **Person**, which has a **first_name** and **last_name**:

    ```
    from django.db import models

      class Person(models.Model):
          first_name = models.CharField(max_length=30)
          last_name = models.CharField(max_length=30)
    ```

  **first_name** and **last_name** are fields of the model. Each field is specified as a class attribute, and each attribute maps to a database column.

  The above **Person** model would create a database table like this:

  ```
  CREATE TABLE myapp_person (
      "id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
      "first_name" varchar(30) NOT NULL,
      "last_name" varchar(30) NOT NULL
  );
  ```

  Some notes:

  - The name of the table, **myapp_person**, is automatically derived from some model metadata but can be overridden. See Table names for more details.
  - An __id__ field is added automatically, but this behavior can be overridden. See Automatic primary key fields.
  - The **CREATE TABLE** SQL in this example is formatted using PostgreSQL syntax, but it’s worth noting Django uses SQL tailored to the database backend specified in your settings file.

---

  #### USING MODELS

  Once you have defined your models, you need to tell Django you’re going to use those models. Do this by editing your settings file and changing the **INSTALLED_APPS** setting to add the name of the module that contains your **models.py**
  
  For example, if the models for your application live in the module **myapp.models** (the package structure that is created for an application by the __manage.py startapp__ script), **INSTALLED_APPS** should read, in part:

  

  When you add new apps to **INSTALLED_APPS**, be sure to run __manage.py migrate__, optionally making migrations for them first with __manage.py makemigrations__

---

  #### FIELDS

  The most important part of a model – and the only required part of a model – is the list of database fields it defines. Fields are specified by class attributes. Be careful not to choose field names that conflict with the models API like __clean, save,__ or **delete**

  Example:

  ```
  from django.db import models

  class Musician(models.Model):
      first_name = models.CharField(max_length=50)
      last_name = models.CharField(max_length=50)
      instrument = models.CharField(max_length=100)

  class Album(models.Model):
      artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
      name = models.CharField(max_length=100)
      release_date = models.DateField()
      num_stars = models.IntegerField()
  ```

  **Field types**
  
  Each field in your model should be an instance of the appropriate **Field** class. Django uses the field class types to determine a few things:
  
  - The column type, which tells the database what kind of data to store (e.g. __INTEGER, VARCHAR, TEXT__).
  - The default HTML widget to use when rendering a form field (e.g. __`<input type="text">, <select>`__).
  - The minimal validation requirements, used in Django’s admin and in automatically-generated forms.
  
  Django ships with dozens of built-in field types; you can find the complete list in the model field reference.

---

  **Field options**
  
  Each field takes a certain set of field-specific arguments (documented in the model field reference). For example, **CharField** (and its subclasses) require a __max_length__ argument which specifies the size of the **VARCHAR** database field used to store the data.

  - There’s also a set of common arguments available to all field types. All are optional. They’re fully explained in the reference, but here’s a quick summary of the most often-used ones:

  __null__

  If **True**, Django will store empty values as __NULL__ in the database. Default is **False**.

  __blank__

  If **True**, the field is allowed to be blank. Default is **False**.

  Note that this is different than __null__. __null__ is purely database-related, whereas __blank__ is validation-related. If a field has __blank=True__, form validation will allow entry of an empty value. If a field has __blank=False__, the field will be required.

  __choices__

  A sequence of 2-tuples to use as choices for this field. If this is given, the default form widget will be a select box instead of the standard text field and will limit choices to the choices given.
  
  A choices list looks like this:

  ```
  YEAR_IN_SCHOOL_CHOICES = [
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    ('SR', 'Senior'),
    ('GR', 'Graduate'),
  ]
  ```

  Note: A new migration is created each time the order of choices changes.

  The first element in each tuple is the value that will be stored in the database. The second element is displayed by the field’s form widget.

  Given a model instance, the display value for a field with __choices__ can be accessed using the __get_FOO_display()__ method. For example:
  ```
  from django.db import models

  class Person(models.Model):
      SHIRT_SIZES = (
          ('S', 'Small'),
          ('M', 'Medium'),
          ('L', 'Large'),
      )
      name = models.CharField(max_length=60)
      shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
  ```
  ```
  >>> p = Person(name="Fred Flintstone", shirt_size="L")
  >>> p.save()
  >>> p.shirt_size
  'L'
  >>> p.get_shirt_size_display()
  'Large'
  ```

  You can also use enumeration classes to define __choices__ in a concise way:
  ```
  from django.db import models

  class Runner(models.Model):
      MedalType = models.TextChoices('MedalType', 'GOLD SILVER BRONZE')
      name = models.CharField(max_length=60)
      medal = models.CharField(blank=True, choices=MedalType.choices, max_length=10)
  ```

  Further examples are available in the model field reference.

  __default__

  The default value for the field. This can be a value or a callable object. If callable it will be called every time a new object is created.

  __help_text__

  Extra “help” text to be displayed with the form widget. It’s useful for documentation even if your field isn’t used on a form.

  __primary_key__

  If **True**, this field is the primary key for the model.

  If you don’t specify __primary_key=True__ for any fields in your model, Django will automatically add an __IntegerField__ to hold the primary key, so you don’t need to set __primary_key=True__ on any of your fields unless you want to override the default primary-key behavior. For more, see Automatic primary key fields.

  The primary key field is read-only. If you change the value of the primary key on an existing object and then save it, a new object will be created alongside the old one. For example:
  ```
  from django.db import models

  class Fruit(models.Model):
      name = models.CharField(max_length=100, primary_key=True)
  ```
  ```
  >>> fruit = Fruit.objects.create(name='Apple')
  >>> fruit.name = 'Pear'
  >>> fruit.save()
  >>> Fruit.objects.values_list('name', flat=True)
  <QuerySet ['Apple', 'Pear']>
  ```

  __unique__
  
  If **True**, this field must be unique throughout the table.
  
  Again, these are just short descriptions of the most common field options. Full details can be found in the common model field option reference.

---

## Views
  Let’s write the first view. Open the file `app_name/views.py` and put the following Python code in it:

  ```
  from django.http import HttpResponse


  def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
  ```

  This is the simplest view possible in Django. To call the view, we need to map it to a URL - and for this we need a URLconf.

  ```
  app_name/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    urls.py
    views.py
  ```

## Url's

  - To create a URLconf in the app directory, create a file called `urls.py`.

  - In the `app_name/urls.py` file include the following code:

  ```
  from django.urls import path

  from . import views

  urlpatterns = [
      path('', views.index, name='index'),
  ]
  ```

  - The next step is to point the root URLconf at the app_name.urls module. In project_name/urls.py, add an import for django.urls.include and insert an include() in the urlpatterns list, so you have:

  ```
  from django.contrib import admin
  from django.urls import include, path

  urlpatterns = [
      path('app_name/', include('app_name.urls')),
      path('admin/', admin.site.urls),
  ]
  ```

  The include() function allows referencing other URLconfs. Whenever Django encounters include(), it chops off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf for further processing.

  The idea behind include() is to make it easy to plug-and-play URLs. Since polls are in their own URLconf (polls/urls.py), they can be placed under “/polls/”, or under “/fun_polls/”, or under “/content/polls/”, or any other path root, and the app will still work.

  ```
  When to use include()

  You should always use include() when you include other URL patterns. admin.site.urls is the only exception to this.

  Page not found?

  If you get an error page here, check that you’re going to http://localhost:8000/polls/ and not http://localhost:8000/.
  ```

  `py manage.py runserver`

---

  The __path()__ function is passed four arguments, two required: __route__ and __view__, and two optional: __kwargs__, and __name__. At this point, it’s worth reviewing what these arguments are for.

---

  __path() argument: route__
  __route__ is a string that contains a URL pattern. When processing a request, Django starts at the first pattern in __urlpatterns__ and makes its way down the list, comparing the requested URL against each pattern until it finds one that matches.

  Patterns don’t search GET and POST parameters, or the domain name. For example, in a request to `https://www.example.com/myapp/`, the URLconf will look for `myapp/`. In a request to `https://www.example.com/myapp/?page=3`, the URLconf will also look for `myapp/`.

---

  __path() argument: view__
  When Django finds a matching pattern, it calls the specified view function with an __HttpRequest__ object as the first argument and any “captured” values from the route as keyword arguments. We’ll give an example of this in a bit.

---

  __path() argument: kwargs__
  Arbitrary keyword arguments can be passed in a dictionary to the target view. We aren’t going to use this feature of Django in the tutorial.

---

  __path() argument: name__
  Naming your URL lets you refer to it unambiguously from elsewhere in Django, especially from within templates. This powerful feature allows you to make global changes to the URL patterns of your project while only touching a single file.

---

## Database Setup
  *`project_name/settings.py`*

  - By default, the configuration uses SQLite. If you’re new to databases, or you’re just interested in trying Django, this is the easiest choice. SQLite is included in Python, so you won’t need to install anything else to support your database. When starting your first real project, however, you may want to use a more scalable database like PostgreSQL, to avoid database-switching headaches down the road. 

  - If you wish to use another database, install the appropriate database bindings and change the following keys in the DATABASES 'default' item to match your database connection settings

  - While you’re editing `project_name/settings.py`, set __TIME_ZONE__ to your time zone

  By default, __INSTALLED_APPS__ contains the following apps, all of which come with Django:

  - __django.contrib.admin__ – The admin site. You’ll use it shortly.
  - __django.contrib.auth__ – An authentication system.
  - __django.contrib.contenttypes__ – A framework for content types.
  - __django.contrib.sessions__ – A session framework.
  - __django.contrib.messages__ – A messaging framework.
  - __django.contrib.staticfiles__ – A framework for managing static files.
  These applications are included by default as a convenience for the common case.

  Some of these applications make use of at least one database table, though, so we need to create the tables in the database before we can use them. To do that, run the following command:

  ```
  py manage.py migrate
  ```

  The **migrate** command looks at the __INSTALLED_APPS__ setting and creates any necessary database tables according to the database settings in your __project_name/settings.py__ file and the database migrations shipped with the app (we’ll cover those later). You’ll see a message for each migration it applies. If you’re interested, run the command-line client for your database and type \dt (PostgreSQL), __SHOW TABLES__; (MariaDB, MySQL), **.tables** (SQLite), or __SELECT TABLE_NAME FROM USER_TABLES__; (Oracle) to display the tables Django created.

    **For the minimalists**
    
    Like we said above, the default applications are included for the common case, but not everybody needs them. If you don’t need any or all of them, feel free to comment-out or delete the appropriate line(s) from __INSTALLED_APPS__ before running **migrate**. The **migrate** command will only run migrations for apps in __INSTALLED_APPS__.


## Creating Models

  - **Philosophy**
  
  A model is the single, definitive source of information about your data. It contains the essential fields and behaviors of the data you’re storing. Django follows the DRY Principle. The goal is to define your data model in one place and automatically derive things from it. 

  In our app, we’ll create two models: **Question** and **Choice**. A **Question** has a question and a publication date. A **Choice** has two fields: the text of the choice and a vote tally. Each **Choice** is associated with a **Question**

  These concepts are represented by Python classes. Edit the `app_name/models.py` file so it looks like this:

  ```
  from django.db import models


  class Question(models.Model):
      question_text = models.CharField(max_length=200)
      pub_date = models.DateTimeField('date published')


  class Choice(models.Model):
      question = models.ForeignKey(Question, on_delete=models.CASCADE)
      choice_text = models.CharField(max_length=200)
      votes = models.IntegerField(default=0)
  ```

  Here, each model is represented by a class that subclasses __django.db.models.Model__. Each model has a number of class variables, each of which represents a database field in the model.

  Each field is represented by an instance of a **Field** class – e.g., **CharField** for character fields and **DateTimeField** for datetimes. This tells Django what type of data each field holds.

  The name of each **Field** instance (e.g. __question_text__ or __pub_date__) is the field’s name, in machine-friendly format. You’ll use this value in your Python code, and your database will use it as the column name.

  You can use an optional first positional argument to a **Field** to designate a human-readable name. That’s used in a couple of introspective parts of Django, and it doubles as documentation. If this field isn’t provided, Django will use the machine-readable name. In this example, we’ve only defined a human-readable name for __Question.pub_date__. For all other fields in this model, the field’s machine-readable name will suffice as its human-readable name.

  Some **Field** classes have required arguments. **CharField**, for example, requires that you give it a __max_length__. That’s used not only in the database schema, but in validation, as we’ll soon see.

  A **Field** can also have various optional arguments; in this case, we’ve set the **default** value of **votes** to 0.

  Finally, note a relationship is defined, using **ForeignKey**. That tells Django each **Choice** is related to a single **Question**. Django supports all the common database relationships: many-to-one, many-to-many, and one-to-one.