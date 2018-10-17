import collections


tasks = collections.defaultdict(list)


while True:
    action = input("""a - add task
l - list tasks
d - delete task
q - quit
?""").lower()
    if action == 'q':
        break
    elif action == 'a':
        date = input("Date?")
        task = input("Task?")
        tasks[date].append(task)
    elif action == 'l':
        date = input("Date?")
        if date in tasks:
            for index, task in enumerate(tasks[date], 1):
                print(index, task)
        else:
            print("There are no tasks on this date")
    elif action == 'd':
        date = input("Date?")
        number = input("Number?")
        try:
            tasks[date].pop(int(number) - 1)
        except (KeyError, IndexError, ValueError):
            print("Incorrect input")
    else:
        print("Incorrect action")
