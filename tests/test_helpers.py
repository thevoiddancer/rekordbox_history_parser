import pytest

from rekordbox_history_parser.helpers import history_to_dict, trim_data, playlist_to_string

@pytest.mark.parametrize(
    "filename, error, expected",
    [
        pytest.param(
            'history_ok.txt',
            None,
            {
                'count': 1,
                'title': 'title'
            },
            id='correct'
        ),
        pytest.param(
            'history_error.txt',
            ValueError,
            None,
            id='incorrect columns #'
        ),
    ]
)
def test_hist_to_dict(filename, error, expected):
    filename = 'tests/data/' + filename
    if error:
        with pytest.raises(error):
            history_to_dict(filename)
    else:
        result = history_to_dict(filename)

        assert len(result) == expected['count']
        assert result[0]['title'] == expected['title']


@pytest.mark.parametrize(
    'keys, error, expected',
    [
        pytest.param(
            ['title', 'artist'],
            None,
            {'keys_count': 2},
            id='correct trim'
        ),
        pytest.param(
            [],
            None,
            {'keys_count': 0},
            id='total trim'
        ),
        pytest.param(
            ['title', 'artist', 'missing'],
            ValueError,
            None,
            id='missing keys error'
        ),
    ]
)
def test_trim_data(keys, error, expected):
    filename = 'tests/data/history_ok.txt'
    playlist = history_to_dict(filename)

    if error:
        with pytest.raises(error):
            trim_data(playlist, keys)
    else:
        result = trim_data(playlist, keys)
        assert len(result[0]) == expected['keys_count']


# @pytest.mark.parametrize(
#     '',
#     [
#         pytest.param(
#             id=''
#         ),
#     ]
# )
def test_output_string():
    filename = 'tests/data/history_ok.txt'
    keys = ['title', 'artist']
    playlist = history_to_dict(filename)
    playlist = trim_data(playlist, keys)
    result = playlist_to_string(playlist)

    assert len(result.split('\n')) == 1
    assert 'artist' in result


