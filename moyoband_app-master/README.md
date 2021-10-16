# Introduction to using xamp.
XAMPP is an easy to install Apache distribution containing MariaDB, PHP, and Perl.Also it can work with sql.
> [XAMPP OFFICIAL SITE TO DOWNLOAD](https://www.apachefriends.org/pl/index.html)

## Importing database
1. Run xampp,click button with label "start" in actions Apache* and MySQL**.

>*This is your site on localhost.
>**This is your serwer for database.
2. After that, click on actions admin buton in MySQL***.
>***Now you are seeing site with MySQL.
3. When you have open website, click import in your bar.Later choose your [sql file](https://gitlab.com/sajdak.radoslaw/moyoband/tree/master/Application%20project/DataBase.sql).
4. Click button "done"
Now you have imported us database which we are using in us programe.


# 2) Installing kivy and pandas on Raspberry Pi
(Copy to terminal)
## Kivy

1. Install the dependencies:
>sudo apt update
>sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
>   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
>   python3-setuptools libgstreamer1.0-dev git-core \
>   gstreamer1.0-plugins-{bad,base,good,ugly} \
>   gstreamer1.0-{omx,alsa} python3-dev libmtdev-dev \
>   xclip xsel libjpeg-dev
2. Install pip dependencies:
>python3 -m pip install --upgrade --user pip setuptools
>python3 -m pip install --upgrade --user Cython==0.29.10 pillow
3. Install Kivy to Python3 globally:
To get the last release from pypi:
>python3 -m pip install --user kivy

To install master:
>python3 -m pip install --user https://github.com/kivy/kivy/archive/master.zip

Or clone locally then pip install
>git clone https://github.com/kivy/kivy
>cd kivy
>python3 -m pip install --user .

## Pandas

Installing pandas:
>sudo apt-get install python3-pandas