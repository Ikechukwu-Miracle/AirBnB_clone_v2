#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

if ! command -v nginx &> /dev/null; then
    apt-get update
    apt-get -y install nginx
fi

mkdir -p /data/web_static/releases/test /data/web_static/shared
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

sudo ln -sf /data/web_static/releases/test /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
sudo sed -i "/location \/hbnb_static\/ {/ {n; s/alias.*/alias \/data\/web_static\/current\/;/}" /etc/nginx/sites-available/default
sudo service nginx restart
exit 0