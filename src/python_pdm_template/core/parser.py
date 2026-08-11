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
        """Lê um CSV de disco e retorna um DataFrame indexado por data.

        Args:
            filepath: caminho do arquivo CSV.

        Returns:
            pd.DataFrame: dados OHLCV indexados por data.

        Raises:
            InvalidCSVError: se o arquivo não puder ser lido ou o conteúdo for inválido.
        """
        try:
            content = Path(filepath).read_text(encoding="utf-8")
        except OSError as exc:
            raise InvalidCSVError(f"Não foi possível ler o arquivo: {filepath}") from exc

        return self.parse_from_string(content)

    def parse_from_string(self, csv_content: str) -> pd.DataFrame:
        """Lê um CSV a partir de uma string.

        Args:
            csv_content: conteúdo CSV em texto.

        Returns:
            pd.DataFrame: dados OHLCV indexados por data.

        Raises:
            InvalidCSVError: se o conteúdo CSV for inválido ou estiver faltando a coluna Date.
        """
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

    @classmethod
    def validate_columns(cls, frame: pd.DataFrame) -> None:
        """Garante a presença das colunas obrigatórias.

        Args:
            frame: DataFrame a ser validado.

        Raises:
            MissingColumnsError: se alguma coluna obrigatória estiver ausente.
        """
        missing_columns = cls.REQUIRED_COLUMNS - set(frame.columns)
        if missing_columns:
            raise MissingColumnsError(f"Colunas ausentes: {', '.join(sorted(missing_columns))}")

    @staticmethod
    def validate_chronological_order(frame: pd.DataFrame) -> None:
        """Garante ordenação cronológica estrita.

        Args:
            frame: DataFrame com índice de datas.

        Raises:
            OutOfOrderDatesError: se as datas não estiverem em ordem ou estiverem duplicadas.
        """
        if frame.index.duplicated().any() or not frame.index.is_monotonic_increasing:
            raise OutOfOrderDatesError("Datas fora de ordem cronológica ou duplicadas.")

    @staticmethod
    def validate_capital(capital: float) -> None:
        """Garante que o capital inicial é positivo.

        Args:
            capital: capital inicial a ser validado.

        Raises:
            ValueError: se o capital inicial for menor ou igual a zero.
        """
        if capital <= 0:
            raise ValueError("O capital inicial deve ser estritamente positivo.")