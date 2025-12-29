import os
import logging
from datetime import datetime

# Setup logger for SMS
logging.basicConfig(level=logging.INFO)
sms_logger = logging.getLogger('nms_sms')
handler = logging.FileHandler('sms_logs.txt')
handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
sms_logger.addHandler(handler)
sms_logger.setLevel(logging.INFO)

class SMSService:
    @staticmethod
    def send_sms(phone, message):
        """
        Sends an SMS. In mock mode, logs to file.
        Real implementation would use Orange API here.
        """
        # Mock Implementation
        log_msg = f"TO: {phone} | MSG: {message}"
        print(f"[SMS MOCK] {log_msg}")
        sms_logger.info(log_msg)
        return True
