from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.engine import Result

import api.models.molecule as mol_model
import api.schemas.molecule as mol_schema


def create_molecule(
        db: Session, mol_create: mol_schema.MoleculeCreate
        ) -> mol_model.Molecule:
    mol = mol_model.Molecule(**mol_create.dict())
    db.add(mol)
    db.commit()
    db.refresh(mol)

    return mol


def create_bonds(
        db: Session, molecule_id: int, bonds_create: list[mol_schema.Bond]
    ) -> list[mol_model.Bond]:
    bonds = []

    try:
        for bond_create in bonds_create:
            bond_dict = bond_create.dict()
            bond_dict["molecule_id"] = molecule_id
            bond = mol_model.Bond(**bond_dict)
            db.add(bond)
            bonds.append(bond)
        db.commit()
        for bond in bonds:
            db.refresh(bond)
    except:
        db.rollback()
        raise

    return bonds


def get_bonds_with_molecule(db: Session):
    result: Result = db.execute(
        select (
            mol_model.Bond,
            mol_model.Molecule
        ).outerjoin(
            mol_model.Molecule
        )
    )

    return result.all()


def get_molecule(db: Session, molecule_id: int) -> mol_model.Molecule | None:
    result: Result = db.execute(
        select(
            mol_model.Molecule
        ).filter(
            mol_model.Molecule.molecule_id == molecule_id
        )
    )

    return result.scalars().first()


def delete_molecule(db: Session, original: mol_model.Molecule) -> None:
    db.delete(original)
    db.commit()