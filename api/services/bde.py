from fastapi import FastAPI, Depends, HTTPException
import subprocess
import api.schemas.molecule as mol_schema
import pandas as pd
import xgboost as xgb
from rdkit import Chem


def get_bonds(mol_create: mol_schema.MoleculeCreate) -> list[mol_schema.Bond]:
    mol = smiles_to_mol(mol_create.smiles)
    mol_with_h = Chem.AddHs(mol)
    df_bond_info = get_bond_info(mol_with_h)
    df_descriptor = calc_bond_descriptor(mol)

    extract_ids = extract_bond_ids_for_bde_estimation(df_bond_info)
    df_pred = df_descriptor.iloc[extract_ids]
    pred = estimate_bde(df=df_pred)
    id_bde = {k: round(float(v), 2) for k, v in zip(extract_ids, pred)}

    bonds = []
    for i, row in df_bond_info.iterrows():
        bond_id = row['id']
        bond = mol_schema.Bond(
            bond_id=bond_id,
            bond_type=row['bond_type'],
            bde=None if bond_id not in id_bde else id_bde[bond_id],
            elements=row['elements'],
            fragments=row['fragments']
        )
        bonds.append(bond)

    return bonds

def get_bond_info(mol_with_h: Chem.rdchem.Mol) -> pd.DataFrame:
    bond_info = {
        "id" : [],
        "elements": [],
        "bond_type": [],
        "is_ring": [],
        "fragments" : [],
    }
    for bond in mol_with_h.GetBonds():
        id = bond.GetIdx()
        elements = (bond.GetBeginAtom().GetSymbol(), bond.GetEndAtom().GetSymbol())
        bond_type = str(bond.GetBondType())
        is_ring = bond.IsInRing()

        # 結合が単結合かつ環状構造じゃないときに、結合を解離してフラグメントを生成
        if bond_type == "SINGLE" and not is_ring:
            fragment_mol = Chem.FragmentOnBonds(mol_with_h, [bond.GetIdx()])
            fragments = tuple(Chem.MolToSmiles(fragment_mol).split("."))
        else:
            fragments = (None, None)


        bond_info["id"].append(id)
        bond_info["elements"].append(elements)
        bond_info["bond_type"].append(bond_type)
        bond_info["is_ring"].append(is_ring)
        bond_info["fragments"].append(fragments)

    df = pd.DataFrame(bond_info)

    return df

def smiles_to_mol(smiles: str) -> Chem.rdchem.Mol:
    mol = Chem.MolFromSmiles(smiles)
    # SMILESからMolオブジェクトへの変換が成功したか確認
    if mol is None:
        raise HTTPException(
            status_code=400,
            detail=f"入力されたSMILESは不適切です: {smiles}"
        )
    # BDEの予測ができるC, H, N, O以外の元素が含まれていないか確認
    for atom in mol.GetAtoms():
        if atom.GetSymbol() not in ['C', 'H', 'N', 'O']:
            raise HTTPException(
                status_code=400,
                detail=f"分子にはC, H, N, O以外の元素が含まれています: {atom.GetSymbol()}"
            )

    return mol


def estimate_bde(df: pd.DataFrame):
    bde_model = xgb.Booster()
    bde_model.load_model('api/resources/estimate_single_bond_bde.json')
    pred = bde_model.predict(xgb.DMatrix(df))

    return pred


def calc_bond_descriptor(mol: Chem.rdchem.Mol) -> pd.DataFrame:
    """
    分子の各結合を表現する特徴量を計算する。
    """
    bond_descriptors_list = []
    jar_path = 'api/lib/TypePairBondDescriptor.jar'
    sdf_file = 'api/resources/mol.sdf'
    w = Chem.SDWriter(sdf_file)
    w.write(mol)
    w.close()
    command = ["java", "-jar", jar_path, "compact", "All", sdf_file, "true"]
    result = subprocess.run(command, capture_output=True, text=True)
    for i, line in enumerate(result.stdout.split('\n')):
        bond_descriptors = {
            "id": i,
            "descriptors": [int(v) for v in line.split()]
        }
        if len(bond_descriptors["descriptors"]) == 131:
            bond_descriptors_list.append(bond_descriptors)
    
    df = pd.DataFrame([[dict['id'], *dict['descriptors']] for dict in bond_descriptors_list])

    # 予測に使用しない列を削除
    unused_columns = [
    0, 1, 2, 7, 10, 11, 13, 14, 15, 16, 21, 24, 27, 28, 29, 30, 38,
    41, 42, 43, 44, 52, 55, 56, 57, 58, 63, 67, 70, 71, 72,
    73, 78, 82, 85, 86, 87, 88, 93, 97, 100, 101, 102, 103, 110
    ]
    df.drop(columns = unused_columns, inplace=True)
    
    return df

def extract_bond_ids_for_bde_estimation(df: pd.DataFrame) -> list[int]:
    condition = (df['bond_type'] == 'SINGLE') & (~df['is_ring'])
    ids = df.index[condition].tolist()

    return ids
