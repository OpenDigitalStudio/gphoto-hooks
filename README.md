# gphoto-hooks
Hook scripts for gphoto2 to use while shooting tethered

Requirements:
-------------

Python requirements for the hook are in `requirements.txt`
They can be installed directly with `pip3 -r requirements.txt`

Tethering script depends on following binaries:
`eog`
`gphoto2`

Configuration:
--------------

Copy the etc/ods.rc.example to /etc/ods/ods.rc or etc/ods.rc and set the
variables as you see fit. It will be picked up by the tethering script
(system defaults can be set in /etc/ods/ods.rc and will be overwritten
from etc/ods.rc to ease config burden).
