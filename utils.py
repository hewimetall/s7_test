import db
from schema import FlightFromDB

def parsing_to_db(file_path):
    # Извлекаем номер рейса и аэропорт вылета из имени файла
    ff = FlightFromDB.to_python(file_path)
    con = db.get_db()
    db.insert_flight(con, ff.filename, ff.flt, ff.dep, ff.date)
    con.close()
