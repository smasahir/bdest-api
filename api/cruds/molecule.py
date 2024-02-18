from sqlalchemy.orm import Session

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