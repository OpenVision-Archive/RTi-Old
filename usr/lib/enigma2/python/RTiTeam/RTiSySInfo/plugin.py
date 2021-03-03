#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from Plugins.Plugin import PluginDescriptor
from Components.config import config
from Screens.Console import Console
from Components.Label import Label
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
import os.path as os
import stat
import sys
import os
from Components.MenuList import MenuList
from Components.Sources.List import List
from enigma import eTimer, getBoxType
from Components.Console import Console
import time
import sys
from Components.Pixmap import Pixmap
from Tools.LoadPixmap import LoadPixmap
from os import listdir, popen, stat, path
import re

model = getBoxType()

pname = _('RTi SySInfo')
pdesc = _('File Manager')


class RTiSySInfoScreen(Screen):
    skin = '\n\t\t<screen name="SySInfoScreen1" position="center,center" size="720,495" title="" >\n\t\t\t<widget name="red" position="20,456" size="140,40" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="green" position="200,456" size="140,40" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="yellow" position="380,456" size="140,40" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="blue" position="560,456" size="140,40" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\n\t\t\t<ePixmap name="pred" position="20,455" size="140,40" zPosition="0" pixmap="buttons/red.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pgreen" position="200,455" size="140,40" zPosition="0" pixmap="buttons/green.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pyellow" position="380,455" size="140,40" zPosition="0" pixmap="buttons/yellow.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pblue" position="560,455" size="140,40" zPosition="0" pixmap="buttons/blue.png" transparent="1" alphatest="on"/>\n\t\t\t<widget name="list1" position="30,110" size="90,100" scrollbarMode="showOnDemand" foregroundColor="#bbbbbb" />\n\t\t\t<widget name="list2" position="120,110" size="90,100" scrollbarMode="showOnDemand" foregroundColor="#bbbbbb" />\n\t\t\t<widget name="list3" position="300,110" size="90,100" scrollbarMode="showOnDemand" foregroundColor="#bbbbbb" />\n\t\t\t<widget name="list4" position="390,110" size="90,100" scrollbarMode="showOnDemand" foregroundColor="#bbbbbb" />\n\t\t\t<widget name="list5" position="30,320" size="90,100" scrollbarMode="showOnDemand" foregroundColor="#bbbbbb" />\n\t\t\t<widget name="list6" position="120,320" size="120,100" scrollbarMode="showOnDemand" foregroundColor="#bbbbbb" />\n\t\t\t<widget name="list7" position="240,320" size="120,100" scrollbarMode="showOnDemand" foregroundColor="#bbbbbb" />\n\t\t\t<widget name="list8" position="360,320" size="120,100" scrollbarMode="showOnDemand" foregroundColor="#bbbbbb" />\n\t\t\t<widget name="list9" position="0,0" size="1,1" scrollbarMode="showOnDemand" foregroundColor="#aaaaaa" />\n\t\t\t<widget name="list10" position="210,110" size="90,100" scrollbarMode="showOnDemand" foregroundColor="#bbbbbb" />\n\t\t\t<widget name="infoM1" position="100,90" zPosition="2" size="100,20" font="Regular;18" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM16" position="195,90" zPosition="2" size="100,20" font="Regular;18" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM2" position="280,90" zPosition="2" size="100,20" font="Regular;18" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM3" position="370,90" zPosition="2" size="100,20" font="Regular;18" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM4" position="105,300" zPosition="2" size="100,20" font="Regular;18" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM5" position="235,300" zPosition="2" size="100,20" font="Regular;18" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM6" position="355,300" zPosition="2" size="100,20" font="Regular;18" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM7" position="480,90" zPosition="2" size="240,15" font="Regular;14" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM8" position="480,105" zPosition="2" size="240,15" font="Regular;14" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM15" position="480,120" zPosition="2" size="240,20" font="Regular;18" foregroundColor="#ffff3f" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM9" position="480,140" zPosition="2" size="240,20" font="Regular;16" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM10" position="480,250" zPosition="2" size="240,15" font="Regular;14" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM11" position="480,265" zPosition="2" size="240,30" font="Regular;14" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM12" position="480,380" zPosition="2" size="240,15" font="Regular;14" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM13" position="480,395" zPosition="2" size="240,30" font="Regular;14" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM14" position="480,157" zPosition="2" size="240,20" font="Regular;16" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="thn1" position="125,20" size="60,60" alphatest="on" />\n\t\t\t<widget name="thn12" position="215,20" size="60,60" alphatest="on" />\n\t\t\t<widget name="thn2" position="305,20" size="60,60" alphatest="on" />\n\t\t\t<widget name="thn3" position="395,20" size="60,60" alphatest="on" />\n\t\t\t<widget name="thn4" position="130,240" size="60,60" alphatest="on" />\n\t\t\t<widget name="thn5" position="255,240" size="60,60" alphatest="on" />\n\t\t\t<widget name="thn6" position="375,240" size="60,60" alphatest="on" />\n\t\t\t<widget name="thn7" position="570,20" size="60,60" alphatest="on" />\n\t\t\t<widget name="thn8" position="570,189" size="60,60" alphatest="on" />\n\t\t\t<widget name="thn9" position="575,320" size="60,60" alphatest="on" />\n\t\t\t<widget name="thn10" position="45,20" size="60,60" alphatest="on" />\n\t\t\t<widget name="thn11" position="45,240" size="60,60" alphatest="on" />\n\t\t</screen>'

    def __init__(self, session, path_left=None):
        self.session = session
        Screen.__init__(self, session)
        self['red'] = Label(_('PS'))
        self['green'] = Label(_('dmesg'))
        self['yellow'] = Label(_('IfConfig'))
        self['blue'] = Label(_('Top'))
        self['actions'] = ActionMap([
            'ChannelSelectBaseActions',
            'WizardActions',
            'DirectionActions',
            'MenuActions',
            'NumberActions',
            'ColorActions'], {
            'ok': self.ok,
            'back': self.exit,
            'red': self.goRed,
            'green': self.goGreen,
            'yellow': self.goYellow,
            'blue': self.goBlue}, -1)
        self.setTitle('RTi SySInfo   v.1.3')
        self.onLayoutFinish.append(self.StartScroll)
        self.msgno = 0
        self.pozicija = 155
        self.maxrec = 0
        self.lin1 = []
        self.lin2 = []
        self.lin3 = []
        self.lin4 = []
        self.lin5 = []
        self.lin6 = []
        self.lin7 = []
        self.encodings = []
        self.listprev = []
        self.tmp = [
            '0',
            '0',
            '0',
            '0%']
        self.tmp1 = [
            'Total :',
            'Used :',
            'Free :',
            'Use% :']
        self.tmp2 = [
            'Size :',
            'Used :',
            'Free :',
            'Use% :']
        self.tmp3 = [
            '    /',
            '0MB',
            '    /',
            '    /']
        self['list1'] = MenuList(self.tmp1)
        self['list2'] = MenuList(self.tmp)
        self['list3'] = MenuList(self.tmp)
        self['list4'] = MenuList(self.tmp)
        self['list5'] = MenuList(self.tmp2)
        self['list6'] = MenuList(self.tmp)
        self['list7'] = MenuList(self.tmp)
        self['list8'] = MenuList(self.tmp)
        self['list9'] = MenuList(self.tmp)
        self['list10'] = MenuList(self.tmp3)
        self['infoM1'] = Label()
        self['infoM2'] = Label()
        self['infoM3'] = Label()
        self['infoM4'] = Label()
        self['infoM5'] = Label()
        self['infoM6'] = Label()
        self['infoM7'] = Label()
        self['infoM8'] = Label()
        self['infoM9'] = Label()
        self['infoM10'] = Label()
        self['infoM11'] = Label()
        self['infoM12'] = Label()
        self['infoM13'] = Label()
        self['infoM14'] = Label()
        self['infoM15'] = Label()
        self['infoM16'] = Label()
        self['thn1'] = Pixmap()
        self['thn2'] = Pixmap()
        self['thn3'] = Pixmap()
        self['thn4'] = Pixmap()
        self['thn5'] = Pixmap()
        self['thn6'] = Pixmap()
        self['thn7'] = Pixmap()
        self['thn8'] = Pixmap()
        self['thn9'] = Pixmap()
        self['thn10'] = Pixmap()
        self['thn11'] = Pixmap()
        self['thn12'] = Pixmap()
        self.mem = []
        self.swp = []
        self.CpuTimer = eTimer()
        self.CpuTimer.callback.append(self.RefreshInfo)
        self.CpuTimer.start(50, True)

    def exit(self):
        self.close()

    def ok(self):
        self.session.open(SySInfoPlay, 'top')

    def goRed(self):
        self.session.open(SySInfoPlay, 'ps')

    def goGreen(self):
        self.session.open(SySInfoPlay, 'dmsg')

    def goYellow(self):
        self.session.open(SySInfoPlay, 'ifconfig')

    def goBlue(self):
        self.session.open(SySInfoPlay, 'top')

    def StartScroll(self):

        try:
            self.slikahdd = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiSySInfo/img/hdd.png')
            self.slikahdd_temp = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiSySInfo/img/hdd_temp.png')
            self.slikaram = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiSySInfo/img/ram.png')
            self.slikaroot = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiSySInfo/img/root.png')
            self.slikasd = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiSySInfo/img/sd.png')
            self.slikasensor = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiSySInfo/img/sensor.png')
            self.slikasumm = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiSySInfo/img/summ.png')
            self.slikanand = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiSySInfo/img/nand.png')
            self.slikausb = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiSySInfo/img/usb.png')
            self.slikacpu = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiSySInfo/img/cpu.png')
            self['thn1'].instance.setPixmap(self.slikaram)
            self['thn12'].instance.setPixmap(self.slikaram)
            self['thn2'].instance.setPixmap(self.slikanand)
            self['thn3'].instance.setPixmap(self.slikasumm)
            self['thn4'].instance.setPixmap(self.slikanand)
            self['thn5'].instance.setPixmap(self.slikahdd)
            self['thn6'].instance.setPixmap(self.slikausb)
            self['thn7'].instance.setPixmap(self.slikacpu)
            self['thn8'].instance.setPixmap(self.slikahdd)
            self['thn9'].instance.setPixmap(self.slikausb)
            self['thn10'].instance.setPixmap(self.slikaroot)
            self['thn11'].instance.setPixmap(self.slikaroot)
        except:
            self['info'].setText('Loading pixmap error !')

        print('ok')
        self['infoM1'].setText('RAM:')
        self['infoM16'].setText('Cache:')
        self['infoM2'].setText('Swap:')
        self['infoM3'].setText('Total:')
        self['infoM4'].setText('NAND :')
        self['infoM5'].setText('HDD1:')
        self['infoM6'].setText('USB:')
        self['infoM15'].setText('Model: ' + model)
        self['infoM9'].setText('LAN IP: 0.0.0.0')
        self['infoM14'].setText('WLAN IP: 0.0.0.0')
        f = os.popen('ifconfig')
        IPtmp = f.readlines()
        f.close()
        eth = 0
        for x in IPtmp:
            ipos = x.find('eth0')
            if ipos >= 0:
                eth = 1

            ipos = x.find('wlan0')
            if ipos >= 0:
                eth = 2

            ipos = x.find('lo')
            if ipos >= 0:
                eth = 3

            ipos = x.find('inet addr:')
            if ipos >= 0:
                ipos1 = x.find('Bcast')
                IP = x[ipos + 10:ipos1]
                if eth == 1:
                    self['infoM9'].setText('LAN IP:' + str(IP))

                if eth == 2:
                    self['infoM14'].setText('WLAN IP:' + str(IP))

            eth == 2

    def RefreshInfo(self):
        self.ShowInfo()
        self.CpuTimer.start(5000, True)

    def ShowInfo(self):
        ram = []
        f = os.popen("free | grep 'Mem:'")
        ramtmp = f.readline().split()
        if ramtmp:
            r4 = '0%'
            r1 = str(int(ramtmp[1]) / 1024) + 'MB'
            r2 = str(int(ramtmp[2]) / 1024) + 'MB'
            r3 = str(int(ramtmp[3]) / 1024) + 'MB'
            if int(ramtmp[1]) > 0:
                r4 = str(int(ramtmp[2]) * 100 / int(ramtmp[1])) + '%'

            ram.append(r1)
            ram.append(r2)
            ram.append(r3)
            ram.append(r4)

        f.close()
        if len(ram) > 0:
            self['list2'].setList(ram)

        cache = []
        f = os.popen('cat /proc/meminfo |grep Cached')
        cachetmp = f.readline().split()
        if ramtmp:
            c2 = '-' + str(int(cachetmp[1]) / 1024) + 'MB'
            c3 = str(int(cachetmp[1]) / 1024) + 'MB'
            cache.append('    /')
            cache.append(c2)
            cache.append(c3)
            cache.append('    /')

        f.close()
        if len(cache) > 0:
            self['list10'].setList(cache)

        swap = []
        f = os.popen("free | grep 'Swap:'")
        swaptmp = f.readline().split()
        if swaptmp:
            s4 = '0%'
            s1 = str(int(swaptmp[1]) / 1024) + 'MB'
            s2 = str(int(swaptmp[2]) / 1024) + 'MB'
            s3 = str(int(swaptmp[3]) / 1024) + 'MB'
            if int(swaptmp[1]) > 0:
                s4 = str(int(swaptmp[2]) * 100 / int(swaptmp[1])) + '%'

            swap.append(s1)
            swap.append(s2)
            swap.append(s3)
            swap.append(s4)

        f.close()
        if len(swap) > 0:
            self['list3'].setList(swap)

        total = []
        t4 = '0%'
        t1 = (int(ramtmp[1]) + int(swaptmp[1])) / 1024
        t1a = str(t1) + 'MB'
        t2 = ((int(ramtmp[2]) - int(cachetmp[1])) + int(swaptmp[2])) / 1024
        t2a = str(t2) + 'MB'
        t3 = str((int(ramtmp[3]) + int(cachetmp[1]) + int(swaptmp[3])) / 1024) + 'MB'
        if t1 > 0:
            t4 = str(t2 * 100 / t1) + '%'

        total.append(t1a)
        total.append(t2a)
        total.append(t3)
        total.append(t4)
        if len(total) > 0:
            self['list4'].setList(total)

        f = os.popen('top -n1 | grep CPU:')
        cputmp = f.readline()
        f.close()

        try:
            ipos = cputmp.find(' sys')
            ipos1 = cputmp.find(' idle')
            self['infoM7'].setText(str(cputmp[:ipos + 4]))
            self['infoM8'].setText('CPU: ' + str(cputmp[ipos + 5:ipos1 + 5]))
        except Exception:
            print('Error')

        if model == 'azboxme' or model == 'azboxminime':
            cmd = "df -h | grep 'mtd'"
        else:
            cmd = "df -h | grep '/dev/hda1'"
        nand = []
        f = os.popen(cmd)
        nandtmp = f.readline()
        f.close()
        ipos = 0

        try:
            ipos = nandtmp.find('/')
        except Exception:
            print('Error')

        nand = nandtmp[5:ipos].split()
        self['list6'].setList(nand)
        uredi = []
        devpath = '/sys/block/'
        for ured in listdir(devpath):
            if (ured[:2] == 'sd' or ured[:2] == 'hd') and ured[:3] != 'hda':
                uredi.append('/dev/' + ured)
                continue
        uredi.sort()
        for i in range(0, 2):

            try:
                hddstate = 'drive state is:  unknown'
                cmd = 'hdparm -C ' + uredi[i]
                f = os.popen(cmd)
                hddstatetmp = f.readlines()
                f.close()
                for x in hddstatetmp:
                    ipos = x.find('drive state is:')
                    if ipos >= 0:
                        hddstate = x
                        continue
                if i == 0:
                    self['infoM10'].setText(str(uredi[i]))
                    self['infoM11'].setText(str(hddstate))

                if i == 1:
                    self['infoM12'].setText(str(uredi[i]))
                    self['infoM13'].setText(str(hddstate))
            except Exception:
                if i == 0:
                    self['infoM10'].setText('NC')
                    self['infoM11'].setText('')

                if i == 1:
                    self['infoM12'].setText('NC')
                    self['infoM13'].setText('')

                print('err')

            try:
                cmd = 'df -h | grep ' + uredi[i]
                nand = []
                f = os.popen(cmd)
                nandtmp = f.readline()
                imedev = nandtmp[:9]
                nandtmp = nandtmp[9:]
                f.close()
                ipos = 0

                try:
                    ipos = nandtmp.find('/')
                except Exception:
                    nand = [
                        'NC']

                if len(nandtmp) > 0:
                    nand = nandtmp[:ipos].split()
                else:
                    nand = [
                        'NC']
                if i == 0:
                    self['list7'].setList(nand)
                    self['infoM5'].setText(str(imedev))

                if i == 1:
                    self['list8'].setList(nand)
                    self['infoM6'].setText(str(imedev))
            except Exception:
                if i == 0:
                    self['list7'].setList([
                        'NC'])

                if i == 1:
                    self['list8'].setList([
                        'NC'])

                i == 1


class SySInfoPlay(Screen):
    skin = '\n\t\t<screen position="center,center" size="720,495" title="">\n\t\t\t<widget name="red" position="20,456" size="140,40" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="green" position="200,456" size="140,40" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="yellow" position="380,456" size="140,40" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="blue" position="560,456" size="140,40" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\n\t\t\t<ePixmap name="pred" position="20,455" size="140,40" zPosition="0" pixmap="buttons/red.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pgreen" position="200,455" size="140,40" zPosition="0" pixmap="buttons/green.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pyellow" position="380,455" size="140,40" zPosition="0" pixmap="buttons/yellow.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pblue" position="560,455" size="140,40" zPosition="0" pixmap="buttons/blue.png" transparent="1" alphatest="on"/>\n\t\t\t<widget name="infoM1" position="10,5" zPosition="2" size="700,18" font="Regular;18" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />\n\t\t\t<widget name="list1" position="10,30" size="710,405" scrollbarMode="showOnDemand" foregroundColor="#aaaaaa" />\n\t\t</screen>'

    def __init__(self, session, pateka):
        self.session = session
        Screen.__init__(self, session)
        self['red'] = Label(_('PS'))
        self['green'] = Label(_('dmesg'))
        self['yellow'] = Label(_('IfConfig'))
        self['blue'] = Label(_('Top'))
        self['actions'] = ActionMap([
            'ChannelSelectBaseActions',
            'WizardActions',
            'DirectionActions',
            'MenuActions',
            'NumberActions',
            'ColorActions'], {
            'back': self.exit,
            'ok': self.exit,
            'red': self.doRed,
            'green': self.doGreen,
            'yellow': self.doYellow,
            'blue': self.doBlue}, -1)
        self['infoM1'] = Label()
        self.setTitle('RTi SySInfo   v.1.3')
        self.pateka = pateka
        self.encname = []
        self['list1'] = MenuList(self.encname)
        self.onLayoutFinish.append(self.openTest)

    def openTest(self):
        self['infoM1'].setText('Filename : ' + str(self.pateka))
        if self.pateka == 'ps':
            self.doRed()

        if self.pateka == 'dmsg':
            self.doGreen()

        if self.pateka == 'ifconfig':
            self.doYellow()

        if self.pateka == 'top':
            self.doBlue()

    def doRed(self):
        self['infoM1'].setText('ps - process status')
        self.Console = Console()
        self.Console.ePopen('ps >/tmp/tt', self.AddToList)

    def doGreen(self):
        self['infoM1'].setText('dmesg - driver/kernel message')
        self.Console = Console()
        self.Console.ePopen('dmesg >/tmp/tt', self.AddToList)

    def doYellow(self):
        self['infoM1'].setText('IfConfig - Network Parameters')
        self.Console = Console()
        self.Console.ePopen('ifconfig >/tmp/tt', self.AddToList)

    def doBlue(self):
        self['infoM1'].setText('TOP - displays all the running process ')
        self.Console = Console()
        self.Console.ePopen('top -n1 >/tmp/tt', self.AddToList)

    def AddToList(self, result, retval, extra_args):
        dat = '/tmp/tt'
        ps = []

        try:
            f = open(dat, 'r')
            lines = f.readlines()
            for line in lines:
                ps.append(str(line))
            self['list1'].setList(ps)
        except Exception:
            print('error')

    def exit(self):
        self.close()


def main(session, **kwargs):
    session.open(RTiSySInfoScreen)


def Plugins(**kwargs):
    return [PluginDescriptor(name=_('RTi SySInfo'), description=_('SySInfo'), icon='SySInfo.png', where=[PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_PLUGINMENU], fnc=main)]
