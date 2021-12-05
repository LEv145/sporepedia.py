from enum import Enum
from typing import Any, List, Optional, Union
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
    name_key: str
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

    assets_count: int
    subscriptions_count: int

    is_default: bool
    is_custom_avatar_image: bool

    create_at: datetime
    newest_asset_create_at: datetime
    update_at: Optional[datetime]
    last_login_at: Optional[datetime]


@dataclass
class AdventureStat():
    id: int
    leaderboard_id: int

    difficulty: int  # TODO: IntEnum
    locked_captain_asset_id: Optional[int]

    plays_count: int
    losses_count: int
    wins_count: int
    points_count: int

    update_at: datetime


@dataclass
class Creation():
    id: int
    original_id: Optional[int]
    parent_id: Optional[int]

    rating: Optional[Union[int, float]]
    name: str
    type: str  # TODO: StrEnum
    description: Optional[str]
    images_count: int
    thumbnail_size: int
    source_ip: Optional[str]
    locale_string: Optional[str]  # TODO: StrEnum
    required_products: List[str]  # TODO: List[StrEnum]
    tags: Optional[List[str]]

    audit_trail: Any

    asset_id: int
    asset_function: str  # TODO: StrEnum

    is_quality: bool

    create_at: datetime
    update_at: datetime
    feature_at: Optional[datetime]

    author: Author
    adventure_stat: Optional[AdventureStat]
    status: Status


@dataclass
class SearchServiceResult():
    result_size: int
    results: List[Creation]
