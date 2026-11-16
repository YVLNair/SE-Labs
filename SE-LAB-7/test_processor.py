import math

from hypothesis import given, strategies as st
import pytest

from processor import (
    compute_dispatch_throughput,
    resolve_safety_restraint_code,
    validate_height_and_fastpass,
)

INPUTS = st.one_of(st.text(), st.none())


@given(INPUTS)
def test_validate_height_and_fastpass_no_crash(value):
    try:
        result = validate_height_and_fastpass(value)
    except Exception as exc:
        assert False, f"validate_height_and_fastpass crashed for {value!r}: {exc}"
    assert isinstance(result, str)


@given(INPUTS)
def test_compute_dispatch_throughput_safe(value):
    try:
        result = compute_dispatch_throughput(value)
    except Exception as exc:
        assert False, f"compute_dispatch_throughput crashed for {value!r}: {exc}"
    assert isinstance(result, (float, str))
    assert not isinstance(result, float) or math.isfinite(result)


@given(INPUTS)
def test_resolve_safety_restraint_code_safe(value):
    try:
        result = resolve_safety_restraint_code(value)
    except Exception as exc:
        assert False, f"resolve_safety_restraint_code crashed for {value!r}: {exc}"
    assert isinstance(result, str)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("140:YES", "Height 140cm: Approved (FastPass Priority)"),
        ("100:NO", "Height 100cm: Denied (Standard Entry)"),
    ],
)
def test_validate_height_and_fastpass_valid_examples(value, expected):
    assert validate_height_and_fastpass(value) == expected


def test_compute_dispatch_throughput_valid_example():
    assert compute_dispatch_throughput("48/2.5") == 19.2


@pytest.mark.parametrize("value", ["1/0", "nan/1", "1e308/1e-308"])
def test_compute_dispatch_throughput_rejects_invalid_rates(value):
    assert isinstance(compute_dispatch_throughput(value), str)


def test_resolve_safety_restraint_code_valid_example():
    assert resolve_safety_restraint_code("CST_01") == "Over-the-Shoulder Harness"
