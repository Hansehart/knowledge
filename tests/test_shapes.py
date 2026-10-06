# SPDX-FileCopyrightText: Copyright (c) 2026 Hansehart
# SPDX-License-Identifier: MIT

"""Check that the rules accept valid data and reject invalid data."""

import pathlib
from importlib import resources

import pyshacl
import pytest
import rdflib
from pyshacl import validator_conformance
from rdflib import collection, term

MANIFEST = rdflib.Namespace("http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#")
RULES = rdflib.URIRef("https://data.hansehart.de/def/shapes")
SHACLTEST = rdflib.Namespace("http://www.w3.org/ns/shacl-test#")


def load(location: term.Node | None) -> rdflib.Graph:
    """Read the graph found at the given location, or the rules the package ships.

    Args:
        location: Where the graph is, or the name of the rules the package ships.

    Returns:
        The graph read from that location.
    """
    if location == RULES:
        rules = resources.files("knowledge").joinpath("schema/shapes.ttl").read_text(encoding="utf-8")
        return rdflib.Graph().parse(data=rules, format="turtle")
    return rdflib.Graph().parse(str(location), format="turtle")


def collect(location: term.Node) -> list[tuple[rdflib.Graph, term.Node]]:
    """Collect every case of a manifest and of the manifests it includes.

    Args:
        location: Where the manifest is.

    Returns:
        One pair per case, the graph that describes it and the case itself.
    """
    tests = load(location)
    own = [
        (tests, entry) for entries in tests.objects(None, MANIFEST.entries) for entry in collection.Collection(tests, entries)
    ]
    included = [case for include in sorted(tests.objects(None, MANIFEST.include), key=str) for case in collect(include)]
    return own + included


CASES = collect(rdflib.URIRef((pathlib.Path(__file__).parent / "shapes" / "manifest.ttl").as_uri()))


@pytest.mark.parametrize(("tests", "entry"), CASES, ids=[str(tests.value(entry, rdflib.RDFS.label)) for tests, entry in CASES])
def test_rules(tests: rdflib.Graph, entry: term.Node) -> None:
    """Each case ends with exactly the result it expects.

    Args:
        tests: The graph that describes the case.
        entry: The case to run.
    """
    action = tests.value(entry, MANIFEST.action)
    data = load(tests.value(action, SHACLTEST.dataGraph))
    shapes = load(tests.value(action, SHACLTEST.shapesGraph))
    expected = tests.value(entry, MANIFEST.result)
    assert isinstance(expected, rdflib.URIRef | rdflib.BNode)
    _, report, _ = pyshacl.validate(data, shacl_graph=shapes)
    assert validator_conformance.check_sht_result(report, tests, expected)
