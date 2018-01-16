from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

from django_generator.form_make import Form
from django_generator.utils import *
from django_generator.view_make import View


# context = {'model': self.model,
#            "name": self.model.__name__}
# self.small_serilizer_text = render_to_string('sit_builder/small-serializer.html', context)
# self.small_serilizer_text = os.linesep.join([s for s in self.small_serilizer_text.splitlines() if s.strip()])
class Command(BaseCommand):
    help = 'Generate default CRUD operations for an app based on its models'

    def add_arguments(self, parser):
        parser.add_argument('name', nargs='+', type=str)

    def handle(self, *args, **options):
        for name in options['name']:
            forms = ""
            views = ""
            urls = ""
            admin = ""
            myapp = apps.get_app_config(name)
            for model in myapp.models.values():
                form = Form(model)
                forms += form.text
                view = View(model, name)
                views += view.view
                urls += view.urls
                admin += view.admin
            CURRENT_PATH = settings.BASE_DIR
            app_folder = join(CURRENT_PATH, name)
            my_file = open(app_folder + '/' + "forms.py", "a")
            my_file.writelines(forms)
            my_file.close()
            my_file = open(app_folder + '/' + "views.py", "a")
            my_file.writelines(views)
            my_file.close()
            my_file = open(app_folder + '/' + "urls.py", "a")
            my_file.writelines(urls)
            my_file.close()
            my_file = open(app_folder + '/' + "admin.py", "a")
            my_file.writelines(admin)
            my_file.close()
            print(forms)
