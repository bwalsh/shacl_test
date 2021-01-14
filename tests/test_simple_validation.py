# -*- coding: utf-8 -*-

"""Tests validation."""

from pyshacl import validate
from pprint import pprint
import json

shapes_file = '''
@prefix dash: <http://datashapes.org/dash#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <http://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
schema:PersonShape
    a sh:NodeShape ;
    sh:targetClass schema:Person ;
    sh:property [
        sh:path schema:givenName ;
        sh:datatype xsd:string ;
        sh:name "given name" ;
    ] ;
    sh:property [
        sh:path schema:birthDate ;
        sh:lessThan schema:deathDate ;
        sh:maxCount 1 ;
    ] ;
    sh:property [
        sh:path schema:gender ;
        sh:in ( "female" "male" ) ;
    ] ;
    sh:property [
        sh:path schema:address ;
        sh:node schema:AddressShape ;
    ] .
schema:AddressShape
    a sh:NodeShape ;
    sh:closed true ;
    sh:property [
        sh:path schema:streetAddress ;
        sh:datatype xsd:string ;
    ] ;
    sh:property [
        sh:path schema:postalCode ;
        sh:or ( [ sh:datatype xsd:string ] [ sh:datatype xsd:integer ] ) ;
        sh:minInclusive 10000 ;
        sh:maxInclusive 99999 ;
    ] .
'''
shapes_file_format = 'turtle'

invalid_data = '''
{
    "@context": { "@vocab": "http://schema.org/" },
    "@id": "http://example.org/ns#Bob",
    "@type": "Person",
    "givenName": "Robert",
    "familyName": "Junior",
    "birthDate": "1971-07-07",
    "deathDate": "1968-09-10",
    "address": {
        "@id": "http://example.org/ns#BobsAddress",
        "streetAddress": "1600 Amphitheatre Pkway",
        "postalCode": 9404
    }
}
'''
data_file_format = 'json-ld'



def test_invalid_data():
    """Test expected errors."""
    conforms, v_graph, v_text = validate(invalid_data, shacl_graph=shapes_file,
                                        data_graph_format=data_file_format,
                                        shacl_graph_format=shapes_file_format,
                                        inference='rdfs', debug=True,
                                        serialize_report_graph=True)

    assert not conforms, "Data should not pass validation"
    assert isinstance(v_graph, bytes), "Should have a serialized graph"
    assert "schema:address" in v_text, "missing expected error in validation report"
    assert "schema:birthDate" in v_text, "missing expected error in validation report"


def test_validation_results():
    """Test basic handling of validation errors."""
    conforms, v_graph, v_text = validate(invalid_data, shacl_graph=shapes_file,
                                         data_graph_format=data_file_format,
                                         shacl_graph_format=shapes_file_format,
                                         inference='rdfs', debug=False,
                                         serialize_report_graph=False)
    actual_results = []
    expected_results = ['http://schema.org/birthDate',
                        'http://schema.org/address']
    for subj, pred, obj in v_graph:
        if str(pred) == 'http://www.w3.org/ns/shacl#resultPath':
            actual_results.append(str(obj))

    for expected_result in expected_results:
        assert expected_result in actual_results


def test_valid_data():
    """Test expected errors."""
    #
    # let's fix the data
    #
    valid_data = json.loads(invalid_data)
    valid_data["deathDate"] = "2020-09-10"
    valid_data["address"]["postalCode"] = 94040
    valid_data = json.dumps(valid_data)


    conforms, v_graph, v_text = validate(valid_data, shacl_graph=shapes_file,
                                        data_graph_format=data_file_format,
                                        shacl_graph_format=shapes_file_format,
                                        inference='rdfs', debug=True,
                                        serialize_report_graph=True)

    assert conforms, f"Data should pass validation\n{v_text}"



