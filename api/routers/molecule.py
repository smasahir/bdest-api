from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import api.schemas.molecule as mol_schema
import api.cruds.molecule as mol_crud
from api.db import get_db
import api.services.bde as bde_service

router = APIRouter()


@router.get("/molecules", response_model=list[mol_schema.Molecule])
async def list_molecules():
    response = [
        mol_schema.Molecule(
            molecule_id=1,
            smiles="CCO",
            bond_list=[
                mol_schema.Bond(
                    bond_id=0,
                    bde=80.2)
                ]
        )
    ]

    return response


@router.post("/molecules", response_model=mol_schema.Molecule)
async def create_molecule(
    molecule_body: mol_schema.MoleculeCreate, db: Session = Depends(get_db)):
    mol = mol_crud.create_molecule(db, molecule_body)
    bonds = mol_crud.create_bonds(db, mol.molecule_id, bde_service.get_bonds(mol.smiles))

    bonds_schema = []
    for bond in bonds:
        bonds_schema.append(
            mol_schema.Bond(
            **{k: v for k, v in bond.__dict__.items() if not k.startswith('_sa_')})
        )

    mol = mol_schema.Molecule(
        molecule_id = mol.molecule_id, smiles = mol.smiles, bond_list = bonds_schema)

    return mol


@router.delete("/molecules/{molecule_id}", response_model=None)
async def delete_molecule(molecule_id: int):
    return
