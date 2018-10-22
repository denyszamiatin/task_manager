import config
import tasks

tasks = tasks.Tasks(config.get_serializer())


def add_task():
    date = input("Date?")
    task = input("Task?")
    tasks.add(date, task)


def list_tasks():
    date = input("Date?")
    for index, task in tasks.list_(date):
        print("{}. {}".format(index, task))


def delete_task():
    date = input("Date?")
    number = input("Number?")
    tasks.delete(date, number)


def default():
    print("Incorrect action")


actions = {
    'a': add_task,
    'l': list_tasks,
    'd': delete_task,
    'q': exit,
}


def main():
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


if __name__ == '__main__':
    main()