"""
Human Design API.

This module provides a FastAPI implementation for the Human Design calculation
system, offering endpoints to calculate various Human Design features.
"""

from fastapi import FastAPI, HTTPException, Query, Depends
from typing import Optional, List
from pytz import all_timezones
import datetime

from .models import (
    BirthData, HumanDesignResponse, EnergyTypeResponse, AuthorityResponse,
    ProfileResponse, DefinedCentersResponse, UndefinedCentersResponse,
    SplitResponse, CrossResponse, ChannelsResponse, GatesResponse,
    VariablesResponse
)

from .calculations import calculate_human_design, get_channel_meanings
from .utils import get_utc_offset_from_tz

app = FastAPI(
    title="Human Design API",
    description="API for calculating Human Design features",
    version="1.0.0",
)

def validate_birth_data(birth_data: BirthData):
    """Validate birth data and convert to timestamp format."""
    # Validate date and time
    try:
        date = datetime.datetime(
            birth_data.year, birth_data.month, birth_data.day,
            birth_data.hour, birth_data.minute, birth_data.second
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date or time: {str(e)}")
    
    # Handle timezone
    if birth_data.timezone_name:
        if birth_data.timezone_name not in all_timezones:
            raise HTTPException(status_code=400, detail=f"Invalid timezone name: {birth_data.timezone_name}")
        try:
            tz_offset = get_utc_offset_from_tz(
                (birth_data.year, birth_data.month, birth_data.day,
                 birth_data.hour, birth_data.minute, birth_data.second),
                birth_data.timezone_name
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error calculating timezone offset: {str(e)}")
    elif birth_data.timezone is not None:
        tz_offset = birth_data.timezone
    else:
        raise HTTPException(status_code=400, detail="Either timezone or timezone_name must be provided")
    
    # Return as timestamp tuple
    return (birth_data.year, birth_data.month, birth_data.day,
            birth_data.hour, birth_data.minute, birth_data.second, tz_offset)

@app.post("/calculate", response_model=HumanDesignResponse, tags=["Human Design"])
async def calculate_human_design_chart(birth_data: BirthData):
    """Calculate the complete Human Design chart based on birth data."""
    timestamp = validate_birth_data(birth_data)
    
    try:
        result = calculate_human_design(timestamp, birth_data.timezone_name)
        
        # Get channel meanings for a better response
        channel_meanings = get_channel_meanings(result["channels_data"])
        result["active_channels"] = [cm["channel"] for cm in channel_meanings]
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.post("/energy-type", response_model=EnergyTypeResponse, tags=["Features"])
async def get_energy_type_and_strategy(birth_data: BirthData):
    """Get the energy type and strategy based on birth data."""
    timestamp = validate_birth_data(birth_data)
    
    try:
        result = calculate_human_design(timestamp, birth_data.timezone_name)
        return {
            "energy_type": result["energy_type"],
            "strategy": result["strategy"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.post("/authority", response_model=AuthorityResponse, tags=["Features"])
async def get_authority(birth_data: BirthData):
    """Get the inner authority based on birth data."""
    timestamp = validate_birth_data(birth_data)
    
    try:
        result = calculate_human_design(timestamp, birth_data.timezone_name)
        return {
            "authority": result["authority"],
            "authority_name": result["authority_name"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.post("/profile", response_model=ProfileResponse, tags=["Features"])
async def get_profile(birth_data: BirthData):
    """Get the profile based on birth data."""
    timestamp = validate_birth_data(birth_data)
    
    try:
        result = calculate_human_design(timestamp, birth_data.timezone_name)
        return {"profile": result["profile"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.post("/defined-centers", response_model=DefinedCentersResponse, tags=["Features"])
async def get_defined_centers(birth_data: BirthData):
    """Get the defined centers based on birth data."""
    timestamp = validate_birth_data(birth_data)
    
    try:
        result = calculate_human_design(timestamp, birth_data.timezone_name)
        return {"defined_centers": result["defined_centers"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.post("/undefined-centers", response_model=UndefinedCentersResponse, tags=["Features"])
async def get_undefined_centers(birth_data: BirthData):
    """Get the undefined centers based on birth data."""
    timestamp = validate_birth_data(birth_data)
    
    try:
        result = calculate_human_design(timestamp, birth_data.timezone_name)
        return {"undefined_centers": result["undefined_centers"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.post("/split", response_model=SplitResponse, tags=["Features"])
async def get_split_definition(birth_data: BirthData):
    """Get the split definition based on birth data."""
    timestamp = validate_birth_data(birth_data)
    
    try:
        result = calculate_human_design(timestamp, birth_data.timezone_name)
        return {"split": result["split"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.post("/incarnation-cross", response_model=CrossResponse, tags=["Features"])
async def get_incarnation_cross(birth_data: BirthData):
    """Get the incarnation cross based on birth data."""
    timestamp = validate_birth_data(birth_data)
    
    try:
        result = calculate_human_design(timestamp, birth_data.timezone_name)
        return {
            "incarnation_cross": result["incarnation_cross"],
            "cross_type": result["cross_type"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.post("/active-channels", response_model=ChannelsResponse, tags=["Features"])
async def get_active_channels(birth_data: BirthData):
    """Get the active channels based on birth data."""
    timestamp = validate_birth_data(birth_data)
    
    try:
        result = calculate_human_design(timestamp, birth_data.timezone_name)
        channel_meanings = get_channel_meanings(result["channels_data"])
        return {"active_channels": channel_meanings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.post("/active-gates", response_model=GatesResponse, tags=["Features"])
async def get_active_gates(birth_data: BirthData):
    """Get the active gates based on birth data."""
    timestamp = validate_birth_data(birth_data)
    
    try:
        result = calculate_human_design(timestamp, birth_data.timezone_name)
        return {
            "active_gates": result["active_gates"],
            "personality_gates": result["personality_gates"],
            "design_gates": result["design_gates"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.post("/variables", response_model=VariablesResponse, tags=["Features"])
async def get_variables(birth_data: BirthData):
    """Get the variables/arrows based on birth data."""
    timestamp = validate_birth_data(birth_data)
    
    try:
        result = calculate_human_design(timestamp, birth_data.timezone_name)
        return {"variables": result["variables"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")
