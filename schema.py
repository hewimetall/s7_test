import datetime
from dataclasses import dataclass

@dataclass
class FlightFromDB(object):
    file_path: str
    filename:str
    flt:int
    dep:str
    date: datetime.date

    @classmethod
    def to_python(cls, file_path):
        # Извлекаем номер рейса и аэропорт вылета из имени файла

        filename = file_path.split('/')[-1]
        flt, dep = filename.split('_')[1:3]
        return cls(
            file_path = file_path,
            filename = filename,
            flt = int(flt),
            date = datetime.datetime.strptime(filename[:8], "%Y%m%d").date(),
            dep = dep[:-4]
        )