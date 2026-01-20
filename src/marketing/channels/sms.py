"""SMS channel integration."""

from typing import Any

from twilio.rest import Client

from ..core.config import settings


class SMSChannel:
    """SMS communication channel via Twilio."""

    def __init__(self):
        self.client = Client(
            settings.twilio_account_sid,
            settings.twilio_auth_token,
        )
        self.from_number = settings.twilio_phone_number

    async def send(
        self,
        to_number: str,
        message: str,
        media_url: str | None = None,
    ) -> dict[str, Any]:
        """Send an SMS message."""
        params = {
            "body": message,
            "from_": self.from_number,
            "to": to_number,
        }

        if media_url:
            params["media_url"] = [media_url]

        msg = self.client.messages.create(**params)

        return {
            "sid": msg.sid,
            "status": msg.status,
            "to": msg.to,
            "price": msg.price,
        }

    async def send_bulk(
        self,
        numbers: list[str],
        message: str,
    ) -> list[dict[str, Any]]:
        """Send SMS to multiple numbers."""
        results = []
        for number in numbers:
            try:
                result = await self.send(number, message)
                results.append({"number": number, "success": True, **result})
            except Exception as e:
                results.append({"number": number, "success": False, "error": str(e)})
        return results

    async def get_stats(
        self,
        start_date: str,
        end_date: str,
    ) -> dict[str, Any]:
        """Get SMS statistics."""
        messages = self.client.messages.list(
            date_sent_after=start_date,
            date_sent_before=end_date,
        )

        stats = {
            "sent": 0,
            "delivered": 0,
            "failed": 0,
            "total_cost": 0.0,
        }

        for msg in messages:
            stats["sent"] += 1
            if msg.status == "delivered":
                stats["delivered"] += 1
            elif msg.status in ("failed", "undelivered"):
                stats["failed"] += 1
            if msg.price:
                stats["total_cost"] += abs(float(msg.price))

        stats["delivery_rate"] = stats["delivered"] / max(stats["sent"], 1)

        return stats

    async def create_messaging_service(
        self,
        name: str,
        use_case: str = "marketing",
    ) -> str:
        """Create a messaging service for campaigns."""
        service = self.client.messaging.v1.services.create(
            friendly_name=name,
            usecase=use_case,
        )
        return service.sid
