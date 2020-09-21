#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import datetime
import time
from threading import Thread


class GenRecipeList(Thread):

    def __init__(self):
        Thread.__init__(self, target=self.loop)
        self.daemon = True
        self.start()

    def loop(self):
        while True:
            now = datetime.datetime.now()
            if now.strftime("%H:%M") == '00:00':
                from hybrid_rec import gen_recipes_lists
                gen_recipes_lists()
            time.sleep(60)


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplom.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    gen_recipe_list = GenRecipeList()
    main()
