#!/usr/bin/env python

import asyncclick as click

from sporepedia import SporepediaClient


_client = SporepediaClient()


@click.group()
async def cli():
    """CLI for Spore REST API"""
