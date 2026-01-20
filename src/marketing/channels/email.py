"""Email channel integration."""

from typing import Any

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, From, Subject, Content

from ..core.config import settings


class EmailChannel:
    """Email communication channel via SendGrid."""

    def __init__(self):
        self.client = SendGridAPIClient(settings.sendgrid_api_key)

    async def send(
        self,
        to_emails: list[str],
        subject: str,
        html_content: str,
        from_email: str = "marketing@hanzo.ai",
        from_name: str = "Hanzo",
    ) -> dict[str, Any]:
        """Send an email."""
        message = Mail(
            from_email=From(from_email, from_name),
            to_emails=[To(email) for email in to_emails],
            subject=Subject(subject),
            html_content=Content("text/html", html_content),
        )

        response = self.client.send(message)

        return {
            "status_code": response.status_code,
            "message_id": response.headers.get("X-Message-Id"),
        }

    async def send_campaign(
        self,
        campaign_id: str,
        segment_id: str,
        template_id: str,
        schedule_time: str | None = None,
    ) -> dict[str, Any]:
        """Send a campaign to a segment."""
        data = {
            "title": f"Campaign {campaign_id}",
            "segment_ids": [int(segment_id)],
            "template_id": template_id,
            "sender_id": 1,
            "suppression_group_id": 1,
        }

        if schedule_time:
            data["send_at"] = schedule_time

        response = self.client.client.marketing.singlesends.post(
            request_body=data
        )

        return response.to_dict

    async def create_segment(
        self,
        name: str,
        conditions: list[dict[str, Any]],
    ) -> str:
        """Create an email segment."""
        data = {
            "name": name,
            "query_dsl": {"conditions": conditions},
        }

        response = self.client.client.marketing.segments.post(
            request_body=data
        )

        return response.to_dict.get("id", "")

    async def get_stats(
        self,
        start_date: str,
        end_date: str,
    ) -> dict[str, Any]:
        """Get email statistics."""
        response = self.client.client.stats.get(
            query_params={
                "start_date": start_date,
                "end_date": end_date,
            }
        )

        if response.to_dict:
            stats = response.to_dict[0].get("stats", [{}])[0].get("metrics", {})
            return {
                "sent": stats.get("requests", 0),
                "delivered": stats.get("delivered", 0),
                "opens": stats.get("opens", 0),
                "clicks": stats.get("clicks", 0),
                "bounces": stats.get("bounces", 0),
                "spam_reports": stats.get("spam_reports", 0),
                "open_rate": stats.get("opens", 0) / max(stats.get("delivered", 1), 1),
                "click_rate": stats.get("clicks", 0) / max(stats.get("opens", 1), 1),
            }

        return {}
