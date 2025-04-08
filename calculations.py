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

from constants import (
    ICHING_OFFSET, SWE_PLANET_DICT, ICHING_CIRCLE_LIST, CHAKRA_LIST,
    GATES_CHAKRA_DICT, CHANNEL_MEANING_DICT, IC_CROSS_TYP,
    STRATEGY_BY_TYPE, AUTHORITY_DESCRIPTIONS
)
from utils import timestamp_to_juldate, calc_create_date, julian_to_datetime

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
                )
                break
    
    # Update ch_gate in the dictionary
    date_to_gate_dict["ch_gate"] = ch_gate_list
    
    # Filter dictionary for active channels (ch_gate is not 0)
    mask = np.array(date_to_gate_dict["ch_gate"]) != 0
    
    # Remove duplicates (e.g., (1,2) = (2,1))
    sorted_channels = [sorted((date_to_gate_dict["gate"][i], date_to_gate_dict["ch_gate"][i])) 
                      for i in range(len(date_to_gate_dict["gate"]))]
    unique_indices = np.unique(sorted_channels, axis=0, return_index=True)[1]
    dupl_mask = np.zeros(len(sorted_channels), dtype=bool)
    dupl_mask[unique_indices] = True
    
    # Filter useful keys to result dict
    active_channels_dict = {}
    for key in ["label", "planets", "gate", "ch_gate"]:
        active_channels_dict[key] = np.array(date_to_gate_dict[key])[dupl_mask & mask]
    
    # Map chakras to gates in new columns
    active_channels_dict["gate_chakra"] = [FULL_DICT["full_gate_chakra_dict"][key] 
                                         for key in active_channels_dict["gate"]]
    active_channels_dict["ch_gate_chakra"] = [FULL_DICT["full_gate_chakra_dict"][key] 
                                            for key in active_channels_dict["ch_gate"]]
    
    # Map labels to gates and channel gates
    gate = active_channels_dict["gate"]
    ch_gate = active_channels_dict["ch_gate"]
    
    gate_label_list = []
    ch_gate_label_list = []
    
    # Convert gates and channel gates to tuple format (1,2)
    for g, ch_g in zip(gate, ch_gate):
        idx_gate = np.where(np.array(date_to_gate_dict['gate']) == g)[0]
        idx_ch_gate = np.where(np.array(date_to_gate_dict['gate']) == ch_g)[0]
        
        gate_labels = [date_to_gate_dict["label"][int(i)] for i in idx_gate]
        ch_gate_labels = [date_to_gate_dict["label"][int(i)] for i in idx_ch_gate]
        
        gate_label_list.append(gate_labels)
        ch_gate_label_list.append(ch_gate_labels)
    
    active_channels_dict["ch_gate_label"] = ch_gate_label_list
    active_channels_dict["gate_label"] = gate_label_list
    
    # Add channel meanings if available
    channels = np.column_stack((active_channels_dict["gate"], active_channels_dict["ch_gate"]))
    
    # Create a full meaning dictionary (normal and reversed)
    full_meaning_dict = {**CHANNEL_MEANING_DICT, 
                        **{key[::-1]: value for key, value in CHANNEL_MEANING_DICT.items()}}
    
    # Get meanings for each channel
    meanings = []
    for channel in channels:
        channel_tuple = tuple(channel)
        meaning = full_meaning_dict.get(channel_tuple, ["Unknown", "Unknown"])
        meanings.append(meaning)
    
    active_channels_dict["meaning"] = meanings
    
    return active_channels_dict, set(active_centers)

def is_connected(active_channels_dict, *args):
    """
    Check if chakras are connected through a channel.
    Direct and indirect connections are supported.
    
    Args:
        active_channels_dict (dict): All active channels
        *args: Chakras to check for connection
    
    Returns:
        bool: True if connected, False otherwise
    """
    # If gate list is empty (Reflector), return False
    if not len(active_channels_dict["gate"]):
        return False
    
    # Check if any gates connect the specified chakras
    gate_chakra_mask = np.array([chakra in args for chakra in active_channels_dict["gate_chakra"]])
    ch_gate_chakra_mask = np.array([chakra in args for chakra in active_channels_dict["ch_gate_chakra"]])
    
    # If gate and channel gate in the same line, they are connected
    mask = gate_chakra_mask & ch_gate_chakra_mask
    
    # For 2 elements need 1 connection, for 3 elements need 2 connections, etc.
    if sum(mask) >= len(args) - 1:
        return True
    
    return False

def get_component(active_channels_dict, chakra):
    """
    Helper function to get the component of a chakra in active channels.
    
    Args:
        active_channels_dict (dict): Dictionary containing channel connections.
        chakra (str): The chakra label to check.
    
    Returns:
        str: Component identifier or None
    """
    # This is a placeholder function for the energy type calculation
    # In a real implementation, this would determine the connected component
    # the chakra belongs to
    return active_channels_dict.get(chakra, None)

def get_energy_type(active_channels_dict, active_centers):
    """
    Determine the Human Design energy type based on defined centers and channels.
    
    Args:
        active_channels_dict (dict): All active channels
        active_centers (set): All active/defined centers
    
    Returns:
        str: Energy Type
    """
    # No active centers => Reflector
    if len(active_centers) == 0:
        return "REFLECTOR"
    
    # Case: Sacral is undefined (can be Manifestor or Projector)
    if "SL" not in active_centers:
        # If Throat is undefined, it must be a Projector
        if "TT" not in active_centers:
            return "PROJECTOR"
        
        # Check connections from motor centers (HT, SP, RT) to throat (=> Manifestor)
        if "HT" in active_centers and is_connected(active_channels_dict, "HT", "TT"):
            return "MANIFESTOR"
        if "SP" in active_centers and is_connected(active_channels_dict, "SP", "TT"):
            return "MANIFESTOR"
        if "RT" in active_centers and is_connected(active_channels_dict, "RT", "TT"):
            return "MANIFESTOR"
        
        # If no motor center is connected to the throat, it's a Projector
        return "PROJECTOR"
    
    # Case: Sacral is defined (can be Generator or Manifesting Generator)
    if "TT" not in active_centers:
        return "GENERATOR"
    
    # Check connections from motor centers to throat (=> Manifesting Generator)
    if "HT" in active_centers and is_connected(active_channels_dict, "HT", "TT"):
        return "MANIFESTING GENERATOR"
    if "SP" in active_centers and is_connected(active_channels_dict, "SP", "TT"):
        return "MANIFESTING GENERATOR"
    if "RT" in active_centers and is_connected(active_channels_dict, "RT", "TT"):
        return "MANIFESTING GENERATOR"
    if is_connected(active_channels_dict, "SL", "TT"):
        return "MANIFESTING GENERATOR"
    
    # No connection to throat => Generator
    return "GENERATOR"

def get_authority(active_centers, active_channels_dict):
    """
    Determine the inner authority based on defined centers
    
    Args:
        active_centers (set): Defined/active centers
        active_channels_dict (dict): All active channels
    
    Returns:
        str: Inner authority code
    """
    outer_auth_conditions = (
        "HD" in active_centers or 
        "AA" in active_centers or 
        "TT" in active_centers or 
        len(active_centers) == 0
    )
    
    if "SP" in active_centers:
        auth = "SP"  # Emotional Authority
    elif "SL" in active_centers:
        auth = "SL"  # Sacral Authority
    elif "SN" in active_centers:
        auth = "SN"  # Splenic Authority
    elif is_connected(active_channels_dict, "HT", "TT"):
        auth = "HT"  # Ego-Manifested Authority
    elif is_connected(active_channels_dict, "GC", "TT"):
        auth = "GC"  # Self-Projected Authority
    elif "GC" in active_centers and "HT" in active_centers:
        auth = "HT_GC"  # Ego-Projected Authority
    elif len(active_centers) == 0:
        auth = "lunar"  # Lunar Authority (for Reflectors)
    elif outer_auth_conditions:
        auth = "outher_auth"  # No Inner Authority
    else:
        auth = "unknown"  # Fallback
    
    return auth

def get_incarnation_cross(date_to_gate_dict):
    """
    Get the Incarnation Cross from Sun and Earth gates
    
    Args:
        date_to_gate_dict (dict): Output of date_to_gate function
    
    Returns:
        str: Incarnation Cross description
    """
    df = date_to_gate_dict
    idx = int(len(df["planets"]) / 2)  # Start index of design values
    
    inc_cross = (
        (df["gate"][0], df["gate"][1]),  # Sun & Earth gate at birth
        (df["gate"][idx], df["gate"][idx+1])  # Sun & Earth gate at design
    )
    
    profile = df["line"][0], df["line"][idx]
    
    # Get cross type (RAC, LAC, JXP)
    if profile in IC_CROSS_TYP:
        cr_typ = IC_CROSS_TYP[profile]
    else:
        # Try reversed profile
        profile_rev = profile[::-1]
        cr_typ = IC_CROSS_TYP.get(profile_rev, "Unknown")
    
    inc_cross_str = f"({inc_cross[0][0]},{inc_cross[0][1]})-({inc_cross[1][0]},{inc_cross[1][1]})-{cr_typ}"
    
    return inc_cross_str

def get_profile(date_to_gate_dict):
    """
    Get the Profile from Sun line of birth and design
    
    Args:
        date_to_gate_dict (dict): Output of date_to_gate function
    
    Returns:
        tuple: Profile, e.g., (1, 4)
    """
    df = date_to_gate_dict
    idx = int(len(df["line"]) / 2)  # Start idx of design values
    
    profile = (df["line"][0], df["line"][idx])  # Sun line at birth and design
    
    # Sort lines to known format
    if profile not in IC_CROSS_TYP.keys():
        profile = profile[::-1]
    
    return profile

def get_variables(date_to_gate_dict):
    """
    Get variables based on tones of Sun and Nodes
    
    Args:
        date_to_gate_dict (dict): Output of date_to_gate function
    
    Returns:
        dict: Variables for arrows
    """
    df = date_to_gate_dict
    idx = int(len(df["tone"]) / 2)  # Start idx of design values
    
    tones = (
        df["tone"][0],     # Sun at birth
        df["tone"][3],     # Node at birth
        df["tone"][idx],   # Sun at design
        df["tone"][idx+3]  # Node at design
    )
    
    keys = ["right_up", "right_down", "left_up", "left_down"]  # arrows, variables
    variables = {keys[i]: "left" if tone <= 3 else "right" for i, tone in enumerate(tones)}
    
    return variables

def get_split(active_channels_dict, active_centers):
    """
    Calculate split definition from active channels and chakras
    
    Args:
        active_channels_dict (dict): All active channels
        active_centers (set): Active/defined centers
    
    Returns:
        int: Split value
    """
    # Extract gate chakras
    gate_chakra = active_channels_dict["gate_chakra"]
    ch_gate_chakra = active_channels_dict["ch_gate_chakra"]
    
    # Create sorted chakra pairs to remove duplicates
    sorted_chakras = [sorted((gate_chakra[i], ch_gate_chakra[i])) 
                    for i in range(len(active_channels_dict["gate_chakra"]))]
    
    # Get unique chakra pairs
    unique_indices = np.unique(sorted_chakras, axis=0, return_index=True)[1]
    dupl_mask = np.zeros(len(sorted_chakras), dtype=bool)
    dupl_mask[unique_indices] = True
    
    len_no_dupl_channel = sum(dupl_mask)
    
    # Calculate split
    # If centers - channels = 0, there's no split (single connected component)
    # If > 0, it indicates multiple disconnected components
    split = len(active_centers) - len_no_dupl_channel
    
    return split

def get_strategy(energy_type):
    """
    Get the strategy based on energy type
    
    Args:
        energy_type (str): Human Design energy type
    
    Returns:
        str: Strategy description
    """
    return STRATEGY_BY_TYPE.get(energy_type, "Unknown")

def get_channel_meanings(active_channels_dict):
    """
    Get descriptions for active channels
    
    Args:
        active_channels_dict (dict): All active channels
    
    Returns:
        list: Channel descriptions
    """
    channels = np.column_stack((active_channels_dict["gate"], active_channels_dict["ch_gate"]))
    
    # Create a full meaning dictionary (normal and reversed)
    full_meaning_dict = {**CHANNEL_MEANING_DICT, 
                        **{key[::-1]: value for key, value in CHANNEL_MEANING_DICT.items()}}
    
    channel_meanings = []
    for channel in channels:
        channel_tuple = tuple(channel)
        if channel_tuple in full_meaning_dict:
            meaning = full_meaning_dict[channel_tuple]
            channel_meanings.append({
                "channel": f"{channel[0]}/{channel[1]}",
                "name": meaning[0],
                "description": meaning[1]
            })
    
    return channel_meanings
