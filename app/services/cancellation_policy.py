from datetime import datetime


def days_until(trip_start_date):
    delta = trip_start_date - datetime.utcnow()
    return max(delta.days, 0)


def compute_refund_percentage(days_before_trip):
    if days_before_trip >= 14:
        return 1.0
    elif days_before_trip >= 7:
        return 0.5
    elif days_before_trip >= 1:
        return 0.2
    else:
        return 0.0