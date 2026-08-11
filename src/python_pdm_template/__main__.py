"""Ponto de entrada em linha de comando da aplicação."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Sequence

from .core.service import (
    SimulationOptions,
    aggregate_runs,
    simulate_file,
    simulate_files,
)


def build_parser() -> argparse.ArgumentParser:
    """Cria o parser de argumentos da CLI.

    Returns:
        argparse.ArgumentParser: parser configurado com as opções da aplicação.
    """
    parser = argparse.ArgumentParser(description="QuantInvest Suite")
    parser.add_argument(
        "--file",
        "-f",
        nargs="+",
        required=False,
        help="Arquivo CSV OHLCV ou lista de arquivos para processamento em lote.",
    )
    parser.add_argument(
        "--strategy",
        "-s",
        default="Buy and Hold",
        choices=["Buy and Hold", "Cruzamento de Médias Móveis"],
        help="Estratégia de investimento.",
    )
    parser.add_argument(
        "--capital",
        "-c",
        type=float,
        default=10_000.0,
        help="Capital inicial.",
    )
    parser.add_argument("--start", help="Data inicial no formato YYYY-MM-DD.")
    parser.add_argument("--end", help="Data final no formato YYYY-MM-DD.")
    parser.add_argument(
        "--short-window",
        type=int,
        default=9,
        help="Janela curta para a estratégia de médias móveis.",
    )
    parser.add_argument(
        "--long-window",
        type=int,
        default=21,
        help="Janela longa para a estratégia de médias móveis.",
    )
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="Formato da saída.",
    )
    return parser


def _format_currency(value: float) -> str:
    return f"R$ {value:,.2f}"


def _format_result(file_path: str, result) -> str:
    lines = [
        f"Arquivo: {Path(file_path).name}",
        f"  Saldo final: {_format_currency(result.final_balance)}",
        f"  Retorno total: {result.total_return_pct:.2f}%",
        f"  Taxa de acerto: {result.win_rate_pct:.2f}%",
        f"  Max drawdown: {result.max_drawdown_pct:.2f}%",
        f"  Operações: {result.total_trades}",
    ]
    return "\n".join(lines)


def run_cli(argv: Sequence[str] | None = None) -> int:
    """Executa a CLI e retorna um código de saída.

    Retorna:
        int: código de saída 0 em caso de sucesso ou 1 em caso de erro.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.file:
        parser.error("Informe ao menos um arquivo com --file")

    file_paths = [str(Path(path)) for path in args.file]
    options = SimulationOptions(
        strategy_name=args.strategy,
        capital=args.capital,
        start_date=args.start,
        end_date=args.end,
        short_window=args.short_window,
        long_window=args.long_window,
    )

    try:
        if len(file_paths) == 1:
            run = simulate_file(file_paths[0], options)
            if args.output == "json":
                print(json.dumps(asdict(run.result), ensure_ascii=False, indent=2, default=str))
            else:
                print(_format_result(file_paths[0], run.result))
            return 0

        runs = simulate_files(file_paths, options)
        summary = aggregate_runs(runs, args.capital)

        if args.output == "json":
            payload = {
                "files": [Path(path).name for path in file_paths],
                "results": [asdict(run.result) for run in runs],
                "summary": asdict(summary),
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
        else:
            for run in runs:
                print(_format_result(run.file_path, run.result))
                print()
            print("Resumo do portfólio")
            print(f"  Saldo final: {_format_currency(summary.final_balance)}")
            print(f"  Retorno total: {summary.total_return_pct:.2f}%")
            print(f"  Taxa de acerto: {summary.win_rate_pct:.2f}%")
            print(f"  Max drawdown: {summary.max_drawdown_pct:.2f}%")
            print(f"  Operações: {summary.total_trades}")
        return 0
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        print(f"Erro: {exc}")
        return 1


def main(argv: Sequence[str] | None = None) -> None:
    """Ponto de entrada para `python -m python_pdm_template`.

    Argumentos:
        argv: Argumentos de linha de comando opcionais.

    Lança:
        SystemExit: quando a CLI finaliza com código de saída.
    """
    raise SystemExit(run_cli(argv))


if __name__ == "__main__":
    main()
