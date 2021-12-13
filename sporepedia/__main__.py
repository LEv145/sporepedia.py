#!/usr/bin/env python
from dataclasses import is_dataclass
from typing import TYPE_CHECKING, Any, Dict, Optional, Type

import asyncclick as click

from sporepedia import (
    SporepediaClient,
    SearchParams,
    FunctionsSearchParam,
    FieldsSearchParam,
    ModelsSearchParam,
    PurposesSearchParam,
    SearchFilter,
)


if TYPE_CHECKING:
    from dataclasses import Field

    from sporepedia import ABCSearchParam

    from asyncclick import Context, Parameter


_client = SporepediaClient()


class BoolDataclassType(click.ParamType):
    name = "bool_dataclass"

    def __init__(self, dataclass_: Type["ABCSearchParam"]):
        if not is_dataclass(dataclass_):  # TODO?: Dataclass type?
            raise ValueError(f"{dataclass_!r} is not dataclass")
        self._dataclass = dataclass_

    def convert(
        self,
        user_input: str,
        parameter: Optional["Parameter"],
        ctx: Optional["Context"]
    ) -> Any:
        if user_input == "all":
            return self._dataclass.all()

        if user_input == "none":
            return self._dataclass.none()

        dataclass_fields: Dict[str, "Field"] = (
            self._dataclass.__dataclass_fields__  # type: ignore
        )

        user_values = [
            item.lower()
            for i in user_input.split(",")
            if (item := i.strip())
        ]

        dataclass_attrs = {}

        for value in user_values:
            if value not in dataclass_fields:
                self.fail(f"{value!r} not in {self._get_metavar()}")
            else:
                dataclass_attrs[value] = True

        return self._dataclass(**dataclass_attrs)  # type: ignore

    def get_metavar(self, parameter: "Parameter") -> str:
        return self._get_metavar()

    def _get_metavar(self) -> str:  # TODO?: Rename
        dataclass_fields: Dict[str, "Field"] = (
            self._dataclass.__dataclass_fields__  # type: ignore
        )

        return f"[{'|'.join(dataclass_fields)}]"


@click.group()
async def cli() -> None:
    """CLI for sporepedia"""


@cli.command(help="Search from sporepedia")
@click.argument(
    "text",
    type=str,
)
@click.option(
    "-Fu", "--functions",
    type=BoolDataclassType(FunctionsSearchParam),
)
@click.option(
    "-Fi", "--fields",
    type=BoolDataclassType(FieldsSearchParam),
)
@click.option(
    "-M", "--models",
    type=BoolDataclassType(ModelsSearchParam),
)
@click.option(
    "-P", "--purposes",
    type=BoolDataclassType(PurposesSearchParam),
)
@click.option(
    "-F", "--filter", "filter_",
    type=click.Choice(SearchFilter._member_names_, case_sensitive=False),
)
async def search(
    text: str,
    functions: Optional[FunctionsSearchParam],
    fields: Optional[FieldsSearchParam],
    models: Optional[ModelsSearchParam],
    purposes: Optional[PurposesSearchParam],
    filter_: Optional[str],
) -> None:
    async with _client as client:
        result = await client.search(
            text,
            params=SearchParams(
                functions=functions,
                fields=fields,
                models=models,
                purposes=purposes,
            ),
            filter=(
                SearchFilter[filter_]
                if filter_ is not None else
                None
            )
        )
        click.echo(result.to_json())


if __name__ == "__main__":
    cli()
