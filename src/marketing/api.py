"""Marketing service API."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .core.config import settings
from .core.models import Campaign, Platform
from .optimizer import GeneticOptimizer, SearchSpace
from .ml import Forecaster, PatternDetector, CampaignGenerator
from .platforms import MetaAds, GoogleAds, TikTokAds
from .channels import EmailChannel, SMSChannel, SocialChannel

app = FastAPI(
    title="Hanzo Marketing",
    description="AI-powered marketing automation with genetic algorithm optimization",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
forecaster = Forecaster()
pattern_detector = PatternDetector()
campaign_generator = CampaignGenerator()


# Request/Response models
class OptimizeRequest(BaseModel):
    platforms: list[str]
    total_budget: float
    target_roas: float = 2.0


class ForecastRequest(BaseModel):
    metric: str
    platform: str | None = None
    days_ahead: int = 30


class GenerateRequest(BaseModel):
    product: str
    target_audience: str
    platform: str
    tone: str = "professional"
    n_variants: int = 3


# Health check
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "hanzo-marketing"}


# Optimization endpoints
@app.post("/api/v1/optimize/budget")
async def optimize_budget(request: OptimizeRequest):
    """Optimize budget allocation across platforms using genetic algorithm."""
    search_space = [
        SearchSpace(name=f"{p}_budget_pct", min_val=0.0, max_val=1.0)
        for p in request.platforms
    ] + [
        SearchSpace(name=f"{p}_bid_mult", min_val=0.5, max_val=2.0)
        for p in request.platforms
    ]

    def fitness(individual):
        budget_pcts = individual[: len(request.platforms)]
        total = sum(budget_pcts)
        if total > 0:
            budget_pcts = [p / total for p in budget_pcts]
        score = sum(
            pct * mult
            for pct, mult in zip(budget_pcts, individual[len(request.platforms) :])
        )
        return (score,)

    optimizer = GeneticOptimizer(
        search_space=search_space,
        fitness_func=fitness,
        generations=50,
    )

    results = optimizer.optimize()
    best = results[-1] if results else None

    if best:
        params = best.best_params
        budget_pcts = [params[f"{p}_budget_pct"] for p in request.platforms]
        total = sum(budget_pcts)

        return {
            "allocation": {
                p: {
                    "budget": round(request.total_budget * (pct / total), 2),
                    "percentage": round(pct / total * 100, 1),
                    "bid_multiplier": round(params[f"{p}_bid_mult"], 2),
                }
                for p, pct in zip(request.platforms, budget_pcts)
            },
            "fitness": round(best.best_fitness, 4),
            "generations": best.generation,
        }

    raise HTTPException(status_code=500, detail="Optimization failed")


# Forecasting endpoints
@app.post("/api/v1/forecast")
async def forecast_metric(request: ForecastRequest):
    """Forecast a marketing metric."""
    return forecaster.forecast_metric(
        metric=request.metric,
        platform=request.platform,
        days_ahead=request.days_ahead,
    )


@app.get("/api/v1/forecast/anomalies")
async def detect_anomalies(
    metric: str,
    platform: str | None = None,
    threshold: float = 2.0,
):
    """Detect anomalies in metric data."""
    return forecaster.detect_anomalies(metric, platform, threshold)


# Pattern detection endpoints
@app.get("/api/v1/patterns/segments")
async def get_segments(n_segments: int = 5):
    """Segment audiences based on behavior."""
    return pattern_detector.segment_audiences(n_segments)


@app.get("/api/v1/patterns/high-value")
async def get_high_value_patterns(threshold: float = 0.1):
    """Find patterns in high-converting users."""
    return pattern_detector.find_high_value_patterns(threshold)


@app.get("/api/v1/patterns/conversion-paths")
async def get_conversion_paths(max_length: int = 5):
    """Analyze conversion paths."""
    return pattern_detector.analyze_conversion_paths(max_length)


@app.get("/api/v1/patterns/fatigue/{campaign_id}")
async def detect_fatigue(campaign_id: str, threshold: float = 0.2):
    """Detect creative/audience fatigue."""
    return pattern_detector.detect_fatigue(campaign_id, threshold)


# Content generation endpoints
@app.post("/api/v1/generate/ad-copy")
async def generate_ad_copy(request: GenerateRequest):
    """Generate ad copy variants."""
    return await campaign_generator.generate_ad_copy(
        product=request.product,
        target_audience=request.target_audience,
        platform=request.platform,
        tone=request.tone,
        n_variants=request.n_variants,
    )


@app.post("/api/v1/generate/social")
async def generate_social_posts(
    topic: str,
    platforms: list[str],
    tone: str = "engaging",
):
    """Generate social media posts."""
    return await campaign_generator.generate_social_posts(
        topic=topic,
        platforms=platforms,
        tone=tone,
    )


# Platform management endpoints
@app.get("/api/v1/platforms")
async def list_platforms():
    """List configured ad platforms."""
    return {
        "platforms": [
            {"name": "meta", "configured": bool(settings.meta_access_token)},
            {"name": "google", "configured": bool(settings.google_ads_developer_token)},
            {"name": "tiktok", "configured": bool(settings.tiktok_access_token)},
        ]
    }


# Channel endpoints
@app.post("/api/v1/channels/email/send")
async def send_email(
    to_emails: list[str],
    subject: str,
    html_content: str,
):
    """Send an email."""
    channel = EmailChannel()
    return await channel.send(to_emails, subject, html_content)


@app.post("/api/v1/channels/sms/send")
async def send_sms(to_number: str, message: str):
    """Send an SMS."""
    channel = SMSChannel()
    return await channel.send(to_number, message)


@app.post("/api/v1/channels/social/post")
async def post_social(platform: str, content: str):
    """Post to social media."""
    channel = SocialChannel()
    if platform == "twitter":
        return await channel.post_twitter(content)
    elif platform == "linkedin":
        return await channel.post_linkedin(content)
    raise HTTPException(status_code=400, detail=f"Unknown platform: {platform}")


def main():
    """Run the marketing service."""
    import uvicorn

    uvicorn.run(
        "marketing.api:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
