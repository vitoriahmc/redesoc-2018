import os

import twitter
from twitter.error import TwitterError


ROOT_USERNAME = 'realDonaldTrump'

DATA_DIR = 'data'


def build_path(username):
    return os.path.join(DATA_DIR, 'twitter', username + '.txt')


def main():
    api = twitter.Api(
        consumer_key='SEU CONSUMER KEY',
        consumer_secret='SEU CONSUMER SECRET',
        access_token_key='SEU ACCESS TOKEN KEY',
        access_token_secret='SEU ACCESS TOKEN SECRET',
        sleep_on_rate_limit=True,
    )

    root_path = build_path(ROOT_USERNAME)

    with open(root_path, 'w', encoding='utf-8') as root_file:
        root_data = api.GetFriends(screen_name=ROOT_USERNAME)

        for root_subdata in root_data:
            username = root_subdata.screen_name

            print(username)

            try:
                data = api.GetFriends(screen_name=username)
            except TwitterError:
                continue

            root_file.write(username + '\n')

            path = build_path(username)

            with open(path, 'w', encoding='utf-8') as file:
                for subdata in data:
                    file.write(subdata.screen_name + '\n')


if __name__ == '__main__':
    main()
