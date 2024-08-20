#SM_InputValidator.py

import re as FormatQA
from datetime import datetime

class SM_InputValidator:
    def Validate_security_symbol(self, security_name):
        """Validate the security symbol format. Expected format: uppercase letters, numbers, and hyphens."""
        return bool(FormatQA.match("^[A-Z0-9-]+$", security_name))

    def Validate_start_date(self, security_start_date):
        """Validate the start date format. Expected format: YYYY-MM-DD."""
        return bool(FormatQA.match("^\d{4}-\d{2}-\d{2}$", security_start_date))

    def Validate_end_date(self, security_end_date):
        """Validate the end date format. Expected format: YYYY-MM-DD."""
        return bool(FormatQA.match("^\d{4}-\d{2}-\d{2}$", security_end_date))
    
    def Validate_telegram_chat_id(self, chat_id):
        """Validate Telegram chat ID format. Expected format: a numeric string, possibly starting with a '-'."""
        return bool(FormatQA.match(r"^-?\d+$", chat_id))

    def Validate_date_order(self, start_date, end_date):
        """Validate that the start date is not later than the end date."""
        if not self.Validate_start_date(start_date) or not self.Validate_end_date(end_date):
            return False

        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

        return start_date_obj <= end_date_obj
