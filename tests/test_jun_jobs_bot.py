import pytest
from jun_jobs_bot.logic import exceptions
from jun_jobs_bot.logic.user_requests import validate_data


@pytest.mark.parametrize('data',
                         [({'language': 'Wrong Python',
                           'compare_type': 'Per Week'}),
                          ({'language': 'Java',
                            'compare_type': 'Wrong Type'})
                          ])
def test_validate_data1(data):
    with pytest.raises(exceptions.NotCorrectMessage):
        validate_data(data)


