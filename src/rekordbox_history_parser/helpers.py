from rekordbox_history_parser.constants import COLUMNS


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
    encodings = ['utf-8', 'utf-16']
    encoding = None
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                file.readline()
            break
        except:
            continue

    with open(filename, 'r', encoding=encoding) as file:
        for line in file.readlines():
            if line[0] == '#':
                continue
            split_lines = line.split('\t')
            if len(split_lines) != len(COLUMNS):
                raise ValueError(f'Incorrect number of columns for line {split_lines[0]}')
            d = {k: v for k, v in zip(COLUMNS, split_lines)}
            data.append(d)
    return data


def trim_data(playlist: list[dict[str, str]], keys: list[str]):
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
    if (missing_keys := set(keys).difference(set(COLUMNS))):
        raise ValueError(f'Keys not found: {missing_keys}')
    playlist = [{k: song[k] for k in keys} for song in playlist]
    return playlist


def playlist_to_string(playlist):
    """Joins the playlist for a string output. Joins in order it's in the dictionary.

    Parameters
    ----------
    data : list[dict[str, str]]
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
