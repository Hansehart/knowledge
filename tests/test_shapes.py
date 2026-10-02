"""Check that the rules accept what is valid and reject what is not."""

from pathlib import Path

import pytest
from pyshacl import validate
from pyshacl.validator_conformance import check_sht_result
from rdflib import BNode, Graph, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import RDFS
from rdflib.term import Node

MANIFEST = Namespace("http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#")
SHACLTEST = Namespace("http://www.w3.org/ns/shacl-test#")


def load(location: Node | None) -> Graph:
    """Read the graph found at the given location."""
    return Graph().parse(str(location), format="turtle")


def collect() -> list[tuple[Graph, Node]]:
    """Collect every case the manifest includes."""
    manifest = load(URIRef((Path(__file__).parent / "shapes" / "manifest.ttl").as_uri()))
    return [
        (tests, entry)
        for include in sorted(manifest.objects(None, MANIFEST.include), key=str)
        for tests in [load(include)]
        for entries in tests.objects(None, MANIFEST.entries)
        for entry in Collection(tests, entries)
    ]


CASES = collect()


@pytest.mark.parametrize(("tests", "entry"), CASES, ids=[str(tests.value(entry, RDFS.label)) for tests, entry in CASES])
def test_rules(tests: Graph, entry: Node) -> None:
    """Each case ends with exactly the result it expects."""
    action = tests.value(entry, MANIFEST.action)
    data = load(tests.value(action, SHACLTEST.dataGraph))
    shapes = load(tests.value(action, SHACLTEST.shapesGraph))
    expected = tests.value(entry, MANIFEST.result)
    assert isinstance(expected, URIRef | BNode)
    _, report, _ = validate(data, shacl_graph=shapes)
    assert check_sht_result(report, tests, expected)
