"""Core data models for marketing automation."""

from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class Platform(str, Enum):
    """Supported ad platforms."""
    META = "meta"
    GOOGLE = "google"
    TIKTOK = "tiktok"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    PROGRAMMATIC = "programmatic"


class Channel(str, Enum):
    """Communication channels."""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    CHAT = "chat"
    SOCIAL = "social"


class CampaignStatus(str, Enum):
    """Campaign lifecycle status."""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    OPTIMIZING = "optimizing"


class Audience(BaseModel):
    """Target audience definition."""
    id: str
    name: str
    filters: dict[str, Any] = Field(default_factory=dict)
    size_estimate: int = 0
    platforms: list[Platform] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Creative(BaseModel):
    """Ad creative / content."""
    id: str
    name: str
    type: str  # image, video, text, carousel
    content: dict[str, Any] = Field(default_factory=dict)
    variants: list[dict[str, Any]] = Field(default_factory=list)
    performance_score: float = 0.0


class Campaign(BaseModel):
    """Marketing campaign."""
    id: str
    name: str
    status: CampaignStatus = CampaignStatus.DRAFT
    platforms: list[Platform] = Field(default_factory=list)
    channels: list[Channel] = Field(default_factory=list)
    audience: Audience | None = None
    creatives: list[Creative] = Field(default_factory=list)
    budget_daily: float = 0.0
    budget_total: float = 0.0
    start_date: datetime | None = None
    end_date: datetime | None = None
    goals: dict[str, float] = Field(default_factory=dict)  # metric: target
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Experiment(BaseModel):
    """A/B test or multivariate experiment."""
    id: str
    campaign_id: str
    name: str
    variants: list[dict[str, Any]] = Field(default_factory=list)
    traffic_split: dict[str, float] = Field(default_factory=dict)
    winning_variant: str | None = None
    confidence: float = 0.0
    status: str = "running"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class OptimizationResult(BaseModel):
    """Result from genetic algorithm optimization."""
    generation: int
    best_fitness: float
    best_params: dict[str, Any]
    population_stats: dict[str, float]
    convergence: bool = False
