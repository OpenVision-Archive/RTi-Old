#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from enigma import ePicLoad, eTimer, getDesktop
from Screens.Screen import Screen
from Tools.Directories import resolveFilename, pathExists, fileExists, SCOPE_MEDIA
from Plugins.Plugin import PluginDescriptor
from Components.Pixmap import Pixmap, MovingPixmap
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Sources.StaticText import StaticText
from Components.FileList import FileList
from Components.AVSwitch import AVSwitch
from Components.Sources.List import List
from Components.ConfigList import ConfigList, ConfigListScreen
from Components.config import config, ConfigSubsection, ConfigInteger, ConfigSelection, ConfigText, ConfigEnableDisable, KEY_LEFT, KEY_RIGHT, KEY_0, getConfigListEntry
from Components.Label import Label
import os
import sys
from Components.MenuList import MenuList
from Components.Sources.List import List
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Tools import Notifications
from ServiceReference import ServiceReference
from Components.Button import Button
from Tools.LoadPixmap import LoadPixmap
import urllib
from Components.config import config, ConfigSubsection, ConfigInteger, ConfigSelection, ConfigText, ConfigEnableDisable, KEY_LEFT, KEY_RIGHT, KEY_0, getConfigListEntry
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Tools.HardwareInfo import HardwareInfo
import shutil

def getScale():
    return AVSwitch().getFramebufferScale()

config.pic = ConfigSubsection()
config.pic.framesize = ConfigInteger(default = 30, limits = (5, 99))
config.pic.slidetime = ConfigInteger(default = 10, limits = (10, 60))
config.pic.resize = ConfigSelection(default = '1', choices = [
    ('0', _('simple')),
    ('1', _('better'))])
config.pic.cache = ConfigEnableDisable(default = True)
config.pic.lastDir = ConfigText(default = resolveFilename(SCOPE_MEDIA))
config.pic.infoline = ConfigEnableDisable(default = True)
config.pic.loop = ConfigEnableDisable(default = True)
config.pic.bgcolor = ConfigSelection(default = '#00000000', choices = [
    ('#00000000', _('black')),
    ('#009eb9ff', _('blue')),
    ('#00ff5a51', _('red')),
    ('#00ffe875', _('yellow')),
    ('#0038FF48', _('green'))])
config.pic.textcolor = ConfigSelection(default = '#0038FF48', choices = [
    ('#00000000', _('black')),
    ('#009eb9ff', _('blue')),
    ('#00ff5a51', _('red')),
    ('#00ffe875', _('yellow')),
    ('#0038FF48', _('green'))])

class subconv(Screen):
    skin = '\n\t\t<screen name="RTiSubtitleConverter007" position="center,center" size="560,290" title="RTi SubtitleConverter   v.1.0" >\n\t\t\t<ePixmap name="red"    position="0,250"   zPosition="2" size="140,40" pixmap="buttons/red.png" transparent="1" alphatest="on" />\n\t\t\t<ePixmap name="blue"   position="420,250" zPosition="2" size="140,40" pixmap="buttons/blue.png" transparent="1" alphatest="on" /> \n\t\t\t<widget name="key_red" position="0,250" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> \n\t\t\t<widget name="key_blue" position="420,250" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" />\n\t\t\t<widget name="thn" position="420,250" size="180,160" alphatest="on" />\n\t\t\t<widget name="filelist" position="5,55" zPosition="2" size="550,187" scrollbarMode="showOnDemand" />\n\t\t\t<widget name="info0" position="5,20" zPosition="2" size="550,20" font="Regular;18" foregroundColor="#aaaaaa" transparent="1" halign="center" valign="center" />\n\t\t\t<widget name="infoL" position="140,265" zPosition="2" size="280,20" font="Regular;22" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />\n\t\t</screen>'
    
    def __init__(self, session):
        Screen.__init__(self, session)
        self['actions'] = ActionMap([
            'OkCancelActions',
            'ColorActions',
            'DirectionActions'], {
            'cancel': self.KeyExit,
            'red': self.KeyOk,
            'blue': self.KeyExit,
            'ok': self.KeyOk }, -1)
        self['key_blue'] = Button(_('Exit'))
        self['key_red'] = Button(_('Select'))
        self['thn'] = Pixmap()
        self['info0'] = Label()
        self['infoL'] = Label()
        currDir = config.pic.lastDir.value
        if not pathExists(currDir):
            currDir = '/'
        
        self.filelist = FileList(currDir, matchingPattern = '(?i)^.*\\.(srt|sub|txt)')
        self['filelist'] = self.filelist
        self['info0'].setText('Select Subtitle for conversion :')
        self['infoL'].setText('www.azbox-enigma.eu')

    
    def KeyGreen(self):
        print('ok')

    
    def KeyYellow(self):
        if not self.filelist.canDescent():
            print('ok')
        

    
    def KeyBlue(self):
        print('ok')

    
    def KeyOk(self):
        if self.filelist.canDescent():
            self.filelist.descent()
        else:
            pateka = '/'
            ime = self.filelist.getFileList()
            if self.filelist.getCurrentDirectory() and self.filelist.getFilename():
                ime = self.filelist.getFileList()
                ind = self.filelist.getSelectionIndex()
                pateka = self.filelist.getCurrentDirectory() + ime[ind][0][0]
            
            self.session.open(SubPreview, str(pateka))

    
    def callbackView(self, val = 0):
        if val > 0:
            self.filelist.moveToIndex(val)
        

    
    def KeyExit(self):
        print('exit')
        if self.filelist.getCurrentDirectory() is None:
            config.pic.lastDir.value = '/'
        else:
            config.pic.lastDir.value = self.filelist.getCurrentDirectory()
        config.pic.save()
        self.close()



class SubPreview(Screen):
    skin = '\n\t\t<screen name="Menusimple2" position="center,center" size="720,530" title="RTi SubtitleConverter   v.1.0" >\n\t\t\t<ePixmap name="red"    position="40,490"   zPosition="2" size="180,40" pixmap="buttons/red.png" transparent="1" alphatest="on" />\n\t\t\t<ePixmap name="blue"   position="540,490" zPosition="2" size="180,40" pixmap="buttons/blue.png" transparent="1" alphatest="on" /> \n\t\t\t<widget name="key_red" position="20,490" size="180,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> \n\t\t\t<widget name="key_blue" position="520,490" size="180,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" />\n\t\t\t<!--widget name="text" position="0,0" size="550,25" font="Regular;20" /-->\n\t\t\t<!--widget name="pixmap" position="200,0" size="190,250" /-->\n\t\t\t<eLabel position="70,100" zPosition="-1" size="100,69" backgroundColor="#222222" />\n\t\t\t<widget name="list" position="30,70" size="200,405" scrollbarMode="showOnDemand" foregroundColor="#aaaaaa" />\n\t\t\t<widget name="info0" position="260,75" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info1" position="260,95" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info2" position="260,115" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info3" position="260,135" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info4" position="260,155" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info5" position="260,175" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info6" position="260,195" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info7" position="260,215" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info8" position="260,235" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info9" position="260,255" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info10" position="260,275" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info11" position="260,295" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info12" position="260,315" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info13" position="260,335" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info14" position="260,355" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info15" position="260,375" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info16" position="260,395" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info17" position="260,415" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info18" position="260,435" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info19" position="260,455" zPosition="2" size="530,18" font="Regular;16" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t\t\t<widget name="info20" position="30,15" zPosition="2" size="660,18" font="Regular;20" foregroundColor="#aaaaaa" transparent="1" halign="center" valign="center" />\n\t\t\t<widget name="infoA" position="30,50" zPosition="2" size="200,18" font="Regular;20" foregroundColor="#aaaaaa" transparent="1" halign="center" valign="center" />\n\t\t\t<widget name="infoB" position="260,50" zPosition="2" size="430,18" font="Regular;20" foregroundColor="#aaaaaa" transparent="1" halign="center" valign="center" />\n\t\t\t<widget name="infoL" position="180,505" zPosition="2" size="360,20" font="Regular;22" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />\n\t\t</screen>'
    
    def __init__(self, session, pateka):
        self.skinName = 'OnlineManager2'
        Screen.__init__(self, session)
        self['actions'] = ActionMap([
            'OkCancelActions',
            'ColorActions',
            'DirectionActions'], {
            'ok': self.okClicked,
            'cancel': self.Izlaz,
            'red': self.okClicked,
            'blue': self.Izlaz,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.keyLeft,
            'right': self.keyRight }, -1)
        self['key_blue'] = Button(_('Exit'))
        self['key_red'] = Button(_('Convert'))
        self.icount = 0
        self.pateka = pateka
        self.encodings = []
        self.encname = []
        self['list'] = MenuList(self.encodings)
        self['info0'] = Label()
        self['info1'] = Label()
        self['info2'] = Label()
        self['info3'] = Label()
        self['info4'] = Label()
        self['info5'] = Label()
        self['info6'] = Label()
        self['info7'] = Label()
        self['info8'] = Label()
        self['info9'] = Label()
        self['info10'] = Label()
        self['info11'] = Label()
        self['info12'] = Label()
        self['info13'] = Label()
        self['info14'] = Label()
        self['info15'] = Label()
        self['info16'] = Label()
        self['info17'] = Label()
        self['info18'] = Label()
        self['info19'] = Label()
        self['info20'] = Label()
        self['infoA'] = Label()
        self['infoB'] = Label()
        self['infoL'] = Label()
        self.onLayoutFinish.append(self.openTest)

    
    def openTest(self):
        self['infoA'].setText('Encoder :  ')
        self['infoB'].setText('Preview :  ')
        self['info20'].setText('Select right encoding and press OK')
        self['infoL'].setText('www.azbox-enigma.eu')
        dat = '/usr/lib/enigma2/python/Plugins/Extensions/RTiSubtitleConverter/encode.lst'
        
        try:
            sfile = open(dat, 'r')
            for line in sfile:
                ipos = line.find('>>')
                remname = line[:ipos]
                enc = line[ipos + 2:len(line) - 1]
                if ipos < 0:
                    remname = line
                    enc = line
                
                self.encname.append(remname)
                self.encodings.append(enc)
            self['list'].setList(self.encname)
        except Exception:
            self.encodings = [
                'windows-1250',
                'windows-1251',
                'windows-1253',
                'iso-8859-7',
                'macgreek']
            self['list'].setList(self.encodings)
            return None

        sfile.close()
        self.vfdprint()

    
    def keyUp(self):
        self['list'].up()
        self.vfdprint()

    
    def keyDown(self):
        self['list'].down()
        self.vfdprint()

    
    def keyLeft(self):
        self['list'].pageUp()
        self.vfdprint()

    
    def keyRight(self):
        self['list'].pageDown()
        self.vfdprint()

    
    def Izlaz(self):
        self.close()

    
    def KeyGreen(self):
        self['text'].right()

    
    def KeyRed(self):
        self['text'].right()

    
    def KeyYellow(self):
        self['text'].right()

    
    def okClicked(self):
        sel = self['list'].getSelectionIndex()
        enc = self.encodings[sel]
        filename = self.pateka
        
        try:
            f = open(filename, 'r').read()
        except Exception:
            return None

        
        try:
            data = f.decode(enc)
        except Exception:
            print('nok')

        fpath = os.path.abspath(filename)
        newfilename = fpath + '.bak'
        
        try:
            shutil.copy(filename, newfilename)
        except Exception:
            e = None
            print(e)

        filenameC = '/tmp/Converted.srt'
        f = open(filenameC, 'w')
        
        try:
            f.write(data.encode('utf-8'))
        except Exception:
            e = None
            print(e)
        finally:
            f.close()

        f1 = open(filename, 'w')
        
        try:
            f1.write(data.encode('utf-8'))
        except Exception:
            e = None
            print(e)
        finally:
            f1.close()

        self.session.openWithCallback(self.callback, MessageBox, _('Subtitle : ' + str(filename) + '\nEncoded using: ' + str(enc) + ' successfully !'), type = 1, timeout = 20)
        self.close()

    
    def vfdprint(self):
        sel = self['list'].getSelectionIndex()
        enc = self.encodings[sel]
        filename = self.pateka
        self['info0'].setText(' ')
        self['info1'].setText(' ')
        self['info2'].setText(' ')
        self['info3'].setText(' ')
        self['info4'].setText(' ')
        self['info5'].setText(' ')
        self['info6'].setText(' ')
        self['info7'].setText(' ')
        self['info8'].setText(' ')
        self['info9'].setText(' ')
        self['info10'].setText(' ')
        self['info11'].setText(' ')
        self['info12'].setText(' ')
        self['info13'].setText(' ')
        self['info14'].setText(' ')
        self['info15'].setText(' ')
        self['info16'].setText(' ')
        self['info17'].setText(' ')
        self['info18'].setText(' ')
        self['info19'].setText(' ')
        
        try:
            f = open(filename, 'r')
            lines = f.readlines()
            self['info0'].setText(lines[0].decode(enc).encode('UTF-8'))
            self['info1'].setText(lines[1].decode(enc).encode('UTF-8'))
            self['info2'].setText(lines[2].decode(enc).encode('UTF-8'))
            self['info3'].setText(lines[3].decode(enc).encode('UTF-8'))
            self['info4'].setText(lines[4].decode(enc).encode('UTF-8'))
            self['info5'].setText(lines[5].decode(enc).encode('UTF-8'))
            self['info6'].setText(lines[6].decode(enc).encode('UTF-8'))
            self['info7'].setText(lines[7].decode(enc).encode('UTF-8'))
            self['info8'].setText(lines[8].decode(enc).encode('UTF-8'))
            self['info9'].setText(lines[9].decode(enc).encode('UTF-8'))
            self['info10'].setText(lines[10].decode(enc).encode('UTF-8'))
            self['info11'].setText(lines[11].decode(enc).encode('UTF-8'))
            self['info12'].setText(lines[12].decode(enc).encode('UTF-8'))
            self['info13'].setText(lines[13].decode(enc).encode('UTF-8'))
            self['info14'].setText(lines[14].decode(enc).encode('UTF-8'))
            self['info15'].setText(lines[15].decode(enc).encode('UTF-8'))
            self['info16'].setText(lines[16].decode(enc).encode('UTF-8'))
            self['info17'].setText(lines[17].decode(enc).encode('UTF-8'))
            self['info18'].setText(lines[18].decode(enc).encode('UTF-8'))
            self['info19'].setText(lines[19].decode(enc).encode('UTF-8'))
            f.close()
        except Exception:
            return None


    
    def keyNumberGlobal(self, number):
        print('pressed', number)
        self['text'].number(number)

    
    def confirmR(self, confirmed):
        if confirmed:
            cmd = 'reboot -f'
            os.system(cmd)
            self.close()
        



def main(session, **kwargs):
    session.open(subconv)


def Plugins(**kwargs):
    boxime = HardwareInfo().get_device_name()
    if boxime == 'elite' and boxime == 'premium' and boxime == 'premium+' and boxime == 'ultra' and boxime == 'me' and boxime == 'minime' or boxime == 'multimedia':
        return [
            PluginDescriptor(name = _('RTi SubtitleConverter'), description = _('fileformats (srt, sub, txt)'), icon = 'RTiSubtitleConverter.png', where = [
                PluginDescriptor.WHERE_EXTENSIONSMENU,
                PluginDescriptor.WHERE_PLUGINMENU], fnc = main)]
    return []

