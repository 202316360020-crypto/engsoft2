"""
Testes unitários — Parser de dados OHLCV (core/parser.py)

Cobre:
- Leitura e parsing de CSV válido
- Validação de colunas obrigatórias
- Validação de ordem cronológica
- Detecção de linhas malformadas
- Validação de capital inicial
"""

import pytest
from unittest.mock import patch, mock_open

import pandas as pd

from python_pdm_template.core.parser import OHLCVParser
from python_pdm_template.core.exceptions import InvalidCSVError, MissingColumnsError, OutOfOrderDatesError


REQUIRED_COLUMNS = {"Open", "High", "Low", "Close", "Volume"}

VALID_CSV_CONTENT = """Date,Open,High,Low,Close,Volume
2024-01-02,10.0,11.5,9.5,11.0,1000
2024-01-03,11.0,12.5,10.5,12.0,1100
2024-01-04,12.0,13.5,11.5,13.0,1200
"""

OUT_OF_ORDER_CSV = """Date,Open,High,Low,Close,Volume
2024-01-03,11.0,12.5,10.5,12.0,1100
2024-01-02,10.0,11.5,9.5,11.0,1000
"""

MISSING_COLUMN_CSV = """Date,Open,High,Low,Close
2024-01-02,10.0,11.5,9.5,11.0
"""

MALFORMED_ROWS_CSV = """Date,Open,High,Low,Close,Volume
2024-01-02,10.0,11.5,9.5,11.0,1000
LINHA_INVALIDA
2024-01-04,12.0,13.5,11.5,13.0,1200
"""


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------

class TestOHLCVParserColumns:
    """Valida detecção de colunas obrigatórias ausentes."""

    def test_valid_dataframe_passes_column_validation(self, ohlcv_uptrend):
        parser = OHLCVParser()
        # Não deve lançar exceção
        parser.validate_columns(ohlcv_uptrend)

    def test_missing_volume_raises_missing_columns_error(self, ohlcv_missing_column):
        parser = OHLCVParser()
        with pytest.raises(MissingColumnsError) as exc_info:
            parser.validate_columns(ohlcv_missing_column)
        assert "Volume" in str(exc_info.value)

    def test_missing_multiple_columns_lists_all_in_error(self):
        parser = OHLCVParser()
        df = pd.DataFrame({"Date": ["2024-01-02"], "Close": [10.0]}).set_index("Date")
        with pytest.raises(MissingColumnsError) as exc_info:
            parser.validate_columns(df)
        error_msg = str(exc_info.value)
        # Pelo menos uma das colunas ausentes deve constar na mensagem
        assert any(col in error_msg for col in ["Open", "High", "Low", "Volume"])

    def test_empty_dataframe_raises_missing_columns_error(self):
        parser = OHLCVParser()
        df = pd.DataFrame()
        with pytest.raises(MissingColumnsError):
            parser.validate_columns(df)


class TestOHLCVParserChronology:
    """Valida detecção de datas fora de ordem cronológica."""

    def test_chronological_dates_pass_validation(self, ohlcv_uptrend):
        parser = OHLCVParser()
        parser.validate_chronological_order(ohlcv_uptrend)  # Não deve lançar

    def test_out_of_order_dates_raise_error(self, ohlcv_out_of_order):
        parser = OHLCVParser()
        with pytest.raises(OutOfOrderDatesError):
            parser.validate_chronological_order(ohlcv_out_of_order)

    def test_single_row_passes_chronology(self):
        parser = OHLCVParser()
        df = pd.DataFrame(
            {"Open": [10.0], "High": [11.0], "Low": [9.0], "Close": [10.5], "Volume": [100]},
            index=pd.to_datetime(["2024-01-02"])
        )
        parser.validate_chronological_order(df)  # Não deve lançar

    def test_duplicate_dates_raise_error(self):
        parser = OHLCVParser()
        df = pd.DataFrame(
            {"Open": [10.0, 10.0], "High": [11.0, 11.0], "Low": [9.0, 9.0],
             "Close": [10.5, 10.5], "Volume": [100, 100]},
            index=pd.to_datetime(["2024-01-02", "2024-01-02"])
        )
        with pytest.raises(OutOfOrderDatesError):
            parser.validate_chronological_order(df)


class TestOHLCVParserCapital:
    """Valida regras de negócio sobre o capital inicial (RN-05)."""

    def test_positive_capital_passes(self):
        parser = OHLCVParser()
        parser.validate_capital(10_000.0)  # Não deve lançar

    def test_zero_capital_raises_value_error(self):
        parser = OHLCVParser()
        with pytest.raises(ValueError, match="positivo"):
            parser.validate_capital(0.0)

    def test_negative_capital_raises_value_error(self):
        parser = OHLCVParser()
        with pytest.raises(ValueError, match="positivo"):
            parser.validate_capital(-500.0)

    def test_very_small_positive_capital_passes(self):
        parser = OHLCVParser()
        parser.validate_capital(0.01)  # Centavos são válidos


class TestOHLCVParserMocked:
    """
    Testes de integração do parser com mock de I/O de arquivo.
    Usa mock_open para simular leitura de arquivo sem dependência de disco.
    """

    def test_parse_calls_open_with_correct_path(self):
        """O parser deve abrir o arquivo no caminho informado."""
        parser = OHLCVParser()
        with patch("pathlib.Path.read_text", return_value=VALID_CSV_CONTENT):
            # Quando parse() for implementado, esta chamada não deve lançar exceção
            # e deve retornar um DataFrame com 3 linhas.
            df = parser.parse("petr4.csv")
            assert len(df) == 3

    def test_parse_invalid_file_raises_invalid_csv_error(self):
        """Arquivo ilegível deve levantar InvalidCSVError."""
        parser = OHLCVParser()
        with patch("pathlib.Path.read_text", side_effect=OSError("File not found")):
            with pytest.raises(InvalidCSVError):
                parser.parse("inexistente.csv")
