import logging
import os
import shutil


def create_directory(path: str) -> None:
    """
    Создает директорию, если ее не существует.
    :param path: Путь к директории.
    :return: None.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def move_file(source_path: str, target_dir: str) -> None:
    """
    Перемещает файл из source_path в target_dir. Если директории target_dir не существует, она создается.
    :param source_path: Путь к файлу, который нужно переместить.
    :param target_dir: Путь к директории, куда нужно переместить файл.
    :return: None.
    """
    sp = source_path.split("/")
    name = sp.pop()
    source_dir = "/".join(sp)
    if source_dir == target_dir:
        return
    create_directory(target_dir)
    if not os.path.exists(os.path.join(target_dir, name)):
        shutil.move(source_path, target_dir)
    else:
        logging.error(f"File exists:{os.path.join(target_dir, name)}")
        os.remove(source_path)

def list_files(path: str, extension: str = None) -> list:
    """
    Возвращает список файлов в директории path с расширением extension (если указано).
    :param path: Путь к директории.
    :param extension: Расширение файлов.
    :return: Список файлов.
    """
    if extension:
        return [os.path.join(path, f) for f in os.listdir(path) if f.endswith(extension)]
    else:
        return [os.path.join(path, f) for f in os.listdir(path)]


def delete_file(file_path: str) -> None:
    """
    Удаляет файл по заданному пути.
    :param file_path: Путь к файлу.
    :return: None.
    """
    os.remove(file_path)


def gen_struct(tmp):
    dirs = [
        "in",
        "out",
        "ok",
        "err"
    ]
    for dir in dirs:
        create_directory(f"{tmp}/{dir}")
