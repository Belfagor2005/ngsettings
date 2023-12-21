#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from Components.ActionMap import ActionMap
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryPixmapAlphaTest
from Components.MultiContent import MultiContentEntryText
from Components.Pixmap import Pixmap
from Screens.Screen import Screen
from enigma import RT_HALIGN_CENTER, RT_VALIGN_CENTER
from enigma import RT_HALIGN_LEFT
from enigma import eListboxPythonMultiContent
from enigma import gFont
from enigma import getDesktop
from enigma import loadPNG
import codecs
import glob
import os
from .Config import ConverDate, Load
from .Language import _
plugin_path = '/usr/lib/enigma2/python/Plugins/Extensions/NGsetting'
SSelect = plugin_path + '/Moduli/NGsetting/Select'
HD = getDesktop(0).size()
skin_path = os.path.join(plugin_path, "Skin/hd/")
if HD.width() == 1920:
    skin_path = plugin_path + '/Skin/fhd/'
if HD.width() == 2560:
    skin_path = plugin_path + '/Skin/uhd/'


class MenuListSelect(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)

        if HD.width() == 2560:
            self.l.setFont(0, gFont('Regular', 48))
            self.l.setItemHeight(56)
        elif HD.width() == 1920:
            self.l.setFont(0, gFont('Regular', 34))
            self.l.setItemHeight(50)
        else:
            self.l.setFont(0, gFont('Regular', 25))
            self.l.setItemHeight(45)


class ListSelect:
    def __init__(self):
        pass

    def readSaveList(self):
        try:
            jw = open(SSelect)
            jjw = jw.readlines()
            jw.close()
            list = []
            for x in jjw:
                try:
                    jx = x.split('---')
                    list.append((jx[0], jx[1].strip()))
                except:
                    pass
            return list
        except:
            pass

    def SaveList(self, list):
        jw = open(SSelect, 'w')
        for dir, name, value in list:
            if value == '1':
                jw.write(dir + '---' + name + '\n')
        jw.close()


    def readBouquetsList(self, pwd, bouquetname):
        try:
            f = open(pwd + '/' + bouquetname)
        except Exception as e:
            print(e)
            return
        ret = []
        while True:
            line = f.readline()
            if line == "":
                break
            if line[:8] != "#SERVICE":
                continue
            tmp = line.strip().split(":")
            line = tmp[len(tmp) - 1]
            filename = None
            if line[:12] == "FROM BOUQUET":
                tmp = line[13:].split(" ")
                # filename = tmp[0].strip("\"")
                filename = tmp[0].strip('"')
            else:
                filename = line
            if filename:
                try:
                    fb = open(pwd + "/" + filename)
                except Exception as e:
                    continue
                tmp = fb.readline().strip()
                if tmp[:6] == "#NAME ":
                    ret.append([filename, tmp[6:]])
                else:
                    ret.append([filename, filename])
                fb.close()
        return ret

    def readBouquetsTvList(self, pwd):
        return self.readBouquetsList(pwd, "bouquets.tv")

    def TvList(self):
        jload = self.readSaveList()
        self.bouquetlist = []
        for x in self.readBouquetsTvList("/etc/enigma2"):
            value = '0'
            try:
                for j, jx in jload:
                    if j == x[0] and jx.find(x[1]) != -1:
                        value = '1'
                        break
            except:
                pass
            self.bouquetlist.append((x[0], x[1], value))
        return self.bouquetlist


class MenuSelect(Screen):
    def __init__(self, session):
        self.session = session
        skin = os.path.join(skin_path, 'Main.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        Screen.__init__(self, session)
        self.ListSelect = ListSelect()
        self['autotimer'] = Label("")
        self['namesat'] = Label("")
        self['text'] = Label("")
        self['dataDow'] = Label("")
        self['Green'] = Pixmap()
        self['Blue'] = Pixmap()
        self['Yellow'] = Pixmap()
        self['Green'].hide()
        self['Yellow'].hide()
        self['Blue'].hide()
        self["Key_Lcn"] = Label('')
        self["Key_Red"] = Label(_("Exit"))
        self["Key_Green"] = Label(_("Setting Installed:"))
        self["Key_Personal"] = Label("")
        self['A'] = MenuListSelect([])
        self['B'] = MenuListSelect([])
        self["B"].selectionEnabled(1)
        self.Info()
        self.Menu()
        self.MenuA()
        self["actions"] = ActionMap(["OkCancelActions",
                                     "ShortcutActions",
                                     "WizardActions",
                                     "ColorActions",
                                     "SetupActions",
                                     "NumberActions",
                                     "MenuActions",
                                     "HelpActions",
                                     "EPGSelectActions"], {
                                                           "ok": self.OkSelect,
                                                           "up": self.keyUp,
                                                           "down": self.keyDown,
                                                           "cancel": self.Uscita,
                                                           "nextBouquet": self["B"].pageUp,
                                                           "prevBouquet": self["B"].pageDown,
                                                           "red": self.Uscita
                                                           }, -1)

    def Info(self):
        AutoTimer, NameSat, Data, Type, Personal, DowDate = Load()
        if str(Data) == '0':
            newdate = ('')
        else:
            newdate = (' - ' + ConverDate(Data))
        if str(DowDate) == '0':
            newDowDate = _('Last Update: Unregistered')
        else:
            newDowDate = _('Last Update: ') + DowDate
        self['namesat'].setText(NameSat + newdate)
        self['dataDow'].setText(newDowDate)

    def Uscita(self):
        self.close()

    def keyUp(self):
        self['B'].up()

    def keyDown(self):
        self['B'].down()

    def hauptListEntry(self, dir, name, value):
        res = [(dir, name, value)]
        icon = skin_path + 'red.png'
        if value == '1':
            icon = skin_path + 'green.png'
        try:
            name = name.split('   ')[0]
        except:
            pass
        if HD.width() == 2560:
            res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 20), size=(20, 20), png=loadPNG(icon)))
            res.append(MultiContentEntryText(pos=(50, 0), size=(1000, 40), font=0, text=name, flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER))
        elif HD.width() == 1920:
            res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 15), size=(20, 20), png=loadPNG(icon)))
            res.append(MultiContentEntryText(pos=(50, 0), size=(1000, 40), font=0, text=name, flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER))
        else:
            res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 11), size=(20, 20), png=loadPNG(icon)))
            res.append(MultiContentEntryText(pos=(50, 0), size=(500, 40), font=0, text=name, flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER))
        res.append(MultiContentEntryText(pos=(0, 0), size=(0, 0), font=0, text=dir, flags=RT_HALIGN_LEFT))
        res.append(MultiContentEntryText(pos=(0, 0), size=(0, 0), font=0, text=value, flags=RT_HALIGN_LEFT))
        return res

    def hauptListEntryA(self, name):
        res = [name]
        try:
            name = name.split('   ')[0]
        except:
            pass
        if HD.width() == 2560:  # 1770
            res.append(MultiContentEntryText(pos=(10, 0), size=(850, 56), font=0, text=name, flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER))
        elif HD.width() == 1920:
            res.append(MultiContentEntryText(pos=(10, 0), size=(500, 40), font=0, text=name, flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER))
        else:
            res.append(MultiContentEntryText(pos=(10, 0), size=(170, 40), font=0, text=name, flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER))
        return res

    def MenuA(self):
        self.jB = []
        lista = self.ListSelect.readSaveList()
        if lista:
            for dir, name in lista:
                self.jB.append(self.hauptListEntryA(name))
        self["A"].setList(self.jB)
        if not self.jB:
            self['text'].setText("      Maintenance\n          Folders\n       Customized")
        else:
            self['text'].setText(" ")
        self["B"].selectionEnabled(1)
        self["A"].selectionEnabled(0)

    def Menu(self):
        self.jA = []
        for dir, name, value in self.ListSelect.TvList():
            # if name != 'Digitale Terrestre' and name != 'Favourites (TV)' and name[2:] != 'Vhannibal Settings':
            # if name != 'Favourites (TV)' and name[2:] != 'Vhannibal Settings':
            self.jA.append(self.hauptListEntry(dir, name, value))
        self["B"].setList(self.jA)

    def OkSelect(self):
        NewName = self["B"].getCurrent()[0][1]
        NewDir = self["B"].getCurrent()[0][0]
        self.list = []
        for dir, name, value in self.ListSelect.TvList():
            if dir == NewDir and name == NewName:
                if value == '0':
                    self.list.append((dir, name, '1'))
            elif value == '1':
                self.list.append((dir, name, '1'))
        self.ListSelect.SaveList(self.list)
        self.Menu()
        self.MenuA()
