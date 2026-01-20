"""Google Ads integration."""

from typing import Any

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from ..core.config import settings
from ..core.models import Campaign, Audience, Creative
from .base import AdPlatform


class GoogleAds(AdPlatform):
    """Google Ads platform integration."""

    name = "google"

    def __init__(self, customer_id: str | None = None):
        self.customer_id = customer_id
        self.client = GoogleAdsClient.load_from_dict({
            "developer_token": settings.google_ads_developer_token,
            "client_id": settings.google_ads_client_id,
            "client_secret": settings.google_ads_client_secret,
            "refresh_token": settings.google_ads_refresh_token,
            "use_proto_plus": True,
        })

    async def create_campaign(self, campaign: Campaign) -> str:
        """Create a Google Ads campaign."""
        campaign_service = self.client.get_service("CampaignService")
        campaign_operation = self.client.get_type("CampaignOperation")

        new_campaign = campaign_operation.create
        new_campaign.name = campaign.name
        new_campaign.advertising_channel_type = (
            self.client.enums.AdvertisingChannelTypeEnum.SEARCH
        )
        new_campaign.status = self.client.enums.CampaignStatusEnum.PAUSED

        # Budget
        if campaign.budget_daily:
            campaign_budget_service = self.client.get_service("CampaignBudgetService")
            budget_operation = self.client.get_type("CampaignBudgetOperation")
            budget = budget_operation.create
            budget.name = f"{campaign.name}_budget"
            budget.amount_micros = int(campaign.budget_daily * 1_000_000)
            budget.delivery_method = (
                self.client.enums.BudgetDeliveryMethodEnum.STANDARD
            )

            budget_response = campaign_budget_service.mutate_campaign_budgets(
                customer_id=self.customer_id,
                operations=[budget_operation],
            )
            new_campaign.campaign_budget = budget_response.results[0].resource_name

        response = campaign_service.mutate_campaigns(
            customer_id=self.customer_id,
            operations=[campaign_operation],
        )

        return response.results[0].resource_name.split("/")[-1]

    async def update_campaign(self, platform_id: str, campaign: Campaign) -> bool:
        """Update a Google Ads campaign."""
        campaign_service = self.client.get_service("CampaignService")
        campaign_operation = self.client.get_type("CampaignOperation")

        update_campaign = campaign_operation.update
        update_campaign.resource_name = (
            f"customers/{self.customer_id}/campaigns/{platform_id}"
        )
        update_campaign.name = campaign.name

        campaign_operation.update_mask.paths.append("name")

        campaign_service.mutate_campaigns(
            customer_id=self.customer_id,
            operations=[campaign_operation],
        )
        return True

    async def pause_campaign(self, platform_id: str) -> bool:
        """Pause a Google Ads campaign."""
        return await self._set_campaign_status(platform_id, "PAUSED")

    async def resume_campaign(self, platform_id: str) -> bool:
        """Resume a Google Ads campaign."""
        return await self._set_campaign_status(platform_id, "ENABLED")

    async def _set_campaign_status(self, platform_id: str, status: str) -> bool:
        """Set campaign status."""
        campaign_service = self.client.get_service("CampaignService")
        campaign_operation = self.client.get_type("CampaignOperation")

        update_campaign = campaign_operation.update
        update_campaign.resource_name = (
            f"customers/{self.customer_id}/campaigns/{platform_id}"
        )
        update_campaign.status = getattr(
            self.client.enums.CampaignStatusEnum, status
        )

        campaign_operation.update_mask.paths.append("status")

        campaign_service.mutate_campaigns(
            customer_id=self.customer_id,
            operations=[campaign_operation],
        )
        return True

    async def get_metrics(
        self,
        platform_id: str,
        start_date: str,
        end_date: str,
    ) -> dict[str, Any]:
        """Get campaign metrics from Google Ads."""
        ga_service = self.client.get_service("GoogleAdsService")

        query = f"""
            SELECT
                campaign.id,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.ctr,
                metrics.average_cpc
            FROM campaign
            WHERE campaign.id = {platform_id}
              AND segments.date BETWEEN '{start_date}' AND '{end_date}'
        """

        response = ga_service.search(customer_id=self.customer_id, query=query)

        metrics = {
            "impressions": 0,
            "clicks": 0,
            "spend": 0.0,
            "conversions": 0,
            "ctr": 0.0,
            "cpc": 0.0,
        }

        for row in response:
            metrics["impressions"] += row.metrics.impressions
            metrics["clicks"] += row.metrics.clicks
            metrics["spend"] += row.metrics.cost_micros / 1_000_000
            metrics["conversions"] += int(row.metrics.conversions)
            metrics["ctr"] = row.metrics.ctr
            metrics["cpc"] = row.metrics.average_cpc / 1_000_000

        return metrics

    async def create_audience(self, audience: Audience) -> str:
        """Create a Google Ads user list."""
        user_list_service = self.client.get_service("UserListService")
        user_list_operation = self.client.get_type("UserListOperation")

        user_list = user_list_operation.create
        user_list.name = audience.name
        user_list.description = f"Hanzo audience: {audience.name}"
        user_list.membership_status = (
            self.client.enums.UserListMembershipStatusEnum.OPEN
        )
        user_list.membership_life_span = 365

        response = user_list_service.mutate_user_lists(
            customer_id=self.customer_id,
            operations=[user_list_operation],
        )

        return response.results[0].resource_name.split("/")[-1]

    async def upload_creative(self, creative: Creative) -> str:
        """Upload creative asset to Google Ads."""
        # Implementation for asset upload
        return "asset_id"

    async def get_account_balance(self) -> float:
        """Get account budget info."""
        # Google Ads doesn't have a simple balance - return budget remaining
        return 0.0
