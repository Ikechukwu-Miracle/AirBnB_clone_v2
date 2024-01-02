#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py) that creates
and distributes an archive to your web servers, using the function deploy
"""
from fabric.api import *
from datetime import datetime
from os.path import exists


env.hosts = ["52.91.126.194", "100.26.170.64"]


def do_pack():
    """Generate a .tgz archive from web_static"""

    local("mkdir -p versions")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archiveName = "web_static_{}.tgz".format(timestamp)

    result = local("tar -cvzf versions/{} web_static".format(archiveName))

    if result.succeeded:
        arch_path = "versions/{}".format(archiveName)
        return arch_path
    else:
        return None


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


def deploy():
    """
    creates and distributes an archive to your web servers
    """
    new_archive = do_pack()

    if not exists(new_archive):
        return False

    res = do_deploy(new_archive)

    return res
