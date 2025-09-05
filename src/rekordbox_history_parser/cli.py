import argparse

from rekordbox_history_parser.helpers import (
    factory_outputter,
    factory_parser,
    renumerate_playlist,
    trim_playlist,
)


def main():
    parser = argparse.ArgumentParser(description='Parse playlist files.')
    parser.add_argument('filepath', help='Path to input file')
    parser.add_argument(
        '--type', required=True, choices=['history', 'recording'], help='Input file type'
    )
    parser.add_argument('--columns', required=True, help='Comma-separated columns to keep')
    parser.add_argument('--output', choices=['txt', 'csv'], default='string', help='Output format')

    args = parser.parse_args()
    keys_to_keep = [col.strip() for col in args.columns.split(',')]

    parser_func = factory_parser(args.type)
    playlist = parser_func(args.filepath)
    playlist = trim_playlist(playlist, keys_to_keep)
    playlist = renumerate_playlist(playlist, keys_to_keep)

    output_func = factory_outputter(args.output)
    output_func(args.filepath, playlist, keys_to_keep)


if __name__ == '__main__':
    main()
