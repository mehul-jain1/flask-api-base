from datetime import datetime
import pytz

def convert_timezone(datetime, timezone):
    """
    Convert a datetime object to a different time zone.
    
    Parameters:
    datetime (datetime): The datetime object to convert.
    timezone (str): The name of the time zone to convert to (e.g. "America/New_York").
    
    Returns:
    datetime: The datetime object converted to the specified time zone.
    """
    # Get the timezone object for the specified time zone
    user_tz = pytz.timezone(timezone)
    
    # Convert the datetime object to the target time zone
    user_time = datetime.replace(tzinfo=pytz.utc).astimezone(user_tz)
    
    formatted_time = user_time.strftime('%Y-%m-%d %H:%M:%S %Z')
    
    return formatted_time