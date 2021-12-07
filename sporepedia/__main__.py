#!/usr/bin/env python

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


_client = SporepediaClient()


@click.group()
async def cli():
    """CLI for Spore REST API"""


@cli.command(help="Search from sporepedia")  # TODO
@click.argument(
    "text",
    type=str,
    prompt="Enter search text",
)
@click.option(
    "-Fu", "--functions",
    type=click.Choice(
        tuple(FunctionsSearchParam.__dataclass_fields__.keys())
    ),
    multiple=True,
)
@click.option(
    "-Fi", "--fields",
    type=click.Choice(
        tuple(FieldsSearchParam.__dataclass_fields__.keys())
    ),
    multiple=True,
)
@click.option(
    "-M", "--models",
    type=click.Choice(
        tuple(ModelsSearchParam.__dataclass_fields__.keys())
    ),
    multiple=True,
)
@click.option(
    "-P", "--purposes",
    type=click.Choice(
        tuple(PurposesSearchParam.__dataclass_fields__.keys())
    ),
    multiple=True,
)
@click.option(
    "-F", "--filter",
    type=click.Choice(
        tuple(SearchFilter._member_names_)
    )
)
async def search(text: str, functions, fields, models, purposes, filter):
    print(text, functions, fields, models, purposes, filter, sep="\n")
