"""
Test script for the refactored Human Design calculation library.
This script demonstrates how to use the library to calculate and display Human Design features.
"""

import sys
import json
from datetime import datetime
from pprint import pprint

# Make sure the library is in your Python path
sys.path.append('.')

# Import the human_design library
from human_design.calculations import calculate_human_design
from human_design.utils import get_utc_offset_from_tz

def test_individual_calculation():
    """Test calculating human design features for a specific birth time"""
    
    # Birth Time Configuration
    # Format: (year, month, day, hour, minute, second)
    zone = 'Asia/Istanbul'  # Timezone for the birth location
    birth_time = (1968, 2, 21, 11, 15, 0)  # Example: February 21, 1968, 11:15 AM
    
    # Get UTC offset based on timezone and birth time
    hours = get_utc_offset_from_tz(birth_time, zone)
    
    # Combine birth time components with timezone offset
    timestamp = tuple(list(birth_time) + [hours])
    
    # Calculate Human Design Features
    results = calculate_human_design(timestamp)
    
    # Display key information
    print("\n=== HUMAN DESIGN CALCULATION RESULTS ===\n")
    print(f"Birth Date: {results['birth_date']}")
    print(f"Design Date: {results['design_date']}")
    print(f"Energy Type: {results['energy_type']}")
    print(f"Strategy: {results['strategy']}")
    print(f"Authority: {results['authority_name']} ({results['authority']})")
    print(f"Profile: {results['profile']}")
    print(f"Incarnation Cross: {results['incarnation_cross']}")
    print(f"Cross Type: {results['cross_type']}")
    print(f"Defined Centers: {', '.join(results['defined_centers'])}")
    print(f"Undefined Centers: {', '.join(results['undefined_centers'])}")
    print(f"Split Definition: {results['split']}")
    print(f"Active Gates: {', '.join(map(str, sorted(results['active_gates'])))}")
    print(f"Active Channels: {', '.join(results['active_channels'])}")
    
    print("\n=== PERSONALITY GATES & LINES ===\n")
    for gate_data in results['personality_gates']:
        print(f"Gate {gate_data['gate']}, Line {gate_data['line']} ({gate_data['planet']})")
    
    print("\n=== DESIGN GATES & LINES ===\n")
    for gate_data in results['design_gates']:
        print(f"Gate {gate_data['gate']}, Line {gate_data['line']} ({gate_data['planet']})")
    
    # Export to JSON (optional)
    with open('human_design_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\nJSON results saved to human_design_results.json")
    
    return results

def test_different_birth_dates():
    """Compare results for two different birth dates"""
    
    # Test case 1: February 21, 1968 (should be a Manifesting Generator)
    zone = 'Asia/Istanbul'
    birth_time1 = (1968, 2, 21, 11, 15, 0)
    hours1 = get_utc_offset_from_tz(birth_time1, zone)
    timestamp1 = tuple(list(birth_time1) + [hours1])
    results1 = calculate_human_design(timestamp1)
    
    # Test case 2: January 19, 1973 (should be a Generator)
    birth_time2 = (1973, 1, 19, 11, 15, 0)
    hours2 = get_utc_offset_from_tz(birth_time2, zone)
    timestamp2 = tuple(list(birth_time2) + [hours2])
    results2 = calculate_human_design(timestamp2)
    
    # Compare energy types
    print("\n=== COMPARISON OF ENERGY TYPES ===\n")
    print(f"Birth date: {birth_time1} - Energy type: {results1['energy_type']}")
    print(f"Birth date: {birth_time2} - Energy type: {results2['energy_type']}")
    
    return results1, results2

if __name__ == "__main__":
    # Run the individual test
    print("Testing individual Human Design calculation...")
    test_individual_calculation()
    
    # Run the comparison test
    print("\nTesting different birth dates...")
    results1, results2 = test_different_birth_dates()
