from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from . import (
        SearchParams,
        SearchFilter,
    )


class SearchRequestComposer():
    def compose(
        self,
        text: str,
        lenght: int,
        params: "SearchParams",
        filter: Optional["SearchFilter"],
        batch_id: int,
        adv: int,
        session_id: str
    ) -> str:
        _filter = (
            "NONE"
            if filter is None else
            filter.value
        )

        data = (
            "callCount=1\n"
            f"scriptSessionId={session_id}\n"
            "c0-scriptName=searchService\n"
            "c0-methodName=searchAssetsDWR\n"
            "c0-id=0\n"
            f"c0-adv={adv}\n"
            f"c0-searchText={text}\n"
            f"c0-maxResults={lenght}\n"
            f"c0-filter={_filter}\n"
            f"c0-fields={params.guaranteed_fields.compose_string()}\n"
            f"c0-functions={params.guaranteed_functions.compose_string()}\n"
            f"c0-purposes={params.guaranteed_purposes.compose_string()}\n"
            f"c0-modes={params.guaranteed_models.compose_string()}\n"
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
