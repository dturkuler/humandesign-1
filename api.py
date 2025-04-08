"""
FastAPI implementation for Human Design calculations.
This provides a RESTful API to access all Human Design features.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

from .calculations import calculate_human_design
from .utils import get_utc_offset_from_tz

app = FastAPI(
    title="Human Design API",
    description="API for calculating Human Design features",
    version="1.0.0"
)

class BirthTimeInput(BaseModel):
    """Schema for birth time input data"""
    year: int = Field(..., example=1980, description="Birth year")
    month: int = Field(..., example=6, description="Birth month (1-12)")
    day: int = Field(..., example=15, description="Birth day (1-31)")
    hour: int = Field(..., example=14, description="Birth hour (0-23)")
    minute: int = Field(..., example=30, description="Birth minute (0-59)")
    second: int = Field(0, example=0, description="Birth second (0-59)")
    timezone: str = Field(..., example="Europe/Berlin", description="Timezone name (e.g., 'Europe/Berlin')")

class FeatureRequest(BaseModel):
    """Schema for requesting specific Human Design features"""
    features: List[str] = Field(
        [], 
        example=["energy_type", "authority", "profile"],
        description="List of features to include (empty for all features)"
    )

@app.post("/calculate", response_model=Dict[str, Any])
async def calculate_design(birth_data: BirthTimeInput, feature_request: Optional[FeatureRequest] = None):
    """
    Calculate Human Design features based on birth time
    
    Returns a dictionary containing all requested Human Design features
    """
    try:
        # Validate input data
        if not (1 <= birth_data.month <= 12):
            raise HTTPException(status_code=400, detail="Month must be between 1 and 12")
        if not (1 <= birth_data.day <= 31):
            raise HTTPException(status_code=400, detail="Day must be between 1 and 31")
        if not (0 <= birth_data.hour <= 23):
            raise HTTPException(status_code=400, detail="Hour must be between 0 and 23")
        if not (0 <= birth_data.minute <= 59):
            raise HTTPException(status_code=400, detail="Minute must be between 0 and 59")
        if not (0 <= birth_data.second <= 59):
            raise HTTPException(status_code=400, detail="Second must be between 0 and 59")
        
        # Get timezone offset
        birth_time = (
            birth_data.year, birth_data.month, birth_data.day,
            birth_data.hour, birth_data.minute, birth_data.second
        )
        
        try:
            hours = get_utc_offset_from_tz(birth_time, birth_data.timezone)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid timezone: {birth_data.timezone}")
        
        # Calculate Human Design features
        timestamp = birth_time + (hours,)
        results = calculate_human_design(timestamp)
        
        # Filter results if specific features were requested
        if feature_request and feature_request.features:
            filtered_results = {k: v for k, v in results.items() if k in feature_request.features}
            # If nothing matched, return the whole result
            if not filtered_results:
                return results
            return filtered_results
        
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.get("/available-features")
async def get_available_features():
    """
    Get a list of all available Human Design features that can be requested
    """
    features = [
        "birth_date", "design_date", "energy_type", "strategy", "authority", 
        "authority_name", "profile", "incarnation_cross", "cross_type",
        "defined_centers", "undefined_centers", "split", "variables",
        "active_gates", "active_channels", "personality_gates", "design_gates"
    ]
    
    return {
        "available_features": features,
        "example_usage": {
            "method": "POST",
            "url": "/calculate",
            "body": {
                "birth_data": {
                    "year": 1980,
                    "month": 6,
                    "day": 15,
                    "hour": 14,
                    "minute": 30,
                    "second": 0,
                    "timezone": "Europe/Berlin"
                },
                "feature_request": {
                    "features": ["energy_type", "authority", "profile"]
                }
            }
        }
    }

# The entry point when running with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
