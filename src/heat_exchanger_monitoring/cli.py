import argparse
from pathlib import Path

from .pipeline import run_monitoring_pipeline


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Analyze heat-exchanger operating data and perform "
            "explainable rule-based fault screening."
        )
    )

    parser.add_argument(
        "input_csv",
        type=Path,
        help="Path to the input operating-data CSV file.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/analysis_results.csv"),
        help="Path for the generated results CSV.",
    )

    parser.add_argument(
        "--reference",
        default="healthy",
        help="Scenario used as the healthy reference.",
    )

    return parser


def main() -> None:
    """Run the monitoring pipeline from the command line."""
    parser = build_parser()
    args = parser.parse_args()

    results = run_monitoring_pipeline(
        input_csv=args.input_csv,
        output_csv=args.output,
        reference_scenario=args.reference,
    )

    display_columns = [
        "timestamp",
        "scenario",
        "is_valid",
        "hot_duty_kw",
        "cold_duty_kw",
        "u_w_m2_k",
        "diagnostic_status",
    ]

    print("\nHeat-exchanger monitoring results:\n")
    print(results[display_columns].to_string(index=False))
    print(f"\nFull results saved to: {args.output}")


if __name__ == "__main__":
    main()