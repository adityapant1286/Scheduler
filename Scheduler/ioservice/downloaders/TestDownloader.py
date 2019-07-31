from ioservice.downloaders.Downloader import Downloader


class TestDownloader(Downloader):

    def change_dir(self, src: str, dest: str):
        raise NotImplementedError

    def change_files(self, files: list):
        raise NotImplementedError

    def download(self):
        print("Test download")

