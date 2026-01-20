"""Social media channel integrations."""

from typing import Any

import tweepy
import httpx

from ..core.config import settings


class SocialChannel:
    """Social media channel for organic posting and engagement."""

    def __init__(self):
        # Twitter/X
        self.twitter_client = tweepy.Client(
            consumer_key=settings.twitter_api_key,
            consumer_secret=settings.twitter_api_secret,
            access_token=settings.twitter_access_token,
            access_token_secret=settings.twitter_access_secret,
        )

        # LinkedIn
        self.linkedin_token = None  # Set via OAuth

    # Twitter/X methods
    async def post_twitter(
        self,
        text: str,
        media_ids: list[str] | None = None,
        reply_to: str | None = None,
    ) -> dict[str, Any]:
        """Post a tweet."""
        params = {"text": text}

        if media_ids:
            params["media_ids"] = media_ids
        if reply_to:
            params["in_reply_to_tweet_id"] = reply_to

        response = self.twitter_client.create_tweet(**params)

        return {
            "id": response.data["id"],
            "text": response.data["text"],
        }

    async def get_twitter_analytics(
        self,
        tweet_id: str,
    ) -> dict[str, Any]:
        """Get tweet engagement metrics."""
        tweet = self.twitter_client.get_tweet(
            tweet_id,
            tweet_fields=["public_metrics", "created_at"],
        )

        if tweet.data:
            metrics = tweet.data.public_metrics
            return {
                "impressions": metrics.get("impression_count", 0),
                "likes": metrics["like_count"],
                "retweets": metrics["retweet_count"],
                "replies": metrics["reply_count"],
                "quotes": metrics["quote_count"],
            }
        return {}

    # LinkedIn methods
    async def post_linkedin(
        self,
        text: str,
        organization_id: str | None = None,
        image_url: str | None = None,
    ) -> dict[str, Any]:
        """Post to LinkedIn."""
        if not self.linkedin_token:
            raise ValueError("LinkedIn not authenticated")

        headers = {
            "Authorization": f"Bearer {self.linkedin_token}",
            "Content-Type": "application/json",
        }

        # Determine author (person or organization)
        author = f"urn:li:organization:{organization_id}" if organization_id else "urn:li:person:me"

        post_data = {
            "author": author,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.linkedin.com/v2/ugcPosts",
                headers=headers,
                json=post_data,
            )
            response.raise_for_status()
            return response.json()

    async def schedule_post(
        self,
        platform: str,
        content: str,
        schedule_time: str,
        media_urls: list[str] | None = None,
    ) -> dict[str, Any]:
        """Schedule a social media post."""
        # Store in database for scheduled posting
        # Worker will pick up and post at scheduled time
        return {
            "platform": platform,
            "content": content,
            "schedule_time": schedule_time,
            "status": "scheduled",
        }

    async def get_mentions(
        self,
        platform: str,
        since_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get mentions/notifications for engagement."""
        if platform == "twitter":
            mentions = self.twitter_client.get_users_mentions(
                id=self.twitter_client.get_me().data.id,
                since_id=since_id,
                tweet_fields=["created_at", "public_metrics"],
            )

            return [
                {
                    "id": tweet.id,
                    "text": tweet.text,
                    "created_at": str(tweet.created_at),
                }
                for tweet in (mentions.data or [])
            ]

        return []
