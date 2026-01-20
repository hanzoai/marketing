"""Core marketing functionality."""

from .config import settings
from .models import Campaign, Audience, Creative, Experiment

__all__ = ["settings", "Campaign", "Audience", "Creative", "Experiment"]
