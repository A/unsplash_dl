class DownloadCommandConfig(object):
    def __init__(self, args):
        self.token = args.get('--token', None)
        self.collection = args.get('--collection', None)
        self.directory = args.get('--directory', None)

        # Filtering
        self.ignore_vertical = args.get('--ignore-vertical', False)
        self.min_width = int(args.get('--min-width')) if args.get('--min-width') else 0
        self.min_height = int(args.get('--min-height')) if args.get('--min-height') else 0
        self.min_likes = int(args.get('--min-likes')) if args.get('--min-likes') else 0

    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)

