"""Leitura e validação de dados OHLCV."""

from __future__ import annotations

from io import StringIO
from pathlib import Path

import pandas as pd

from .exceptions import InvalidCSVError, MissingColumnsError, OutOfOrderDatesError


class OHLCVParser:
    """Parser de arquivos CSV com colunas OHLCV."""

    REQUIRED_COLUMNS = {"Open", "High", "Low", "Close", "Volume"}

    def parse(self, filepath: str) -> pd.DataFrame:
        """Lê um CSV de disco e retorna um DataFrame indexado por data."""
        try:
            content = Path(filepath).read_text(encoding="utf-8")
        except OSError as exc:
            raise InvalidCSVError(f"Não foi possível ler o arquivo: {filepath}") from exc

        return self.parse_from_string(content)

    def parse_from_string(self, csv_content: str) -> pd.DataFrame:
        """Lê um CSV a partir de uma string."""
        try:
            frame = pd.read_csv(StringIO(csv_content), on_bad_lines="skip")
        except Exception as exc:  # pragma: no cover - pandas boundary
            raise InvalidCSVError("CSV inválido.") from exc

        if "Date" not in frame.columns:
            raise InvalidCSVError("CSV precisa conter a coluna Date.")

        frame["Date"] = pd.to_datetime(frame["Date"], errors="coerce")
        frame = frame.dropna(subset=["Date"])
        frame = frame.set_index("Date")

        self.validate_columns(frame)
        self.validate_chronological_order(frame)
        return frame

    def validate_columns(self, frame: pd.DataFrame) -> None:
        """Garante a presença das colunas obrigatórias."""
        missing_columns = self.REQUIRED_COLUMNS - set(frame.columns)
        if missing_columns:
            raise MissingColumnsError(f"Colunas ausentes: {', '.join(sorted(missing_columns))}")

    def validate_chronological_order(self, frame: pd.DataFrame) -> None:
        """Garante ordenação cronológica estrita."""
        if frame.index.duplicated().any() or not frame.index.is_monotonic_increasing:
            raise OutOfOrderDatesError("Datas fora de ordem cronológica ou duplicadas.")

    def validate_capital(self, capital: float) -> None:
        """Garante que o capital inicial é positivo."""
        if capital <= 0:
            raise ValueError("O capital inicial deve ser estritamente positivo.")