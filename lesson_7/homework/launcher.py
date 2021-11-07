from subprocess import Popen, CREATE_NEW_CONSOLE

PROCESS = []

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESS.append(Popen('python server.py', creationflags=CREATE_NEW_CONSOLE))
        for _ in range(1):
            PROCESS.append(Popen('python client.py -m send', creationflags=CREATE_NEW_CONSOLE))
        for _ in range(3):
            PROCESS.append(Popen('python client.py -m listen', creationflags=CREATE_NEW_CONSOLE))
    elif ACTION == 'x':
        while PROCESS:
            subproc = PROCESS.pop()
            subproc.kill()
