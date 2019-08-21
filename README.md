# Marauder

Marauder is a python program used to automatically download media artworks. Currently, it only uses iTunes database.

## Installation

Download the source file and install requirements using [pip](https://pip.pypa.io/en/stable/) package manager.
```bash
pip3 install -r requirements.txt
```

## Usage

```bash
python3 /path/to/marauder.py [options] [-q manual_query] [-c category] [-p path] [-d artwork_dimensions] [-n artwork_name] 
```
Tries to find the artwork of query in defined category and save it to path. For music category, when not provided with a query, the program uses [mutagen](https://github.com/quodlibet/mutagen) to scan music files present in path and detect one album. If option -a is set, the artwork for any album present in path will be downloaded.
