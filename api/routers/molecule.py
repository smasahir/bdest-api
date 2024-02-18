from fastapi import APIRouter

import api.schemas.molecule as mol_schema

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


@router.get("/molecules/{molecule_id}")
async def molecule(molecule_id: int):
    response = mol_schema.Molecule(
        molecule_id=molecule_id,
        smiles="CCO",
        bond_list=[
            mol_schema.Bond(
                bond_id=0,
                bde=80.2)
        ]
    )

    return response


@router.post("/molecules", response_model=mol_schema.Molecule)
async def create_molecule(molecule_body: mol_schema.MoleculeCreate):
    return mol_schema.Molecule(molecule_id=1, **molecule_body.dict())


@router.delete("/molecules/{molecule_id}", response_model=None)
async def delete_molecule(molecule_id: int):
    return
