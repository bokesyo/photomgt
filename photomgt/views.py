from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from pathlib import Path
import os
import time
from PIL import Image
import PIL
import json


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PHOTO_BASE_DIR = BASE_DIR.parent
DATA_DIR = os.path.join(BASE_DIR, 'data')

print("BASE_DIR", str(BASE_DIR))
print("DATA_DIR", str(DATA_DIR))

global_mapping = None
prev_day_mapping = None
next_day_mapping = None
sorted_day = None


def load_indexing():
    global global_mapping, prev_day_mapping, next_day_mapping, sorted_day
    try:
        with open(os.path.join(DATA_DIR, 'date_mapping.json'), 'r') as f:
            global_mapping = json.load(f)
    except:
        print("Index is not found, please run /index_all!")
    try:
        with open(os.path.join(DATA_DIR, 'prev_day_mapping.json'), 'r') as f:
            prev_day_mapping = json.load(f)
        with open(os.path.join(DATA_DIR, 'next_day_mapping.json'), 'r') as f:
            next_day_mapping = json.load(f)
        with open(os.path.join(DATA_DIR, 'sorted_day.json'), 'r') as f:
            sorted_day = json.load(f)
    except:
        print("QuickNavigateData is not found, please run /create_navigate_index!")


load_indexing()


def get_all_file_paths(directory):
    file_paths = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            file_paths.append(os.path.join(dirpath, filename))
    return file_paths


def get_relative_file_paths(root_directory, directory):
    file_paths = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            file_paths.append(os.path.relpath(os.path.join(dirpath, filename), root_directory))
    return file_paths


#获得文件的文件的创建时间 ，使用os.path.getmtime()方法
def getfile_creat_date(path):
    ti = time.localtime(os.path.getmtime(path))
    # 对时间进行格式化
    file_creat_date = time.strftime('%Y:%m:%d', ti)
    return file_creat_date
 

# 获得照片的拍摄时间，拍摄时间不同于创建时间及修改时间
def get_mapping(files_names, base_dir):
    date_item_mapping = {}

    PIL_UnidentifiedImageError = 0
    SUCCESS = 0
    EXIF_AttributeError = 0
    EXIF_KeyError = 0
    EXIF_TypeError = 0
    No_EXIF = 0
    DateValueError = 0

    for item in files_names:
        if SUCCESS % 1000 == 0:
            print("UnidentifiedImageError", PIL_UnidentifiedImageError)
            print("EXIF_AttributeError", EXIF_AttributeError)
            print("EXIF_KeyError", EXIF_KeyError)
            print("SUCCESS", SUCCESS)
            print("No_EXIF", No_EXIF)
            print("EXIF_TypeError", EXIF_TypeError)
            print("DateValueError", DateValueError)
            print('-------')
        
        # 定义需要整理的文件格式，支持以下几种格式的照片
        if item[-3:] == 'jpg' or item[-4:] == 'jpeg' or item[-3:] == 'png' or item[-3:] == 'bmp':
            try:
                image = Image.open(item)
                h = image.height
                w = image.width
                ratio = w / h * 200
            except PIL.UnidentifiedImageError:
                PIL_UnidentifiedImageError += 1
                # 这些已经损坏 不需要索引
                continue
            try:
                file_creat_date = image._getexif()[306]
            except AttributeError:
                file_creat_date = getfile_creat_date(item)
                EXIF_AttributeError += 1
            except KeyError:
                file_creat_date = getfile_creat_date(item)
                EXIF_KeyError += 1
            except TypeError:
                file_creat_date = getfile_creat_date(item)
                EXIF_TypeError += 1
        else:
            # 若不是以上指定的格式的照片直接采用getfile_creat_date（）方法获得文件的创建时间
            file_creat_date = getfile_creat_date(item)
            No_EXIF += 1
            # 这些不是图片 不需要索引
            continue
        
        # 获得以日期命名的列表
        try:
            int(file_creat_date[0:4])
            int(file_creat_date[5:7])
            int(file_creat_date[8:10])
        except ValueError:
            DateValueError += 1
            continue
        
        yearmd = f"{file_creat_date[0:4]}-{file_creat_date[5:7]}-{file_creat_date[8:10]}"

        rel_path = os.path.relpath(item, base_dir)
        element = {"rel_path": rel_path, "ratio": ratio}
        # 添加到索引mapping
        if date_item_mapping.get(yearmd, None) is None:
            date_item_mapping[yearmd] = [element]
        else:
            date_item_mapping[yearmd].append(element)
        
        SUCCESS += 1
    
    summary = {
        "PIL_UnidentifiedImageError": PIL_UnidentifiedImageError,
        "SUCCESS": SUCCESS,
        "EXIF_AttributeError": EXIF_AttributeError,
        "EXIF_KeyError": EXIF_KeyError,
        "EXIF_TypeError": EXIF_KeyError,
        "No_EXIF": No_EXIF,
        "DateValueError": DateValueError
    }

    return date_item_mapping, summary


def index_all(request):
    """
    进行全面索引
    """
    abs_file_paths = get_all_file_paths(PHOTO_BASE_DIR)
    # print(abs_file_paths[:100])
    date_mapping, summary = get_mapping(abs_file_paths, PHOTO_BASE_DIR)
    outfile = os.path.join(DATA_DIR, 'date_mapping.json')
    print(summary)
    with open(outfile, 'w') as f:
        json.dump(date_mapping, f)
    
    create_navigate_index(request)

    load_indexing()

    return render(request, 'indexfinish.html', summary)


def create_navigate_index(request):
    """
    实现经济的导航(前一天、后一天)
    """
    with open(os.path.join(DATA_DIR, 'date_mapping.json'), 'r') as f:
        date_mapping = json.load(f)
    sorted_keys = sorted(date_mapping.keys())
    next_day_mapping = {}
    prev_day_mapping = {}

    for today_idx, today in enumerate(sorted_keys):
        # print(today_idx, today)
        prev_day_mapping[today] = sorted_keys[max(0, today_idx-1)]
        next_day_mapping[today] = sorted_keys[min(len(sorted_keys)-1, today_idx+1)]
    
    prev_day_mapping_json = os.path.join(DATA_DIR, 'prev_day_mapping.json')
    next_day_mapping_json = os.path.join(DATA_DIR, 'next_day_mapping.json')
    sorted_day_json = os.path.join(DATA_DIR, 'sorted_day.json')

    with open(prev_day_mapping_json, 'w') as f:
        json.dump(prev_day_mapping, f)
    with open(next_day_mapping_json, 'w') as f:
        json.dump(next_day_mapping, f)
    with open(sorted_day_json, 'w') as f:
        json.dump(sorted_keys, f)
    
    return HttpResponse("Create OK.")

def return_property(request, name):
    abs_img_path = os.path.join(PHOTO_BASE_DIR, name)
    image_data = open(abs_img_path, "rb").read()
    return HttpResponse(image_data,content_type="image/png")

def return_avail_dates(request):
    return JsonResponse(sorted_day, safe=False)

def frontpage(request):
    if sorted_day is None:
        last_day = "0000-00-00"
    else:
        last_day = sorted_day[-1]
    return render(request, 'frontpage.html', {'photoBaseDir': str(PHOTO_BASE_DIR), "lastDay": last_day})

def daypage(request, day_string):
    if global_mapping is None:
        prev_day = "0000-00-00"
        next_day = "0000-00-00"
        imgElementList = []
        day_string = "No indexing found, please first create indexing"
    else:
        prev_day = prev_day_mapping[day_string]
        next_day = next_day_mapping[day_string]
        imgElementList = global_mapping[day_string]
    return render(request, 'daypage.html', {'imgElementList':imgElementList, 'title':day_string, 'prevDay':prev_day, 'nextDay': next_day, 'availableDates': sorted_day})

