import functools

import arrow.parser


def validate_date(f):
    @functools.wraps(f)
    def wrapper(self, date, *args):
        try:
            arrow.get(date, 'DD.MM.YYYY')
        except arrow.parser.ParserError:
            raise ValueError('Incorrect date')
        return f(self, date, *args)
    return wrapper


class Tasks:
    def __init__(self, serializer):
        self.serializer = serializer
        self.tasks = self.serializer.load()

    @validate_date
    def add(self, date, task):
        self.tasks[date].append(task)
        self.serializer.save(self.tasks)

    @validate_date
    def list_(self, date):
        if date in self.tasks and self.tasks[date]:
            return [(index, task) for index, task in enumerate(self.tasks[date], 1)]
        else:
            raise ValueError("There are no tasks on this date")

    @validate_date
    def delete(self, date, number):
        try:
            self.tasks[date].pop(int(number) - 1)
        except (KeyError, IndexError, ValueError):
            raise ValueError("Incorrect input")
        self.serializer.save(self.tasks)
