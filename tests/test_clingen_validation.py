# -*- coding: utf-8 -*-

"""Tests validation."""

from pyshacl import validate

import requests
 
shapes_file_format = 'turtle'
data_file_format = 'json-ld'


def test_validate_via_http():
    """Test validation by passing urls."""
    conforms, v_graph, v_text = validate('https://raw.githubusercontent.com/clingen-data-model/spec2shacl/master/examples/examples.json', shacl_graph='https://raw.githubusercontent.com/clingen-data-model/spec2shacl/master/shapes/shapes.ttl',
                                        data_graph_format=data_file_format,
                                        shacl_graph_format=shapes_file_format,
                                        inference='rdfs', debug=True,
                                        serialize_report_graph=True)

    assert conforms, "Data should pass validation"


def test_validate_via_strings():
    """Test validation by passing raw data."""
    data = requests.get(
        'https://raw.githubusercontent.com/clingen-data-model/spec2shacl/master/examples/examples.json').text
    shacl = requests.get(
        'https://raw.githubusercontent.com/clingen-data-model/spec2shacl/master/shapes/shapes.ttl').text
    conforms, v_graph, v_text = validate(data, shacl=shacl,
                                         data_graph_format=data_file_format,
                                         shacl_graph_format=shapes_file_format,
                                         inference='rdfs', debug=True,
                                         serialize_report_graph=True)

    assert conforms, "Data should pass validation"
