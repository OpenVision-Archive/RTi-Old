#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from enigma import *
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.GUIComponent import GUIComponent
from Components.HTMLComponent import HTMLComponent
from Tools.Directories import fileExists
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Pixmap import Pixmap
from Tools.LoadPixmap import LoadPixmap
from Components.Label import Label
from About import AboutTeam
from RTiUpdate.plugin import Getfolderlist
from RTiFileManager.plugin import RTiFileManagerScreen
from RTiSySInfo.plugin import RTiSySInfoScreen
from RTiHDDSetup.plugin import HDDSetupScreen
from TimeSet.plugin import TimeSetConfig
from ImageBackUp.plugin import ImageBackUpScreen
from Plus import ExtrasList, SimpleEntry


class Panel(Screen):
    skin = '\n\t\t<screen position="center,center" size="725,405" title="RTi Panel v.1.0" >\n\t\t<widget name="menu" position="10,10" size="455,385" scrollbarMode="showOnDemand" />\n\t\t<widget name="thn" position="467,40" size="256,256" alphatest="on" />\n\t\t<widget name="infoM0" position="467,336" zPosition="2" size="256,40" font="Regular;26" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t<widget name="l001" position="80,50" size="350,1" alphatest="on" />\n\t\t<widget name="l002" position="80,98" size="350,1" alphatest="on" />\n\t\t<widget name="l003" position="80,146" size="350,1" alphatest="on" />\n\t\t<widget name="l004" position="80,194" size="350,1" alphatest="on" />\n\t\t<widget name="l005" position="80,242" size="350,1" alphatest="on" />\n\t\t<widget name="l006" position="80,290" size="350,1" alphatest="on" />\n\t\t<widget name="l007" position="80,338" size="350,1" alphatest="on" />\n\t\t<widget name="l008" position="80,386" size="350,1" alphatest="on" />\n\t\t</screen>'

    def __init__(self, session, args=0):
        Screen.__init__(self, session)
        self.session = session
        self.list = []
        self.list.append(SimpleEntry(_('CAMD Manager'), 'CAMD.png'))
        self.list.append(SimpleEntry(_('RTi Update'), 'onlineupdate.png'))
        self.list.append(SimpleEntry('---', 'line.png'))
        self.list.append(SimpleEntry(_('Image BackUp'), 'ImageBackUp.png'))
        self.list.append(SimpleEntry(_('Media Player'), 'MPlayer.png'))
        self.list.append(SimpleEntry(_('Network browser'), 'network.png'))
        self.list.append(SimpleEntry(_('Network mounts'), 'netmount.png'))
        self.list.append(SimpleEntry(_('RTi HDD Setup'), 'partitionmanager.png'))
        self.list.append(SimpleEntry(_('RTi File Manager'), 'filemanager.png'))
        self.list.append(SimpleEntry(_('RTi SySInfo'), 'sysinfo.png'))
        self.list.append(SimpleEntry(_('Time Set'), 'TimeSet.png'))
        self.list.append(SimpleEntry(_('About'), 'about.png'))
        self.list.append(SimpleEntry('---', 'line.png'))
        self.list.append(SimpleEntry(_('Restart GUI'), 'restart.png'))
        self['menu'] = ExtrasList(self.list)
        self['actions'] = ActionMap([
            'SetupActions',
            'DirectionActions'], {
            'ok': self.ok,
            'cancel': self.quit,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.keyLeft,
            'right': self.keyRight}, -2)
        self['thn'] = Pixmap()
        self['infoM0'] = Label()
        self['l001'] = Pixmap()
        self['l002'] = Pixmap()
        self['l003'] = Pixmap()
        self['l004'] = Pixmap()
        self['l005'] = Pixmap()
        self['l006'] = Pixmap()
        self['l007'] = Pixmap()
        self['l008'] = Pixmap()
        self.onLayoutFinish.append(self.startup)

    def emu(self, result):
        if result == 0:
            self.session.open(Emulator)
        elif result == 1:
            self.session.open(CardServer)

    def ok(self):
        index = self['menu'].getSelectedIndex()
        if index == 0:

            try:
                ScSelection = ScSelection
                import Plugins.PLi.SoftcamSetup.Sc
            except Exception:
                e = None
                print(str(e))
                return None

            self.session.open(ScSelection)

        if index == 3:
            self.session.open(ImageBackUpScreen)

        if index == 4:

            try:
                MediaPlayer = MediaPlayer
                import Plugins.Extensions.MediaPlayer.plugin
            except Exception:
                e = None
                print(str(e))
                return None

            self.session.open(MediaPlayer)
        elif index == 5:

            try:
                NetworkBrowserMain = NetworkBrowserMain
                import Plugins.SystemPlugins.NetworkBrowser.plugin
            except Exception:
                e = None
                print(str(e))
                return None

            NetworkBrowserMain(self.session)
        elif index == 6:

            try:
                MountManagerMain = MountManagerMain
                import Plugins.SystemPlugins.NetworkBrowser.plugin
            except Exception:
                e = None
                print(str(e))
                return None

            MountManagerMain(self.session)
        elif index == 1:
            self.session.open(Getfolderlist)
        elif index == 7:
            self.session.open(HDDSetupScreen)
        elif index == 8:
            self.session.open(RTiFileManagerScreen)
        elif index == 9:
            self.session.open(RTiSySInfoScreen)
        elif index == 10:
            self.session.open(TimeSetConfig)
        elif index == 11:
            self.session.open(AboutTeam)
        elif index == 12:
            TryQuitMainloop = TryQuitMainloop
            import Screens.Standby
            self.session.open(TryQuitMainloop, 3)

    def quit(self):
        self.close()

    def keyUp(self):
        self['menu'].up()
        sel = self['menu'].getSelectionIndex()
        self.ReWrite(sel)

    def keyDown(self):
        self['menu'].down()
        sel = self['menu'].getSelectionIndex()
        self.ReWrite(sel)

    def keyLeft(self):
        self['menu'].pageUp()
        sel = self['menu'].getSelectionIndex()
        self.ReWrite(sel)

    def keyRight(self):
        self['menu'].pageDown()
        sel = self['menu'].getSelectionIndex()
        self.ReWrite(sel)

    def ReWrite(self, sel):
        if sel == 0:
            self.slikanoname = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/Ico1/camd.png')

        if sel == 1:
            self.slikanoname = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/Ico1/SUpdate.png')

        if sel == 3:
            self.slikanoname = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/Ico1/ImageBackUp.png')

        if sel == 4:
            self.slikanoname = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/Ico1/MPlayer.png')

        if sel == 5:
            self.slikanoname = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/Ico1/network.png')

        if sel == 6:
            self.slikanoname = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/Ico1/netmount.png')

        if sel == 7:
            self.slikanoname = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/Ico1/hdd.png')

        if sel == 8:
            self.slikanoname = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/Ico1/filemanager.png')

        if sel == 9:
            self.slikanoname = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/Ico1/sysinfo.png')

        if sel == 10:
            self.slikanoname = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/Ico1/TimeSet.png')

        if sel == 11:
            self.slikanoname = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/Ico1/about.png')

        if sel == 13:
            self.slikanoname = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/Ico1/restart.png')

        self['thn'].instance.setPixmap(self.slikanoname)
        ime = self.list[sel][0][0]
        self['infoM0'].setText(str(ime))

    def startup(self):
        picture = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/Ico/line1.png')
        self['l001'].instance.setPixmap(picture)
        self['l002'].instance.setPixmap(picture)
        self['l003'].instance.setPixmap(picture)
        self['l004'].instance.setPixmap(picture)
        self['l005'].instance.setPixmap(picture)
        self['l006'].instance.setPixmap(picture)
        self['l007'].instance.setPixmap(picture)
        self['l008'].instance.setPixmap(picture)
        self.keyUp()
