import pytest
from amusement_park_ride_access import process_ride_admissions, inspect_safety_restraints

# Example test case:
def test_single_adult_family_ride():
    groups = [
        {
            "is_open": True,
            "ride_type": "family",
            "has_fast_lane": False,
            "patrons": [{"height_cm": 150, "health_warning": False, "is_child": False}]
        }
    ]
    result = process_ride_admissions(groups, 5.0)
    assert result["total_revenue"] == 10.0
    assert result["status"] == "COMPLETED"

# TODO: Add test cases to achieve 90-100% on both Line and Branch coverage!
def test_invalid_groups():
    with pytest.raises(ValueError):
        process_ride_admissions("invalid", 5.0)


def test_negative_express_pass_fee():
    with pytest.raises(ValueError):
        process_ride_admissions([], -1.0)


def test_closed_ride_is_skipped():
    groups = [
        {
            "is_open": False,
            "ride_type": "family",
            "patrons": [
                {"height_cm": 150, "health_warning": False}
            ],
        }
    ]

    result = process_ride_admissions(groups, 5.0)

    assert result == {
        "total_revenue": 0.0,
        "status": "ZERO_ADMISSIONS",
    }


def test_roller_coaster_admission():
    groups = [
        {
            "is_open": True,
            "ride_type": "roller_coaster",
            "patrons": [
                {
                    "height_cm": 150,
                    "health_warning": False,
                    "is_child": False,
                }
            ],
        }
    ]

    result = process_ride_admissions(groups, 5.0)

    assert result["total_revenue"] == 25.0
    assert result["status"] == "COMPLETED"


def test_water_ride_child_with_fast_lane():
    groups = [
        {
            "is_open": True,
            "ride_type": "water_ride",
            "has_fast_lane": True,
            "patrons": [
                {
                    "height_cm": 130,
                    "health_warning": False,
                    "is_child": True,
                }
            ],
        }
    ]

    result = process_ride_admissions(groups, 5.0)

    assert result["total_revenue"] == 15.8
    assert result["status"] == "COMPLETED"


def test_unknown_ride_type():
    groups = [
        {
            "is_open": True,
            "ride_type": "unknown",
            "patrons": [
                {"height_cm": 150, "health_warning": False}
            ],
        }
    ]

    result = process_ride_admissions(groups, 5.0)

    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_ADMISSIONS"


def test_patron_with_invalid_height():
    groups = [
        {
            "is_open": True,
            "ride_type": "family",
            "patrons": [
                {"height_cm": 0, "health_warning": False}
            ],
        }
    ]

    result = process_ride_admissions(groups, 5.0)

    assert result["status"] == "ZERO_ADMISSIONS"


def test_patron_below_minimum_height():
    groups = [
        {
            "is_open": True,
            "ride_type": "family",
            "patrons": [
                {
                    "height_cm": 100,
                    "health_warning": False,
                    "is_child": True,
                }
            ],
        }
    ]

    result = process_ride_admissions(groups, 5.0)

    assert result["status"] == "ZERO_ADMISSIONS"


def test_health_warning_on_family_ride():
    groups = [
        {
            "is_open": True,
            "ride_type": "family",
            "patrons": [
                {
                    "height_cm": 150,
                    "health_warning": True,
                    "is_child": False,
                }
            ],
        }
    ]

    result = process_ride_admissions(groups, 5.0)

    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_ADMISSIONS"


def test_health_warning_on_roller_coaster():
    groups = [
        {
            "is_open": True,
            "ride_type": "roller_coaster",
            "patrons": [
                {
                    "height_cm": 150,
                    "health_warning": True,
                    "is_child": False,
                },
                {
                    "height_cm": 150,
                    "health_warning": False,
                    "is_child": False,
                },
            ],
        }
    ]

    result = process_ride_admissions(groups, 5.0)

    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_ADMISSIONS"


def test_safety_audit_after_multiple_rejections():
    groups = [
        {
            "is_open": True,
            "ride_type": "family",
            "patrons": [
                {"height_cm": 0},
                {"height_cm": 0},
                {"height_cm": 0},
                {"height_cm": 0},
                {"height_cm": 0},
            ],
        }
    ]

    result = process_ride_admissions(groups, 5.0)

    assert result["status"] == "SAFETY_AUDIT"
    assert result["total_revenue"] == 0.0


def test_empty_restraint_data():
    assert inspect_safety_restraints([]) == "NO_DATA"


def test_safe_restraint_readings():
    readings = [
        [1, 1, 1],
        [1, 0, 1],
    ]

    assert inspect_safety_restraints(readings) == "SAFE"


def test_emergency_lock_after_two_consecutive_unlatched_readings():
    readings = [
        [1, 0, 0, 1],
    ]

    assert inspect_safety_restraints(readings) == "EMERGENCY_LOCK"


def test_unlatched_streak_resets_after_latched_reading():
    readings = [
        [0, 1, 0, 1, 0],
    ]

    assert inspect_safety_restraints(readings) == "SAFE"