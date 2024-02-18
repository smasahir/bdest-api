from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import api.schemas.molecule as mol_schema
import api.cruds.molecule as mol_crud
import api.models.molecule as mol_model
from api.db import get_db
import api.services.bde as bde_service

router = APIRouter()


@router.get("/molecules", response_model=list[mol_schema.Molecule])
async def list_molecules(db: Session = Depends(get_db)):
    bonds = mol_crud.get_bonds_with_molecule(db)

    molecule_dict = {}
    for bond in bonds:
        id = bond.Bond.molecule_id
        if id in molecule_dict.keys():
            molecule_dict[id].bond_list.append(bond_model_to_schema(bond.Bond))
        else:
            mol = bond.Molecule
            molecule_dict[id] = mol_schema.Molecule(
                molecule_id=mol.molecule_id,
                smiles=mol.smiles,
                bond_list = [bond_model_to_schema(bond.Bond)]
            )

    response = [v for v in molecule_dict.values()]

    return response


@router.post("/molecules", response_model=mol_schema.Molecule)
async def create_molecule(
    molecule_body: mol_schema.MoleculeCreate, db: Session = Depends(get_db)):
    mol = mol_crud.create_molecule(db, molecule_body)
    bonds = mol_crud.create_bonds(db, mol.molecule_id, bde_service.get_bonds(mol.smiles))

    bonds_schema = []
    for bond in bonds:
        bonds_schema.append(bond_model_to_schema(bond))

    mol = mol_schema.Molecule(
        molecule_id = mol.molecule_id, smiles = mol.smiles, bond_list = bonds_schema)

    return mol


@router.delete("/molecules/{molecule_id}", response_model=None)
async def delete_molecule(molecule_id: int, db: Session = Depends(get_db)):
    mol = mol_crud.get_molecule(db, molecule_id=molecule_id)
    if mol is None:
        raise HTTPException(status_code=404, detail="Molecule not found")

    return mol_crud.delete_molecule(db, original=mol)


def bond_model_to_schema(bond: mol_model.Bond) -> mol_schema.Bond:
    result = mol_schema.Bond(
            **{k: v for k, v in bond.__dict__.items() if not k.startswith('_sa_')}
    )

    return result
