from heat_exchanger_monitoring.data_io import load_operating_data
from heat_exchanger_monitoring.validation import validate_operating_data


def test_validation_marks_bad_sensor_row_invalid():
    data = load_operating_data("data/synthetic_operating_data.csv")

    validated_data = validate_operating_data(data)

    assert validated_data["is_valid"].tolist() == [
        True,
        True,
        True,
        False,
    ]
    assert "terminal temperature differences" in validated_data.loc[
        3, "validation_message"
    ]


def test_validation_rejects_nonpositive_area():
    data = load_operating_data("data/synthetic_operating_data.csv")
    data.loc[0, "area_m2"] = 0.0

    validated_data = validate_operating_data(data)

    assert not validated_data.loc[0, "is_valid"]
    assert "must be positive" in validated_data.loc[
        0, "validation_message"
    ]