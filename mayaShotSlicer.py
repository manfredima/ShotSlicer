#coding: utf-8

from pymel.core import *
from collections import OrderedDict
import os
import sys
from pprint import pprint

# вводные
full_path = ''
origFile = ''  # source
# onlyPath = os.path.split(full_path)[0]
# onlyPath = '/home/users/d.liubimov/Documents/TEMP FILES'
onlyPath = 'H:\Autodesk\CGF\TEST_SCENE'



maxtime = 0.0
mode_name = ''
name_dict = dict()
order_dict = dict()
shots = []  # лог
shots_mute = set()
shot_list = []  # список имен шотов
shot_selected = set()
mode=''
shot_list_dict = OrderedDict()
byorder = OrderedDict()
nonRefList = []

acurves = dict()  # name:[type, point numbers, time range]
one_point_acurves = dict()
lonely = []  # одинокие кривые
shot_acurve = dict()  # shotName:[members]

def_cams = ['front', 'left', 'persp', 'side', 'top']
refs = listReferences()


def getInfo():
    print('get info')
    print('get info')
    print '\n === SHOT SLICER: FINAL report === \n'

    print 'Reference Files:'
    pprint(refs, indent=4)

    if shots_mute:
        print 'Shots Muted:', shots_mute
    else:
        print 'Shots Muted: NO'

    print 'AnimCurve Outputs:', len(acurves)
    print 'Lonely AnimCurves:', len(lonely)
    print 'OnePoint AnimCurves:', len(one_point_acurves), '\n'


# saving cleaned source file
def saveCleanUpSourceFile():
    # print 'SS: saveCleanedSourceFile'
    global full_path

    clean_file = 'cleanUp_' + origFile
    clean_path = os.path.normpath(os.path.join(onlyPath, clean_file))

    if not os.path.exists(clean_path):
        print 'SAVE:', clean_path
        saveAs(clean_path, force=True)  # сохранение нового файла (и открытие)

    full_path = clean_path


# Removing unused animation curves
def clearLonelyAcurves():
    # print 'SS: clearLonelyAcurve'
    global lonely

    cutKey(lonely, clear=True)
    # lonely = []


# make animcurve dict
def getAnimCurveDict():
    # print 'SS: getAnimCurveDict'
    global acurves, lonely, maxtime, one_point_acurves

    lonely = []
    acurves.clear()
    acurs = [x for x in ls(type='animCurve') if not x.isReferenced()]  # без референсных

    # временной диапазон всех шотов
    ks = shot_list_dict.keys()
    alltime_range = [shot_list_dict[ks[0]][0], shot_list_dict[ks[-1]][1]]

    for acur in acurs:
        # если не одинока
        if acur.outputs():
            nums = acur.numKeys()

            if nums > 1:
                timerange = [int(acur.getTime(0)),
                             int(acur.getTime(nums-1))]

                acurves[acur] = [str(acur.animCurveType()), nums, timerange]

            else:
                # для статистики
                point_time = int(acur.getTime(0))
                one_point_acurves[acur] = [str(acur.animCurveType()), point_time]

                # растяжка кривой на диапазон всех шотов
                attr = acur.outputs(p=True)[0]
                attr.setKey(time=alltime_range[0], insert=True)
                attr.setKey(time=alltime_range[1], insert=True)

                pn = acur.numKeys()
                timerange = [acur.getTime(0), acur.getTime(pn-1)]

                # if point_time < alltime_range[0] or point_time > alltime_range[1]:
                #     print '\nPOINT TIME OUT:', point_time, '\nPN:', pn, '\nTIME RANGE:', timerange, '\n'

                acurves[acur] = [str(acur.animCurveType()), pn, timerange]

        else:
            lonely.append(acur)

    if not maxtime:
        last_points = set()
        for a in acurves:
            lp = acurves[a][2][1]
            last_points.add(lp)

        maxtime = max(last_points)
        print 'MAXTIME:', maxtime

    if len(lonely):
        print 'LONELY:', len(lonely), '\n'
        clearLonelyAcurves()  # удаление одиноких кривых

    #pprint(acurves, indent=4)
    #pprint(one_point_acurves, indent=4)


# deleting all shots except current
def removeOtherShots(sn):
    # print 'SS: removeOtherShots'
    global shots

    sht = PyNode(sn)
    shots = sequenceManager(listShots=True)  # лог
    shots.remove(sht)  # удаление текущего шота из лога

    # удаление всех шотов из файла шота по списку лога
    if len(shots):
        for nts in reversed(shots):
            # print 'DELETE SHOT', nts
            delete(nts)

#  editing shot's animcurves
def editPointsOnAnimCurve(sn):
    # print 'SS: editPointsOnAnimCurve'

    sht = PyNode(sn)
    start = shot(sht, q=True, startTime=True)
    end = shot(sht, q=True, endTime=True)

    # print '\nSHOT:', sn, '| ', start , end, '\n'

    outs = []
    ints = []

    # проход по списку кривых шота
    for ac in acurves:
        nums = ac.numKeys()
        t1 = ac.getTime(0)
        t2 = ac.getTime(nums-1)

        if t1 == start and t2 == end:
            continue

        if (t1 < start and t2 < start) or (t1 > end and t2 > end):
            outs.append(ac)

        if (start <= t1 <= end) or \
           (start <= t2 <= end) or \
           (t1 < start and t2 > end):
            ints.append(ac)

    # print 'OUTS:', len(outs)
    # print 'INTS:', len(ints), '\n'

    # удаление внешних кривых
    for ac in outs:
        nums = ac.numKeys()
        t1 = ac.getTime(0)
        t2 = ac.getTime(nums-1)

        cutKey(ac, time=(t1, t2), clear=True)

    # добавление и удаление ключей на кривых, включенных в шот
    for ac in ints:
        pn = ac.numKeys()

        # if str(ac) == 'house_v01_barrier5_MaxHandle':
        #     print 'AC:', pn, '|', type(ac), '|', ac

        attr = ac.outputs(p=True)[0]  # атрибут для ключа
        points = [float(ac.getTime(n)) for n in range(pn)]  # ключи кривой

        if start not in points:
            attr.setKey(time=start, insert=True) # добавление ключей

        if end not in points:
            attr.setKey(time=end, insert=True)

        # удаление лишних
        if points[0] < start:
            cutKey(ac, time=(points[0], start - 1), clear=True)

        if points[pn - 1] > end:
            cutKey(ac, time=(end + 1, points[pn - 1]), clear=True)


# set shot's camera to Playblast panel
def setCameraOnPanel(sn):
    #print 'SS: setCameraOnPanel'

    # имя панели плейбласта
    vp = playblast(activeEditor=True)
    name = vp.split('|')[-1]

    sht = PyNode(sn)
    cam = shot(sht, q=True, currentCamera=True)
    windows.modelPanel(name, camera=cam, e=True)


def outVideo(sn):
    #print 'SS: outVideo'
    #setCameraOnPanel(sn)  # установка камеры

    movie_path = os.path.normpath(os.path.join(onlyPath, sn + '.qt'))
    start = shot_list_dict[sn][0]
    end   = shot_list_dict[sn][1]

    playblast(format='qt',
              viewer=0,
              showOrnaments=0,
              percent=50,
              compression="H.264",
              quality=100,
              f=movie_path,
              height=720,
              width=1280,
              forceOverwrite=1,
              startTime=start,
              endTime=end)

def removeOtherCams(sn):
    #print 'SS: removeOtherCams'

    #scene_cams = set()
    all_cams = listCameras()
    sht_cam = shot_list_dict[sn][2]
    scene_cams = set(def_cams)
    scene_cams.add(sht_cam)

    #print 'SHOT:', sn
    #print 'SHT CAM:', sht_cam
    #print 'SCENE CAMS:', scene_cams

    # cam_namespace = PyNode(sht_cam).namespace()  # namespace камеры сцены
    refs_namespace = []  # namespace всех референсов
    for r in refs:
        refs_namespace.append(r.namespace)

    #print 'REF NAMESPACE:', refs_namespace

    # обход всех камер и удаление лишних
    for cam in all_cams:
        if cam not in scene_cams:
            cam_namespace = PyNode(cam).namespace()
            #print 'CAM NAMESPACE:', cam_namespace  # namespace камеры

            if cam_namespace.endswith(':'):
                cam_namespace = cam_namespace[:-1]
                # если в списке референсов - выгружаем
                if cam_namespace in refs_namespace:
                    rfile = FileReference(namespace=cam_namespace)
                    rfile.unload()
                else:
                    #print 'DELETE 1:', cam
                    delete(PyNode(cam))
            else:
                #print 'DELETE 2:', cam
                delete(PyNode(cam))

    # scene_cams.clear()
    setCameraOnPanel(sn)  # установка камеры


# передвижение в начало timeline аним.кривых
def moveAnimToStart(sn):
    print 'SS: moveAnimToStart'
    #animDisplay(refAnimCurvesEditable=True)

    start = int(shot_list_dict[sn][0])
    end   = int(shot_list_dict[sn][1])
    new_end = end - start + 1

    print '\nSHOT:', sn, '| ', start, end

    if start != 1.0:
        acurs = [x for x in ls(type='animCurve')]
        print 'ACURS:', len(acurs)

        shot_acurs = []

        for ac in acurs:
            pn = ac.numKeys()
            t1 = ac.getTime(0)
            t2 = ac.getTime(pn-1)
            # print 'AC:', t1, t2

            if t1 == start and t2 == end:
                shot_acurs.append(ac)

        print 'NEW END:', new_end
        print 'SHOT ACURS:', len(shot_acurs), '\n'
        scaleKey(shot_acurs, time=(start, end), newStartTime=1, newEndTime=new_end)

    # удаление последнего шота
    if len(sequenceManager(listShots=True)):
        sht = PyNode(sn)
        # print 'DELETE SHOT CAMERA:', sht
        delete(sht)


# генерация номера очередности
def genPrefName(sn):
    print 'SS: genPrefName'
    global name_dict, order_dict
    # print 'MODE:', mode_name

    if shot_list:
        pre = ''
        if mode_name == 'by Sequenser Order':
            if not order_dict.keys():
                for i, s in enumerate(shot_list):
                    order_dict[s] = i + 1

            pre = "%03d" % (order_dict[sn]) + '_'

        if mode_name == 'by Name':
            if not name_dict.keys():
                sort_list = sorted(shot_list)
                print 'SORT LIST:', sort_list

                for y, s in enumerate(sort_list):
                    name_dict[s] = y + 1

            pre = "%03d" % (name_dict[sn]) + '_'

        print '\nPRE:', pre, '\n'
        return pre

    else:
        print '\n!!! shot_list is empty\n'


# сохранение файла текущего шота
def saveShotFile(sn):
    #print 'SS: saveShotFile'

    pre = genPrefName(sn)
    print 'GEN PRE:', pre + sn

    shot_path = os.path.normpath(os.path.join(onlyPath, pre + sn + '.mb'))
    saveAs(shot_path)  # сохранение нового файла шота (и его открытие)

    # обработка в файле шота
    removeOtherShots(sn)
    editPointsOnAnimCurve(sn)
    removeOtherCams(sn)
    moveAnimToStart(sn)
    saveFile()
    print 'SAVE SH:', shot_path
    # outVideo(sn)


# pass shots list, make shot dict
# открытие файла исходника
def beOnBeat(sn):
    # print 'SHOT SLICER: beOnBeat'
    global shot_acurve

    print '\n ==== STEP:', sn, '| SCENE NAME:', sceneName(), '==== \n'
    #print 'FP:', full_path

    if sceneName() != full_path:
        print 'OPEN FILE:', full_path, '\n'
        openFile(full_path)
        getAnimCurveDict()

    sht = PyNode(sn)
    start = shot_list_dict[sn][0]
    end   = shot_list_dict[sn][1]
    members = []

    for a in acurves:
        first = acurves[a][2][0]  # первая точка кривой
        last  = acurves[a][2][1]  # последняя точка кривой
        if first <= end and last >= start:
            members.append(a)

    # pprint(members, indent=4)
    shot_acurve[sht] = members  # {shot:members}
    # pprint(shot_acurve, indent=4)

    saveShotFile(sn)  # сохранение и обработка


# make shots dict
def getShots():
    global shots_mute, shot_list, shot_list_dict

    if sequenceManager(listShots=True):
        byName = sequenceManager(listShots=True)
        times = dict()

        for sht in byName:
            start = shot(sht, q=True, sequenceStartTime=True)
            times[start] = sht.getName()

        if not shot_list:
            for k in sorted(times.keys()):
                shot_list.append(times[k])

        #print 'SHOT LIST:', shot_list

        for sn in shot_list:
            sht = PyNode(sn)
            start = shot(sht, q=True, startTime=True)
            end = shot(sht, q=True, endTime=True)
            cam = shot(sht, q=True, currentCamera=True)

            shot_list_dict[sn] = [start, end, cam]

            muted = shot(sht, q=True, mute=True)
            if muted:
                shots_mute.add(sn)

        #print 'MUTED:', shots_mute
    else:
        system.displayWarning('= Shots not found =')

    return shot_list, shots_mute


# start
def launch(shot_selected, mode):
    global shot_list, full_path, origFile, mode_name

    print '\nSHOT SELECTED:', shot_selected

    mode_name = mode
    full_path = sceneName()
    origFile = os.path.basename(full_path)

    shot_list = list(shot_selected)

    # словарь шотов
    if not shot_list:
        getShots()

    # список кривых
    getAnimCurveDict()
    saveCleanUpSourceFile()

    # обход по списку шотов
    for sn in reversed(shot_list):
        beOnBeat(sn)
        # print 'BREAK...'
        # break

    getInfo()

launch(shot_selected, mode)