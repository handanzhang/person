import py_compile
import os
import shutil

def remove_pyc(path):
    for file_name in os.listdir(path):
        if os.path.isfile(file_name):
            _, base_name = os.path.split(file_name)
            if base_name.startswith('to_pyc'):
                continue
            if base_name.endswith('.pyc'):
                os.remove(file_name)


def create_pyc(path):
    for file_name in os.listdir(path):
        if os.path.isfile(file_name):
            if os.path.split(file_name)[1].startswith('to_pyc'):
                continue
            py_compile.compile(file_name)

def move_pyc(path):
    dst_path = os.path.join(path, 'pyc')
    for file_name in os.listdir(path):
        if os.path.isfile(file_name):
            _, base_name = os.path.split(file_name)
            if base_name.startswith('to_pyc'):
                continue
            if base_name.endswith('.pyc'):
                if os.path.exists(os.path.join(dst_path, base_name)):
                    os.remove(os.path.join(dst_path, base_name))
                shutil.move(file_name, dst_path)
    

if __name__ == '__main__':
    file_path = os.path.realpath(__file__)
    path = os.path.split(file_path)[0]
    remove_pyc(path)
    create_pyc(path)
    move_pyc(path)