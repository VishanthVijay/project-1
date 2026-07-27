from datetime import date, timedelta
from typing import List, Tuple, Optional


def calculate_streaks(
    completion_dates: List[date], today: Optional[date] = None
) -> Tuple[int, int]:
    """
    Calculates (current_streak, longest_streak) from a list of completion dates.

    Rules:
    - Current Streak:
      * Counts consecutive calendar days.
      * Includes today if completed.
      * If today is not completed yet, but yesterday was, streak remains active.
      * If yesterday was missed, current streak is 0.
    - Longest Streak:
      * Maximum consecutive days sequence recorded in history.
    """
    if not completion_dates:
        return 0, 0

    if today is None:
        today = date.today()

    # Sort dates ascending and remove duplicates
    unique_dates = sorted(set(completion_dates))

    # ----------------------------------------------------
    # 1. Calculate Longest Streak
    # ----------------------------------------------------
    longest_streak = 0
    temp_streak = 0
    prev_date: Optional[date] = None

    for d in unique_dates:
        if prev_date is None or d == prev_date + timedelta(days=1):
            temp_streak += 1
        else:
            temp_streak = 1

        if temp_streak > longest_streak:
            longest_streak = temp_streak

        prev_date = d

    # ----------------------------------------------------
    # 2. Calculate Current Streak
    # ----------------------------------------------------
    dates_set = set(unique_dates)
    current_streak = 0

    # Determine starting point: check today, or fallback to yesterday
    check_date = today
    if check_date not in dates_set:
        check_date = today - timedelta(days=1)

    while check_date in dates_set:
        current_streak += 1
        check_date -= timedelta(days=1)

    return current_streak, longest_streak
