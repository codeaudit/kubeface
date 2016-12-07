import os
import glob
from . import bucket_storage


def is_google_storage_bucket(name):
    return name.startswith("gs://")


def list_contents(prefix):
    if is_google_storage_bucket(prefix):
        return bucket_storage.list_contents(prefix)

    else:
        return glob.glob(prefix + "*")


def put(name, input_handle, readers=[], owners=[]):
    if is_google_storage_bucket(name):
        return bucket_storage.put(name, input_handle, readers, owners)

    # Local file
    with open(name, 'wb') as fd:
        fd.write(input_handle.read())


def get(name, output_handle=None):
    if is_google_storage_bucket(name):
        return bucket_storage.get(name, output_handle)

    # Local file
    if output_handle is None:
        return open(name)

    with open(name) as fd:
        output_handle.write(fd.read())

    return output_handle


def delete(name):
    if is_google_storage_bucket(name):
        return bucket_storage.delete(name)

    os.unlink(name)