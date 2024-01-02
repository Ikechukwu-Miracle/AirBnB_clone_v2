#!/usr/bin/python3
""" This module contains the function do_pack that generates a .tgz archive
    from the contents of the web_static folder (fabric script) """

from fabric.api import local
from datetime import datetime

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
