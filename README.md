# MWG Photo Manager

Cross-platform photo manager with unified indexing (that means create indexing for once, you can browse your photos on any other platforms or other devices). The indexing uses relative path, don't worrry if you move photos to new devices!

The project is based on python. Configure your virtual environments, then enjoy using it.

<br/>
<br/>
<br/>

## Using Scenario

1. I am using MacOS, but I would like to open my album on Windows with `zero cost`. (no re-indexing, sync all my favorates, etc)

2. My album is on a portable drive, I would like to browse my photos using other devices with `zero cost`.

3. I would like to move my albums to another place with `zero cost`.

<br/>
<br/>
<br/>

## Demo

![](demo.png)





## Codeless usage

1. Download `release_macos.zip`.

3. Unzip it, and you will find a folder `manage`.

4. Open `manage` folder, find a program called `manage`. Double-click it.

5. Open browser and go to `http://127.0.0.1:8000`.

<br/>

## (Optional) Migrate to new places or new OS

If the new OS is the same with the current one, directly copy both photomgt and all the photos to new places.

If the new OS is different from the current one, just copy `data` folder, and download another distribution.


<br/>
<br/>
<br/>


## Developers

### Clone this project

```bash
git clone https://github.com/bokesyo/photomgt.git
```

### Move this project to your photo directory

You need to place all your photos in a directory, say `Photos`. Then please move this directory to `Photos` as well.

```bash
mv -r photomgt /Users/xxxx/Photos
```

### Configure virtual enviroments

For each OS, you just need to configure this once. Firstly you need to install python3. Then use pip to install dependencies.


```bash
cd /Users/xxxx/Photos/photomgt
pip install -r requirements.txt
```


### Start server

```bash
python manage.py runserver 127.0.0.1:8000
```

