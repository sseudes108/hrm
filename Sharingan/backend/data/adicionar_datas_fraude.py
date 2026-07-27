"""Adiciona datas de ocorrência distribuídas de forma reprodutível ao dataset."""

from datetime import date, datetime, time
from pathlib import Path

import numpy as np
import pandas as pd


DATA_PATH = Path(__file__).resolve().parent / "dados_fraude.csv"
START_DATE = date(2026, 1, 1)
SEED = 20260726


def main() -> None:
    dataframe = pd.read_csv(DATA_PATH)
    end_of_today = datetime.combine(date.today(), time.max)
    start = datetime.combine(START_DATE, time.min)
    if end_of_today < start:
        raise ValueError("A data atual não pode ser anterior a 01/01/2026.")

    generator = np.random.default_rng(SEED)
    total_seconds = int((end_of_today - start).total_seconds())
    offsets = generator.integers(0, total_seconds + 1, len(dataframe))
    dataframe["occurred_at"] = [
        (start + pd.Timedelta(seconds=int(offset))).isoformat(timespec="seconds")
        for offset in offsets
    ]

    temporary = DATA_PATH.with_suffix(".tmp")
    dataframe.to_csv(temporary, index=False)
    temporary.replace(DATA_PATH)
    print(f"{len(dataframe)} propostas datadas entre {START_DATE.isoformat()} e {date.today().isoformat()}.")


if __name__ == "__main__":
    main()
