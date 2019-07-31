from ioservice.downloaders.Downloader import Downloader
from ioservice.uploaders.Uploader import Uploader
from ioservice.cleaners.Cleaner import Cleaner
import utils.Constants as Sc
from auditlogging.Auditor import audit_params
from utils.Utils import current_time_in_millis, time_taken


def download(downloader: Downloader) -> list:
    """
    The caller should inject the appropriate implementation to perform
    download operation as per use case

    Parameters
    ----------
    downloader: Downloader
                instance of custom downloader implementation which has overridden
                download() function

    Returns
    ----------
    list
        list of downloaded files ordered by last modified time,
        earlier will be the first element

    """
    _start = current_time_in_millis()
    audit_params(Sc.OPERATION_DOWNLOAD, Sc.STATUS_PROCESSING, 'Files are downloading from source to destination')

    files = downloader.download()

    audit_params(Sc.OPERATION_DOWNLOAD, Sc.STATUS_COMPLETE, 'Files are downloaded to destination' + time_taken(_start))

    return files


def upload(uploader: Uploader) -> list:
    """
    The caller should inject the appropriate implementation to perform
    upload operation as per use case

    Parameters
    ----------
    uploader: Uploader
              instance of custom uploader implementation which has overridden
              upload() function

    Returns
    --------
    list
        a list of uploaded files

    """
    _start = current_time_in_millis()
    audit_params(Sc.OPERATION_UPLOAD, Sc.STATUS_PROCESSING, 'Files are uploading from source to destination')

    files = uploader.upload()

    audit_params(Sc.OPERATION_UPLOAD, Sc.STATUS_COMPLETE, 'Files are uploaded to destination' + time_taken(_start))

    return files


def cleanup(cleaner: Cleaner):
    """
    The caller should inject the appropriate implementation to perform
    cleanup operation as per use case

    Parameters
    ----------
    cleaner: Cleaner
             instance of custom cleaner implementation which has overridden
             clean() function

    """
    _start = current_time_in_millis()
    audit_params(Sc.OPERATION_FILE_DELETE, Sc.STATUS_PROCESSING, 'Cleaning proecssed files')

    cleaner.clean()

    audit_params(Sc.OPERATION_FILE_DELETE, Sc.STATUS_COMPLETE, 'Processed files are cleaned' + time_taken(_start))

