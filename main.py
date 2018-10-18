import collections
import functools
import pickle
import json
import configparser

import arrow.parser


config = configparser.ConfigParser()
config.read('todo.ini')
format = config['Serializer']['format']


def load_pickle():
    try:
        with open('tasks.pickle', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return collections.defaultdict(list)


def save_pickle(obj):
    with open('tasks.pickle', 'wb') as f:
        pickle.dump(obj, f)


def load_json():
    try:
        with open('tasks.json', 'rt') as f:
            return json.load(f, object_hook=lambda dct: collections.defaultdict(list, dct))
    except FileNotFoundError:
        return collections.defaultdict(list)


def save_json(obj):
    with open('tasks.json', 'wt') as f:
        json.dump(obj, f)


if format == 'pickle':
    load, save = load_pickle, save_pickle
elif format == 'json':
    load, save = load_json, save_json
else:
    raise ImportError


tasks = load()


def validate_date(f):
    @functools.wraps(f)
    def wrapper(date, *args):
        try:
            arrow.get(date, 'DD.MM.YYYY')
        except arrow.parser.ParserError:
            raise ValueError('Incorrect date')
        return f(date, *args)
    return wrapper


@validate_date
def add(date, task):
    tasks[date].append(task)
    save(tasks)


@validate_date
def list_(date):
    if date in tasks and tasks[date]:
        return [(index, task) for index, task in enumerate(tasks[date], 1)]
    else:
        raise ValueError("There are no tasks on this date")


@validate_date
def delete(date, number):
    try:
        tasks[date].pop(int(number) - 1)
    except (KeyError, IndexError, ValueError):
        raise ValueError("Incorrect input")
    save(tasks)


def add_task():
    date = input("Date?")
    task = input("Task?")
    add(date, task)


def list_tasks():
    date = input("Date?")
    for index, task in list_(date):
        print("{}. {}".format(index, task))


def delete_task():
    date = input("Date?")
    number = input("Number?")
    delete(date, number)


def default():
    print("Incorrect action")


actions = {
    'a': add_task,
    'l': list_tasks,
    'd': delete_task,
    'q': exit,
}

while True:
    action = input("""a - add task
l - list tasks
d - delete task
q - quit
?""").lower()
    try:
        actions.get(action, default)()
    except ValueError as e:
        print(e)