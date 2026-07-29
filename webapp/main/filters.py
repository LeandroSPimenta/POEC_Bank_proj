from datetime import datetime

from webapp.main import bp as main_bp


@main_bp.app_template_filter("make_caps")
def caps(text):
    """Convert a string to all caps."""
    return str(text).upper()


@main_bp.app_template_filter("date_format")
def date_format(date):
    """Format a date"""
    if isinstance(date, datetime):
        return date.strftime("%d/%m/%Y")
    return date
