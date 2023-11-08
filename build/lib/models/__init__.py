from models.engine.dbs_manager import DBSManager
from repository.hotel_reservation_crud_port import HotelReservationCrudPort
storage: HotelReservationCrudPort = DBSManager()
#storage = DBSManager()
storage.reload()