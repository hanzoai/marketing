"""TikTok Ads integration."""

from typing import Any

import httpx

from ..core.config import settings
from ..core.models import Campaign, Audience, Creative
from .base import AdPlatform


class TikTokAds(AdPlatform):
    """TikTok Ads platform integration."""

    name = "tiktok"
    base_url = "https://business-api.tiktok.com/open_api/v1.3"

    def __init__(self, advertiser_id: str | None = None):
        self.advertiser_id = advertiser_id
        self.access_token = settings.tiktok_access_token
        self.headers = {
            "Access-Token": self.access_token,
            "Content-Type": "application/json",
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: dict | None = None,
    ) -> dict[str, Any]:
        """Make API request to TikTok."""
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/{endpoint}"

            if method == "GET":
                response = await client.get(url, headers=self.headers, params=data)
            else:
                response = await client.post(url, headers=self.headers, json=data)

            response.raise_for_status()
            result = response.json()

            if result.get("code") != 0:
                raise Exception(f"TikTok API error: {result.get('message')}")

            return result.get("data", {})

    async def create_campaign(self, campaign: Campaign) -> str:
        """Create a TikTok Ads campaign."""
        data = {
            "advertiser_id": self.advertiser_id,
            "campaign_name": campaign.name,
            "objective_type": "CONVERSIONS",
            "budget_mode": "BUDGET_MODE_DAY" if campaign.budget_daily else "BUDGET_MODE_TOTAL",
            "budget": campaign.budget_daily or campaign.budget_total,
        }

        result = await self._request("POST", "campaign/create/", data)
        return result.get("campaign_id", "")

    async def update_campaign(self, platform_id: str, campaign: Campaign) -> bool:
        """Update a TikTok Ads campaign."""
        data = {
            "advertiser_id": self.advertiser_id,
            "campaign_id": platform_id,
            "campaign_name": campaign.name,
        }

        if campaign.budget_daily:
            data["budget"] = campaign.budget_daily

        await self._request("POST", "campaign/update/", data)
        return True

    async def pause_campaign(self, platform_id: str) -> bool:
        """Pause a TikTok Ads campaign."""
        data = {
            "advertiser_id": self.advertiser_id,
            "campaign_ids": [platform_id],
            "operation_status": "DISABLE",
        }
        await self._request("POST", "campaign/update/status/", data)
        return True

    async def resume_campaign(self, platform_id: str) -> bool:
        """Resume a TikTok Ads campaign."""
        data = {
            "advertiser_id": self.advertiser_id,
            "campaign_ids": [platform_id],
            "operation_status": "ENABLE",
        }
        await self._request("POST", "campaign/update/status/", data)
        return True

    async def get_metrics(
        self,
        platform_id: str,
        start_date: str,
        end_date: str,
    ) -> dict[str, Any]:
        """Get campaign metrics from TikTok Ads."""
        data = {
            "advertiser_id": self.advertiser_id,
            "report_type": "BASIC",
            "dimensions": ["campaign_id"],
            "metrics": [
                "spend",
                "impressions",
                "clicks",
                "conversion",
                "ctr",
                "cpc",
                "cpm",
            ],
            "filters": [
                {
                    "field_name": "campaign_id",
                    "filter_type": "IN",
                    "filter_value": f"[\"{platform_id}\"]",
                }
            ],
            "start_date": start_date,
            "end_date": end_date,
        }

        result = await self._request("GET", "report/integrated/get/", data)

        if result.get("list"):
            row = result["list"][0]["metrics"]
            return {
                "impressions": int(row.get("impressions", 0)),
                "clicks": int(row.get("clicks", 0)),
                "spend": float(row.get("spend", 0)),
                "conversions": int(row.get("conversion", 0)),
                "ctr": float(row.get("ctr", 0)),
                "cpc": float(row.get("cpc", 0)),
                "cpm": float(row.get("cpm", 0)),
            }

        return {}

    async def create_audience(self, audience: Audience) -> str:
        """Create a custom audience on TikTok."""
        data = {
            "advertiser_id": self.advertiser_id,
            "custom_audience_name": audience.name,
            "audience_type": "CUSTOMER_FILE",
        }

        result = await self._request("POST", "dmp/custom_audience/create/", data)
        return result.get("custom_audience_id", "")

    async def upload_creative(self, creative: Creative) -> str:
        """Upload creative to TikTok."""
        # Implementation for video/image upload
        return "creative_id"

    async def get_account_balance(self) -> float:
        """Get advertiser account balance."""
        data = {"advertiser_ids": [self.advertiser_id]}
        result = await self._request("GET", "advertiser/info/", data)

        if result.get("list"):
            return float(result["list"][0].get("balance", 0))
        return 0.0
