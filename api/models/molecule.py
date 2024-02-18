from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

from api.db import Base


class Molecule(Base):
    __tablename__="molecules"

    molecule_id = Column(Integer, primary_key=True)
    smiles = Column(String)

    bonds = relationship("Bond", back_populates="molecule", cascade="delete")


class Bond(Base):
    __tablename__ = 'bonds'

    molecule_id = Column(Integer, ForeignKey('molecules.molecule_id'), primary_key=True)
    bond_id = Column(Integer, primary_key=True)
    bde = Column(Float)
    bond_type = Column(String)
    elements = Column(ARRAY(String))
    fragments = Column(ARRAY(String))

    molecule = relationship("Molecule", back_populates="bonds")
