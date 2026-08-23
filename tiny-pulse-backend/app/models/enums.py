"""Shared enums used across models & schemas"""

import enum


class SiteStatus(str, enum.Enum):
    """Result classification for a single health check"""

    UP = "UP"
    DOWN = "DOWN"
