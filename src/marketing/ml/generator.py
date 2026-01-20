"""AI-powered campaign content generation."""

from typing import Any

import httpx

from ..core.config import settings
from ..core.models import Campaign, Creative


class CampaignGenerator:
    """
    AI-powered campaign content generator.

    Uses LLM via Hanzo Router to generate:
    - Ad copy variations
    - Email subject lines
    - Social media posts
    - Landing page content
    - A/B test variants
    """

    def __init__(self):
        self.router_url = settings.router_url
        self.api_key = settings.router_api_key

    async def _call_llm(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """Call LLM via Hanzo Router."""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.router_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4",
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                },
                timeout=60.0,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def generate_ad_copy(
        self,
        product: str,
        target_audience: str,
        platform: str,
        tone: str = "professional",
        n_variants: int = 3,
    ) -> list[dict[str, str]]:
        """Generate ad copy variants."""
        system_prompt = f"""You are an expert marketing copywriter.
        Generate compelling ad copy for {platform} that resonates with the target audience.
        Keep copy concise and action-oriented. Include a clear CTA."""

        prompt = f"""Generate {n_variants} different ad copy variants for:

Product: {product}
Target Audience: {target_audience}
Platform: {platform}
Tone: {tone}

For each variant, provide:
1. Headline (max 40 chars)
2. Primary text (max 125 chars)
3. Call to action

Format as JSON array with keys: headline, text, cta"""

        response = await self._call_llm(prompt, system_prompt, temperature=0.8)

        # Parse response (simplified - in production use proper JSON parsing)
        try:
            import json
            # Find JSON in response
            start = response.find("[")
            end = response.rfind("]") + 1
            if start >= 0 and end > start:
                variants = json.loads(response[start:end])
                return variants
        except Exception:
            pass

        return [{"headline": "Generated copy", "text": response, "cta": "Learn More"}]

    async def generate_email_content(
        self,
        campaign_type: str,
        product: str,
        target_audience: str,
        key_benefits: list[str],
        n_variants: int = 2,
    ) -> list[dict[str, Any]]:
        """Generate email content variants."""
        system_prompt = """You are an email marketing expert.
        Create engaging email content that drives opens and clicks.
        Focus on clear value propositions and compelling CTAs."""

        prompt = f"""Generate {n_variants} email variants for a {campaign_type} campaign:

Product: {product}
Target Audience: {target_audience}
Key Benefits: {', '.join(key_benefits)}

For each variant provide:
1. Subject line (max 50 chars, include emoji if appropriate)
2. Preview text (max 100 chars)
3. Email body (HTML with clear sections)
4. CTA button text

Format as JSON array."""

        response = await self._call_llm(prompt, system_prompt, temperature=0.7)

        try:
            import json
            start = response.find("[")
            end = response.rfind("]") + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except Exception:
            pass

        return [{"subject": "Check this out", "body": response}]

    async def generate_social_posts(
        self,
        topic: str,
        platforms: list[str],
        tone: str = "engaging",
        include_hashtags: bool = True,
    ) -> dict[str, list[str]]:
        """Generate platform-specific social posts."""
        results = {}

        for platform in platforms:
            char_limit = {
                "twitter": 280,
                "linkedin": 700,
                "instagram": 2200,
                "facebook": 500,
            }.get(platform, 500)

            prompt = f"""Generate 3 {platform} posts about: {topic}

Tone: {tone}
Max length: {char_limit} characters
{"Include relevant hashtags" if include_hashtags else "No hashtags"}

Return as JSON array of strings."""

            response = await self._call_llm(prompt, temperature=0.8)

            try:
                import json
                start = response.find("[")
                end = response.rfind("]") + 1
                if start >= 0 and end > start:
                    results[platform] = json.loads(response[start:end])
                else:
                    results[platform] = [response]
            except Exception:
                results[platform] = [response]

        return results

    async def optimize_content(
        self,
        original_content: str,
        performance_data: dict[str, float],
        optimization_goal: str = "ctr",
    ) -> dict[str, Any]:
        """Optimize existing content based on performance data."""
        prompt = f"""Analyze and improve this marketing content:

Original: {original_content}

Current Performance:
- CTR: {performance_data.get('ctr', 0):.2%}
- Conversion Rate: {performance_data.get('cvr', 0):.2%}
- Engagement: {performance_data.get('engagement', 0):.2%}

Optimization Goal: Improve {optimization_goal}

Provide:
1. Analysis of why current content may be underperforming
2. 3 improved versions with specific changes
3. Expected improvement reasoning

Format as JSON with keys: analysis, variants (array), reasoning"""

        response = await self._call_llm(
            prompt,
            temperature=0.6,
            max_tokens=1500,
        )

        try:
            import json
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except Exception:
            pass

        return {"analysis": response, "variants": [], "reasoning": ""}
