import os
import shutil
import random
import sqlite3
import time
from operator import itemgetter

import yaml
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
import win32gui
import sys
from selenium.webdriver.support import expected_conditions as EC
import logging
import glob


yml_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + r'\data\data.yml'
f = open(yml_path, encoding="utf-8")
yml_data = yaml.load(f, Loader=yaml.FullLoader)


def log():
    log_path = yml_data['log'][0]
    # 先获取日志name
    logger = logging.getLogger(__name__)
    # 全局定义最低级别
    logger.setLevel(level=logging.DEBUG)
    # 文件输出信息级别
    handler = logging.FileHandler(log_path, encoding="utf-8", mode="a")
    handler.setLevel(logging.DEBUG)
    # 屏幕输出信息级别
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # add formatter
    formatter = logging.Formatter('%(asctime)s - %(module)s:%(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    console.setFormatter(formatter)
    # add to logger
    logger.handlers = []
    logger.addHandler(handler)
    # logger.debug(message)
    # logger.handlers = []
    logger.addHandler(console)
    # logger.debug(message)
    return logger


def get_files(path):
    file_list = []
    # os.walk 得到 tupple(dirpath, dirnames, filenames)
    # dirpath：string，代表目录的路径；
    # dirnames：list，包含了当前dirpath路径下所有的子目录名字（不包含目录路径）；
    # filenames：list，包含了当前dirpath路径下所有的非目录子文件的名字（不包含目录路径）
    for a in os.walk(path):
        file_list = file_list + a[2]
    return file_list


def get_file_number(path):
    n = len(get_files(path))
    # log().debug(n)
    return n


# compare if files in two folders are same
def compare_files(source_path, target_path):
    source_files = get_files(source_path)
    target_files = get_files(target_path)
    source_files.sort()
    target_files.sort()
    if source_files == target_files:
        log().debug('FILES ARE SAME')
        return True
    else:
        log().debug('FILES ARE DIFFERENT!')
        return False


# def read_yml(key):
#     return yml_data[key]


def clear_sub_folder(path_list):
    # 找出文件夹下的所有子文件夹，删除
    for path in path_list:
        sub_folder = []
        for root, dirs, files in os.walk(path):
            sub_folder.append(root)
        sub_folder.pop(0)
        sub_folder.reverse()
        for i in sub_folder:
            os.rmdir(i)


def load_param(class_name, case_name):
    old = list(yml_data[class_name][case_name].values())
    x = len(old)
    y = len(old[0])
    new = []
    n = []
    i = 0
    j = 0
    while i < y:
        while j < x:
            n.append(old[j][i])
            j = j + 1
        j = 0
        new.append(n)
        i = i + 1
        n = []
    return new


def del_file(path):
    if os.path.exists(path):
        for i in os.listdir(path):
            path_file = os.path.join(path, i)
            if os.path.isfile(path_file):
                os.remove(path_file)
            else:
                del_file(path_file)


# init Vegas Prepare when start automation testing
def ini_vp():
    from ruamel import yaml
    # # init config.ini and database
    # configure_ini = yml_data['configure_ini']
    # database = yml_data['database']
    # shutil.copyfile(configure_ini[1], configure_ini[0])
    # shutil.copyfile(database[1], database[0])
    # delete related data from appdata
    appdata = yml_data['appdata']
    del_file(appdata+'HubDB')
    del_file(appdata+'VEGAS Hub')
    # copy prepared configure.ini to appdata
    os.makedirs(appdata+'VEGAS Hub\\Config', exist_ok=True)
    # os.mknod(yml_data['configure_ini'][0])
    shutil.copyfile(yml_data['configure_ini'][1], yml_data['configure_ini'][0])
    # copy prepared 'VEGAS Hub.exe.config' to build path
    shutil.copyfile(yml_data['build_config'][1], yml_data['build_config'][0])
    # prepare folder for case "test_add_root_folder"
    os.makedirs(yml_data['TestLibrary']['test_add_root_folder']['folder'][0], exist_ok=True)
    os.makedirs(yml_data['TestLibrary']['test_add_root_folder']['folder'][1], exist_ok=True)
    # get build version
    version = yml_data['build'].__str__().split('[')[1].split(']')[0]
    # get automation target folder to create 'existing' target folder
    t = yml_data['target_partition']
    dir_path = t + 'AutoTarget_' + version
    if os.path.exists(dir_path):
        # shutil.move(dir_path, dir_path + time.strftime('_%Y%m%d_%H%M%S', time.localtime(time.time())))
        # archived_path = dir_path + time.strftime('_%Y%m%d_%H%M%S', time.localtime(time.time()))
        # shutil.move(dir_path, archived_path)
        shutil.rmtree(dir_path)
    os.makedirs(dir_path, exist_ok=True)
    t1 = dir_path + '\\target1'
    t2 = dir_path + '\\target2'
    os.makedirs(t1, exist_ok=True)
    os.makedirs(t2, exist_ok=True)
    # update "import_target" in data.yml
    yml_data['import_target'] = dir_path
    # update target for test case "test_import_to_existing_target" in data.yml
    yml_data['TestImport']['test_import_to_existing_target']['target'][0] = t1
    yml_data['TestImport']['test_import_to_existing_target']['target'][1] = t2
    with open(yml_path, 'w', encoding="utf-8") as nf:
        yaml.dump(yml_data, nf, Dumper=yaml.RoundTripDumper, allow_unicode=True)
    # for some source folder which is imported to library directly, maybe VEGAS Prepare will create sub folder under it
    # need clean it
    path_list = yml_data['TestImport']['test_import_to_library']['source']
    path_list = path_list + yml_data['TestLibrary']['test_add_root_folder']['folder']
    clear_sub_folder(path_list)


# according keyword name, find its id
def db_assigned_keyword_id(n):
    current_database = yml_data['database']
    mydb = sqlite3.connect(current_database)
    cursor = mydb.cursor()
    # excute_sen = "select id from tag where name is '%s';" % n
    excute_sen = "select Id from Keyword where Name is '%s';" % n
    cursor.execute(excute_sen)
    tables = cursor.fetchall()
    keyword_id = tables[0][0]
    return keyword_id


# # 根据需求的类型，从数据库里随机获取，返回路径
# def db_random(s_type, n='random'):
#     # according s_type, get all from tables:
#     # collection-->all collections
#     # collection_set-->all collection sets
#     # collection_file-->all collections and collection sets
#     # library, library_file-->all folders
#     t_db = ''
#     if s_type == 'collection' or s_type == 'collection_set' or s_type == 'collection&set' or s_type == 'collection_file':
#         t_db = 'collection'
#     elif s_type == 'library' or s_type == 'library_file':
#         t_db = 'dir'
#     current_database = read_yml('database')[0]
#     mydb = sqlite3.connect(current_database)
#     cursor = mydb.cursor()
#     excute_sen = "select * from %s;" % t_db
#     if s_type == 'collection':
#         excute_sen = "select * from %s where isset=0;" % t_db
#     elif s_type == 'collection_set':
#         excute_sen = "select * from %s where isset=1;" % t_db
#     cursor.execute(excute_sen)
#     # 读取collection或者dir两张数据库表，满足条件的所有数据，放到tables里，列表嵌套列表的形式
#     tables = cursor.fetchall()
#     logger.info(tables)
#     # 如果数据库的collection或者dir里没有数据，返回False
#     if not tables:
#         logger.info('no data')
#         return False
#     # 有数据的话，取collection/collection set/folder, and its path
#     else:
#         # 如果传入的n是random，从数据库里随机取一个
#         if n == 'random':
#             # 从tables里随机选出一个值
#             random_c = random.choice(tables)
#             logger.info(random_c)
#         else:
#             # 如果变量传入了值，根据需要第几个item来pop
#             random_c = tables.pop(int(n) - 1)
#         # 获取选中的item的id
#         random_id = random_c[0]
#         # 获取该item的name，并创造一个random_path的列表
#         random_path = [random_c[1]]
#         # 如果选中的item的parent id不是0，继续下面的循环
#         while random_c[2] != 0:
#             # 根据random_c[2]，也就是parent id找到parent那一行
#             cursor.execute("select * from %s where id='%s';" % (t_db, random_c[2]))
#             tables = cursor.fetchall()
#             # 因为是列表嵌套列表的形式，所以需要读取第一个列表
#             random_c = tables[0]
#             # 读取parent的name，加到random_path里
#             random_path.append(random_c[1])
#         # 循环完所有的parent，把random_path整个列表翻转一下
#         random_path.reverse()
#         # 在random_path列表里加上选中的item的id
#         random_path.append(random_id)
#         logger.info(random_path)
#         return random_path


def get_from_db(excute_sen):
    current_database = yml_data['database']
    mydb = sqlite3.connect(current_database)
    cursor = mydb.cursor()
    cursor.execute(excute_sen)
    tables = cursor.fetchall()
    # return [(a1,b1), (a2,b2)]
    return tables


# When select imported folder, all subs are selected
def get_subfolder_from_folder(folderid):
    folder_list = [folderid, ]
    subfolder_list = get_from_db("select Id from AssetFolder where ParentFolderId=%s" % folderid)
    while True:
        middle = []
        if subfolder_list:
            for i in subfolder_list:
                folder_list.append(i[0])
                middle = middle + get_from_db("select Id from AssetFolder where ParentFolderId=%s" % i[0])
            subfolder_list = middle
            continue
        else:
            break
    return folder_list


# 根据需求的类型，从数据库里随机获取，返回路径
def db_random(s_type, n='random'):
    current_database = yml_data['database']
    mydb = sqlite3.connect(current_database)
    cursor = mydb.cursor()
    # according s_type, get all from tables:
    if s_type == 'collection':
        t_db = 'Collections'
        excute_sen = "select * from %s;" % t_db
    elif s_type == 'collection_set':
        t_db = 'CollectionSets'
        excute_sen = "select * from %s;" % t_db
    elif s_type == 'collection&set':
        c = ['Collections', 'CollectionSets']
        t_db = random.choice(c)
        excute_sen = "select * from %s;" % t_db
        # 判断选中的collection set或者collection的表是否是空的
        cursor.execute(excute_sen)
        tables = cursor.fetchall()
        log().debug(tables)
        if not tables:
            c.remove(t_db)
            t_db = c[0]
            excute_sen = "select * from %s;" % t_db
        # # 判断如果选中collection set的话，是否这个表是空的
        # if t_db == 'CollectionSets':
        #     cursor.execute(excute_sen)
        #     tables = cursor.fetchall()
        #     log().debug(tables)
        #     if not tables:
        #         t_db = 'Collections'
        #         excute_sen = "select * from %s;" % t_db
    # 文件夹的数据库表里会多写入父文件夹，所以要多加一个过滤条件
    elif s_type == 'library':
        t_db = 'AssetFolder'
        excute_sen = "select * from %s WHERE IsImported=1;" % t_db
    else:
        log().debug('UNKNOWN TYPE!!')
        return False
    cursor.execute(excute_sen)
    # 读取collection或者library两张数据库表，满足条件的所有数据，放到tables里，列表嵌套列表的形式
    tables = cursor.fetchall()
    log().debug(tables)
    # 如果数据库的collection或者dir里没有数据，返回False
    if not tables:
        log().debug('NO DATA IN THIS TABLE!!')
        return False
    # 有数据的话，取collection/collection set/folder, and its path
    else:
        # 如果传入的n是random，从数据库里随机取一个
        if n == 'random':
            random_c = random.choice(tables)
            tables.remove(random_c)
        else:
            # 如果变量传入了值，根据需要第几个item来pop
            random_c = tables.pop(int(n) - 1)
        log().debug(random_c)
        log().debug(tables)
        # 获取选中的item的id
        random_id = random_c[0]
        # 获取该item的name，并创造一个random_path的列表
        random_path = [random_c[1]]
        # folder, collection, collection set判断parent的方法都不一样，分开写
        cursor.execute("select * from JoinCollectionSetAndCollectionSet;")
        tables_join_sets = cursor.fetchall()
        log().debug(tables_join_sets)
        cursor.execute("select * from CollectionSets;")
        tables_sets = cursor.fetchall()
        log().debug(tables_sets)
        if t_db == 'Collections':
            cursor.execute("select * from JoinCollectionAndCollectionSet;")
            tables = cursor.fetchall()
            for i in tables:
                if random_id == i[0]:
                    p_id = i[1]
                    cursor.execute("select Name from CollectionSets WHERE Id=%d;" % i[1])
                    p_name = cursor.fetchall()[0][0]
                    log().debug(p_name)
                    random_path.append(p_name)
                    n = len(tables_join_sets)
                    while n > 0:
                        for j in tables_join_sets:
                            if p_id == j[0]:
                                cursor.execute("select Name from CollectionSets WHERE Id=%d;"%j[1])
                                p_name = cursor.fetchall()[0][0]
                                log().debug(p_name)
                                random_path.append(p_name)
                                p_id = j[1]
                                tables_join_sets.remove(j)
                                n = len(tables_join_sets)
                                log().debug(tables_join_sets)
                                log().debug(random_path)
                                break
                            else:
                                n = n - 1
                                continue
                    break
                else:
                    continue
        elif t_db == 'CollectionSets':
            n = len(tables_join_sets)
            p_id = random_id
            while n > 0:
                for i in tables_join_sets:
                    if p_id == i[0]:
                        cursor.execute("select Name from CollectionSets WHERE Id=%d;" % i[1])
                        p_name = cursor.fetchall()[0][0]
                        log().debug(p_name)
                        random_path.append(p_name)
                        p_id = i[1]
                        tables_join_sets.remove(i)
                        n = len(tables_join_sets)
                        log().debug(tables_join_sets)
                        log().debug(random_path)
                        break
                    else:
                        n = n - 1
                        continue
        elif t_db == 'AssetFolder':
            p_id = random_c[2]
            n = len(tables)
            while n > 0:
                for i in tables:
                    if p_id == i[0]:
                        random_path.append(i[1])
                        p_id = i[2]
                        tables.remove(i)
                        n = len(tables)
                        log().debug(tables)
                        log().debug(random_path)
                        break
                    else:
                        n = n - 1
                        continue
        log().debug(random_path)
        # 循环完所有的parent，把random_path整个列表翻转一下
        random_path.reverse()
        # 在random_path列表里加上选中的item的t_db，也就是在数据库里对应的表
        random_path.append(t_db)
        # 在random_path列表里加上选中的item的id
        random_path.append(random_id)
        log().debug(random_path)
        return random_path


# move collection set
# set_id is id of moved collection set
# old database
# def db_selected_set_when_move_collection_set(set_id):
#     current_database = read_yml('database')
#     mydb = sqlite3.connect(current_database)
#     cursor = mydb.cursor()
#     excute_sen = "select id, pid from collection where isset=1;"
#     cursor.execute(excute_sen)
#     # 读取collection或者dir两张数据库表，满足条件的所有数据，放到tables里，列表嵌套列表的形式
#     tables = cursor.fetchall()
#     for i in tables:
#         if i[0] == set_id:
#             tables.remove(i)
#     tables_bak = tables[:]
#     log().debug(tables)
#     for i in tables:
#         if i[1] == set_id:
#             set_id = i[0]
#             tables_bak.remove(i)
#     selected_set_id = tables_bak[0][0]
#     return selected_set_id

# move collection set
# set_id is id of moved collection set
def db_selected_set_when_move_collection_set(set_id):
    # get all collection sets
    all_sets = get_from_db("select Id, Name from CollectionSets")
    # remove selected collection set from all_sets which will be moved
    for i in all_sets:
        if i[0] == set_id:
            all_sets.remove(i)
    # all_sets.remove((set_id,))
    # Remove all child sets of selected collection set
    child_set_table = get_from_db(
        "select ChildCollectionSetId from JoinCollectionSetAndCollectionSet where ParentCollectionSetId=%s" % set_id)
    while True:
        child_child_set_table = []
        for i in child_set_table:
            table = get_from_db(
                "select ChildCollectionSetId from JoinCollectionSetAndCollectionSet where ParentCollectionSetId=%s" % i[0])
            for j in all_sets:
                if j[0] == i[0]:
                    all_sets.remove(j)
            child_child_set_table = child_child_set_table + table
        if not child_child_set_table:
            break
        else:
            child_set_table = child_child_set_table
            continue
    # In case move collection set, only move down one time, so select the first set after "All"
    set_table = sorted(all_sets, key=itemgetter(1), reverse=True)
    return set_table


# According FUNC: db_selected_collection, check if there is collection set, if there are more than 2 collection
def db_check_collection():
    table = get_from_db("select Id, Name from CollectionSets")
    set_table = sorted(table, key=itemgetter(1), reverse=True)
    if not set_table:
        collection_table = get_from_db("select Id from Collections")
    else:
        set_id = set_table[0][0]
        collection_table = get_from_db(
            "select CollectionId from JoinCollectionAndCollectionSet where CollectionSetId=%s" % set_id)
    if len(collection_table) <= 1:
        return False
    elif len(collection_table) >= 2:
        return True


# add to collection/move to collection
def db_selected_collection(checked):
    # 点击collection set，默认选择All，down一次，选择第一个collection set
    # 点击collection，默认选中第一个collection，down一次，选择第二个collection
    # 根据新的数据库，返回id
    table = get_from_db("select Id, Name from CollectionSets")
    set_table = sorted(table, key=itemgetter(1), reverse=True)
    if not set_table:
        table = get_from_db("select Id, Name from Collections")
        collection_table = sorted(table, key=itemgetter(1), reverse=True)
    else:
        set_id = set_table[0][0]
        table = get_from_db(
            "select CollectionId from JoinCollectionAndCollectionSet where CollectionSetId=%s" % set_id)
        collection_table = sorted(table)
    log().debug(collection_table)
    log().debug(checked)
    if checked:
        selected_collection_id = collection_table[1][0]
    else:
        selected_collection_id = collection_table[-1][0]
    return selected_collection_id


# # move to folder
# def db_selected_folder():
#     # 默认选择第一个folder
#     p_table = get_from_db("select ParentFolderId from AssetFolder where IsImported=1")
#     p = sorted(list(set(p_table)))[0][0]
#     table = get_from_db("select Id, Name from AssetFolder where IsImported=1 and ParentFolderId=%s" % p)
#     folderId = sorted(table, key=itemgetter(1), reverse=True)[0][0]
#     return folderId

# move to folder
def db_selected_folder():
    # 默认选择第一个folder
    f_table = get_from_db("select Id, Name, ParentFolderId from AssetFolder where IsImported=1")
    log().debug(f_table)
    f_table_bak = f_table.copy()
    for i in f_table:
        if i[2] == 0:
            continue
        p = get_from_db("select ParentFolderId from AssetFolder where Id=%s" % i[0])
        p_is_imported = get_from_db("select IsImported from AssetFolder where Id=%s" % p[0])
        # log().debug(p)
        # log().debug(p_is_imported)
        if p_is_imported[0][0] == 1:
            f_table_bak.remove(i)
            # log().debug(f_table_bak)
    # log().debug(f_table_bak)
    folderId = sorted(f_table_bak, key=itemgetter(1), reverse=False)[0][0]
    return folderId


def create_screenshot_path(current_def):
    version = yml_data['build'].__str__().split('[')[1].split(']')[0]
    dir_path = yml_data['screenshot_path'] + '\\Screenshot_' + version
    os.makedirs(dir_path, exist_ok=True)
    # hwnd = win32gui.FindWindow(None, 'VEGAS Prepare')
    # app = QApplication(sys.argv)
    # screen = QApplication.primaryScreen()
    # img = screen.grabWindow(hwnd).toImage()
    file_name = '%s' % current_def + time.strftime('_%Y%m%d_%H%M%S', time.localtime(time.time())) + '.jpg'
    imgPath = dir_path + '\\' + file_name
    return imgPath


# def get_screenshot(current_def):
#     version = read_yml('build').__str__().split('[')[1].split(']')[0]
#     dir_path = read_yml('screenshot_path') + '\\Screenshot_' + version
#     os.makedirs(dir_path, exist_ok=True)
#     hwnd = win32gui.FindWindow(None, 'VEGAS Prepare')
#     app = QApplication(sys.argv)
#     screen = QApplication.primaryScreen()
#     img = screen.grabWindow(hwnd).toImage()
#     file_name = '%s' % current_def + time.strftime('_%Y%m%d_%H%M%S', time.localtime(time.time())) + '.jpg'
#     imgPath = dir_path + '\\' + file_name
#     img.save(imgPath)
#     return imgPath


# get target collection id from config.ini, returned id is str
def get_target_id():
    config_file = open(yml_data['configure_ini'][0])
    try:
        config_list = config_file.read().splitlines()
    finally:
        config_file.close()
    t = ''
    for t in config_list:
        if 'targetid' in t:
            break
    target_id = t.split('=')[1]
    log().debug('target id: %s' % target_id)
    try:
        float(target_id)
        if target_id == '0':
            return False
        else:
            return target_id
    except ValueError:
        return False

