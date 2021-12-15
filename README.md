# sporepedia.py
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green)

A unofficial wrapper for the Sporepedia API (https://www.spore.com/sporepedia) on Python (But нщг can be used from any other language)

# How to use
```
> sporepedia --help
Usage: sporepedia [OPTIONS] COMMAND [ARGS]...

  CLI for sporepedia

Options:
  --help  Show this message and exit.

Commands:
  search  Search from sporepedia

> sporepedia.exe search CAT --functions "is_civ_creature, is_adventure_creature, is_industry" --models "is_water" -F "most_popular_new"
{"result_size": 363, "results": [...]}
```
A simple and intuitive script, convenient output data in the form of json:3
(You can use a script from any programming language)

# Build

Build binary:
```
pyinstaller pyinstaller.spec \
  --distpath pyinstaller_builds/dist \
  --workpath pyinstaller_builds/build
```
Build for python (requires Python 3.7+)
```
pip install --editable .
```

# Work in Python
### Install:
```
pip install git+https://github.com/LEv145/sporepedia.py
```

Client:
```py
import asyncio

from sporepedia import (
    SporepediaClient,
    SearchParams,
    FieldsSearchParam,
    FunctionsSearchParam,
    PurposesSearchParam,
    SearchFilter,
)


async def main() -> None:
    async with SporepediaClient() as client:
        result = await client.search(
            text="test",
            lenght=20,
            params=SearchParams(
                fields=FieldsSearchParam(
                    is_name=True,
                    is_author=True,
                    is_tag=True,
                ),
                functions=FunctionsSearchParam(
                    is_tribe_creature=True,
                    is_adventure_creature=True,
                    is_industry=True,
                    is_adv_collect=True,
                    is_adv_puzzle=True,
                    is_adv_template=True
                ),
                purposes=PurposesSearchParam(
                    is_military=True,
                    is_cultural=True,
                ),
            ),
            filter=SearchFilter.featured,
        )
        print(result)  # SearchServiceResult(result_size=48, results=[...])


asyncio.run(main())
```
Low level API (More options to customize!>3):
```py
import asyncio

from sporepedia import (
    APIClient,
)


async def main() -> None:
    async with APIClient() as client:
        result = await client.search(
            text="test",
            adv=1,
            batch_id=2,
        )
        print(result)  # SearchServiceResult(result_size=48, results=[...])


asyncio.run(main())
```


# Coverage
```
Name                                                Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------------------------------------
sporepedia/__init__.py                                  0      0      0      0   100%
sporepedia/__main__.py                                  0      0      0      0   100%
sporepedia/api/__init__.py                              0      0      0      0   100%
sporepedia/api/client.py                                0      0      0      0   100%
sporepedia/api/methods/__init__.py                      0      0      0      0   100%
sporepedia/api/methods/dwr_parser.py                    0      0      0      0   100%
sporepedia/api/methods/mixin_protocol.py                0      0      0      0   100%
sporepedia/api/methods/mixins/__init__.py               0      0      0      0   100%
sporepedia/api/methods/mixins/search/__init__.py        0      0      0      0   100%
sporepedia/api/methods/mixins/search/builders.py        0      0      0      0   100%
sporepedia/api/methods/mixins/search/composers.py       0      0      0      0   100%
sporepedia/api/methods/mixins/search/methods.py         0      0      0      0   100%
sporepedia/api/methods/mixins/search/models.py          0      0      0      0   100%
sporepedia/client.py                                    0      0      0      0   100%
tests/test_api.py                                       0      0      0      0   100%
tests/test_cli.py                                       0      0      0      0   100%
tests/test_client.py                                    0      0      0      0   100%
tests/test_dwr_parser.py                                0      0      0      0   100%
tests/test_search.py                                    0      0      0      0   100%
-----------------------------------------------------------------------------------------------
TOTAL                                                   0      0      0      0   100%
```

TODO:
- [ ] Autotest from git (Tox)
- [x] 100% tests
- [x] Cli client
- [ ] Docs
- [ ] New methods
