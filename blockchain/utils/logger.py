import json
import logging
from datetime import datetime
from typing import Any, Dict

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter for logging."""

    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]) -> None:
        """
        Add custom fields to the log record.
        
        """
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):

            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


        log_record.pop("color_message", None)  # Remove uvicorn color message
        if "http" in record.__dict__:
            log_record["http"] = record.__dict__["http"]


def json_translate(obj: Any) -> Dict[str, Any]:
    """
    Translate objects to JSON-serializable format.
    
    """
    from ..p2p.p2p_communication import SocketCommunication

    if isinstance(obj, SocketCommunication):
        return {
            "ip": obj.socket_connector.ip,
            "port": obj.socket_connector.port,
        }
    return obj


# Create the logger
logger = logging.root
logger.setLevel(logging.INFO)

# Create and configure the log handler
logHandler = logging.StreamHandler()
formatter = CustomJsonFormatter(
    json_default=json_translate, json_encoder=json.JSONEncoder
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

# Disable uvicorn access logs
logging.getLogger("uvicorn.access").disabled = True