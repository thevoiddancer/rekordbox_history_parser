import pytest

from rekordbox_history_parser.helpers import (
    factory_outputter,
    factory_parser,
    history_to_dict,
    new_name,
    playlist_to_string,
    recording_to_dict,
    renumerate_playlist,
    trim_playlist,
    write_to_csv,
    write_to_text,
)


@pytest.mark.parametrize(
    'filename, error, expected',
    [
        pytest.param('history_ok.txt', None, {'count': 1, 'title': 'title'}, id='correct'),
        pytest.param('history_error.txt', ValueError, None, id='incorrect columns #'),
    ],
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
    'filename, error, expected',
    [
        pytest.param(
            'recording_ok.cue',
            None,
            {
                'count': 1,
                'title': 'track_title',
                'artist': 'artist_name',
                'file': 'file_location',
                'order': 'index',
                'timestamp': 'timestamp',
            },
            id='correct',
        ),
    ],
)
def test_rec_to_dict(filename, error, expected):
    filename = 'tests/data/' + filename
    if error:
        with pytest.raises(error):
            recording_to_dict(filename)
    else:
        result = recording_to_dict(filename)

        assert len(result) == expected.pop('count')
        for k, v in expected.items():
            assert result[0][k] == v
    pass


@pytest.mark.parametrize(
    'keys, error, expected',
    [
        pytest.param(['title', 'artist'], None, {'keys_count': 2}, id='correct trim'),
        pytest.param([], None, {'keys_count': 0}, id='total trim'),
        pytest.param(['title', 'artist', 'missing'], ValueError, None, id='missing keys error'),
    ],
)
def test_trim_playlist(keys, error, expected):
    filename = 'tests/data/history_ok.txt'
    playlist = history_to_dict(filename)

    if error:
        with pytest.raises(error):
            trim_playlist(playlist, keys)
    else:
        result = trim_playlist(playlist, keys)
        assert len(result[0]) == expected['keys_count']


def test_output_string():
    filename = 'tests/data/history_ok.txt'
    keys = ['title', 'artist']
    playlist = history_to_dict(filename)
    playlist = trim_playlist(playlist, keys)
    result = playlist_to_string(playlist)

    assert len(result.split('\n')) == 1
    assert 'artist' in result


@pytest.mark.parametrize(
    'keys, expected',
    [
        pytest.param(
            ['order', 'title', 'artist'], {'first value': '1'}, id='renumerate with order'
        ),
        pytest.param(['title', 'artist'], {'first value': 'title'}, id='renumerate without order'),
    ],
)
def test_renumerate_playlist(keys, expected):
    filename = 'tests/data/history_ok.txt'
    playlist = history_to_dict(filename)
    playlist = trim_playlist(playlist, keys)
    result = renumerate_playlist(playlist, keys)

    assert next(iter(result[0].values())) == expected['first value']


@pytest.mark.parametrize(
    'filename, extension, expected',
    [
        pytest.param('file_name.txt', 'csv', 'file_name_output.csv', id='change extension'),
    ],
)
def test_new_name(filename, extension, expected):
    result = new_name(filename, extension)
    assert result == expected


def test_write_text(tmp_path):
    playlist = [
        {'title': 'title1', 'artist': 'artist1'},
        {'title': 'title2', 'artist': 'artist2'},
    ]
    filename = tmp_path / 'test.txt'
    write_to_text(str(filename), playlist)

    output = tmp_path / 'test_output.txt'
    saved_output = output.read_text()
    assert len(saved_output.split('\n')) == 2
    assert 'title1' in saved_output
    assert 'artist1' in saved_output
    assert 'title2' in saved_output
    assert 'artist2' in saved_output


@pytest.mark.parametrize(
    'columns, error',
    [
        pytest.param(['title', 'artist'], None, id='correct'),
        pytest.param(['title'], ValueError, id='missing key'),
    ],
)
def test_write_csv(tmp_path, columns, error):
    playlist = [
        {'title': 'title1', 'artist': 'artist1'},
        {'title': 'title2', 'artist': 'artist2'},
    ]
    filename = tmp_path / 'test.txt'
    if error:
        with pytest.raises(error):
            write_to_csv(str(filename), playlist, columns)
    else:
        write_to_csv(str(filename), playlist, columns)

        output = tmp_path / 'test_output.csv'
        saved_output = output.read_text()
        assert len(saved_output.split('\n')) == len(playlist) + 2  # including header and newline
        assert 'title1' in saved_output
        assert 'artist1' in saved_output
        assert 'title2' in saved_output
        assert 'artist2' in saved_output


@pytest.mark.parametrize(
    'kind, expected, error',
    [
        pytest.param('history', history_to_dict, None, id='history'),
        pytest.param('recording', recording_to_dict, None, id='recording'),
        pytest.param('invalid', None, ValueError, id='unknown'),
    ],
)
def test_factory_parser(kind, expected, error):
    if error:
        with pytest.raises(error):
            factory_parser(kind)
    else:
        result = factory_parser(kind)
        assert result == expected


@pytest.mark.parametrize(
    'kind, expected, error',
    [
        pytest.param('csv', write_to_csv, None, id='csv'),
        pytest.param('txt', write_to_text, None, id='txt'),
        pytest.param('invalid', None, ValueError, id='unknown'),
    ],
)
def test_factory_outputter(kind, expected, error):
    if error:
        with pytest.raises(error):
            factory_outputter(kind)
    else:
        result = factory_outputter(kind)
        assert result == expected
