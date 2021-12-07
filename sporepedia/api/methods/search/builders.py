from typing import cast
from unittest.mock import patch

import js2py.base

from sporepedia.api.dwr_parser import parse_dwr
from .models import (
    SearchServiceResult,
    Creation,
    Author,
    AdventureStat,
    Status,
    StatusName,
    Difficulty,
)
from .mockups import to_python__mockup


class SearchResponceBuilder():
    def build(self, raw_data: str) -> SearchServiceResult:
        js_object = parse_dwr(raw_data)

        with patch.object(
            js2py.base,
            "to_python",
            to_python__mockup,
        ):
            data = js_object.to_dict()

        result_size = cast(int, data["resultSize"])
        raw_results = cast(list, data["results"])

        return SearchServiceResult(
            result_size=result_size,
            results=[
                self.build_creation(raw_result)
                for raw_result in raw_results
            ]
        )

    def build_creation(self, raw_data: dict) -> Creation:  # TODO?: Use cast for typing
        return Creation(
            id=raw_data["id"],
            original_id=raw_data["originalId"],
            parent_id=raw_data["parentId"],
            rating=raw_data["rating"],
            name=raw_data["name"],
            type=raw_data["type"],
            description=raw_data["description"],
            images_count=raw_data["imageCount"],
            asset_id=raw_data["assetId"],
            thumbnail_size=raw_data["thumbnailSize"],
            source_ip=raw_data["sourceIp"],
            audit_trail=raw_data["auditTrail"],
            locale_string=raw_data["localeString"],
            required_products=raw_data["requiredProducts"],
            asset_function=raw_data["assetFunction"],
            is_quality=raw_data["quality"],
            create_at=raw_data["created"],
            update_at=raw_data["updated"],
            tags=(
                raw_data["tags"].split(",")
                if raw_data["tags"] is not None else
                None
            ),
            feature_at=(
                raw_data["featured"]
                if raw_data["featured"] is not None else
                None
            ),
            author=self.build_author(raw_data["author"]),
            adventure_stat=(
                self.build_adventure_stat(raw_data["adventureStat"])
                if raw_data["adventureStat"] is not None else
                None
            ),
            status=self.build_status(raw_data["status"]),
        )

    def build_author(self, raw_data: dict) -> Author:
        return Author(
            id=raw_data["id"],
            user_id=raw_data["userId"],
            nucleus_user_id=raw_data["nucleusUserId"],
            persona_id=raw_data["personaId"],
            name=raw_data["name"],
            screen_name=raw_data["screenName"],
            avatar_image=f"https://www.spore.com/static/{raw_data['avatarImage']}",
            tagline=raw_data["tagline"],
            assets_count=raw_data["assetCount"],
            subscriptions_count=raw_data["subscriptionCount"],
            is_default=raw_data["default"],
            is_custom_avatar_image=raw_data["avatarImageCustom"],
            create_at=raw_data["dateCreated"],
            update_at=(
                raw_data["updated"]
                if raw_data["updated"] is not None else
                None
            ),
            last_login_at=(
                raw_data["lastLogin"]
                if raw_data["lastLogin"] is not None else
                None
            ),
            newest_asset_create_at=raw_data["newestAssetCreated"],
        )

    def build_adventure_stat(self, raw_data: dict) -> AdventureStat:
        return AdventureStat(
            id=raw_data["adventureId"],
            leaderboard_id=raw_data["adventureLeaderboardId"],
            difficulty=Difficulty(raw_data["difficulty"]),
            locked_captain_asset_id=raw_data["lockedCaptainAssetId"],
            plays_count=raw_data["totalPlays"],
            losses_count=raw_data["losses"],
            wins_count=raw_data["wins"],
            points_count=raw_data["pointValue"],
            update_at=raw_data["updated"],
        )

    def build_status(self, raw_data: dict) -> Status:
        return Status(
            name=StatusName(raw_data["name"]),
            name_key=raw_data["nameKey"],
            declaring_class_name=raw_data["declaringClass"]["name"],
        )
