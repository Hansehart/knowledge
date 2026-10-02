"""Check that the rules accept what is valid and reject what is not."""

from importlib.resources import files

import pytest
from pyshacl import validate
from rdflib import Graph

SHAPES = Graph().parse(data=files("knowledge").joinpath("schema/shapes.ttl").read_text(encoding="utf-8"), format="turtle")

# The example things every case is built from: invented, in the real formats.
PREFIXES = """
@prefix item:         <http://zotero.org/users/0/items/> .
@prefix resourcelist: <http://purl.org/vocab/resourcelist/schema#> .
@prefix source:       <https://data.hansehart.de/id/source/> .
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
            "item:AAAAAAAA a zotero:UserItem ; resourcelist:resource source:example-one .",
            True,
            id="one item points to one source",
        ),
        pytest.param(
            "item:AAAAAAAA a zotero:UserItem ; resourcelist:resource source:example-one , source:example-two .",
            False,
            id="one item points to two sources",
        ),
        pytest.param(
            """item:AAAAAAAA a zotero:UserItem ; resourcelist:resource source:example-one .
               item:BBBBBBBB a zotero:UserItem ; resourcelist:resource source:example-one .""",
            False,
            id="two items point to the same source",
        ),
        pytest.param(
            "item:AAAAAAAA a zotero:UserItem .",
            False,
            id="an item points to no source",
        ),
    ],
)
def test_rules(data: str, *, expected: bool) -> None:
    """Each example is accepted or rejected as the rules intend."""
    assert conforms(data) is expected
