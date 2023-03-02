from datetime import datetime

from pydantic import BaseModel, Field


class FlightModel(BaseModel):
    hex: str
    reg_number: str
    flag: str = None
    lat: float = None
    lng: float = None
    alt: int = None
    dir: int = None
    speed: float = None
    v_speed: float = None
    squawk: str = None
    flight_number: str = None
    flight_icao: str = None
    flight_iata: str = None
    dep_icao: str
    dep_iata: str
    arr_icao: str
    arr_iata: str
    airline_icao: str = None
    airline_iata: str = None
    aircraft_icao: str = None
    updated: datetime
    status: str

    parsed: datetime = Field(default_factory=datetime.now)
