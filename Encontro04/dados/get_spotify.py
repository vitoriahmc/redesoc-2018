import os

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


ROOT_BANDID = '5M52tdBnJaKSvOpJGz8mfZ'
ROOT_NAME = 'Black Sabbath'

ROOT_DEPTH = 2

DATA_DIR = 'data'


def get_relateds(api, bandid, depth=1, names=None):
    relateds = set()

    data = api.artist_related_artists(bandid)

    for subdata in data['artists']:
        related = subdata['id']

        relateds.add(related)

        if names is not None:
            names[related] = subdata['name']

    if depth > 1:
        relateds_copy = relateds.copy()

        for related in relateds_copy:
            relateds |= get_relateds(api, related, depth - 1, names)

    return relateds


def save_relateds(bandid, relateds, names=None):
    path = os.path.join(DATA_DIR, 'spotify', bandid + '.txt')

    with open(path, 'w', encoding='utf-8') as file:
        for related in relateds:
            file.write(related)

            if names is not None:
                file.write(' ' + names[related])

            file.write('\n')


def main():
    client_credentials_manager = SpotifyClientCredentials(
        client_id='SEU CLIENT ID',
        client_secret='SEU CLIENT SECRET',
    )

    api = Spotify(client_credentials_manager=client_credentials_manager)

    names = {}
    root_relateds = get_relateds(api, ROOT_BANDID, ROOT_DEPTH, names)

    if ROOT_BANDID in names:
        del names[ROOT_BANDID]
        root_relateds.discard(ROOT_BANDID)

    save_relateds(ROOT_BANDID, root_relateds, names)

    for bandid in root_relateds:
        print(names[bandid])

        relateds = get_relateds(api, bandid)

        save_relateds(bandid, relateds)


if __name__ == '__main__':
    main()
