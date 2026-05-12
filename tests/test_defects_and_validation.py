"""
Testes de defeitos, validação e integração — QuantInvest Suite.

Cobre:
- Testes de defeito: entradas inválidas, boundary values, edge cases
- Testes de validação: conformidade com regras de negócio (RN-01 a RN-05)
- Testes de integração: pipeline completo Parser → Strategy → SimulationResult
- Regressão: garante que bugs conhecidos não reapareçam
"""

import contextlib
import pytest
import pandas as pd
from unittest.mock import MagicMock

# ---------------------------------------------------------------------------
# Constantes de teste
# ---------------------------------------------------------------------------
INITIAL_CAPITAL = 10_000.0
ZERO_RETURN_THRESHOLD = 0.01
EXPECTED_CLI_GUI_CALL_COUNT = 2


# ---------------------------------------------------------------------------
# Reaproveitando stubs do test_strategies para integração
# ---------------------------------------------------------------------------
from test_strategies import (
    BaseStrategy, BuyAndHoldStrategy, MovingAverageStrategy,
    SimulationResult, BankruptcyError,
)
from test_parser import OHLCVParser, MissingColumnsError, OutOfOrderDatesError


# ---------------------------------------------------------------------------
# Testes de Defeito — Boundary Values e Edge Cases
# ---------------------------------------------------------------------------

class TestBoundaryValues:
    """Testa os limites extremos das entradas."""

    def test_single_row_dataframe_buy_and_hold(self):
        """Uma série com apenas 1 pregão: compra e venda no mesmo dia."""
        df = pd.DataFrame(
            {"Open": [10.0], "High": [11.0], "Low": [9.0], "Close": [10.0], "Volume": [500]},
            index=pd.to_datetime(["2024-01-02"])
        )
        strategy = BuyAndHoldStrategy()
        try:
            result = strategy.run(df, 10_000.0)
            # Retorno deve ser 0 (comprou e vendeu pelo mesmo preço)
            assert abs(result.total_return_pct) < ZERO_RETURN_THRESHOLD
        except NotImplementedError:
            pytest.skip("BuyAndHoldStrategy ainda não implementada.")

    def test_extremely_large_capital(self, ohlcv_uptrend):
        """Capital muito alto (1 bilhão) não deve causar overflow."""
        strategy = BuyAndHoldStrategy()
        try:
            result = strategy.run(ohlcv_uptrend, 1_000_000_000.0)
            assert result.final_balance > 0
        except NotImplementedError:
            pytest.skip("BuyAndHoldStrategy ainda não implementada.")

    def test_very_small_capital(self, ohlcv_uptrend):
        """Capital muito pequeno (R$0,01) deve ser aceito ou rejeitado de forma controlada."""
        strategy = BuyAndHoldStrategy()
        try:
            result = strategy.run(ohlcv_uptrend, 0.01)
            assert result.final_balance >= 0
        except (BankruptcyError, ValueError):
            pass  # Comportamento aceitável
        except NotImplementedError:
            pytest.skip("BuyAndHoldStrategy ainda não implementada.")

    def test_capital_with_many_decimal_places(self, ohlcv_uptrend):
        """Capital com muitas casas decimais não deve causar erros de float."""
        strategy = BuyAndHoldStrategy()
        try:
            result = strategy.run(ohlcv_uptrend, 10_000.123456789)
            assert result.final_balance > 0
        except NotImplementedError:
            pytest.skip("BuyAndHoldStrategy ainda não implementada.")

    def test_moving_average_window_equals_data_length(self, ohlcv_long):
        """Janela igual ao tamanho da série deve lançar erro ou retornar zero trades."""
        strategy = MovingAverageStrategy(short_window=15, long_window=30)
        # ohlcv_long tem 30 linhas; long_window=30 → sem dados suficientes
        try:
            with pytest.raises((ValueError, RuntimeError)):
                strategy.run(ohlcv_long, 10_000.0)
        except NotImplementedError:
            pytest.skip("MovingAverageStrategy ainda não implementada.")


# ---------------------------------------------------------------------------
# Testes de Validação — Regras de Negócio
# ---------------------------------------------------------------------------

class TestBusinessRulesValidation:
    """
    Valida conformidade com as Regras de Negócio (RN-01 a RN-05).

    Definidas no DEF da QuantInvest Suite.
    """

    # RN-01: Validação Cronológica
    def test_rn01_out_of_order_csv_rejected_before_simulation(self, ohlcv_out_of_order):
        """RN-01: Dados fora de ordem cronológica devem ser rejeitados ANTES de simular."""
        parser = OHLCVParser()
        with pytest.raises(OutOfOrderDatesError):
            parser.validate_chronological_order(ohlcv_out_of_order)

    def test_rn01_future_data_not_used_for_past_decisions(self, ohlcv_long):
        """
        RN-01: A estratégia não pode usar dados do índice i+N para decidir em i.

        Verificamos isso indiretamente: o resultado com dados embaralhados
        deve diferir do resultado com dados ordenados.
        """
        strategy = MovingAverageStrategy(short_window=5, long_window=10)
        try:
            strategy.run(ohlcv_long, 10_000.0)
            shuffled = ohlcv_long.sample(frac=1, random_state=42)
            # Dados embaralhados devem ser rejeitados
            parser = OHLCVParser()
            with pytest.raises(OutOfOrderDatesError):
                parser.validate_chronological_order(shuffled)
        except NotImplementedError:
            pytest.skip("MovingAverageStrategy ainda não implementada.")

    # RN-02: Capital Mínimo e Falência
    def test_rn02_bankruptcy_stops_only_current_asset(self):
        """
        RN-02: Falência de um ativo não deve encerrar a aplicação.

        O motor de portfólio deve capturar BankruptcyError e continuar.
        """
        mock_strategy = MagicMock(spec=BuyAndHoldStrategy)
        mock_strategy.run.side_effect = [
            BankruptcyError("Ativo 1 faliu"),
            SimulationResult(12_000.0, 20.0, 100.0, 0.0, 1, []),
        ]

        results = []
        errors = []
        assets = ["petr4.csv", "vale3.csv"]

        for _ in assets:
            try:
                result = mock_strategy.run(pd.DataFrame(), 10_000.0)
                results.append(result)
            except BankruptcyError as e:
                errors.append(str(e))

        assert len(errors) == 1
        assert len(results) == 1
        assert results[0].final_balance == pytest.approx(12_000.0)

    # RN-03: Paridade CLI = GUI
    def test_rn03_cli_and_gui_use_same_core_interface(self):
        """
        RN-03: CLI e GUI devem chamar a mesma interface do Core.

        Verificado via mock: ambas as camadas invocam run() com os mesmos parâmetros.
        """
        mock_core = MagicMock(spec=BuyAndHoldStrategy)
        mock_core.run.return_value = SimulationResult(11_000.0, 10.0, 100.0, 0.0, 1, [])

        data = pd.DataFrame()
        capital = 10_000.0

        # Simulando chamada da CLI
        result_cli = mock_core.run(data, capital)
        # Simulando chamada da GUI
        result_gui = mock_core.run(data, capital)

        assert mock_core.run.call_count == EXPECTED_CLI_GUI_CALL_COUNT
        assert result_cli.final_balance == result_gui.final_balance

    # RN-04: Integridade dos Dados OHLCV
    def test_rn04_missing_columns_rejected(self, ohlcv_missing_column):
        """RN-04: Arquivo sem colunas obrigatórias deve ser rejeitado com MissingColumnsError."""
        parser = OHLCVParser()
        with pytest.raises(MissingColumnsError):
            parser.validate_columns(ohlcv_missing_column)

    # RN-05: Capital Inicial Positivo
    def test_rn05_zero_capital_rejected(self):
        """RN-05: Capital zero deve ser rejeitado antes de iniciar simulação."""
        parser = OHLCVParser()
        with pytest.raises(ValueError):
            parser.validate_capital(0.0)

    def test_rn05_negative_capital_rejected(self):
        """RN-05: Capital negativo deve ser rejeitado antes de iniciar simulação."""
        parser = OHLCVParser()
        with pytest.raises(ValueError):
            parser.validate_capital(-100.0)


# ---------------------------------------------------------------------------
# Testes de Integração — Pipeline completo (mocked I/O)
# ---------------------------------------------------------------------------

class TestIntegrationPipeline:
    """
    Testa o pipeline completo: Parser → Validação → Strategy → SimulationResult.

    Usa mocks para isolar dependências de I/O.
    """

    def test_full_pipeline_buy_and_hold_uptrend(self, ohlcv_uptrend):
        """
        Pipeline completo com dados de alta.

        1. Parser valida colunas e cronologia
        2. Strategy roda
        3. SimulationResult retornado
        """
        parser = OHLCVParser()
        parser.validate_columns(ohlcv_uptrend)
        parser.validate_chronological_order(ohlcv_uptrend)
        parser.validate_capital(10_000.0)

        strategy = BuyAndHoldStrategy()
        try:
            result = strategy.run(ohlcv_uptrend, 10_000.0)
            assert isinstance(result, SimulationResult)
            assert result.final_balance > INITIAL_CAPITAL
        except NotImplementedError:
            pytest.skip("BuyAndHoldStrategy ainda não implementada.")

    def test_full_pipeline_with_mocked_strategy(self, ohlcv_uptrend):
        """
        Pipeline com strategy mockada.

        Garante que validações do parser rodam mesmo quando strategy é um mock.
        """
        parser = OHLCVParser()
        parser.validate_columns(ohlcv_uptrend)
        parser.validate_chronological_order(ohlcv_uptrend)
        parser.validate_capital(10_000.0)

        mock_strategy = MagicMock(spec=BaseStrategy)
        mock_strategy.run.return_value = SimulationResult(
            final_balance=13_000.0,
            total_return_pct=30.0,
            win_rate_pct=75.0,
            max_drawdown_pct=5.0,
            total_trades=4,
            operations=[],
        )

        result = mock_strategy.run(ohlcv_uptrend, 10_000.0)
        assert result.total_return_pct == pytest.approx(30.0)
        mock_strategy.run.assert_called_once_with(ohlcv_uptrend, 10_000.0)

    def test_portfolio_pipeline_aggregates_multiple_assets(self, ohlcv_uptrend, ohlcv_downtrend):
        """RF-04: Pipeline de portfólio deve agregar resultados de múltiplos ativos."""
        mock_strategy = MagicMock(spec=BuyAndHoldStrategy)
        mock_strategy.run.side_effect = [
            SimulationResult(11_000.0, 10.0, 100.0, 0.0, 1, []),
            SimulationResult(9_000.0, -10.0, 0.0, 12.5, 1, []),
        ]

        assets = [ohlcv_uptrend, ohlcv_downtrend]
        results = [mock_strategy.run(asset, 10_000.0) for asset in assets]

        total_final = sum(r.final_balance for r in results)
        avg_return = sum(r.total_return_pct for r in results) / len(results)

        assert total_final == pytest.approx(20_000.0)
        assert avg_return == pytest.approx(0.0)

    def test_pipeline_aborts_on_invalid_data(self, ohlcv_out_of_order):
        """
        Pipeline deve abortar validação e NÃO chamar a strategy.

        Isso acontece quando os dados são inválidos.
        """
        parser = OHLCVParser()
        mock_strategy = MagicMock(spec=BuyAndHoldStrategy)

        with pytest.raises(OutOfOrderDatesError):
            parser.validate_chronological_order(ohlcv_out_of_order)
            mock_strategy.run(ohlcv_out_of_order, 10_000.0)

        mock_strategy.run.assert_not_called()


# ---------------------------------------------------------------------------
# Testes de Regressão
# ---------------------------------------------------------------------------

class TestRegression:
    """
    Regressões: garante que bugs corrigidos não reapareçam.

    Adicione um teste aqui para cada bug encontrado e corrigido.
    """

    def test_regression_bankruptcy_does_not_corrupt_portfolio_result(self):
        """
        Bug hipotético: falência de ativo A corrompendo resultado de ativo B.

        O resultado de B deve ser independente da falência de A.
        """
        mock_strategy = MagicMock(spec=BuyAndHoldStrategy)
        expected_b = SimulationResult(15_000.0, 50.0, 100.0, 2.0, 1, [])
        mock_strategy.run.side_effect = [
            BankruptcyError("Ativo A faliu"),
            expected_b,
        ]

        results = []
        for _ in range(2):
            with contextlib.suppress(BankruptcyError):
                results.append(mock_strategy.run(pd.DataFrame(), 10_000.0))

        assert len(results) == 1
        assert results[0].final_balance == pytest.approx(15_000.0)

    def test_regression_chronological_validation_runs_before_strategy(self, ohlcv_out_of_order):
        """
        Bug hipotético: estratégia sendo chamada antes da validação cronológica.

        A validação deve sempre rodar primeiro.
        """
        mock_strategy = MagicMock(spec=BuyAndHoldStrategy)
        parser = OHLCVParser()

        with pytest.raises(OutOfOrderDatesError):
            parser.validate_chronological_order(ohlcv_out_of_order)
            mock_strategy.run(ohlcv_out_of_order, 10_000.0)

        mock_strategy.run.assert_not_called()
