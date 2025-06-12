"""
Sample test data for use in tests
"""

# Sample weapons data
SAMPLE_WEAPONS = [
    {"id": 1, "weapon": "Remington 700", "caliber": "7.62 mm"},
    {"id": 2, "weapon": "Barrett M82", "caliber": "12.7 mm"},
    {"id": 3, "weapon": "Accuracy International", "caliber": "0.308 in"},
]

# Sample ammunition data
SAMPLE_AMMUNITION = [
    {"id": 1, "ammunition": "Federal Match", "caliber": "7.62 mm"},
    {"id": 2, "ammunition": "Hornady ELD-M", "caliber": "7.62 mm"},
    {"id": 3, "ammunition": "Winchester Match", "caliber": "0.308 in"},
]

# Sample distances data
SAMPLE_DISTANCES = [
    {"id": 1, "distance": "100", "unit": "m"},
    {"id": 2, "distance": "200", "unit": "m"},
    {"id": 3, "distance": "300", "yd"},
]

# Sample results data
SAMPLE_RESULTS = [
    {"id": 1, "weapon_id": 1, "ammunition_id": 1, "distance_id": 1, "result": "15"},
    {"id": 2, "weapon_id": 1, "ammunition_id": 1, "distance_id": 2, "result": "25"},
    {"id": 3, "weapon_id": 2, "ammunition_id": 2, "distance_id": 1, "result": "20"},
]

# Test scenarios for click calculations
CALCULATION_SCENARIOS = [
    {"current": 10, "target": 25, "expected_clicks": 15, "expected_direction": "up"},
    {"current": 25, "target": 10, "expected_clicks": 15, "expected_direction": "down"},
    {"current": 15, "target": 15, "expected_clicks": 0, "expected_direction": None},
    {"current": 0, "target": 10, "expected_clicks": 10, "expected_direction": "up"},
    {"current": -5, "target": 5, "expected_clicks": 10, "expected_direction": "up"},
]

# Validation test cases
VALIDATION_TEST_CASES = {
    "numbers": {
        "valid": ["123", "0", "-123", "+456"],
        "invalid": ["abc", "12.3", "", " ", "12a3"]
    },
    "decimals": {
        "valid": ["123", "12.3", "0.5", "-12.3", "+45.6"],
        "invalid": ["abc", "", "12.3.4", "12a.3"]
    },
    "names": {
        "valid": ["Remington 700", "Federal Match", "M24", "Test-Name_123"],
        "invalid": ["", "   ", "a" * 101, "Name@#$"]
    },
    "calibers": {
        "valid": ["7.62 mm", "0.308 in", "9 mm", "0.22 in"],
        "invalid": ["invalid", "7.62", "mm 7.62", "7.62 cm"]
    }
}
