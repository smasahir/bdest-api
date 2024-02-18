from pydantic import BaseModel, Field


class MoleculeBase(BaseModel):
    smiles: str = Field(example="CN1CCC[C@H]1c2cccnc2")


class MoleculeCreate(MoleculeBase):
    pass


class Bond(BaseModel):
    bond_id: int
    bde: float | None = Field(None)
    bond_type: str = ("UNKNOWN")
    elements: tuple[str, str] = (("C", "C"))
    fragments: tuple[str, str] = (("*", "*"))


class Molecule(MoleculeBase):
    molecule_id: int
    bond_list: list[Bond] | None = Field([])
