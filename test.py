"""
Test script for Human Design Calculator.

This script tests the functionality of the Human Design calculation package
by verifying results for known birth dates.
"""

import sys
import json
from datetime import datetime

# Try to import the human_design package 
try:
    from calculations import calculate_human_design
    from utils import get_utc_offset_from_tz
except ImportError:
    print("Human Design package not found. Make sure it's installed or in the PYTHONPATH.")
    print("If you're running this script directly from the project directory,")
    print("try: PYTHONPATH=. python test.py")
    sys.exit(1)

# Test cases with known results for validation
TEST_CASES = [
    {
        "name": "Test Case 1: Manifesting Generator",
        "birth_data": (1968, 2, 21, 11, 15, 0, 3),  # UTC+3
        "timezone_name": "Europe/Istanbul",
        "expected": {
            "energy_type": "MANIFESTING GENERATOR",
            "authority": "SP"  # Emotional Authority
        }
    },
    {
        "name": "Test Case 2: Generator",
        "birth_data": (1973, 1, 19, 11, 15, 0, 3),  # UTC+3
        "timezone_name": "Europe/Istanbul",
        "expected": {
            "energy_type": "GENERATOR",
            "authority": "SL"  # Sacral Authority
        }
    },
    {
        "name": "Test Case 3: Dalai Lama - Projector",
        "birth_data": (1935, 7, 6, 4, 48, 0, 8),  # UTC+8
        "timezone_name": "Asia/Shanghai",
        "expected": {
            "energy_type": "PROJECTOR"
        }
    },
]

def run_tests():
    """Run all test cases and verify results."""
    total_tests = 0
    passed_tests = 0
    
    for test_case in TEST_CASES:
        print(f"\n{test_case['name']}")
        print("-" * len(test_case['name']))
        
        # Get the birth data
        birth_data = test_case["birth_data"]
        timezone_name = test_case.get("timezone_name")
        
        # If timezone_name is provided, recalculate the offset
        if timezone_name:
            try:
                # Get year, month, day, hour, minute, second from birth_data
                timestamp = birth_data[:6]
                offset = get_utc_offset_from_tz(timestamp, timezone_name)
                birth_data = (*timestamp, offset)
                print(f"Using timezone: {timezone_name} (UTC{'+' if offset >= 0 else ''}{offset})")
            except Exception as e:
                print(f"Error calculating timezone offset: {e}")
        
        try:
            # Calculate the Human Design
            result = calculate_human_design(birth_data, timezone_name)
            
            # Print summary of results
            print(f"Birth Date: {result['birth_date']}")
            print(f"Design Date: {result['design_date']}")
            print(f"Energy Type: {result['energy_type']}")
            print(f"Authority: {result['authority_name']}")
            print(f"Profile: {result['profile']}")
            print(f"Incarnation Cross: {result['incarnation_cross']}")
            print(f"Defined Centers: {', '.join(result['defined_centers'])}")
            print(f"Channels: {', '.join(result['active_channels'])}")
            
            # Verify expected results
            expected = test_case.get("expected", {})
            
            for key, expected_value in expected.items():
                total_tests += 1
                actual_value = result.get(key)
                
                if actual_value == expected_value:
                    print(f"✓ {key}: {actual_value}")
                    passed_tests += 1
                else:
                    print(f"✗ {key}: Expected {expected_value}, got {actual_value}")
            
        except Exception as e:
            print(f"Error calculating Human Design: {e}")
    
    # Print summary
    print("\n" + "=" * 50)
    print(f"Test Summary: {passed_tests}/{total_tests} tests passed")
    
    return passed_tests == total_tests

def test_api():
    """Test the API functionality if available."""
    try:
        from fastapi.testclient import TestClient
        from human_design.api import app
        
        client = TestClient(app)
        
        print("\nTesting API")
        print("-" * 20)
        
        # Test the main calculation endpoint
        test_data = {
            "year": 1968,
            "month": 2,
            "day": 21,
            "hour": 11,
            "minute": 15,
            "second": 0,
            "timezone": 3,
            "timezone_name": "Europe/Istanbul"
        }
        
        response = client.post("/calculate", json=test_data)
        
        if response.status_code == 200:
            print("✓ API /calculate endpoint works")
            response_data = response.json()
            print(f"  Energy Type: {response_data['energy_type']}")
            print(f"  Authority: {response_data['authority_name']}")
        else:
            print(f"✗ API /calculate endpoint failed: {response.status_code}")
            print(response.json())
        
        # Test a specific feature endpoint
        response = client.post("/energy-type", json=test_data)
        
        if response.status_code == 200:
            print("✓ API /energy-type endpoint works")
            print(f"  Result: {response.json()}")
        else:
            print(f"✗ API /energy-type endpoint failed: {response.status_code}")
            print(response.json())
            
        return response.status_code == 200
        
    except ImportError:
        print("FastAPI or TestClient not available. Skipping API tests.")
        return True
    except Exception as e:
        print(f"Error testing API: {e}")
        return False

def save_example_output():
    """Generate and save example output for documentation."""
    # Calculate for a sample birth date
    birth_data = (1968, 2, 21, 11, 15, 0, 3)  # Feb 21, 1968, 11:15 AM, UTC+3
    result = calculate_human_design(birth_data)
    
    # Save to a JSON file
    with open("example_output.json", "w") as f:
        json.dump(result, f, indent=2)
    
    print("\nSaved example output to example_output.json")

if __name__ == "__main__":
    print("Human Design Calculator Test Suite")
    print("================================\n")
    
    # Run the main tests
    all_tests_passed = run_tests()
    
    # Test the API if available
    api_test_passed = test_api()
    
    # Save example output
    try:
        save_example_output()
    except Exception as e:
        print(f"Error saving example output: {e}")
    
    # Exit with appropriate code
    if all_tests_passed and api_test_passed:
        print("\nAll tests passed!")
        sys.exit(0)
    else:
        print("\nSome tests failed.")
        sys.exit(1)
