"""
Human Design calculations module.

This module provides the core functions for calculating Human Design features
based on a person's birth data. It includes calculations for:

- Energy Type
- Authority
- Defined/Undefined Centers
- Profile
- Gates and Channels
- Incarnation Cross
- Split Definition
- And other Human Design characteristics
"""

import swisseph as swe
import numpy as np
from datetime import datetime
from typing import Dict, List, Set, Tuple, Any, Union

from .constants import (
    ICHING_OFFSET, SWE_PLANET_DICT, ICHING_CIRCLE_LIST, CHAKRA_LIST,
    GATES_CHAKRA_DICT, CHANNEL_MEANING_DICT, IC_CROSS_TYP,
    STRATEGY_BY_TYPE, AUTHORITY_DESCRIPTIONS
)
from .utils import timestamp_to_juldate, calc_create_date, julian_to_datetime

# Pre-calculate the full dictionaries once for efficiency
def _calc_full_gates_chakra_dict(gates_chakra_dict):
    """
    From GATES_CHAKRA_DICT add keys in reversed order ([1,2]==[2,1])
    """
    cols = [
        "full_ch_chakra_list",  # Chakra & Ch_Chakra of all channels
        "full_ch_list",         # All channels
        "full_ch_gates_chakra_dict",  # Dict channels:chakra
        "full_chakra_1_list",   # Col 1 of full_chakra_list
        "full_chakra_2_list",   # Col 2 of full_chakra_list
        "full_gate_1_list",     # Col 1 of full_ch_list
        "full_gate_2_list",     # Col 2 of full_ch_list
        "full_gate_chakra_dict"  # Dict gate:chakra
    ]
    
    # Initialize dict
    full_dict = {k: [] for k in cols}
    
    # Channels in normal and reversed order
    full_dict["full_ch_chakra_list"] = list(gates_chakra_dict.values()) + [item[::-1] for item in gates_chakra_dict.values()]
    
    # Channel gates in normal and reversed order
    full_dict["full_ch_list"] = list(gates_chakra_dict.keys()) + [item[::-1] for item in gates_chakra_dict.keys()]
    
    # Make dict from channels and channel chakras e.g. (1,2):("XX","YY")
    full_dict["full_ch_gates_chakra_dict"] = dict(
        zip(full_dict["full_ch_list"], full_dict["full_ch_chakra_list"])
    )
    
    # Select each first chakra
    full_dict["full_chakra_1_list"] = [item[0] for item in full_dict["full_ch_chakra_list"]]
    
    # Select each second chakra
    full_dict["full_chakra_2_list"] = [item[1] for item in full_dict["full_ch_chakra_list"]]
    
    # Select each first gate
    full_dict["full_gate_1_list"] = [item[0] for item in full_dict["full_ch_list"]]
    
    # Select each second gate (channel gate)
    full_dict["full_gate_2_list"] = [item[1] for item in full_dict["full_ch_list"]]
    
    # Make dict from first gate and first chakra list
    full_dict["full_gate_chakra_dict"] = dict(
        zip(full_dict["full_gate_1_list"], full_dict["full_chakra_1_list"])
    )
    
    return full_dict

# Create the full dictionary globally
FULL_DICT = _calc_full_gates_chakra_dict(GATES_CHAKRA_DICT)

def date_to_gate(jdut, label):
    """
    Calculate the Human Design gates, lines, colors, tones, and bases
    from planetary positions (longitude).
    
    Args:
        jdut (float): Timestamp in Julian day format
        label (str): Indexing for "prs" (personality) or "des" (design) values
    
    Returns:
        dict: Dict containing calculated values
    """
    # Synchronize zodiac and I-Ching circle (58°)
    offset = ICHING_OFFSET
    
    result_dict = {
        k: [] for k in ["label", "planets", "lon", "gate", "line", 
                        "color", "tone", "base", "ch_gate"]
    }
    
    for planet, planet_code in SWE_PLANET_DICT.items():
        xx = swe.calc_ut(jdut, planet_code)
        long = xx[0][0]
        
        # Earth is in opposite position from Sun
        if planet == "Earth":
            long = (long + 180) % 360
        
        # South Node is in opposite position from North Node
        elif planet == "South_Node":
            long = (long + 180) % 360
            
        angle = (long + offset) % 360
        angle_percentage = angle / 360
        
        # Convert angle to gate, line, color, tone, base
        gate = ICHING_CIRCLE_LIST[int(angle_percentage * 64)]
        line = int((angle_percentage * 64 * 6) % 6 + 1)
        color = int((angle_percentage * 64 * 6 * 6) % 6 + 1)
        tone = int((angle_percentage * 64 * 6 * 6 * 6) % 6 + 1)
        base = int((angle_percentage * 64 * 6 * 6 * 6 * 5) % 5 + 1)
        
        result_dict["label"].append(label)
        result_dict["planets"].append(planet)
        result_dict["lon"].append(long)
        result_dict["gate"].append(gate)
        result_dict["line"].append(line)
        result_dict["color"].append(color)
        result_dict["tone"].append(tone)
        result_dict["base"].append(base)
        result_dict["ch_gate"].append(0)  # Will be filled later
    
    return result_dict

def calculate_human_design(timestamp, timezone_info=None):
    """
    Calculate all Human Design features for a given birth time
    
    Args:
        timestamp (tuple): Year, month, day, hour, minute, second, timezone_offset
        timezone_info (str, optional): Timezone name (e.g., 'Europe/Berlin')
            If provided, it will override the timezone_offset in timestamp
    
    Returns:
        dict: Complete Human Design calculation results
    """
    # Validate timestamp format
    if len(timestamp) != 7:
        raise ValueError("Timestamp must be in format: (year, month, day, hour, minute, second, timezone_offset)")
    
    year, month, day, hour, minute, second, tz_offset = timestamp
    
    # Convert to Julian date
    birth_julday = timestamp_to_juldate(timestamp)
    
    # Calculate design/create date (88° before birth)
    create_julday = calc_create_date(birth_julday)
    create_date = julian_to_datetime(create_julday)
    
    # Get planetary positions for birth (personality) and design
    birth_planets = date_to_gate(birth_julday, "prs")
    design_planets = date_to_gate(create_julday, "des")
    
    # Combine birth and design data
    combined_data = {
        key: birth_planets[key] + design_planets[key] 
        for key in birth_planets.keys()
    }
    
    # Calculate channels and defined centers
    channels_dict, active_centers = get_channels_and_centers(combined_data)
    
    # Get individual Human Design features
    energy_type = get_energy_type(channels_dict, active_centers)
    authority = get_authority(active_centers, channels_dict)
    profile = get_profile(combined_data)
    incarnation_cross = get_incarnation_cross(combined_data)
    split = get_split(channels_dict, active_centers)
    variables = get_variables(combined_data)
    strategy = get_strategy(energy_type)
    
    # Calculate undefined centers
    undefined_centers = list(set(CHAKRA_LIST) - set(active_centers))
    
    # Separate personality and design gates & lines
    personality_gates = extract_personality_gates(combined_data)
    design_gates = extract_design_gates(combined_data)
    
    # Format birth and design dates for output
    birth_date_str = f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"
    design_date_str = f"{create_date[0]}-{create_date[1]:02d}-{create_date[2]:02d} {create_date[3]:02d}:{create_date[4]:02d}:{create_date[5]:02d}"
    
    # Compile the complete results
    results = {
        "birth_date": birth_date_str,
        "design_date": design_date_str,
        "energy_type": energy_type,
        "strategy": strategy,
        "authority": authority,
        "authority_name": AUTHORITY_DESCRIPTIONS.get(authority, authority),
        "profile": f"{profile[0]}/{profile[1]}",
        "incarnation_cross": incarnation_cross,
        "cross_type": incarnation_cross.split("-")[-1] if "-" in incarnation_cross else "",
        "defined_centers": list(active_centers),
        "undefined_centers": undefined_centers,
        "split": split,
        "variables": variables,
        "active_gates": [gate for gate in set(combined_data["gate"]) if gate != 0],
        "active_channels": [f"{gate}/{ch_gate}" for gate, ch_gate in zip(channels_dict["gate"], channels_dict["ch_gate"])],
        "personality_gates": personality_gates,
        "design_gates": design_gates,
        "all_gate_data": combined_data,
        "channels_data": channels_dict
    }
    
    return results

def extract_personality_gates(date_to_gate_dict):
    """
    Extract gates and lines from the personality (conscious) side
    
    Args:
        date_to_gate_dict (dict): Combined gate data dictionary
    
    Returns:
        list: Dictionary of gate numbers and lines
    """
    personality_gates = []
    for i, label in enumerate(date_to_gate_dict["label"]):
        if label == "prs":
            personality_gates.append({
                "gate": date_to_gate_dict["gate"][i],
                "line": date_to_gate_dict["line"][i],
                "planet": date_to_gate_dict["planets"][i]
            })
    return personality_gates

def extract_design_gates(date_to_gate_dict):
    """
    Extract gates and lines from the design (unconscious) side
    
    Args:
        date_to_gate_dict (dict): Combined gate data dictionary
    
    Returns:
        list: Dictionary of gate numbers and lines
    """
    design_gates = []
    for i, label in enumerate(date_to_gate_dict["label"]):
        if label == "des":
            design_gates.append({
                "gate": date_to_gate_dict["gate"][i],
                "line": date_to_gate_dict["line"][i],
                "planet": date_to_gate_dict["planets"][i]
            })
    return design_gates

def get_channels_and_centers(date_to_gate_dict):
    """
    Calculate active channels and centers from planetary gate positions
    
    Args:
        date_to_gate_dict (dict): Output from date_to_gate function
            keys: ["label", "planets", "lon", "gate", "line", "color", "tone", "base", "ch_gate"]
    
    Returns:
        tuple: (active_channels_dict, active_centers)
            - active_channels_dict: Dict of active channels
            - active_centers: Set of defined energy centers
    """
    # Get gate list
    gate_list = date_to_gate_dict["gate"]
    ch_gate_list = date_to_gate_dict["ch_gate"].copy()
    active_centers = []
    
    # Map channel gates to gates, if channel exists
    for idx, gate in enumerate(gate_list):
        ch_gate_a = FULL_DICT["full_gate_1_list"]
        ch_gate_b = FULL_DICT["full_gate_2_list"]
        
        gate_indices = np.where(np.array(ch_gate_a) == gate)[0]
        
        for index in gate_indices:
            potential_ch_gate = ch_gate_b[index]
            if potential_ch_gate in gate_list:
                ch_gate_list[idx] = potential_ch_gate
                # Add the centers associated with this gate
                active_centers.append(
                    FULL_DICT["full_chakra_1_list"][FULL_DICT["full_gate_1_list"].index(gate)]
                )
                active_centers.append(
                    FULL_DICT["full_chakra_2_list"][FULL_DICT["full_gate_2_list"].index(gate)]
