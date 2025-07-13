# models/driver.py
from pydantic import BaseModel

class Biography(BaseModel):
    dob: str
    pob: str
    info: str
    quote: str
    hisimage: str
    carimage: str

class Driver(BaseModel):
    name: str
    team: str
    number: str
    abbrv: str
    nationality: str
    image: str
    biography: Biography
