from enum import Enum
from typing import Any, List, Optional
from datetime import datetime
from dataclasses import dataclass


class StatusName(str, Enum):
    classified = "CLASSIFIED"
    purged = "PURGED"
    invalid = "INVALID"
    deleted = "DELETED"


@dataclass
class Status():
    name: StatusName
    key_name: str
    declaring_class_name: str


@dataclass
class Author():
    id: int
    user_id: int
    nucleus_user_id: int
    persona_id: int
    name: str
    screen_name: str
    avatar_image: str
    tagline: Optional[str]
    asset_count: int
    subscription_count: int
    is_default: bool
    is_custom_avatar_image: bool
    create_at: datetime
    update_at: datetime
    last_login_at: datetime
    newest_asset_create_at: datetime


@dataclass
class AdventureStat():
    adventure_id: int
    adventure_leaderboard_id: int
    difficulty: int  # TODO: IntEnum
    locked_captain_asset_id: Optional[int]
    losses: int
    wins: int
    point_value: int
    total_plays: int


@dataclass
class Creation():
    id: int
    original_id: Optional[int]
    parent_id: Optional[int]
    is_quality: bool
    rating: int
    name: str
    image_count: int
    locale_string: str  # TODO: StrEnum
    adventure_stat: AdventureStat
    asset_function: str  # TODO: StrEnum
    asset_id: int
    audit_trail: Optional[Any]
    author: Author
    description: str
    featured: Optional[datetime]
    required_products: List[str]  # TODO: List[StrEnum]
    source_ip: Optional[str]
    status: Status
    tags: Optional[List[str]]
    thumbnail_size: int
    type: str  # TODO: StrEnum
    update_at: datetime
