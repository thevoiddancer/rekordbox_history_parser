import typing as tp
import csv
import math

COLUMNS_HISTORY = ['order', 'artwork', 'title', 'artist', 'album', 'genre', 'BPM', 'rating', 'time', 'key', 'added']
COLUMNS_RECORDING = ['order', 'title', 'artist', 'file', 'timestamp']


def detect_encoding(filename: str):
    """Detects the file encoding from a list of hardcoded encodings

    Parameters
    ----------
    filename : str
        File name for the file to detect decoding

    Returns
    -------
    str
        Encoding of the file.

    Raises
    ------
    ValueError
        If none of the encodings fit.
    """
    encodings = ['utf-8', 'utf-16']
    encoding = None
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                file.readline()
            break
        except:
            continue
    else:
        raise ValueError('Encoding not in the list of encodings')
    return encoding


def history_to_dict(filename: str) -> list[dict[str, str]]:
    """Parses the history .txt file into a list of dictionary.

    Parameters
    ----------
    filename : str
        File name for the history .txt file

    Returns
    -------
    list[dict[str, str]]
        List of songs played. Each song has all the available attributes.

    Raises
    ------
    ValueError
        If number of columns is different the the expected. Indicates format change.
    """
    data: list[dict[str, str]] = []
    encoding = detect_encoding(filename)

    with open(filename, 'r', encoding=encoding) as file:
        for line in file.readlines():
            if line[0] == '#':
                continue
            split_lines = line.split('\t')
            if len(split_lines) != len(COLUMNS_HISTORY):
                raise ValueError(f'Incorrect number of columns for line {split_lines[0]}')
            d = {k: v for k, v in zip(COLUMNS_HISTORY, split_lines)}
            data.append(d)
    return data


def recording_to_dict(filename: str):
    """Parses the playlist .cue file into a list of dictionary.

    Parameters
    ----------
    filename : str
        File name for the playlist .cue file

    Returns
    -------
    list[dict[str, str]]
        List of songs played. Each song has all the available attributes.

    Raises
    ------
    ValueError
        If number of columns is different the the expected. Indicates format change.
    """
    data = []
    d = {}
    encoding = detect_encoding(filename)
    with open(filename, 'r', encoding=encoding) as file:
        for line in file.readlines():
            if not line.startswith('\t'):
                continue
            # print(line)
            if line.startswith('\tTRACK'):
                if d:
                    data.append(d)
                d = {}
            elif line.startswith('\t\t'):
                k, v = line.split(' ', maxsplit=1)
                k = k.strip().lower()
                if k == 'file':
                    v = v.rsplit(' ', maxsplit=1)[0]
                elif k == 'index':
                    k = 'order'
                    v, time = v.split(' ')
                    d['timestamp'] = time.strip()
                elif k == 'performer':
                    k = 'artist'
                v = v.strip().strip('"')
                d[k] = v
        data.append(d)
    return data


def trim_playlist(playlist: list[dict[str, str]], keys: list[str]):
    """Trims the playlist to just the columns specified in keys.

    Parameters
    ----------
    playlist : list[dict[str, str]]
        Playlist
    keys : list[str]
        List of keys for trimming

    Returns
    -------
    list[dict[str, str]]
        Trimmed playlist dictionary

    Raises
    ------
    ValueError
        If key is specified that does not exist in the input playlist.
    """
    if (missing_keys := set(keys).difference(set(playlist[0].keys()))):
        raise ValueError(f'Keys not found: {missing_keys}')
    playlist = [{k: song[k] for k in keys} for song in playlist]
    return playlist


def playlist_to_string(playlist):
    """Joins the playlist for a string output. Joins in order it's in the dictionary.

    Parameters
    ----------
    playlist : list[dict[str, str]]
        Playlist data
    keys : list[str]
        List of keys for trimming

    Returns
    -------
    list[dict[str, str]]
        Trimmed playlist dictionary

    Raises
    ------
    ValueError
        If key is specified that does not exist in the input playlist.
    """
    output_string = '\n'.join([' - '.join(song.values()) for song in playlist])
    return output_string


def renumerate_playlist(playlist, keys):
    """Renumerates the playlist list.

    Parameters
    ----------
    playlist : list[dict[str, str]]
        Playlist data
    keys : list[str]
        List of keys for trimming

    Returns
    -------
    list[dict[str, str]]
        Trimmed playlist dictionary

    Raises
    ------
    None
    """
    if 'order' in keys:
        digits = math.ceil(math.log10(len(playlist)))
        for idx, song in enumerate(playlist):
            song['order'] = str(idx + 1).zfill(digits)
    return playlist


def new_name(filename, extension):
    name = filename.rsplit('.', maxsplit=1)[0]
    name += '_output.' + extension
    return name


def write_to_text(filename, playlist):
    filename = new_name(filename, 'txt')

    with open(filename, 'w') as file:
        output = playlist_to_string(playlist)
        file.write(output)


def write_to_csv(filename, columns, playlist):
    filename = new_name(filename, 'csv')

    with open(filename, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(playlist)


def factory_parser(kind: str) -> tp.Callable:
    if kind == 'history':
        return history_to_dict
    elif kind == 'recording':
        return recording_to_dict
    else:
        raise ValueError(f'Unknown type: {kind}')


def factory_outputter(kind: str) -> tp.Callable:
    if kind == 'csv':
        return write_to_csv
    elif kind == 'txt':
        return write_to_text
