from pathlib import Path

import pandas as pd

from .analysis import analyze_operating_data
from .data_io import load_operating_data
from .diagnostics import screen_faults


def run_monitoring_pipeline(
    input_csv: str | Path,
    output_csv: str | Path | None = None,
    reference_scenario: str = "healthy",
) -> pd.DataFrame:
    """Run the complete heat-exchanger monitoring pipeline."""
    data = load_operating_data(input_csv)
    analyzed_data = analyze_operating_data(data)
    results = screen_faults(
        analyzed_data,
        reference_scenario=reference_scenario,
    )

    if output_csv is not None:
        output_path = Path(output_csv)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        results.to_csv(output_path, index=False)

    return results