"""Check that the rules accept what is valid and reject what is not."""

from importlib.resources import files
from pathlib import Path

import pytest
from pyshacl import validate
from rdflib import Graph

SHAPES = Graph().parse(data=files("knowledge").joinpath("schema/shapes.ttl").read_text(encoding="utf-8"), format="turtle")

EXAMPLES = (Path(__file__).parent / "examples.ttl").read_text(encoding="utf-8")


def conforms(data: str) -> bool:
    """Tell whether the given data follows every rule."""
    graph = Graph().parse(data=EXAMPLES + data, format="turtle")
    result = validate(graph, shacl_graph=SHAPES)
    return bool(result[0])


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        pytest.param(
            """<http://zotero.org/users/0/items/AAAAAAAA>
                   a zotero:UserItem ;
                   <http://purl.org/vocab/resourcelist/schema#resource> <https://data.hansehart.de/id/source/example-one> .""",
            True,
            id="one item points to one source",
        ),
        pytest.param(
            """<http://zotero.org/users/0/items/AAAAAAAA>
                   a zotero:UserItem ;
                   <http://purl.org/vocab/resourcelist/schema#resource> <https://data.hansehart.de/id/source/example-one> ,
                                                                        <https://data.hansehart.de/id/source/example-two> .""",
            False,
            id="one item points to two sources",
        ),
        pytest.param(
            """<http://zotero.org/users/0/items/AAAAAAAA>
                   a zotero:UserItem ;
                   <http://purl.org/vocab/resourcelist/schema#resource> <https://data.hansehart.de/id/source/example-one> .
               <http://zotero.org/users/0/items/BBBBBBBB>
                   a zotero:UserItem ;
                   <http://purl.org/vocab/resourcelist/schema#resource> <https://data.hansehart.de/id/source/example-one> .""",
            False,
            id="two items point to the same source",
        ),
        pytest.param(
            """<http://zotero.org/users/0/items/AAAAAAAA>
                   a zotero:UserItem .""",
            False,
            id="an item points to no source",
        ),
    ],
)
def test_rules(data: str, *, expected: bool) -> None:
    """Each example is accepted or rejected as the rules intend."""
    assert conforms(data) is expected
