#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""


from fabric.api import put, run, env
from os.path import exists
from datetime import datetime

env.hosts = ["52.91.126.194", "100.26.170.64"]


def do_deploy(archive_path):
    """
    Distributes an archive to your webservers
    """

    if not exists(archive_path):
        return False

    fileName = archive_path.split('/')[-1]
    no_ex = '/data/web_static/releases/' + "{}".format(fileName.split('.')[0])
    tmp = "/tmp/" + fileName

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}/".format(no_ex))
        run("tar -xzf {} -C {}/".format(tmp, no_ex))
        run("rm {}".format(tmp))
        run("mv {}/web_static/* {}/".format(no_ex, no_ex))
        run("rm -rf {}/web_static".format(no_ex))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(no_ex))
        return True
    except Exception as e:
        return False
