from typing import TYPE_CHECKING, cast, Optional

from .constants import BASE_URL
from .dwr_parser import parse_dwr
from .models import (
    SearchServiceResult,
    Creation,
    Author,
    AdventureStat,
    Status,
    StatusName,
)


if TYPE_CHECKING:
    from sporepedia.api import SearchParams
    from sporepedia.enums import SearchFilter


class SearchRequestBuilder():  # TODO?: Conpositer, not builder
    def build(
        self,
        text: str,
        lenght: int,
        params: "SearchParams",
        filter: Optional["SearchFilter"],
        batch_id: int,
        adv: int
    ) -> str:
        _filter = (
            "NONE"
            if filter is None else
            filter.value
        )

        data = (
            "callCount=1\n"
            "scriptSessionId=B46A8740BB941667AB32B719F1B7115A19\n"
            "c0-scriptName=searchService\n"
            "c0-methodName=searchAssetsDWR\n"
            "c0-id=0\n"
            f"c0-adv={adv}\n"
            f"c0-searchText={text}\n"
            f"c0-maxResults={lenght}\n"
            f"c0-filter={_filter}\n"
            f"c0-fields={params._fields.compose_string()}\n"
            f"c0-functions={params._functions.compose_string()}\n"
            f"c0-purposes={params._purposes.compose_string()}\n"
            f"c0-modes={params._models.compose_string()}\n"
            "c0-param0=Object_Object:{"
                "adv:reference:c0-adv, "  # noqa: E131
                "searchText:reference:c0-searchText, "
                "maxResults:reference:c0-maxResults, "
                "fields:reference:c0-fields, "
                "functions:reference:c0-functions, "
                "purposes:reference:c0-purposes, "
                "modes:reference:c0-modes, "
                "filter:reference:c0-filter "
            "}\n"
            f"batchId={batch_id}"
        )
        return data


class SearchResponceBuilder():
    def build(self, raw_data: str) -> SearchServiceResult:
        js_object = parse_dwr(raw_data)

        result_size = cast(int, js_object["resultSize"])
        raw_results = cast(list, js_object["results"])

        return SearchServiceResult(
            result_size=result_size,
            results=[
                self.build_creation(raw_result)
                for raw_result in raw_results
            ]
        )

    def build_creation(self, raw_data) -> Creation:  # TODO?: Use cast for typing
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
            tags=raw_data["tags"].split(","),
            asset_function=raw_data["assetFunction"],
            is_quality=raw_data["quality"],
            create_at=raw_data["created"]._obj.to_utc_dt(),
            update_at=raw_data["updated"]._obj.to_utc_dt(),
            feature_at=(
                None
                if raw_data["featured"] is None else
                raw_data["featured"]._obj.to_utc_dt()
            ),
            author=self.build_author(raw_data["author"]),
            adventure_stat=(
                self.build_adventure_stat(raw_data["adventureStat"])
                if raw_data["adventureStat"] is not None else
                None
            ),
            status=self.build_status(raw_data["status"]),
        )

    def build_author(self, raw_data) -> Author:
        return Author(
            id=raw_data["id"],
            user_id=raw_data["userId"],
            nucleus_user_id=raw_data["nucleusUserId"],
            persona_id=raw_data["personaId"],
            name=raw_data["name"],
            screen_name=raw_data["screenName"],
            avatar_image=f'{BASE_URL}/static/{raw_data["avatarImage"]}',
            tagline=raw_data["tagline"],
            assets_count=raw_data["assetCount"],
            subscriptions_count=raw_data["subscriptionCount"],
            is_default=raw_data["default"],
            is_custom_avatar_image=raw_data["avatarImageCustom"],
            create_at=raw_data["dateCreated"]._obj.to_utc_dt(),
            update_at=(
                raw_data["updated"]._obj.to_utc_dt()
                if raw_data["updated"] is not None else
                None
            ),
            last_login_at=(
                raw_data["lastLogin"]._obj.to_utc_dt()
                if raw_data["lastLogin"] is not None else
                None
            ),
            newest_asset_create_at=raw_data["newestAssetCreated"]._obj.to_utc_dt(),
        )

    def build_adventure_stat(self, raw_data) -> AdventureStat:
        return AdventureStat(
            id=raw_data["adventureId"],
            leaderboard_id=raw_data["adventureLeaderboardId"],
            difficulty=raw_data["difficulty"],
            locked_captain_asset_id=raw_data["lockedCaptainAssetId"],
            plays_count=raw_data["totalPlays"],
            losses_count=raw_data["losses"],
            wins_count=raw_data["wins"],
            points_count=raw_data["pointValue"],
            update_at=raw_data["updated"]._obj.to_utc_dt(),
        )

    def build_status(self, raw_data) -> Status:
        return Status(
            name=StatusName(raw_data["name"]),
            name_key=raw_data["nameKey"],
            declaring_class_name=raw_data["declaringClass"]["name"],
        )
