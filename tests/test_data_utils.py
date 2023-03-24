from   freezegun import freeze_time
import os
import pytest
import sys
from   time import time

try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

from commonpy.data_utils import *


def test_sliced():
    assert list(sliced([1, 2, 3, 4], 2)) == [[1, 3], [2, 4]]
    assert list(sliced([1, 2, 3, 4, 5], 2)) == [[1, 3, 5], [2, 4]]


def test_expanded_range():
    assert expanded_range('1-5') == ['1', '2', '3', '4', '5']
    assert expanded_range('2-10') == ['2', '3', '4', '5', '6', '7', '8', '9', '10']
    assert expanded_range('-5') == ['1', '2', '3', '4', '5']
    try:
        # It's a malformed expression.
        assert expanded_range('5-') == '5-'
    except ValueError:
        pass
    except Exception:
        raise


def test_unique():
    assert unique([1, 2, 3]) == [1, 2, 3]
    assert unique([1, 2, 3, 3]) == [1, 2, 3]
    assert unique([3, 2, 2]) == [2, 3]


def test_ordinal():
    assert ordinal(1) == '1st'
    assert ordinal(2) == '2nd'
    assert ordinal(3) == '3rd'
    assert ordinal(4) == '4th'
    assert ordinal(5) == '5th'
    assert ordinal(10) == '10th'


def test_pluralized():
    assert pluralized('flower', 1) == 'flower'
    assert pluralized('flower', 2) == 'flowers'
    assert pluralized('error', [1]) == 'error'
    assert pluralized('error', [1, 2]) == 'errors'
    assert pluralized('word', 3) == 'words'
    assert pluralized('bus', 3) == 'buses'
    assert pluralized('theory', 2) == 'theories'
    assert pluralized('dictionary', 2) == 'dictionaries'
    assert pluralized('flower', 1, True) == '1 flower'
    assert pluralized('flower', 2, True) == '2 flowers'
    assert pluralized('error', [1, 2], True) == '2 errors'
    assert pluralized('word', 10000, True) == '10,000 words'


def test_flattened():
    assert flattened([[1, 2], 3, [4, 5], []]) == [1, 2, 3, 4, 5]
    original = dict({'a': 1, 'b': {'c': 2}, 'd': {'e': 3, 'f': 4, 'g': [5, 6]}})
    assert flattened(original) == {'a': 1, 'b.c': 2, 'd.e': 3, 'd.f': 4, 'd.g.0': 5, 'd.g.1': 6}
    assert flattened([original, original]) == [{'a': 1, 'b.c': 2, 'd.e': 3, 'd.f': 4, 'd.g.0': 5, 'd.g.1': 6}, {'a': 1, 'b.c': 2, 'd.e': 3, 'd.f': 4, 'd.g.0': 5, 'd.g.1': 6}]
    assert flattened([[1, 2], original, [original]]) == [1, 2, {'a': 1, 'b.c': 2, 'd.e': 3, 'd.f': 4, 'd.g.0': 5, 'd.g.1': 6}, {'a': 1, 'b.c': 2, 'd.e': 3, 'd.f': 4, 'd.g.0': 5, 'd.g.1': 6}]
    assert flattened(iter(range(0, 3))) == [0, 1, 2]
    assert flattened(['abc', [1, 2], 'def']) == ['abc', 1, 2, 'def']
    original = r = [('35047019633510',
                     [{'id': '6a904e08-34dd-4392-be3d-7cbe0046c8d2',
                       'status': {'name': 'Available', 'date': '2021-09-15T21:36:13.318+00:00'},
                       'contributorNames': [{'name': 'Back, K. (Kerry)'}],
                       'formerIds': [],
                       'discoverySuppress': None,
                       'tags': {'tagList': []}}])]
    assert flattened(original) == ['35047019633510',
                                   {'id': '6a904e08-34dd-4392-be3d-7cbe0046c8d2',
                                    'status.name': 'Available',
                                    'status.date': '2021-09-15T21:36:13.318+00:00',
                                    'contributorNames.0.name': 'Back, K. (Kerry)',
                                    'formerIds': [],
                                    'discoverySuppress': None,
                                    'tags.tagList': []}]
    x = {'a':1}
    y = {'b':2}
    assert flattened([d.keys() for d in [x, y]]) == ['a', 'b']
    assert flattened([x.keys(), 1, 2, [3], 'a', 'b']) == ['a', 1, 2, 3, 'a', 'b']


def test_flattened2():
    # From a question to S.O.: https://stackoverflow.com/q/51359783/743730
    r = {
        "count": 13,
        "virtualmachine": [
            {
                "id": "1082e2ed-ff66-40b1-a41b-26061afd4a0b",
                "name": "test-2",
                "displayname": "test-2",
                "securitygroup": [
                    {
                        "id": "9e649fbc-3e64-4395-9629-5e1215b34e58",
                        "name": "test",
                        "tags": [],
                    }
                ],
                "nic": [
                    {
                        "id": "79568b14-b377-4d4f-b024-87dc22492b8e",
                        "networkid": "05c0e278-7ab4-4a6d-aa9c-3158620b6471",
                    },
                    {
                        "id": "3d7f2818-1f19-46e7-aa98-956526c5b1ad",
                        "networkid": "b4648cfd-0795-43fc-9e50-6ee9ddefc5bd",
                        "traffictype": "Guest",
                    }
                ],
                "hypervisor": "KVM",
                "affinitygroup": [],
                "isdynamicallyscalable": False
            }
        ]
    }
    assert flattened(r) == {
        'count': 13,
        'virtualmachine.0.id': '1082e2ed-ff66-40b1-a41b-26061afd4a0b',
        'virtualmachine.0.name': 'test-2',
        'virtualmachine.0.displayname': 'test-2',
        'virtualmachine.0.securitygroup.0.id': '9e649fbc-3e64-4395-9629-5e1215b34e58',
        'virtualmachine.0.securitygroup.0.name': 'test',
        'virtualmachine.0.securitygroup.0.tags': [],
        'virtualmachine.0.nic.0.id': '79568b14-b377-4d4f-b024-87dc22492b8e',
        'virtualmachine.0.nic.0.networkid': '05c0e278-7ab4-4a6d-aa9c-3158620b6471',
        'virtualmachine.0.nic.1.id': '3d7f2818-1f19-46e7-aa98-956526c5b1ad',
        'virtualmachine.0.nic.1.networkid': 'b4648cfd-0795-43fc-9e50-6ee9ddefc5bd',
        'virtualmachine.0.nic.1.traffictype': 'Guest',
        'virtualmachine.0.hypervisor': 'KVM',
        'virtualmachine.0.affinitygroup': [],
        'virtualmachine.0.isdynamicallyscalable': False
    }


def test_flattened_separator():
    original = [('35047019633510',
                 [{'id': '6a904e08-34dd-4392-be3d-7cbe0046c8d2',
                   'status': {'name': 'Available', 'date': '2021-09-15T21:36:13.318+00:00'},
                   'contributorNames': [{'name': 'Back, K. (Kerry)'}],
                   'formerIds': [],
                   'discoverySuppress': None,
                   'tags': {'tagList': []}}])]
    assert flattened(original, separator = '_') == ['35047019633510',
                                                    {'id': '6a904e08-34dd-4392-be3d-7cbe0046c8d2',
                                                     'status_name': 'Available',
                                                     'status_date': '2021-09-15T21:36:13.318+00:00',
                                                     'contributorNames_0_name': 'Back, K. (Kerry)',
                                                     'formerIds': [],
                                                     'discoverySuppress': None,
                                                     'tags_tagList': []}]



def test_flattened_separator2():
    r = {
        'a': {'a': ["x0", "x1", "x2"]},
        'b': {'b': 'foo', 'c': 'bar'},
        'c': {'c': [
            {'foo': 2, 'bar': 6, 'baz':
             ["n1", "n2", "n3", "n1.1", "n2.2"]},
            {'foo': 5, 'bar': 7, 'baz': ["n4", "n5", "n6"]},
            {'foo': 100},
        ]},
        'd': {'g': 10},
        'f': {'h': 100, 'gar': [
            {"gup": 200, "garp": [
                {"gu": 300, "gat": ["f7", "f8"]},
                {"gu": 800, "gat": ["f9", "f10", "f11"]}
            ]
             }]}
    }
    assert flattened(r, separator = '_') == {
        'a_a_0': 'x0',
        'a_a_1': 'x1',
        'a_a_2': 'x2',
        'b_b': 'foo',
        'b_c': 'bar',
        'c_c_0_bar': 6,
        'c_c_0_baz_0': 'n1',
        'c_c_0_baz_1': 'n2',
        'c_c_0_baz_2': 'n3',
        'c_c_0_baz_3': 'n1.1',
        'c_c_0_baz_4': 'n2.2',
        'c_c_0_foo': 2,
        'c_c_1_bar': 7,
        'c_c_1_baz_0': 'n4',
        'c_c_1_baz_1': 'n5',
        'c_c_1_baz_2': 'n6',
        'c_c_1_foo': 5,
        'c_c_2_foo': 100,
        'd_g': 10,
        'f_gar_0_garp_0_gat_0': 'f7',
        'f_gar_0_garp_0_gat_1': 'f8',
        'f_gar_0_garp_0_gu': 300,
        'f_gar_0_garp_1_gat_0': 'f9',
        'f_gar_0_garp_1_gat_1': 'f10',
        'f_gar_0_garp_1_gat_2': 'f11',
        'f_gar_0_garp_1_gu': 800,
        'f_gar_0_gup': 200,
        'f_h': 100
    }


def test_flattened_separator3():
    r = { '@context': 'http://127.0.0.1:8082/inventory/instances/context',
           'alternativeTitles': [],
           'childInstances': [],
           'classifications': [ { 'classificationNumber': 'QC806 .F625 2005',
                                  'classificationTypeId': 'ce176ace-a53e-4b4d-aa89-725ed7b2edac'}],
           'contributors': [ { 'contributorNameTypeId': '2b94c631-fca9-4892-a730-03ee529ffe2a',
                               'contributorTypeId': '9f0a2cf0-7a9b-45a2-a403-f68d2850d07c',
                               'contributorTypeText': 'Contributor',
                               'name': 'Fowler, C. M. R',
                               'primary': True}],
           'discoverySuppress': False,
           'editions': ['2nd ed'],
           'electronicAccess': [],
           'hrid': '672423',
           'id': '848d5d4b-6e49-49d9-b02b-c9eb19d8b07d',
           'identifiers': [ { 'identifierTypeId': 'c858e4f2-2b6b-4385-842b-60732ee14abb',
                              'value': '2003065424'},
                            { 'identifierTypeId': '8261054f-be78-422d-bd51-4ed9f33c3422',
                              'value': '0521584094'},
                            { 'identifierTypeId': '8261054f-be78-422d-bd51-4ed9f33c3422',
                              'value': '0521893070 (pbk.)'},
                            { 'identifierTypeId': '7e591197-f335-4afb-bc6d-a6d76ca3bace',
                              'value': '.b13829580'},
                            { 'identifierTypeId': '439bfbae-75bc-4f74-9fc7-b2a2d47ce3ef',
                              'value': '(OCoLC)53325178'},
                            { 'identifierTypeId': '56e2db07-522d-417b-84b4-a78c123a78e5',
                              'value': '.b13829580'},
                            { 'identifierTypeId': '56e2db07-522d-417b-84b4-a78c123a78e5',
                              'value': 'oai:caltech.tind.io:672423'}],
           'indexTitle': 'Solid earth : an introduction to global geophysics',
           'instanceFormatIds': [],
           'instanceTypeId': '6312d172-f0cf-40f6-b27d-9fa8feaf332f',
           'isBoundWith': False,
           'languages': ['eng'],
           'links': { 'self': 'http://127.0.0.1:8082/inventory/instances/848d5d4b-6e49-49d9-b02b-c9eb19d8b07d'},
           'metadata': { 'createdByUserId': '25148b30-565b-4012-8300-451fb5cbe124',
                         'createdDate': '2021-09-15T19:04:33.900+00:00',
                         'updatedByUserId': '25148b30-565b-4012-8300-451fb5cbe124',
                         'updatedDate': '2021-09-15T19:04:33.900+00:00'},
           'modeOfIssuanceId': '9d18a02f-5897-4c31-9106-c9abb5c7ae8b',
           'natureOfContentTermIds': [],
           'notes': [ { 'instanceNoteTypeId': '86b6e817-e1bc-42fb-bab0-70e7547de6c1',
                        'note': 'Includes bibliographical references and index',
                        'staffOnly': False},
                      { 'instanceNoteTypeId': '957f0d61-6cea-443a-b39e-2bc1e644c8a1',
                        'note': 'PP',
                        'staffOnly': True},
                      { 'instanceNoteTypeId': '3b66e7a6-2389-4701-b801-6bdc72106598',
                        'note': '091204',
                        'staffOnly': True}],
           'parentInstances': [],
           'physicalDescriptions': ['xviii, 685 p. : ill. (some col.) ; 25 cm'],
           'precedingTitles': [],
           'previouslyHeld': False,
           'publication': [ { 'dateOfPublication': '2005',
                              'place': 'New York Cambridge, UK',
                              'publisher': 'Cambridge University Press',
                              'role': None}],
           'publicationFrequency': [],
           'publicationRange': [],
           'series': [],
           'source': 'MARC',
           'staffSuppress': False,
           'statisticalCodeIds': [],
           'statusUpdatedDate': '2021-09-15T19:04:33.899+0000',
           'subjects': ['Geophysics', 'Earth (Planet)'],
           'succeedingTitles': [],
           'tags': {'tagList': []},
           'title': 'The solid earth : an introduction to global geophysics / C.M.R. '
           'Fowler'
          }
    assert flattened(r, separator = '_') == {
        '@context': 'http://127.0.0.1:8082/inventory/instances/context',
        'alternativeTitles': [],
        'childInstances': [],
        'classifications_0_classificationNumber': 'QC806 .F625 2005',
        'classifications_0_classificationTypeId': 'ce176ace-a53e-4b4d-aa89-725ed7b2edac',
        'contributors_0_contributorNameTypeId': '2b94c631-fca9-4892-a730-03ee529ffe2a',
        'contributors_0_contributorTypeId': '9f0a2cf0-7a9b-45a2-a403-f68d2850d07c',
        'contributors_0_contributorTypeText': 'Contributor',
        'contributors_0_name': 'Fowler, C. M. R',
        'contributors_0_primary': True,
        'discoverySuppress': False,
        'editions_0': '2nd ed',
        'electronicAccess': [],
        'hrid': '672423',
        'id': '848d5d4b-6e49-49d9-b02b-c9eb19d8b07d',
        'identifiers_0_identifierTypeId': 'c858e4f2-2b6b-4385-842b-60732ee14abb',
        'identifiers_0_value': '2003065424',
        'identifiers_1_identifierTypeId': '8261054f-be78-422d-bd51-4ed9f33c3422',
        'identifiers_1_value': '0521584094',
        'identifiers_2_identifierTypeId': '8261054f-be78-422d-bd51-4ed9f33c3422',
        'identifiers_2_value': '0521893070 (pbk.)',
        'identifiers_3_identifierTypeId': '7e591197-f335-4afb-bc6d-a6d76ca3bace',
        'identifiers_3_value': '.b13829580',
        'identifiers_4_identifierTypeId': '439bfbae-75bc-4f74-9fc7-b2a2d47ce3ef',
        'identifiers_4_value': '(OCoLC)53325178',
        'identifiers_5_identifierTypeId': '56e2db07-522d-417b-84b4-a78c123a78e5',
        'identifiers_5_value': '.b13829580',
        'identifiers_6_identifierTypeId': '56e2db07-522d-417b-84b4-a78c123a78e5',
        'identifiers_6_value': 'oai:caltech.tind.io:672423',
        'indexTitle': 'Solid earth : an introduction to global geophysics',
        'instanceFormatIds': [],
        'instanceTypeId': '6312d172-f0cf-40f6-b27d-9fa8feaf332f',
        'isBoundWith': False,
        'languages_0': 'eng',
        'links_self': 'http://127.0.0.1:8082/inventory/instances/848d5d4b-6e49-49d9-b02b-c9eb19d8b07d',
        'metadata_createdByUserId': '25148b30-565b-4012-8300-451fb5cbe124',
        'metadata_createdDate': '2021-09-15T19:04:33.900+00:00',
        'metadata_updatedByUserId': '25148b30-565b-4012-8300-451fb5cbe124',
        'metadata_updatedDate': '2021-09-15T19:04:33.900+00:00',
        'modeOfIssuanceId': '9d18a02f-5897-4c31-9106-c9abb5c7ae8b',
        'natureOfContentTermIds': [],
        'notes_0_instanceNoteTypeId': '86b6e817-e1bc-42fb-bab0-70e7547de6c1',
        'notes_0_note': 'Includes bibliographical references and index',
        'notes_0_staffOnly': False,
        'notes_1_instanceNoteTypeId': '957f0d61-6cea-443a-b39e-2bc1e644c8a1',
        'notes_1_note': 'PP',
        'notes_1_staffOnly': True,
        'notes_2_instanceNoteTypeId': '3b66e7a6-2389-4701-b801-6bdc72106598',
        'notes_2_note': '091204',
        'notes_2_staffOnly': True,
        'parentInstances': [],
        'physicalDescriptions_0': 'xviii, 685 p. : ill. (some col.) ; 25 cm',
        'precedingTitles': [],
        'previouslyHeld': False,
        'publicationFrequency': [],
        'publicationRange': [],
        'publication_0_dateOfPublication': '2005',
        'publication_0_place': 'New York Cambridge, UK',
        'publication_0_publisher': 'Cambridge University Press',
        'publication_0_role': None,
        'series': [],
        'source': 'MARC',
        'staffSuppress': False,
        'statisticalCodeIds': [],
        'statusUpdatedDate': '2021-09-15T19:04:33.899+0000',
        'subjects_0': 'Geophysics',
        'subjects_1': 'Earth (Planet)',
        'succeedingTitles': [],
        'tags_tagList': [],
        'title': 'The solid earth : an introduction to global geophysics / C.M.R. '
        'Fowler'
    }

def test_flattened_separator4():
    # From https://github.com/amirziai/flatten/blob/master/test_flatten.py
    r = {
        "a": 1,
        "b": 2,
        "c": [{"d": ['2', 3, 4], "e": [{"f": 1, "g": 2}]}]
    }
    assert flattened(r, separator = '_') == {
        'a': 1,
        'b': 2,
        'c_0_d_0': '2',
        'c_0_d_1': 3,
        'c_0_d_2': 4,
        'c_0_e_0_f': 1,
        'c_0_e_0_g': 2
    }


@freeze_time("2012-01-14 03:21:34", tz_offset=-4)
def test_timestamp():
    assert timestamp() == "Jan 13 2012 15:21:34 PST"


@freeze_time("2012-01-14 03:21:34", tz_offset=-4)
def test_parsed_datetime():
    assert str(parsed_datetime(timestamp())) == "2012-01-13 15:21:34-08:00"
