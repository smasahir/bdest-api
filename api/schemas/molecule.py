from pydantic import BaseModel, Field


class MoleculeBase(BaseModel):
    smiles: str = Field(example="CN1CCC[C@H]1c2cccnc2")


class MoleculeCreate(MoleculeBase):
    pass


class Bond(BaseModel):
    bond_id: int


class BDE(BaseModel):
    bond_id: int
    bde: float

    class Config:
        orm_mode = True


class Molecule(MoleculeBase):
    molecule_id: int
    bde_list: list[BDE] = Field([])

    class Config:
        orm_mode = True
