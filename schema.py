import datetime
import pathlib
from dataclasses import dataclass


@dataclass
class PathHelper(object):
    full_path: pathlib.Path
    prefix: pathlib.Path
    name: str

    @classmethod
    def to_python(cls, file_path: str):
        path = pathlib.Path(file_path)
        return cls(
            full_path=path,
            prefix=path.parent,
            name=path.name
        )

    def path_dirs(self) -> pathlib.Path:
        return self.prefix.parent

    def path(self, namedir: str):
        return self.path_dirs().joinpath(namedir).joinpath(self.name)

    def path_in(self):
        return self.path_dirs("in")

    def path_out(self):
        """ Возвращяет путь для сохранения в формате json """
        return self.path_dirs().joinpath("out").joinpath(self.name[:-3] + "json")

    def path_ok(self):
        """ Возвращяет путь для сохранения ok """
        return self.path_dirs().joinpath("ok")

    def path_err(self):
        """ Возвращяет путь для сохранения err """
        return self.path_dirs().joinpath("err")

    def __str__(self):
        return str(self.full_path)


@dataclass
class FlightFromName(object):
    file_path: PathHelper
    filename: str
    flt: int
    dep: str
    date: datetime.date

    @classmethod
    def to_python(cls, file_path):
        # Извлекаем номер рейса и аэропорт вылета из имени файла
        path = PathHelper.to_python(file_path)
        flt, dep = path.name.split('_')[1:3]
        return cls(
            file_path=path,
            filename=path.name,
            flt=int(flt),
            date=datetime.datetime.strptime(path.name[:8], "%Y%m%d").date(),
            dep=dep[:-4]
        )
