from typing import TYPE_CHECKING, cast

from .constants import BASE_URL
from .dwr_parser import parse_dwr
from .models import (
    SearchServiceResult,
    Creation,
    Author,
    AdventureStat,
    Status,
)


def build_creation(raw_data: str) -> SearchServiceResult:  # TODO: Class
    js_object = parse_dwr(raw_data)

    result_size = cast(int, js_object["resultSize"])
    results = cast(list, js_object["resultSize"])

    return SearchServiceResult(
        result_size=result_size,
        results=[
            Creation(
                id=result["id"],
                original_id=result["originalId"],
                parent_id=result["parentId"],
                rating=result["rating"],
                name=result["name"],
                type=result["type"],
                description=result["description"],
                images_count=result["imageCount"],
                asset_id=result["assetId"],
                thumbnail_size=result["thumbnailSize"],
                source_ip=result["sourceIp"],
                audit_trail=result["auditTrail"],
                locale_string=result["localeString"],
                required_products=result["requiredProducts"],
                tags=result["tags"].split(","),
                asset_function=result["assetFunction"],
                is_quality=result["quality"],
                create_at=result["created"]._obj.to_utc_dt(),
                update_at=result["updated"]._obj.to_utc_dt(),
                feature_at=result["featured"]._obj.to_utc_dt(),  # FIXME
                author=Author(
                    id=result["author"]["id"],
                    user_id=result["author"]["userId"],
                    nucleus_user_id=result["author"]["nucleusUserId"],
                    persona_id=result["author"]["personaId"],
                    name=result["author"]["name"],
                    screen_name=result["author"]["screenName"],
                    avatar_image=f'{BASE_URL}/static/{result["author"]["avatarImage"]}',
                    tagline=result["author"]["tagline"],
                    assets_count=result["author"]["assetCount"],
                    subscriptions_count=result["author"]["subscriptionCount"],
                    is_default=result["author"]["default"],
                    is_custom_avatar_image=result["author"]["avatarImageCustom"],
                    create_at=result["author"]["dateCreated"]._obj.to_utc_dt(),
                    update_at=result["author"]["updated"]._obj.to_utc_dt(),
                    last_login_at=result["author"]["lastLogin"]._obj.to_utc_dt(),
                    newest_asset_create_at=result["author"]["newestAssetCreated"]._obj.to_utc_dt(),
                ),
                adventure_stat=AdventureStat(
                    id=result["adventureStat"]["adventureId"],
                    leaderboard_id=result["adventureStat"]["adventureLeaderboardId"],
                    difficulty=result["adventureStat"]["difficulty"],
                    locked_captain_asset_id=result["adventureStat"]["lockedCaptainAssetId"],
                    plays_count=result["adventureStat"]["totalPlays"],
                    losses_count=result["adventureStat"]["losses"],
                    wins_count=result["adventureStat"]["wins"],
                    points_count=result["adventureStat"]["pointValue"],
                    update_at=result["adventureStat"]["updated"]._obj.to_utc_dt(),
                ),
                status=Status(
                    name=result["status"]["name"],
                    name_key=result["status"]["nameKey"],
                    declaring_class_name=result["status"]["declaringClass"]["name"],
                )
            )
            for result in results
        ]
    )
