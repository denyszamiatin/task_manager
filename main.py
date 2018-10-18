import collections
import functools

import arrow.parser

tasks = collections.defaultdict(list)


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


@validate_date
def list(date):
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


def add_task():
    date = input("Date?")
    task = input("Task?")
    add(date, task)


def list_tasks():
    date = input("Date?")
    for index, task in list(date):
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