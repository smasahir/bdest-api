import api.schemas.molecule as mol_schema


def get_bonds(mol: mol_schema.MoleculeCreate) -> list[mol_schema.Bond]:
    bonds = []

    bde = 100.5
    bond_type = "SINGLE"
    elements = ("C", "O")
    fragments = ("CCO*", "CC")
    for i in range(0, 5):
        bond = mol_schema.Bond(
            bond_id=i,
            bond_type=bond_type,
            bde=bde,
            elements=elements,
            fragments=fragments
        )
        bonds.append(bond)

    return bonds