from unsplash_dl.logger import log
from unsplash_dl.unsplash_service import UnsplashService


class DownloadCommand:
    def __init__(self, config) -> None:
        self.config = config
        self.unsplash_service = UnsplashService(token=self.config.token)

    def run(self):
        log.info(f'Execute download command with config: {self.config}')
        collection = self.config.collection
        directory = self.config.directory
        ignore_vertical = self.config.ignore_vertical
        min_width = self.config.min_width
        min_height = self.config.min_height
        min_likes = self.config.min_likes

        files = self.unsplash_service.get_files(collection)
        files = self.unsplash_service.filter_files(
            files,
            directory,
            ignore_vertical=ignore_vertical, 
            min_width=min_width,
            min_height=min_height,
            min_likes=min_likes,
        )
        self.unsplash_service.download_files(files, directory, ignore_vertical=ignore_vertical)
