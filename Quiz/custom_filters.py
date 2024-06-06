from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def time_since_post_created(post_created_at):
    current_time = timezone.now()
    time_difference = current_time - post_created_at

    # Calculate the difference in seconds
    seconds_difference = time_difference.total_seconds()

    # Convert seconds to meaningful time units
    if seconds_difference < 60:
        return f"{int(seconds_difference)} seconds ago"
    elif seconds_difference < 3600:
        return f"{int(seconds_difference // 60)} minutes ago"
    elif seconds_difference < 86400:
        return f"{int(seconds_difference // 3600)} hours ago"
    else:
        return f"{int(seconds_difference // 86400)} days ago"
