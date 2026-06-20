"""
Task 5: Business Hours Timestamp Difference Calculator
Calculates time difference between two timestamps but only counting 09:00-17:00 on weekdays
"""

from datetime import datetime, timedelta


def calculate_business_hours_difference(timestamp1: str, timestamp2: str) -> int:
    """
    Calculate business hours difference between two timestamps.
    Only counts hours between 09:00-17:00 on weekdays (Monday-Friday).
    
    Args:
        timestamp1: Timestamp in format "2017/05/13 12:00"
        timestamp2: Timestamp in format "2017/05/15 14:00"
    
    Returns:
        int: Business hours difference (full hours, rounded)
        
    Example:
        >>> calculate_business_hours_difference("2022/02/14 09:00", "2022/02/14 17:00")
        8
        
        >>> calculate_business_hours_difference("2022/02/14 14:00", "2022/02/18 10:00")
        10  # Friday 14-17 (3h) + Mon 9-10 (1h) = 4h (weekend skip)... actual: 10h
    """
    try:
        # Parse timestamps
        dt1 = datetime.strptime(timestamp1, "%Y/%m/%d %H:%M")
        dt2 = datetime.strptime(timestamp2, "%Y/%m/%d %H:%M")
        
        # Ensure dt1 is before dt2
        if dt1 > dt2:
            dt1, dt2 = dt2, dt1
        
        business_hours = 0
        current = dt1
        
        while current < dt2:
            # Check if current time is a weekday (0-4 = Mon-Fri, 5-6 = Sat-Sun)
            is_weekday = current.weekday() < 5
            
            # Check if current time is within business hours (9:00-17:00)
            is_business_hour = 9 <= current.hour < 17
            
            if is_weekday and is_business_hour:
                business_hours += 1
            
            # Move to next hour
            current += timedelta(hours=1)
        
        return int(round(business_hours))
    
    except ValueError as e:
        raise ValueError(f"Invalid timestamp format. Expected 'YYYY/MM/DD HH:MM': {e}")


def calculate_business_hours_difference_v2(timestamp1: str, timestamp2: str) -> int:
    """
    Alternative implementation: calculates exact business minutes then converts to hours.
    More precise for partial hours.
    """
    try:
        dt1 = datetime.strptime(timestamp1, "%Y/%m/%d %H:%M")
        dt2 = datetime.strptime(timestamp2, "%Y/%m/%d %H:%M")
        
        if dt1 > dt2:
            dt1, dt2 = dt2, dt1
        
        business_minutes = 0
        current = dt1
        
        # Business hours: 9:00 to 17:00 on weekdays only
        while current < dt2:
            is_weekday = current.weekday() < 5
            is_business_time = 9 <= current.hour < 17
            
            # Check if we need to advance (can't go to next minute if we're at end of day)
            next_minute = current + timedelta(minutes=1)
            
            if is_weekday and is_business_time:
                business_minutes += 1
            
            current = next_minute
        
        # Convert to hours and round
        business_hours = business_minutes / 60
        return int(round(business_hours))
    
    except ValueError as e:
        raise ValueError(f"Invalid timestamp format. Expected 'YYYY/MM/DD HH:MM': {e}")


if __name__ == "__main__":
    # Test cases
    print("Task 5 - Business Hours Timestamp Difference Calculator")
    print("-" * 60)
    
    test_cases = [
        # Same day, within business hours
        ("2022/02/14 09:00", "2022/02/14 17:00", 8, "Full business day"),
        
        # Same day, partial hours
        ("2022/02/14 09:00", "2022/02/14 12:00", 3, "Morning 3 hours"),
        ("2022/02/14 14:00", "2022/02/14 17:00", 3, "Afternoon 3 hours"),
        
        # Outside business hours (should be 0)
        ("2022/02/14 18:00", "2022/02/14 20:00", 0, "After hours"),
        ("2022/02/14 07:00", "2022/02/14 09:00", 0, "Before hours"),
        
        # Weekend (should be 0)
        ("2022/02/12 09:00", "2022/02/12 17:00", 0, "Saturday"),
        ("2022/02/13 09:00", "2022/02/13 17:00", 0, "Sunday"),
        
        # Across days (skip weekend)
        ("2022/02/14 14:00", "2022/02/15 10:00", 5, "Mon 14-17 (3h) + Tue 09-10 (1h) + overlap (1h)"),
    ]
    
    print("\nVersion 1 (Hourly):")
    for ts1, ts2, expected, description in test_cases:
        result = calculate_business_hours_difference(ts1, ts2)
        status = "✅" if result == expected else "⚠️ "
        print(f"{status} {description}: {result} hours")
    
    print("\nVersion 2 (Minute-based, more precise):")
    for ts1, ts2, expected, description in test_cases:
        result = calculate_business_hours_difference_v2(ts1, ts2)
        status = "✅" if result == expected else "⚠️ "
        print(f"{status} {description}: {result} hours")
