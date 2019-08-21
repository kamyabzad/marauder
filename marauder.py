import requests
import mutagen
import os
import argparse

extensions = ['mp3', 'flac', 'aac', 'ape', 'ogg', 'wav']
iTunes_url = 'https://itunes.apple.com/search?term={}&entity={}'
artwork_key = 'artworkUrl60'
default_category = 'album'
artwork_default_dim = 600
artwork_name_template = '{}{}.jpg'
artwork_default_name = 'artwork'


def format_url(url, size):
    name = '{}x{}bb.jpg'.format(size, size)
    return '/'.join(url.split('/')[:-1]) + '/' + name


def get_queries_from_files(use_all, path):
    audio_files = []
    if use_all:
        audio_files = [mutagen.File(f) for f in os.listdir(path) if f.split('.')[-1].lower() in extensions]
    else:
        for f in os.listdir(path):
            if f.split('.')[-1].lower() in extensions:
                audio_files.append(mutagen.File(f))
                break

    return list(set(['{} {}'.format(','.join(f['artist']), ','.join(f['album'])) for f in audio_files]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', nargs='+', type=str, default=[],
                        help='Queries to search on iTunes artworks')
    parser.add_argument('-c', default=default_category,
                        help='Entities you want to find iTunes artwork for: album, movie, ebook, podcast, etc.')
    parser.add_argument('-d', type=int, default=artwork_default_dim, help='Artwork dimensions in pixels.')
    parser.add_argument('-n', type=str, default=artwork_default_name, help='File name for artwork photo.')
    parser.add_argument('-p', type=str, default=os.getcwd(), help='Path to save acquired artworks and read media.')
    parser.add_argument('-a', action='store_true',
                        help='Whether or not you want to inspect all files\' tags. Only useful with album category')

    args = parser.parse_args()
    queries = args.q
    category = args.c
    use_all = args.a
    artwork_dim = args.d
    artwork_name = args.n
    path = args.p

    if not queries:
        if args.c == 'album':
            queries = get_queries_from_files(use_all, path)

    request_urls = [iTunes_url.format(query, category) for query in queries]

    if request_urls:
        if len(request_urls) == 1:
            artwork_name_list = [artwork_name_template.format(artwork_name, '')]
        else:
            artwork_name_list = [artwork_name_template.format(query + ' ', artwork_name) for query in queries]

        for i in range(len(request_urls)):
            try:
                artwork_url = requests.get(request_urls[i]).json()['results'][0][artwork_key]
                artwork_photo = requests.get(format_url(artwork_url, artwork_dim)).content

                with open(os.path.join(path, artwork_name_list[i]), 'wb') as handler:
                    handler.write(artwork_photo)
            except Exception as e:
                print(r'Couldn\'t acquire artwork for {}'.format(queries[i]))