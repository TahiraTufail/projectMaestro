import os

def command_executor(commands:dict):
    for command in commands.values():
        os.system(command)