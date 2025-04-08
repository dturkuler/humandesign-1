"""
Models for Human Design API.

This module defines the data models for input and output of the Human Design API,
using Pydantic for data validation.
"""

from typing import List, Dict, Optional, Tuple, Any
from pydantic import BaseModel, Field
from datetime import datetime

class BirthData(BaseModel):
    """Input data for Human Design calculation."""
    year: int = Field(..., description="Birth year")
    month: int = Field(..., description="Birth month (1-12)")
    day: int = Field(..., description="Birth day (1-31)")
    hour: int = Field(..., description="Birth hour (0-23)")
    minute: int = Field(..., description="Birth minute (0-59)")
    second: int = Field(0, description="Birth second (0-59)")
    timezone: Optional[float] = Field(None, description="Timezone offset in hours (e.g., 2.0 for UTC+2)")
    timezone_name: Optional[str] = Field(None, description="Timezone name (e.g., 'Europe/Berlin')")

class GateData(BaseModel):
    """Model for gate information."""
    gate: int = Field(..., description="Gate number")
    line: int = Field(..., description="Line number")
    planet: str = Field(..., description="Planet name")

class ChannelData(BaseModel):
    """Model for channel information."""
    channel: str = Field(..., description="Channel (e.g., '10/34')")
    name: Optional[str] = Field(None, description="Channel name")
    description: Optional[str] = Field(None, description="Channel description")

class Variables(BaseModel):
    """Model for variables."""
    right_up: str = Field(..., description="Right upper arrow (left/right)")
    right_down: str = Field(..., description="Right lower arrow (left/right)")
    left_up: str = Field(..., description="Left upper arrow (left/right)")
    left_down: str = Field(..., description="Left lower arrow (left/right)")

class HumanDesignResponse(BaseModel):
    """Complete Human Design calculation response."""
    birth_date: str = Field(..., description="Original birth date/time")
    design_date: str = Field(..., description="Design/unconscious date/time")
    energy_type: str = Field(..., description="Energy type")
    strategy: str = Field(..., description="Strategy based on energy type")
    authority: str = Field(..., description="Authority code")
    authority_name: str = Field(..., description="Authority full name")
    profile: str = Field(..., description="Profile (e.g., '1/3')")
    incarnation_cross: str = Field(..., description="Incarnation cross")
    cross_type: str = Field(..., description="Cross type (RAC, LAC, JXP)")
    defined_centers: List[str] = Field(..., description="Defined/active centers")
    undefined_centers: List[str] = Field(..., description="Undefined centers")
    split: int = Field(..., description="Split definition")
    variables: Variables = Field(..., description="Variables/arrows")
    active_gates: List[int] = Field(..., description="All active gates")
    active_channels: List[str] = Field(..., description="All active channels")
    personality_gates: List[GateData] = Field(..., description="Conscious gates")
    design_gates: List[GateData] = Field(..., description="Unconscious gates")

class EnergyTypeResponse(BaseModel):
    """Energy type response."""
    energy_type: str = Field(..., description="Energy type")
    strategy: str = Field(..., description="Strategy")

class AuthorityResponse(BaseModel):
    """Authority response."""
    authority: str = Field(..., description="Authority code")
    authority_name: str = Field(..., description="Authority name")

class ProfileResponse(BaseModel):
    """Profile response."""
    profile: str = Field(..., description="Profile (e.g., '1/3')")

class DefinedCentersResponse(BaseModel):
    """Defined centers response."""
    defined_centers: List[str] = Field(..., description="Defined/active centers")

class UndefinedCentersResponse(BaseModel):
    """Undefined centers response."""
    undefined_centers: List[str] = Field(..., description="Undefined centers")

class SplitResponse(BaseModel):
    """Split definition response."""
    split: int = Field(..., description="Split definition")

class CrossResponse(BaseModel):
    """Incarnation cross response."""
    incarnation_cross: str = Field(..., description="Incarnation cross")
    cross_type: str = Field(..., description="Cross type (RAC, LAC, JXP)")

class ChannelsResponse(BaseModel):
    """Active channels response."""
    active_channels: List[ChannelData] = Field(..., description="Active channels with descriptions")

class GatesResponse(BaseModel):
    """Active gates response."""
    active_gates: List[int] = Field(..., description="All active gates")
    personality_gates: List[GateData] = Field(..., description="Conscious gates")
    design_gates: List[GateData] = Field(..., description="Unconscious gates")

class VariablesResponse(BaseModel):
    """Variables response."""
    variables: Variables = Field(..., description="Variables/arrows")
