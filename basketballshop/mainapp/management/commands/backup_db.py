from os import name
from adminapp.views import index
from django.apps import apps
import sys
from django.core.management.base import BaseCommand, CommandError
from collections import ChainMap

from basketballshop.settings import INSTALLED_APPS


apps.get_model('mainapp', 'Product')


def start_backup(models):
    m, n = check_models(models)
    print(m)
    if n != []:
        print(f'Такой(их) модели(ей) не существует: {n}')

    for app, models in m.items():
        for model in models:
            Model = apps.get_model(app, model)
            data = get_data_model(Model)
            name = get_filename(app, model)
            create_json_file(name, data)


def get_list_models(*args):
    list_models = []
    for model in args:
        list_models = list_models + \
            dir(model)[:dir(model).index('__builtins__')]

    return list_models


def get_apps(settings_inst_apps=[]):
    first_app = settings_inst_apps.index('mainapp')
    last_app = settings_inst_apps.index('debug_toolbar')
    return settings_inst_apps[first_app:last_app]


def get_dict_models():
    dict_models = {}
    for project_app in get_apps(INSTALLED_APPS):
        dict_models[project_app] = list(ChainMap(apps.all_models[project_app]))

    return dict_models


def check_models(models):
    dict_models = get_dict_models()
    exist_models = {}
    not_exist_models = models.copy()
    lst = []
    for model in models:
        for k in dict_models.keys():
            if model.lower() in dict_models[k]:
                if exist_models.get(k) == None:
                    exist_models[k] = []
                exist_models[k].append(model)
                not_exist_models.remove(model)
    return exist_models, not_exist_models


def get_data_model(class_modell):
    return list(class_modell.objects.all().values())


def get_filenames(exist_models={}):
    names = []
    for app, models in exist_models.items():
        for model in models:
            names.append(f'{app}/json/{model}')
    return names


def get_filename(app, model):
    return f'{app}/json/{model}'


def create_json_file(name_file, data=[]):
    with open(f'{name_file}.json', "w") as f:
        print(data, file=f)


class Command(BaseCommand):
    help = 'makes a backup copy of the model and saves it in json format'

    def add_arguments(self, parser):
        parser.add_argument('-m', '--model', help='model list input',
                            type=lambda s: [str(item) for item in s.split('+')])

    def handle(self, *args, **options):
        start_backup(options['model'])
