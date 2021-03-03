#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Sources.List import List
from Screens.MessageBox import MessageBox
from Plugins.Plugin import PluginDescriptor
from Components.Pixmap import Pixmap
from ServiceReference import ServiceReference
from Components.Button import Button
from Components.Label import Label
import os
from time import sleep


class CAMDManager(Screen):
    skin = '\n        \t<screen name="Menusimple" position="center,center" size="580,450" title="" >\n\n                <widget name="list" position="75,50" size="430,100" scrollbarMode="showOnDemand" />\n\t\t<!--eLabel position="70,100" zPosition="-1" size="100,69" backgroundColor="#222222" /-->\n                <widget name="info" position="110,170" zPosition="4" size="360,220" font="Regular;18" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />\n\t        <ePixmap name="red"    position="10,400"   zPosition="2" size="140,40" pixmap="buttons/red.png" transparent="1" alphatest="on" />\n\t        <ePixmap name="green"  position="150,400" zPosition="2" size="140,40" pixmap="buttons/green.png" transparent="1" alphatest="on" />\n\t        <ePixmap name="yellow" position="290,400" zPosition="2" size="140,40" pixmap="buttons/yellow.png" transparent="1" alphatest="on" /> \n        \t<ePixmap name="blue"   position="430,400" zPosition="2" size="140,40" pixmap="buttons/blue.png" transparent="1" alphatest="on" /> \n\n        \t<widget name="key_red" position="10,400" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> \n        \t<widget name="key_green" position="150,400" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> \n                <widget name="key_yellow" position="290,400" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" />\n        \t<widget name="key_blue" position="430,400" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" />\n                </screen>'

    def __init__(self, session, args=0):
        self.session = session
        Screen.__init__(self, session)
        self.skinName = 'CAMDManager'
        self.index = 0
        self.sclist = []
        self.namelist = []
        self.oldService = self.session.nav.getCurrentlyPlayingServiceReference()
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'ok': self.action,
         'cancel': self.Izlaz,
         'green': self.action,
         'red': self.stop,
         'blue': self.ecmcls,
         'yellow': self.ecm}, -1)
        self['key_green'] = Button(_('Start/Restart'))
        self['key_blue'] = Button(_('Clear'))
        self['key_red'] = Button(_('Stop'))
        self['key_yellow'] = Button(_('Ecm Info'))
        self.lastCam = self.readCurrent()
        self.camdlist = []
        self['info'] = Label()
        self['list'] = MenuList(self.camdlist)
        self.readScripts()
        title = 'CAMD Manager'
        self.setTitle(title)
        self['pixmap'] = Pixmap()
        self.onShown.append(self.openTest)

    def openTest(self):
        pass

    def Izlaz(self):
        os.system('cat /etc/.vfdtmp > /proc/vfd')
        self.close()

    def getLastIndex(self):
        a = 0
        if len(self.namelist) > 0:
            for x in self.namelist:
                if x == self.lastCam:
                    return a
                a += 1

        else:
            return -1
        return -1

    def action(self):
        self.session.nav.playService(None)
        last = self.getLastIndex()
        var = -1
        var = self['list'].getSelectionIndex()
        self.cmdS = ''
        if last > -1 and var > -1:
            self.cmdS = '/usr/script/' + self.sclist[var] + ' stop &'
            if last == var:
                self.cmd0 = '/usr/script/' + self.sclist[var] + ' stop &'
                self.cmd1 = '/usr/script/' + self.sclist[var] + ' start &'
                try:
                    os.system(self.cmd0)
                    sleep(0.25)
                    os.system(self.cmd1)
                    sleep(0.25)
                    self.session.openWithCallback(self.callback, MessageBox, _('Stop Camd: ' + str(self.namelist[var]) + '\nStart Camd: ' + str(self.namelist[var])), type=1, timeout=8)
                except OSError:
                    print('ReStart script failed.')

            else:
                self.cmd0 = '/usr/script/' + self.sclist[last] + ' stop &'
                self.cmd1 = '/usr/script/' + self.sclist[var] + ' start &'
                try:
                    os.system(self.cmd0)
                    sleep(0.25)
                    os.system(self.cmd1)
                    sleep(0.25)
                    self.session.openWithCallback(self.callback, MessageBox, _('Stop Camd: ' + str(self.namelist[last]) + '\nStart Camd: ' + str(self.namelist[var])), type=1, timeout=8)
                except OSError:
                    print('Stop/Start scripts failed.')

        else:
            try:
                self.cmd1 = '/usr/script/' + self.sclist[var] + ' start &'
                os.system(self.cmd1)
                os.system('sleep 3')
                self.session.openWithCallback(self.callback, MessageBox, _('Start Camd: ' + str(self.namelist[var])), type=1, timeout=8)
            except:
                self.Izlaz()

        try:
            self.lastCam = self.namelist[var]
            open('/etc/.ActiveCamd', 'w').write(self.lastCam)
            sleep(0.15)
            open('/etc/.CamdStart.sh', 'w').write('#!/bin/sh\n' + self.cmdS + '\nsleep 5\n' + self.cmd1)
            self.cmd2 = 'chmod 755 /etc/.CamdStart.sh &'
            os.system(self.cmd2)
        except:
            self.Izlaz()

        self.readScripts()
        self.session.nav.playService(self.oldService)
        self.Izlaz()

    def stop(self):
        self.session.nav.playService(None)
        last = self.getLastIndex()
        if last > -1:
            self.cmd1 = '/usr/script/' + self.sclist[last] + ' stop &'
            os.system(self.cmd1)
            self.session.openWithCallback(self.callback, MessageBox, _('Stop Camd: ' + str(self.namelist[last])), type=1, timeout=9)
        else:
            return
        self.lastCam = 'no'
        open('/etc/.CamdStart.sh', 'w').write('#!/bin/sh\n' + self.cmd1)
        self.cmd2 = 'chmod 755 /etc/.CamdStart.sh &'
        os.system(self.cmd2)
        os.system('sleep 4')
        self.readScripts()
        self['info'].setText(' ')
        self.session.nav.playService(self.oldService)

    def readScripts(self):
        self.index = 0
        scriptliste = []
        scriptliste1 = []
        pliste = []
        path = '/usr/script/'
        for root, dirs, files in os.walk(path):
            for name in files:
                if 'cam' in dirs:
                    dirs.remove('cam')
                if str(name[len(name) - 7:len(name)]) == '_cam.sh' and root == path:
                    scriptliste.append(name)
                    cmddu = 'dos2unix ' + path + name
                    os.system(cmddu)

        self.sclist = scriptliste
        i = len(self.camdlist)
        del self.camdlist[0:i]
        for lines in scriptliste:
            dat = path + lines
            sfile = open(dat, 'r')
            namime = ''
            namime1 = ''
            nam = ''
            nam1 = ''
            for line in sfile:
                if line[0:7] == 'CAMD_ID':
                    nam = line[8:len(line) - 1]
                if line[0:5] == 'CAMID':
                    nam = line[6:len(line) - 1]
                if line[0:9] == 'CAMD_NAME':
                    namime = line[11:len(line) - 2]
                if line[0:7] == 'CAMNAME':
                    namime1 = line[9:len(line) - 2]

            sfile.close()
            if not nam:
                nam = nam1
            if not namime:
                namime = namime1
            if not namime:
                namime = nam + ' - w/o CAMD_NAME'
            if nam:
                scriptliste1.append(lines)
                self.sclist = scriptliste1
                pliste.append(namime)
                if self.lastCam is not None:
                    if namime == self.lastCam:
                        self.camdlist.append(namime + '\t\tActive')
                    else:
                        self.camdlist.append(namime)
                    self.index += 1
                else:
                    self.camdlist.append(namime)
                    self.index += 1
            self['list'].setList(self.camdlist)
            self.namelist = pliste

    def readCurrent(self):
        try:
            clist = open('/etc/.ActiveCamd', 'r')
        except:
            return

        if clist is not None:
            for line in clist:
                lastcam = line

            clist.close()
        return lastcam

    def ecmcls(self):
        ecmfc = ''
        self['info'].setText(ecmfc)

    def ecm(self):
        ecmf = ''
        if os.path.isfile('/tmp/ecm.info') is True:
            myfile = open('/tmp/ecm.info')
            ecmf = ''
            for line in myfile.readlines():
                print(line)
                ecmf = ecmf + line

            self['info'].setText(ecmf)
        else:
            self['info'].setText(ecmf)
            return

    def autocam(self):
        current = None
        try:
            clist = open('/etc/.ActiveCamd', 'r')
            print('found list')
        except:
            return

        if clist is not None:
            for line in clist:
                current = line

            clist.close()
        print('current =', current)
        if os.path.isfile('/etc/autocam.txt') is False:
            alist = open('/etc/autocam.txt', 'w')
            alist.close()
        self.cleanauto()
        alist = open('/etc/autocam.txt', 'a')
        alist.write(self.oldService.toString() + '\n')
        last = self.getLastIndex()
        alist.write(current + '\n')
        alist.close()
        self.session.openWithCallback(self.callback, MessageBox, _('Autocam assigned to the current channel'), type=1, timeout=10)

    def cleanauto(self):
        delcam = 'no'
        if os.path.isfile('/etc/autocam.txt') is False:
            return
        myfile = open('/etc/autocam.txt', 'r')
        myfile2 = open('/etc/autocam2.txt', 'w')
        icount = 0
        for line in myfile.readlines():
            print('We are in CAMDManager line, self.oldService.toString() =', line, self.oldService.toString())
            if line[:-1] == self.oldService.toString():
                delcam = 'yes'
                icount = icount + 1
                continue
            if delcam == 'yes':
                delcam = 'no'
                icount = icount + 1
                continue
            myfile2.write(line)
            icount = icount + 1

        myfile.close()
        myfile2.close()
        os.system('rm /etc/autocam.txt')
        os.system('cp /etc/autocam2.txt /etc/autocam.txt')


def startConfig(session, **kwargs):
    session.open(CAMDManager)


def mainmenu(session, **kwargs):
    session.open(CAMDManager)


def autostart(reason, session=None, **kwargs):
    """called with reason=1 to during shutdown, with reason=0 at startup?"""
    print('[CAMDManager] Started')
    if reason == 0:
        try:
            os.system('mv /usr/bin/dccamd /usr/bin/dccamdB &')
            os.system('sleep 2')
            os.system('/etc/.CamdStart.sh &')
            self.session.openWithCallback(self.callback, MessageBox, _('Start Camd...'), type=1, timeout=9)
        except:
            pass


def Plugins(**kwargs):
    return [PluginDescriptor(name=_('CAMD Manager'), where=[PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_PLUGINMENU], fnc=mainmenu), PluginDescriptor(name='CAMD Manager', description='CAMDManager', where=[PluginDescriptor.WHERE_AUTOSTART], fnc=autostart)]
