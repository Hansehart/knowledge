"""Check that the rules accept what is valid and reject what is not."""

from importlib.resources import files

import pytest
from pyshacl import validate
from rdflib import Graph

SHAPES = Graph().parse(data=files("knowledge").joinpath("schema/shapes.ttl").read_text(encoding="utf-8"), format="turtle")

PREFIXES = """
@prefix resourcelist: <http://purl.org/vocab/resourcelist/schema#> .
@prefix zotero:       <http://www.zotero.org/namespaces/export#> .
"""


def conforms(data: str) -> bool:
    """Tell whether the given data follows every rule."""
    graph = Graph().parse(data=PREFIXES + data, format="turtle")
    result = validate(graph, shacl_graph=SHAPES)
    return bool(result[0])


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        pytest.param(
            """<http://zotero.org/users/1/items/AAAAAAAA> a zotero:UserItem ;
                   resourcelist:resource <https://data.hansehart.de/id/source/one> .""",
            True,
            id="one item points to one source",
        ),
        pytest.param(
            """<http://zotero.org/users/1/items/AAAAAAAA> a zotero:UserItem ;
                   resourcelist:resource <https://data.hansehart.de/id/source/one> ,
                                         <https://data.hansehart.de/id/source/two> .""",
            False,
            id="one item points to two sources",
        ),
        pytest.param(
            """<http://zotero.org/users/1/items/AAAAAAAA> a zotero:UserItem ;
                   resourcelist:resource <https://data.hansehart.de/id/source/one> .
               <http://zotero.org/users/1/items/BBBBBBBB> a zotero:UserItem ;
                   resourcelist:resource <https://data.hansehart.de/id/source/one> .""",
            False,
            id="two items point to the same source",
        ),
        pytest.param(
            """<http://zotero.org/users/1/items/AAAAAAAA> a zotero:UserItem .""",
            False,
            id="an item points to no source",
        ),
    ],
)
def test_rules(data: str, *, expected: bool) -> None:
    """Each example is accepted or rejected as the rules intend."""
    assert conforms(data) is expected
