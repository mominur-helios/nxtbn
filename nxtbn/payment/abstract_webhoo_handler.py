from abc import ABC, abstractmethod
from typing import Any, Dict
from django.http import HttpRequest, JsonResponse
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

class WebhookHandler(ABC):
    """Abstract base class for handling payment gateway webhooks."""

    @abstractmethod
    def validate_webhook(self, request: HttpRequest) -> bool:
        """Validate the incoming webhook request."""
        pass

    @abstractmethod
    def parse_webhook(self, request: HttpRequest) -> Dict[str, Any]:
        """Parse and return the key data from the webhook request."""
        pass

    @abstractmethod
    def process_event(self, event_data: Dict[str, Any]) -> JsonResponse:
        """Process the parsed webhook event."""
        pass
