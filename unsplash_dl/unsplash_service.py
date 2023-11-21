import os
from requests.models import HTTPError
from unsplash_dl.logger import log
import requests
import math
from tqdm.auto import tqdm
import functools
import pathlib
import shutil
from urllib.parse import urlparse

PER_PAGE = 30

class UnsplashService:

    def __init__(self, token):
        self.token = token

    def _get_headers(self):
        return { "Authorization": f"Client-ID {self.token}" }

    def _get_pages_len(self, total):
        return math.ceil(total / PER_PAGE)

    def get_collection(self, collection):
        log.info(f'Getting collection "{collection}"')
        url = f"https://api.unsplash.com/collections/{collection}"
        try:
            response = requests.get(
                url, 
                headers=self._get_headers(),
            )
            return response.json()

        except HTTPError as e:
             if e.response.status_code == 404:
                 print("Collection hasn't been found")
                 return None

    def get_files(self, collection):
        log.info(f'Getting files in collection "{collection}"')
        collection_meta = self.get_collection(collection)

        if collection_meta is None:
            print("Collection hasn't been found")
            return []

        page = 1
        photos = []

        total_photos = collection_meta.get('total_photos', 0)
        total_pages = self._get_pages_len(total_photos)
        url = f"https://api.unsplash.com/collections/{collection}/photos"
        
        log.info(f"photos: {total_photos}")
        log.info(f"Pages: {total_pages}")
        print(f"Getting collection {collection}: {total_photos} photos")

        while page <= total_pages:
            log.info(f"Fetching page {page}")
            try:
                response = requests.get(
                    url, 
                    params={ "per_page": PER_PAGE, "page": page },
                    headers=self._get_headers(),
                )
                photos.extend(response.json())
                page += 1

            except HTTPError as e:
                 if e.response.status_code == 404:
                     print("Collection hasn't been found")
                     return None

        return photos

    def filter_files(self, files, directory, ignore_vertical, min_width, min_height, min_likes):
        next_files = []

        for file in files:
            width = file.get("width", 0)
            height = file.get("height", 0)
            likes = file.get("likes", 0)
            path = self._get_filename(directory, file)

            if ignore_vertical and width < height:
                log.info('Skipping vertical file')
                continue

            if min_width and width < min_width:
                self._print_file_meta(file, 0, 0)
                print('Skipping by min_width')
                continue

            if min_height and height < min_height:
                self._print_file_meta(file, 0, 0)
                print('Skipping by min_height')
                continue

            if min_likes and likes < min_likes:
                self._print_file_meta(file, 0, 0)
                print('Skipping by min_likes')
                continue

            if os.path.isfile(path):
                self._print_file_meta(file, 0, 0)
                print('Exists')
                continue

            next_files.append(file)

        print()
        return next_files

    def download_files(self, files, directory, ignore_vertical):
        total = len(files)
        for i, file in enumerate(files, 1):
            self._print_file_meta(file, i, total)
            path = self.download_file(file, directory)
            print(f" {path}\n")

    def download_file(self, file, directory):
        url = file.get('urls', {}).get('full')
        filename = self._get_filename(directory, file)
        r = requests.get(url, stream=True, allow_redirects=True)

        if r.status_code != 200:
                r.raise_for_status()  # Will only raise for 4xx codes, so...
                raise RuntimeError(f"Request to {url} returned status code {r.status_code}")

        file_size = int(r.headers.get('Content-Length', 0))

        path = pathlib.Path(filename).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)

        desc = "(Unknown total file size)" if file_size == 0 else ""
        r.raw.read = functools.partial(r.raw.read, decode_content=True)  # Decompress if needed
        with tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc) as r_raw:
            with path.open("wb") as f:
                shutil.copyfileobj(r_raw, f)

        return path

    def _get_filename(self, directory, file):
        url = file.get('urls', {}).get('full')
        parsed = urlparse(url)
        filename = f"{parsed.path.rsplit('/', 1)[-1]}.jpg"
        return f"{directory}/{filename}"

    def _print_file_meta(self, file, i, total):
        user = file.get("user", {}).get("name", "-")
        description = file.get("description") if file.get("description") else "-"
        likes = file.get("likes", "-")
        width = file.get("width", "-")
        height = file.get("height", "-")

        if description:
             description = description.replace("\\r\\n", "")

        if description is not None and len(description) > 40:
            description = f"{description[:40]}…"

        if total:
            print(f"[{i}/{total}]  {user} 󰲍 {description}, {width}x{height}  {likes}")
        else:
            print(f" {user} 󰲍 {description}, {width}x{height}  {likes}", end=" ")





