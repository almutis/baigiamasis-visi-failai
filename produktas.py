from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
import datetime

engine = create_engine('sqlite:///prooduktai.db')
Base = declarative_base()  # su ()


class Produktas(Base):
    __tablename__ = 'Produktas'
    id = Column(Integer, primary_key=True)  # PRIMARY KEY
    preke = Column("PREKE", String)
    kaina = Column("KAINA", String)
    akcija = Column("AKCIJA", Boolean)
    idejimo_data = Column("DATA", DateTime, default=datetime.datetime.now)

    def __init__(self, preke, kaina, akcija):
        self.preke = preke
        self.kaina = kaina
        self.akcija = akcija

    def __repr__(self):
        return f"{self.id} {self.preke} {self.kaina} {self.akcija}  {self.idejimo_data}"


Base.metadata.create_all(engine)