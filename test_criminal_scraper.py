import pytest
import json 
from criminal_scraper import fetching_records


def test_scrapper_valid_data():
    expected_output = {
        'docket_number': 'MJ-44302-CR-0000159-2019',
        'court_office': 'MDJ-44-3-02',
        'short_caption': 'Comm. v. Smith, Steven C.',
        'filling_date': 'Closed',
        'county': 'Wyoming',
        'primary_participant': 'Smith, Steven C.',
        'otn': 'U7703754',
        'complaint_number': '2019 019120',
        'dob': '4/23/2001'
    }

    query_parms = {
        'last_name':'rios',
        'first_name':'william',
        'date_of_birth':'07/31/1975'
    }

    scraper_result = fetching_records(query_parms)

    assert expected_output == scraper_result


