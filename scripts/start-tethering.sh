#!/usr/bin/env bash

if [ -f /etc/ods/ods.rc ]; then
    . /etc/ods/ods.rc
fi

if [ -f ../etc/ods.rc ]; then
    . ../etc/ods.rc
fi

ods_cache=$ODS_WORKDIR/cache
start_folder=`pwd`
hooks_folder=`echo $start_folder | sed 's/scripts/hooks/'`
hook=$hooks_folder/ods-gphoto2-hook.py

if [ ! -d $ODS_WORKDIR ]; then
    mkdir $ODS_WORKDIR
fi

if [ ! -d $ods_cache ]; then
    mkdir $ods_cache
fi

if [ ! -f $ODS_WORKDIR/newest.jpg ]; then
    cp $ODS_LOGO $ODS_WORKDIR/newest.jpg
fi

eog $ODS_WORKDIR/newest.jpg &

pushd $ods_cache
gphoto2 -q --capture-tethered --hook-script=$hook
popd
