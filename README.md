# django generator

django generator is a small code generator to generate basic functionality of websites


## Quick start
1. install the package using "pip install git+git://github.com/ahmadiga/django-generator.git" or "pip install django-generator"
2. Add "django_generator" to your INSTALLED_APPS setting.

## What can i do with this?
Basically this package contains two django management commands:
1. Generate_app <APP NAME>: which creates a scaffold a new app following [django-starterkit](https://github.com/ahmadiga/django-starterkit) Guidelines
2. Generate_views <APP NAME>: which generate code for basic CRUD operations for every model in the app models including urls,admins,templates and crispy forms.

## How to use the package
1. Install the package using the steps above
2. Run `python manage.py generate_app <APP NAME>`
3. Add your django models in `<APP NAME>/models.py`
4. Run `python manage.py generate_views <APP NAME>`
5. You will find all new codes as commented lines of codes inside there specified files
6. Uncomment what is needed and delete what is not.
7. Import any missing libraries.

PS: The code generator will append commented codes at the end of each file
PS 2: code generator will generate the following:
1.List view for each model
2.Add/edit view for each model
3.Detail view for each model item
4.All forms are rendered using crispy forms and validated with django-parsly
