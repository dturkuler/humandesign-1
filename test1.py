#!/usr/bin/env python3

"""
Example usage of Human Design Calculator.

This script demonstrates how to use the Human Design calculator
to analyze birth data and output the results.
"""

from calculations import calculate_human_design
from utils import get_utc_offset_from_tz
import json
from datetime import datetime

def main():
    print("Human Design Calculator Example")
    print("==============================\n")
    
    # Example 1: Calculate with manual timezone offset
    print("Example 1: Calculate with manual timezone offset")
    print("-------------------------------------------------")
    
    # Birth data: February 21, 1968, 11:15 AM, UTC+3
    birth_data = (1968, 2, 21, 11, 15, 0, 3)
    
    result = calculate_human_design(birth_data)
    
    print(f"Birth Date: {result['birth_date']}")
    print(f"Design Date: {result['design_date']}")
    print(f"Energy Type: {result['energy_type']}")
    print(f"Strategy: {result['strategy']}")
    print(f"Authority: {result['authority_name']}")
    print(f"Profile: {result['profile']}")
    print(f"Incarnation Cross: {result['incarnation_cross']}")
    print(f"Defined Centers: {', '.join(result['defined_centers'])}")
    print(f"Undefined Centers: {', '.join(result['undefined_centers'])}")
    print(f"Split: {result['split']}")
    print(f"Active Channels: {', '.join(result['active_channels'])}")
    print()
    
    # Example 2: Calculate with timezone name
    print("Example 2: Calculate with timezone name")
    print("---------------------------------------")
    
    # Birth data components
    year = 1973
    month = 1
    day = 19
    hour = 11
    minute = 15
    second = 0
    timezone_name = "Europe/Istanbul"
    
    # Get the UTC offset from the timezone name
    timestamp = (year, month, day, hour, minute, second)
    offset = get_utc_offset_from_tz(timestamp, timezone_name)
    
    print(f"Calculated UTC offset for {timezone_name}: {offset}")
    
    # Calculate Human Design
    birth_data = (*timestamp, offset)
    result = calculate_human_design(birth_data, timezone_name)
    
    print(f"Birth Date: {result['birth_date']}")
    print(f"Energy Type: {result['energy_type']}")
    print(f"Authority: {result['authority_name']}")
    print(f"Profile: {result['profile']}")
    print(f"Defined Centers: {', '.join(result['defined_centers'])}")
    print()
    
    # Example 3: Access specific features
    print("Example 3: Access specific features")
    print("----------------------------------")
    
    # Calculate Human Design
    birth_data = (1935, 7, 6, 4, 48, 0, 8)  # Dalai Lama
    result = calculate_human_design(birth_data)
    
    # Access specific features
    print(f"Energy Type: {result['energy_type']}")
    print(f"Profile: {result['profile']}")
    
    # Personality gates
    print("\nPersonality Gates:")
    for gate_data in result['personality_gates']:
        print(f"  Gate {gate_data['gate']}, Line {gate_data['line']} ({gate_data['planet']})")
    
    # Design gates
    print("\nDesign Gates:")
    for gate_data in result['design_gates']:
        print(f"  Gate {gate_data['gate']}, Line {gate_data['line']} ({gate_data['planet']})")
    
    # Save the full result to a JSON file
    with open("full_result.json", "w") as f:
        json.dump(result, f, indent=2)
    
    print("\nFull result saved to full_result.json")

if __name__ == "__main__":
    main()
