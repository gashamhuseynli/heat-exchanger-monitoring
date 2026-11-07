from heat_exchanger_monitoring.pipeline import run_monitoring_pipeline
from heat_exchanger_monitoring.visualization import create_monitoring_summary


def test_create_monitoring_summary(tmp_path):
    results = run_monitoring_pipeline(
        "data/synthetic_operating_data.csv"
    )

    output_path = tmp_path / "monitoring_summary.png"

    returned_path = create_monitoring_summary(
        results,
        output_path,
    )

    assert returned_path == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0