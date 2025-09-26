from enum import Enum

class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class DeliveryType(str, Enum):
    IN_APP = "in_app"
    EMAIL = "email"  # For future use
    SMS = "sms"     # For future use