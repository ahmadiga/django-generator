import os
from os.path import join
from subprocess import call
from os import rename

import time

from django_generator.utils import *
from django.conf import settings

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('name', nargs='+', type=str)

    def handle(self, *args, **options):
        for name in options['name']:
            package = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')
            CURRENT_PATH = settings.BASE_DIR
            call(["tar", "xvzf", join(package, "app_template.tar.gz"), "-C", CURRENT_PATH])
            time.sleep(1)

            rename(join(CURRENT_PATH, "app_template"), join(CURRENT_PATH, name))
            replace_app_template(join(CURRENT_PATH, name), name)
            add_app_to_settings(name, CURRENT_PATH)
            self.stdout.write('APP "%s" Created' % name)
