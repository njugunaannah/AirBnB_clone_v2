#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that
distributes an archive to your web servers, using the function do_deploy
"""

from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime

env.hosts = ['3.80.18.189', '18.209.224.4']


def do_pack():
    """Packs the web_static content into a .tgz file"""
    try:
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = "versions/web_static_{}.tgz".format(current_time)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        """Extract the archive to the folder
        /data/web_static/releases/<archive filename without extension>"""
        file_name = archive_path.split('/')[-1]
        folder_name =
        "/data/web_static/releases/{}".format(file_name.split('.')[0])
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_name))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(file_name))

        # Move contents to the proper location
        run("mv {}/web_static/* {}".format(folder_name, folder_name))

        # Remove the web_static folder
        run("rm -rf {}/web_static".format(folder_name))

        # Remove the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(folder_name))

        print("New version deployed!")
        return True

    except Exception as e:
        return False
