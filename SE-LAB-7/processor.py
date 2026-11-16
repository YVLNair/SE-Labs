"""Input validation helpers for the Amusement Park Ride Access lab."""

import math


def validate_height_and_fastpass(rider_spec):
    """Validate a ``height:fastpass`` value and return a rider decision."""
    if not isinstance(rider_spec, str):
        return "Invalid rider specification: expected HEIGHT:YES or HEIGHT:NO."

    parts = rider_spec.strip().split(":")
    if len(parts) != 2:
        return "Invalid rider specification: expected HEIGHT:YES or HEIGHT:NO."

    height_str, pass_str = (part.strip() for part in parts)
    try:
        height = int(height_str)
    except (TypeError, ValueError):
        return "Invalid rider specification: height must be a whole number."

    if height < 0:
        return "Invalid rider specification: height cannot be negative."

    pass_value = pass_str.upper()
    if pass_value not in {"YES", "NO"}:
        return "Invalid rider specification: fastpass must be YES or NO."

    has_fastpass = pass_value == "YES"
    eligible = height >= 120
    status = "FastPass Priority" if has_fastpass else "Standard Entry"
    decision = "Approved" if eligible else "Denied"
    return f"Height {height}cm: {decision} ({status})"


def compute_dispatch_throughput(ride_metric_str):
    """Return riders per minute from ``riders/minutes`` or an error message."""
    if not isinstance(ride_metric_str, str):
        return "Invalid ride metric: expected RIDERS/MINUTES."

    parts = ride_metric_str.strip().split("/")
    if len(parts) != 2:
        return "Invalid ride metric: expected RIDERS/MINUTES."

    try:
        riders, cycle_minutes = (float(part.strip()) for part in parts)
    except (TypeError, ValueError):
        return "Invalid ride metric: riders and minutes must be numbers."

    if not math.isfinite(riders) or not math.isfinite(cycle_minutes):
        return "Invalid ride metric: values must be finite numbers."
    if riders < 0:
        return "Invalid ride metric: riders cannot be negative."
    if cycle_minutes <= 0:
        return "Invalid ride metric: cycle minutes must be greater than zero."

    rate = riders / cycle_minutes
    if not math.isfinite(rate):
        return "Invalid ride metric: throughput must be a finite number."

    return round(rate, 2)


def resolve_safety_restraint_code(zone_code):
    """Resolve a known ride-zone prefix or return a useful error message."""
    if not isinstance(zone_code, str):
        return "Unknown ride zone code."

    prefix = zone_code.strip().upper()[:3]
    restraint_types = {
        "CST": "Over-the-Shoulder Harness",
        "WTR": "Lap Bar and Seatbelt",
        "DRP": "Hydraulic Shoulder Vest",
        "WHL": "Manual Safety Bar",
    }
    return restraint_types.get(prefix, "Unknown ride zone code.")


def main():
    print("==== Running validate_height_and_fastpass ====")
    rider_spec = input("Enter rider spec (Height:FastPass, e.g. 140:YES): ")
    print(validate_height_and_fastpass(rider_spec))

    print("\n==== Running compute_dispatch_throughput ====")
    ride_metric = input("Enter riders/mins (e.g. 48/2.5): ")
    print("Throughput (riders/min):", compute_dispatch_throughput(ride_metric))

    print("\n==== Running resolve_safety_restraint_code ====")
    zone_code = input("Enter ride zone code (e.g. CST_01, WTR_A): ")
    print("Restraint:", resolve_safety_restraint_code(zone_code))


if __name__ == "__main__":
    main()
