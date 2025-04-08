"""
Utility functions for Human Design calculations.

This module provides helper functions for date/time handling,
timezone conversion, and other utility operations used in
Human Design calculations.
"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pytz import timezone
import swisseph as swe

def get_utc_offset_from_tz(timestamp, zone):
    """
    Get UTC offset from given time zone.
    DST (daylight saving time) is respected (data from pytz lib)
    
    Args:
        timestamp (tuple): Year, month, day, hour, minute, second
        zone (str): e.g. "Europe/Berlin"
    
    Returns:
        float: Offset hours (decimal hours e.g. 0.75 for 45 min)
    """
    country = timezone(zone)
    tz_offset = country.localize(datetime(*timestamp)).utcoffset().total_seconds()
    hours = tz_offset / 3600
    return hours

def timestamp_to_juldate(timestamp):
    """
    Calculate Julian date from given timestamp.
    Uses swiss_ephemeris lib from astro.com
    
    Args:
        timestamp (tuple): Format: year, month, day, hour, minute, second, time_zone_offset
    
    Returns:
        float: Julian date
    """
    time_zone = swe.utc_time_zone(*timestamp)
    jdut = swe.utc_to_jd(*time_zone)
    return jdut[1]

def calc_create_date(jdut):
    """
    Calculate design/creation date from birth date.
    Sun position -88° longitude, approximately 3 months before birth
    (Source: Ra Uru Hu)
    
    Args:
        jdut (float): Julian day format timestamp
    
    Returns:
        float: Creation date in Julian day format
    """
    design_pos = 88
    sun_long = swe.calc_ut(jdut, swe.SUN)[0][0]
    long = swe.degnorm(sun_long - design_pos)
    tstart = jdut - 100  # approximation is start -100°
    res = swe.solcross_ut(long, tstart)
    create_date = swe.revjul(res)
    create_julday = swe.julday(*create_date)
    return create_julday

def julian_to_datetime(julian_date):
    """
    Convert Julian date to a datetime object
    
    Args:
        julian_date (float): Date in Julian format
    
    Returns:
        tuple: Year, month, day, hour, minute, second
    """
    return swe.jdut1_to_utc(julian_date)[:-1]

def generate_timestamp_range(start_date, end_date, percentage=1.0, time_unit="days", interval=1):
    """
    Generate a list of timestamps within a given range
    
    Args:
        start_date (tuple): (year, month, day, hour, minute, second, timezone_offset)
        end_date (tuple): (year, month, day, hour, minute, second, timezone_offset)
        percentage (float): Percentage of the time range to process (0.0-1.0)
        time_unit (str): "years", "months", "days", "hours", or "minutes"
        interval (int): Step size in the specified time unit
    
    Returns:
        list: List of timestamp tuples
    """
    start_date = datetime(*start_date)
    end_date = datetime(*end_date)
    
    # Calculate the time unit in seconds
    if time_unit == "years":
        unit = 60 * 60 * 24 * 365.2425
    elif time_unit == "months":
        unit = 60 * 60 * 24 * 365.25 / 12
    elif time_unit == "days":
        unit = 60 * 60 * 24
    elif time_unit == "hours":
        unit = 60 * 60
    elif time_unit == "minutes":
        unit = 60
    else:
        raise ValueError(f"Invalid time unit: {time_unit}")
    
    # Calculate the number of steps
    time_diff_range = int((end_date - start_date).total_seconds() / unit)
    total_steps = int(time_diff_range * percentage / interval)
    
    timestamp_list = []
    for i in range(total_steps):
        # Calculate the new date for this step
        if time_unit in ["years", "months"]:
            # relativedelta handles years and months properly
            new_date = end_date - i * relativedelta(**{time_unit: interval})
        else:
            # timedelta is faster for days, hours, minutes
            new_date = end_date - i * timedelta(seconds=unit * interval)
            
        timestamp = (new_date.year, new_date.month, new_date.day, 
                    new_date.hour, new_date.minute, 0, 0)
        timestamp_list.append(timestamp)
    
    # Sanity check
    if not timestamp_list:
        raise ValueError('Check that startdate < enddate & (enddate-interval) >= startdate')
    
    return timestamp_list
