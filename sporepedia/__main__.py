#!/usr/bin/env python
from dataclasses import is_dataclass
from typing import TYPE_CHECKING, Dict, Optional, Type

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

    from click import Context, Parameter


_client = SporepediaClient()


class BoolDatetimeType(click.ParamType):
    def __init__(self, dataclass_: Type["ABCSearchParam"]):
        if not is_dataclass(dataclass_):  # TODO?: Dataclass type?
            raise ValueError(f"{dataclass_!r} is not dataclass")
        self._dataclass = dataclass_

    def convert(
        self,
        user_input: str,
        parameter: Optional["Parameter"],
        ctx: Optional["Context"]
    ):
        if user_input == "all":
            return self._dataclass.all()

        if user_input == "none":
            return self._dataclass.none()

        dataclass_fields: Dict[str, Field] = (
            self._dataclass.__dataclass_fields__  # type: ignore
        )

        user_values = [
            item
            for i in user_input.split(",")
            if (item := i.strip())
        ]

        dataclass_attrs = {}

        for value in user_values:
            if value not in dataclass_fields:
                self.fail(f"{value!r} not in parametes [{', '.join(dataclass_fields.keys())}]")
            else:
                dataclass_attrs[value] = True

        return self._dataclass(**dataclass_attrs)  # type: ignore


@click.group()
async def cli():
    """CLI for Spore REST API"""
