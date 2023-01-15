# MWG Photo Manager

Cross-platform photo manager with unified indexing (that means create indexing for once, you can browse your photos on any other platforms or other devices). The indexing uses relative path, don't worrry if you move photos to new devices!

The project is based on python. Configure your virtual environments, then enjoy using it.

## Using Scenario

1. I am using MacOS, but I would like to open my album on Windows with `zero cost`. (no re-indexing, sync all my favorates, etc)

2. My album is on a portable drive, I would like to browse my photos using other devices with `zero cost`.

3. I would like to move my albums to another place with `zero cost`.



## Setup

### Place this project to proper place

You need to place all your photos in a directory, say `Photos`. Then you put this directory in `Photos` as well. i.e.

-Photos
    -photomgt
    -xxxx.jpg
    -xxxx.jpg
    -folder1
        -xxxxx.jpg
        -xxxxx.jpg
    
### Configure Virtual Enviroments

For each OS, you just need to configure this once.

```bash
mkdir envs
cd envs
mkdir macos_env
cd macos_env
python -m venv .

cd ..
cd ..

./envs/macos_env/bin/python -m pip install -r requirements.txt
```

### Run Server

```bash
./envs/macos_env/bin/python manage.py runserver 0.0.0.0:80
```

### Create Index

Only need to run this once (if no new photos added)

http://localhost/index_all/


## After setup

http://localhost/

## Demo

![](images/demo.png)