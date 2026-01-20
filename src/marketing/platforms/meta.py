"""Meta (Facebook/Instagram) Ads integration."""

from typing import Any

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign as FBCampaign
from facebook_business.adobjects.customaudience import CustomAudience

from ..core.config import settings
from ..core.models import Campaign, Audience, Creative
from .base import AdPlatform


class MetaAds(AdPlatform):
    """Meta Ads (Facebook/Instagram) platform integration."""

    name = "meta"

    def __init__(self, ad_account_id: str | None = None):
        FacebookAdsApi.init(
            app_id=settings.meta_app_id,
            app_secret=settings.meta_app_secret,
            access_token=settings.meta_access_token,
        )
        self.ad_account_id = ad_account_id
        self.ad_account = AdAccount(f"act_{ad_account_id}") if ad_account_id else None

    async def create_campaign(self, campaign: Campaign) -> str:
        """Create a Meta campaign."""
        if not self.ad_account:
            raise ValueError("Ad account not configured")

        params = {
            "name": campaign.name,
            "objective": "OUTCOME_SALES",  # Map from campaign.goals
            "status": "PAUSED",
            "special_ad_categories": [],
        }

        if campaign.budget_daily:
            params["daily_budget"] = int(campaign.budget_daily * 100)  # Cents
        elif campaign.budget_total:
            params["lifetime_budget"] = int(campaign.budget_total * 100)

        result = self.ad_account.create_campaign(params=params)
        return result["id"]

    async def update_campaign(self, platform_id: str, campaign: Campaign) -> bool:
        """Update a Meta campaign."""
        fb_campaign = FBCampaign(platform_id)
        params = {"name": campaign.name}

        if campaign.budget_daily:
            params["daily_budget"] = int(campaign.budget_daily * 100)

        fb_campaign.api_update(params=params)
        return True

    async def pause_campaign(self, platform_id: str) -> bool:
        """Pause a Meta campaign."""
        fb_campaign = FBCampaign(platform_id)
        fb_campaign.api_update(params={"status": "PAUSED"})
        return True

    async def resume_campaign(self, platform_id: str) -> bool:
        """Resume a Meta campaign."""
        fb_campaign = FBCampaign(platform_id)
        fb_campaign.api_update(params={"status": "ACTIVE"})
        return True

    async def get_metrics(
        self,
        platform_id: str,
        start_date: str,
        end_date: str,
    ) -> dict[str, Any]:
        """Get campaign insights from Meta."""
        fb_campaign = FBCampaign(platform_id)
        insights = fb_campaign.get_insights(
            params={
                "time_range": {"since": start_date, "until": end_date},
                "fields": [
                    "impressions",
                    "clicks",
                    "spend",
                    "conversions",
                    "cpc",
                    "cpm",
                    "ctr",
                    "reach",
                    "frequency",
                ],
            }
        )

        if insights:
            data = insights[0]
            return {
                "impressions": int(data.get("impressions", 0)),
                "clicks": int(data.get("clicks", 0)),
                "spend": float(data.get("spend", 0)),
                "conversions": int(data.get("conversions", 0)),
                "cpc": float(data.get("cpc", 0)),
                "cpm": float(data.get("cpm", 0)),
                "ctr": float(data.get("ctr", 0)),
                "reach": int(data.get("reach", 0)),
                "frequency": float(data.get("frequency", 0)),
            }

        return {}

    async def create_audience(self, audience: Audience) -> str:
        """Create a custom audience on Meta."""
        if not self.ad_account:
            raise ValueError("Ad account not configured")

        params = {
            "name": audience.name,
            "subtype": "CUSTOM",
            "description": f"Hanzo audience: {audience.name}",
            "customer_file_source": "USER_PROVIDED_ONLY",
        }

        result = self.ad_account.create_custom_audience(params=params)
        return result["id"]

    async def upload_creative(self, creative: Creative) -> str:
        """Upload creative to Meta."""
        # Implementation for image/video upload
        return "creative_id"

    async def get_account_balance(self) -> float:
        """Get ad account spend cap."""
        if not self.ad_account:
            return 0.0

        account = self.ad_account.api_get(fields=["spend_cap", "amount_spent"])
        spend_cap = float(account.get("spend_cap", 0)) / 100
        amount_spent = float(account.get("amount_spent", 0)) / 100
        return spend_cap - amount_spent
