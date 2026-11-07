from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_monitoring_summary(
    results: pd.DataFrame,
    output_path: str | Path,
) -> Path:
    """Create and save a summary figure for valid operating scenarios."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    valid_data = results.loc[results["is_valid"]].copy()

    if valid_data.empty:
        raise ValueError("No valid operating rows are available for plotting.")

    scenario_labels = (
        valid_data["scenario"]
        .str.replace("_", " ", regex=False)
        .str.title()
    )

    x_positions = np.arange(len(valid_data))
    bar_width = 0.36

    status_colors = {
        "normal": "#2E8B57",
        "possible_fouling": "#D95F02",
        "possible_low_flow": "#377EB8",
        "energy_imbalance": "#984EA3",
        "reduced_heat_transfer": "#E6AB02",
    }

    colors = [
        status_colors.get(status, "#777777")
        for status in valid_data["diagnostic_status"]
    ]

    figure, axes = plt.subplots(1, 3, figsize=(16, 5.5))

    # Heat-duty comparison
    hot_bars = axes[0].bar(
        x_positions - bar_width / 2,
        valid_data["hot_duty_kw"],
        width=bar_width,
        label="Hot-side duty",
        color="#C44E52",
    )
    cold_bars = axes[0].bar(
        x_positions + bar_width / 2,
        valid_data["cold_duty_kw"],
        width=bar_width,
        label="Cold-side duty",
        color="#4C72B0",
    )

    axes[0].bar_label(hot_bars, fmt="%.0f", padding=3)
    axes[0].bar_label(cold_bars, fmt="%.0f", padding=3)
    axes[0].set_title("Heat-Duty Comparison")
    axes[0].set_ylabel("Heat duty (kW)")
    axes[0].set_xticks(x_positions, scenario_labels)
    axes[0].legend()

    # U relative to healthy reference
    u_bars = axes[1].bar(
        x_positions,
        valid_data["u_ratio_percent"],
        color=colors,
    )

    axes[1].bar_label(u_bars, fmt="%.1f%%", padding=3)
    axes[1].axhline(
        100.0,
        color="#333333",
        linestyle="--",
        linewidth=1.2,
        label="Healthy reference",
    )
    axes[1].axhline(
        85.0,
        color="#C44E52",
        linestyle=":",
        linewidth=1.5,
        label="Reduced-U threshold",
    )
    axes[1].set_title("Heat-Transfer Performance")
    axes[1].set_ylabel("U relative to healthy reference (%)")
    axes[1].set_xticks(x_positions, scenario_labels)
    axes[1].legend(fontsize=8)

    # Pressure-drop comparison
    hot_dp_bars = axes[2].bar(
        x_positions - bar_width / 2,
        valid_data["hot_pressure_drop_kpa"],
        width=bar_width,
        label="Hot side",
        color="#DD8452",
    )
    cold_dp_bars = axes[2].bar(
        x_positions + bar_width / 2,
        valid_data["cold_pressure_drop_kpa"],
        width=bar_width,
        label="Cold side",
        color="#55A868",
    )

    axes[2].bar_label(hot_dp_bars, fmt="%.0f", padding=3)
    axes[2].bar_label(cold_dp_bars, fmt="%.0f", padding=3)
    axes[2].set_title("Pressure-Drop Comparison")
    axes[2].set_ylabel("Pressure drop (kPa)")
    axes[2].set_xticks(x_positions, scenario_labels)
    axes[2].legend()

    for axis in axes:
        axis.grid(axis="y", linestyle="--", alpha=0.35)
        axis.set_axisbelow(True)

    invalid_count = int((~results["is_valid"]).sum())

    figure.suptitle(
        "Heat Exchanger Monitoring Summary",
        fontsize=16,
        fontweight="bold",
    )
    figure.text(
        0.5,
        0.01,
        f"Valid scenarios shown; invalid rows excluded: {invalid_count}",
        ha="center",
        fontsize=9,
        color="#555555",
    )

    figure.tight_layout(rect=(0, 0.04, 1, 0.94))
    figure.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(figure)

    return output_path