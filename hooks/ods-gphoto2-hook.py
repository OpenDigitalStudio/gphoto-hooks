#!/usr/bin/env python3

import os
import shutil

import imageio
from PIL import Image
import pyexiv2
import rawpy

ORIENTATIONS = {
        0:0,
        1:0,
        3:3,
        4:3,
        5:6,
        6:6,
        7:5,
        8:5
        }

def init():
    pass

def start():
    print("ODS Tethering is running!")
    # TODO(jokke): Ensure all paths exists.

def download():
    source = os.getenv("ARGUMENT")
    box = int(os.getenv("ODS_FIT_BOX", default=0))
    gallery = os.getenv("ODS_GALLERY_PATH", default="").rstrip("/")
    session = os.getenv("ODS_SESSION", default="")
    destinations = os.getenv("ODS_RAW_DESTINATIONS", default="./").split(",")
    work_dir = os.getenv("ODS_WORKDIR", default=".")

    print(source+" has been downloaded")
    target_jpg = '.'.join((source.split('.')[0], "jpg"))
    md = pyexiv2.ImageMetadata(source)
    md.read()
    flip = ORIENTATIONS[md['Exif.Image.Orientation'].value]
    with rawpy.imread(source) as raw:
        rgb = raw.postprocess(no_auto_bright=True,
                              use_auto_wb=False,
                              use_camera_wb=True,
                              user_flip=flip,
                              half_size=True,
                              output_bps=8)
        imageio.imwrite("./buf.jpg", rgb)

    if box:
        with Image.open("./buf.jpg") as buf:
            long_side = 0 if buf.size[0] > buf.size[1] else 1
            factor = 1
            while buf.size[long_side]/factor > box:
                factor *= 2
            buf = buf.resize((int(buf.size[0]/factor),
                              int(buf.size[1]/factor)),
                             Image.BICUBIC)
            buf.save("./buf.jpg")
    jpgmd = pyexiv2.ImageMetadata("./buf.jpg")
    jpgmd.read()
    md.copy(jpgmd)
    jpgmd.write()

    if session:
        for i, path in enumerate(destinations):
            destinations[i] = '/'.join((path.rstrip('/'), session))
    if gallery:
        if session:
            gallery = '/'.join((gallery, session))
        shutil.copy('./buf.jpg', '/'.join((gallery, target_jpg)))
    shutil.move("./buf.jpg", "/".join((work_dir, "newest.jpg")))
    for path in destinations:
        if not path.endswith('/'):
            path = path+'/'
        shutil.copy2(source, path)
    os.unlink(source)

def stop():
    pass

ACTIONS = {
        "init":init,
        "start":start,
        "download":download,
        "stop":stop
        }

if __name__ == "__main__":
    ACTIONS[os.getenv("ACTION")]()
