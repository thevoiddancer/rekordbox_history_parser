from rekordbox_history_parser.helpers import (
    history_to_dict,
    trim_playlist,
    renumerate_playlist,
    write_to_text,
    write_to_csv,
    recording_to_dict,
)
import argparse
from abc import ABC, abstractmethod

class ParserStrategy(ABC):
    @abstractmethod
    def parse(self, filename):
        raise NotImplementedError

class HistoryParserStrategy(ParserStrategy):
    def parse(self, filename):
        return history_to_dict(filename)
    
class RecordingParserStrategy(ParserStrategy):
    def parse(self, filename):
        return recording_to_dict(filename)

class WriterStrategy(ABC):
    @abstractmethod
    def write(self, filename, playlist, columns):
        raise NotImplementedError

class TXTWriterStrategy(WriterStrategy):
    def write(self, filename, playlist, columns=None):
        return write_to_text(filename, playlist)

class CSVWriterStrategy(WriterStrategy):
    def write(self, filename, playlist, columns):
        return write_to_csv(filename, playlist, columns)

class ParserProcessor:
    def __init__(self, parser: ParserStrategy, writer: WriterStrategy):
        self.parser = parser
        self.writer = writer

    def parse(self, filename, columns):
        playlist = self.parser.parse(filename)
        playlist = trim_playlist(playlist, columns)
        playlist = renumerate_playlist(playlist)
        self.writer.write(filename, playlist, columns)



# def history_to_txt(file_name_history):
#     columns = ['order', 'artist', 'title']

#     playlist = history_to_dict(file_name_history)
#     playlist = trim_playlist(playlist, columns)
#     playlist = renumerate_playlist(playlist)

#     write_to_text(file_name_history, playlist)

# def history_to_csv(file_name_history):
#     columns = ['order', 'artist', 'title']

#     playlist = history_to_dict(file_name_history)
#     playlist = trim_playlist(playlist, columns)
#     playlist = renumerate_playlist(playlist)

#     write_to_csv(file_name_history, columns, playlist)    

# def recording_to_txt(file_name_recording):
#     columns = ['order', 'artist', 'title']

#     playlist = recording_to_dict(file_name_recording)
#     playlist = trim_playlist(playlist, columns)
#     playlist = renumerate_playlist(playlist)

#     write_to_text(file_name_recording, playlist)

# def recording_to_csv(file_name_recording):
#     columns = ['order', 'artist', 'title']

#     playlist = recording_to_dict(file_name_recording)
#     playlist = trim_playlist(playlist, columns)
#     playlist = renumerate_playlist(playlist)

#     write_to_csv(file_name_recording, columns, playlist)    

def parse_args():
    parser = argparse.ArgumentParser(description="Parse RBOX files")
    parser.add_argument("type", help="File type (history, recording)")
    parser.add_argument("filename", help="File name")
    parser.add_argument(
        "--columns",
        help="Comma-separated list of columns to include",
        type=lambda s: [item.strip() for item in s.split(",")]
    )
    parser.add_argument(
        "--output",
        help="Output format",
        choices=["txt", "csv"],
        default="txt"
    )
    return parser.parse_args()

args = parse_args()

print(args.type)
print(args.filename)
print(args.columns)
print(args.output)

# if args.type == 'history':
#     parser = HistoryParserStrategy
# else:
#     parser = RecordingParserStrategy

# if args.output == 'txt':
#     writer = TXTWriterStrategy
# else:
#     writer = CSVWriterStrategy

