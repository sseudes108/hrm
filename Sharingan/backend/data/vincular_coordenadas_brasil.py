"""Vincula cada registro de fraude a uma coordenada real de município brasileiro.

O vínculo é propositalmente sintético, porém determinístico: o mesmo ID sempre
recebe o mesmo município para uma mesma seed. Não representa o endereço real de
um cliente e serve apenas para posicionamento geográfico consistente no dashboard.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


DATA_DIR = Path(__file__).resolve().parent
FRAUD_PATH = DATA_DIR / "dados_fraude.csv"
BRAZIL_PATH = DATA_DIR / "brasil.csv"
LOCATION_COLUMNS = ["ibge", "municipio", "latitude", "longitude", "estado", "uf", "regiao"]


def load_locations() -> pd.DataFrame:
    locations = pd.read_csv(BRAZIL_PATH, usecols=LOCATION_COLUMNS)
    locations = locations.dropna(subset=["latitude", "longitude", "ibge"]).drop_duplicates("ibge")
    if locations.empty:
        raise ValueError("brasil.csv não contém municípios com coordenadas válidas.")
    return locations.reset_index(drop=True)


def enrich(seed: int) -> pd.DataFrame:
    frauds = pd.read_csv(FRAUD_PATH)
    required_columns = {"id", "lat", "lng"}
    missing = required_columns.difference(frauds.columns)
    if missing:
        raise ValueError(f"dados_fraude.csv sem as colunas obrigatórias: {sorted(missing)}")

    locations = load_locations()
    generator = np.random.default_rng(seed)
    location_indexes = generator.integers(0, len(locations), size=len(frauds))
    assigned_locations = locations.iloc[location_indexes].reset_index(drop=True)

    frauds = frauds.copy()
    frauds["lat"] = assigned_locations["latitude"].to_numpy()
    frauds["lng"] = assigned_locations["longitude"].to_numpy()
    frauds["ibge"] = assigned_locations["ibge"].astype("int64").to_numpy()
    frauds["municipio"] = assigned_locations["municipio"].to_numpy()
    frauds["uf"] = assigned_locations["uf"].to_numpy()
    frauds["estado"] = assigned_locations["estado"].to_numpy()
    frauds["regiao"] = assigned_locations["regiao"].to_numpy()
    return frauds


def validate(frauds: pd.DataFrame) -> None:
    locations = load_locations()
    required_columns = {"lat", "lng", "ibge", "municipio", "uf", "estado", "regiao"}
    missing = required_columns.difference(frauds.columns)
    if missing:
        raise ValueError(f"Dados enriquecidos sem as colunas esperadas: {sorted(missing)}")

    if frauds[list(required_columns)].isna().any().any():
        raise ValueError("Foram encontradas coordenadas ou metadados geográficos vazios.")

    reference = locations.rename(columns={"latitude": "lat", "longitude": "lng"})
    merged = frauds.merge(
        reference,
        on=["ibge", "municipio", "uf", "estado", "regiao", "lat", "lng"],
        how="left",
        indicator=True,
    )
    unmatched = (merged["_merge"] != "both").sum()
    if unmatched:
        raise ValueError(f"{unmatched} registros não correspondem a municípios de brasil.csv.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Vincula fraudes a municípios reais do Brasil.")
    parser.add_argument("--seed", type=int, default=20260726, help="Seed para distribuição reprodutível.")
    parser.add_argument("--check", action="store_true", help="Valida o CSV atual sem reescrevê-lo.")
    args = parser.parse_args()

    if args.check:
        current = pd.read_csv(FRAUD_PATH)
        validate(current)
        print(f"Validação concluída: {len(current)} fraudes com coordenadas reais de municípios brasileiros.")
        return

    enriched = enrich(args.seed)
    validate(enriched)

    temporary_path = FRAUD_PATH.with_suffix(".tmp")
    enriched.to_csv(temporary_path, index=False)
    temporary_path.replace(FRAUD_PATH)
    print(f"{len(enriched)} fraudes vinculadas a {enriched['ibge'].nunique()} municípios reais.")


if __name__ == "__main__":
    main()
