#! /bin/python
import pkg_resources
from docopt import docopt
from unsplash_dl.download_command_config import DownloadCommandConfig
from unsplash_dl.download_command import DownloadCommand
from unsplash_dl.logger import log

doc = """unsplash

CLI to download images from unsplash.

Usage:
  unsplash
  unsplash --version
  unsplash download -c=<str> -t=<str> -d=<str> [--min-width=<int>] [--min-height=<int>] [--min-likes=<int>] [-H] [-v]

Options:
  -h --help                     Show this screen
  -v --verbose                  Enable logging
  --version                     Show version.

  -c=<str> --collection=<str>   Collection to download
  -t=<str> --token=<str>        Unsplash API token
  -d=<str> --directory=<str>    Directory to download to
  -H --ignore-vertical          Ignore vertical photos
  --min-width=<int>             Minimal width
  --min-height=<int>            Minimal height
  --min-likes=<int>             Minimal likes
"""

version = pkg_resources.get_distribution('unsplash_dl').version


def main():
    args = docopt(doc, version=version)

    if args.get('--verbose'):
        log.setLevel('INFO')
        log.info('Verbose logging has been enabled')

    log.info(f'{args}')

    if args['download'] == True:
        config = DownloadCommandConfig(args)
        DownloadCommand(config).run()
        exit(0)

if __name__ == '__main__':
    main()
