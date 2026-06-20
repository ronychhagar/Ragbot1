"""
Task 4: Timestamp Difference Calculator
Calculates the difference between two timestamps in hours (full hours, rounded)
"""

from datetime import datetime


def calculate_hour_difference(timestamp1: str, timestamp2: str) -> int:
    """
    Calculate the difference between two timestamps in full hours (rounded).
    
    Args:
        timestamp1: Timestamp in format "2017/05/13 12:00"
        timestamp2: Timestamp in format "2017/05/13 14:30"
    
    Returns:
        int: Full hour difference (rounded)
        
    Example:
        >>> calculate_hour_difference("2022/02/15 00:05", "2022/02/15 01:00")
        1
    """
    try:
        # Parse timestamps
        dt1 = datetime.strptime(timestamp1, "%Y/%m/%d %H:%M")
        dt2 = datetime.strptime(timestamp2, "%Y/%m/%d %H:%M")
        
        # Calculate difference
        diff = abs(dt2 - dt1)
        
        # Convert to hours and round
        hours = diff.total_seconds() / 3600
        rounded_hours = round(hours)
        
        return rounded_hours
    
    except ValueError as e:
        raise ValueError(f"Invalid timestamp format. Expected 'YYYY/MM/DD HH:MM': {e}")


if __name__ == "__main__":
    # Test cases
    print("Task 4 - Timestamp Difference Calculator")
    print("-" * 50)
    
    test_cases = [
        ("2022/02/15 00:05", "2022/02/15 01:00", 1),
        ("2022/02/15 00:00", "2022/02/15 01:00", 1),
        ("2022/02/15 00:30", "2022/02/15 01:30", 1),
        ("2022/02/15 00:00", "2022/02/16 00:00", 24),
        ("2017/05/13 12:00", "2017/05/13 14:30", 2),
        ("2017/05/13 12:15", "2017/05/13 12:20", 0),
    ]
    
    for ts1, ts2, expected in test_cases:
        result = calculate_hour_difference(ts1, ts2)
        status = "✅" if result == expected else "❌"
        print(f"{status} {ts1} -> {ts2}: {result} hours (expected {expected})")
