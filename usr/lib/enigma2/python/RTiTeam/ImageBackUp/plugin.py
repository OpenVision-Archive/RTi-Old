#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from enigma import *
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.GUIComponent import GUIComponent
from Components.HTMLComponent import HTMLComponent
from Tools.Directories import fileExists, crawlDirectory
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Button import Button
from Components.Label import Label
from Components.ConfigList import ConfigListScreen
from Components.config import ConfigSelection, getConfigListEntry, config
import os
import sys
import re
from Tools.HardwareInfo import HardwareInfo
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from Tools.LoadPixmap import LoadPixmap
from Components.Harddisk import harddiskmanager
from os import system, listdir, statvfs, popen, makedirs, stat, major, minor, path, access
from Screens.MessageBox import MessageBox
from Components.ProgressBar import ProgressBar
from enigma import eTPM, eTimer
from Components.Console import Console

class ImageBackUpScreen(Screen):
    skin = '\n\t\t<screen name="ImageBackUpScreen1" position="center,center" size="580,215" title="ImageBackUp Main   v.1.1" >\n\t\t\t<widget name="red" position="10,170" size="140,40" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="green" position="150,170" size="140,40" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="yellow" position="290,170" size="140,40" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="blue" position="430,170" size="140,40" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\n\t\t\t<ePixmap name="pred" position="10,170" size="140,40" zPosition="0" pixmap="buttons/red.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pgreen" position="150,170" size="140,40" zPosition="0" pixmap="buttons/green.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pyellow" position="290,170" size="140,40" zPosition="0" pixmap="buttons/yellow.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pblue" position="430,170" size="140,40" zPosition="0" pixmap="buttons/blue.png" transparent="1" alphatest="on"/>\n\t\t\t<widget name="infoM1" position="10,10" zPosition="2" size="560,20" font="Regular;18" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM2" position="10,30" zPosition="2" size="560,20" font="Regular;18" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM3" position="10,55" zPosition="2" size="560,20" font="Regular;18" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="scan_progress" position="center,92" zPosition="1" borderWidth="1" size="400,12" backgroundColor="dark" />\n\t\t\t<widget name="poraka1" position="10,110" zPosition="4" size="560,17" font="Regular;16" foregroundColor="#ffffff" backgroundColor="#9f1313" transparent="1" halign="center" valign="center" />\n\t\t\t<widget name="poraka2" position="10,130" zPosition="4" size="560,17" font="Regular;16" foregroundColor="#ffffff" backgroundColor="#9f1313" transparent="1" halign="center" valign="center" />\n\t\t</screen>'
    
    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        self['red'] = Label(_('Select Device'))
        self['green'] = Label(_('Select Boot'))
        self['yellow'] = Label(_('BackUp'))
        self['blue'] = Label(_('Exit'))
        self['actions'] = ActionMap([
            'OkCancelActions',
            'ColorActions',
            'DirectionActions',
            'NumberActions'], {
            'cancel': self.Izlez,
            'red': self.goRed,
            'green': self.goGreen,
            'yellow': self.goYellow,
            'blue': self.goBlue }, -2)
        self['scan_progress'] = ProgressBar()
        self['poraka1'] = Label()
        self['poraka2'] = Label()
        self['infoM1'] = Label()
        self['infoM2'] = Label()
        self['infoM3'] = Label()
        self['infoM6'] = Label()
        self['infoM1'].setText('Where to save BackUp files :')
        self['infoM2'].setText('---')
        self['infoM3'].setText('Make BackUp from : ')
        self['infoM6'].setText('Press OK Button to change Device/Partition List.')
        self.deviceliste = []
        self.partitions = []
        self.SelEn = 0
        self.rereshenable = 0
        self.onLayoutFinish.append(self.drawInfo)

    
    def drawInfo(self):
        self.bootchoice = 0
        self.ProgressValue = 0
        self['scan_progress'].setValue(0)
        self['scan_progress'].hide()
        self['poraka1'].hide()
        self['poraka2'].hide()

    
    def ProgressB(self):
        self.ProgressValue += 1
        if self.ProgressValue > 100:
            self.ProgressValue = 0
        
        self['scan_progress'].setValue(self.ProgressValue)
        self.ProgressTimer1.start(100, True)

    
    def Izlez(self):
        self.close()

    
    def goRed(self):
        self['scan_progress'].setValue(0)
        self['scan_progress'].hide()
        self['poraka1'].hide()
        self['poraka2'].hide()
        self.session.openWithCallback(self.ClBack, ImageBackUpScreen2)

    
    def ClBack(self, komanda):
        self['infoM2'].setText(str(komanda))

    
    def goGreen(self):
        self['scan_progress'].setValue(0)
        self['scan_progress'].hide()
        self['poraka1'].hide()
        self['poraka2'].hide()
        self.session.openWithCallback(self.ClBack2, ChoiceBoot)

    
    def ClBack2(self, komanda):
        if komanda == '1':
            string = 'BOOT-0'
        
        if komanda == '2':
            string = 'BOOT-1'
        
        if komanda == '3':
            string = 'BOOT-2'
        
        self.bootchoice = komanda
        self['infoM3'].setText('Make BackUp from : ' + string)

    
    def goYellow(self):
        location = self['infoM2'].getText().splitlines()[0]
        if location == '---':
            self.session.openWithCallback(self.callback, MessageBox, _('You Must Select Device First !!!\n(where to save BackUp files)'), type = 1, timeout = 8)
            return None
        if int(self.bootchoice) < 1 or int(self.bootchoice) > 3:
            self.session.openWithCallback(self.callback, MessageBox, _('You Must Select BOOT Partition First !!!\n(Make BackUp from ?)'), type = 1, timeout = 8)
            return None
        self['scan_progress'].setValue(0)
        self['scan_progress'].show()
        self['poraka1'].show()
        self['poraka2'].show()
        self['poraka1'].setText('Please wait...')
        self['poraka2'].setText('Preparing...')
        self.ProgressTimer1 = eTimer()
        self.ProgressTimer1.callback.append(self.ProgressB)
        self.ProgressTimer1.start(100, True)
        self.BackUpRootFS()

    
    def BackUpRootFS(self):
        self.SwapState = 0
        self.Console = Console()
        boxime = HardwareInfo().get_device_name()
        if boxime == 'me':
            self.BackUpRootfsMe()
        elif boxime == 'minime':
            self.SwapOnBackUp()
        

    
    def BackUpRootfsMe(self):
        string = 'rm -rf /tmp/root'
        self.Console.ePopen(string, self.BackUpRootfsDone0)

    
    def SwapOnBackUp(self):
        self['poraka1'].setText('Please wait...')
        self['poraka2'].setText('SWAP creation in process...')
        location1 = self['infoM2'].getText().splitlines()[0] + '/BackUp'
        string = 'dd if=/dev/zero of=' + location1 + '/swapfile_backup bs=1024k count=128'
        self.Console.ePopen(string, self.SwapOnBackUp1)

    
    def SwapOnBackUp1(self, result, retval, extra_args):
        location1 = self['infoM2'].getText().splitlines()[0] + '/BackUp'
        string = 'mkswap ' + location1 + '/swapfile_backup'
        self.Console.ePopen(string, self.SwapOnBackUp2)

    
    def SwapOnBackUp2(self, result, retval, extra_args):
        self.SwapState = 1
        location1 = self['infoM2'].getText().splitlines()[0] + '/BackUp'
        string = 'swapon ' + location1 + '/swapfile_backup'
        self.Console.ePopen(string, self.BackUpRootfsDone00)

    
    def BackUpRootfsDone00(self, result, retval, extra_args):
        string = 'rm -rf /tmp/root'
        self.Console.ePopen(string, self.BackUpRootfsDone0)

    
    def BackUpRootfsDone0(self, result, retval, extra_args):
        location1 = self['infoM2'].getText().splitlines()[0] + '/BackUp'
        string = 'mkdir -p ' + location1
        self.Console.ePopen(string, self.BackUpRootfsDone1)

    
    def BackUpRootfsDone1(self, result, retval, extra_args):
        string = 'mkdir -p /tmp/root'
        self.Console.ePopen(string, self.BackUpRootfsDone2)

    
    def BackUpRootfsDone2(self, result, retval, extra_args):
        boxime = HardwareInfo().get_device_name()
        self['poraka1'].setText('Please wait about 3min.')
        self['poraka2'].setText('RootFS BackUp in progress...')
        if boxime == 'me':
            if self.bootchoice == '1':
                particija = 'mtd3'
            
            if self.bootchoice == '2':
                particija = 'mtd5'
            
            if self.bootchoice == '3':
                particija = 'mtd7'
            
        elif boxime == 'minime':
            if self.bootchoice == '1':
                particija = 'mtd3'
            
            if self.bootchoice == '2':
                particija = 'mtd4'
            
        
        string = 'mount -t jffs2 ' + particija + ' /tmp/root'
        self.Console.ePopen(string, self.BackUpRootfsDone3)

    
    def BackUpRootfsDone3(self, result, retval, extra_args):
        ime = '/root'
        location1 = self['infoM2'].getText().splitlines()[0] + '/BackUp'
        if self.bootchoice == '1':
            ime = '/image0'
        
        if self.bootchoice == '2':
            ime = '/image1'
        
        if self.bootchoice == '3':
            ime = '/image2'
        
        string = 'mkfs.jffs2 --root=/tmp/root/ --faketime --output=' + location1 + ime + '.jffs2 --eraseblock=0x20000 --pagesize=0x800 -l -p -n'
        self.Console.ePopen(string, self.BackUpRootfsDone4)

    
    def BackUpRootfsDone4(self, result, retval, extra_args):
        string = 'sync'
        self.Console.ePopen(string, self.BackUpRootfsDone5)

    
    def BackUpRootfsDone5(self, result, retval, extra_args):
        string = 'umount -f /tmp/root'
        self.Console.ePopen(string, self.BackUpRootfsDone6)

    
    def BackUpRootfsDone6(self, result, retval, extra_args):
        tmpList = result.split(' ')
        self['poraka1'].setText('DONE')
        self['poraka2'].setText('')
        self.ProgressTimer1.stop()
        self['scan_progress'].setValue(100)
        if self.SwapState == 1:
            self.SwapOffBackUp()
        

    
    def SwapOffBackUp(self):
        location1 = self['infoM2'].getText().splitlines()[0] + '/BackUp'
        string = 'swapoff ' + location1 + '/swapfile_backup 2> /dev/null'
        self.Console.ePopen(string, self.SwapOffBackUp1)

    
    def SwapOffBackUp1(self, result, retval, extra_args):
        location1 = self['infoM2'].getText().splitlines()[0] + '/BackUp'
        string = 'rm -rf ' + location1 + '/swapfile_backup'
        self.Console.ePopen(string, self.SwapOffBackUp2)

    
    def SwapOffBackUp2(self, result, retval, extra_args):
        self.SwapState = 0

    
    def BackUpKernel(self):
        print('OK')

    
    def BackUpKernelDone(self, result, retval, extra_args):
        tmpList = result.split(' ')
        self['poraka1'].setText('DONE')
        self['poraka2'].setText('')
        self.ProgressTimer1.stop()
        self['scan_progress'].setValue(100)

    
    def goBlue(self):
        self.close()



class ImageBackUpScreen2(Screen):
    skin = '\n\t\t<screen name="ImageBackUpScreen1" position="center,center" size="560,380" title="Select Device" >\n\t\t\t<widget name="list1" position="40,35" size="480,75" scrollbarMode="showOnDemand" foregroundColor="#bbbbbb" />\n\t\t\t<widget name="list2" position="10,235" size="540,75" scrollbarMode="showAlways" foregroundColor="#bbbbbb" />\n\t\t\t<widget name="infoM0" position="10,10" zPosition="2" size="540,20" font="Regular;18" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM1" position="10,130" zPosition="2" size="540,20" font="Regular;18" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM2" position="10,150" zPosition="2" size="540,20" font="Regular;18" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM3" position="10,210" zPosition="2" size="540,20" font="Regular;18" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM6" position="5,330" zPosition="2" size="550,20" font="Regular;16" foregroundColor="#00afff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM7" position="5,350" zPosition="2" size="550,20" font="Regular;16" foregroundColor="#00afff" transparent="0" halign="center" valign="center" />\n\t\t</screen>'
    
    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap([
            'OkCancelActions',
            'ColorActions',
            'DirectionActions',
            'NumberActions'], {
            'ok': self.ListChange,
            'cancel': self.Izlez,
            'up': self.keyUp,
            'down': self.keyDown }, -2)
        self.tmp = []
        self['list1'] = MenuList(self.tmp)
        self['list2'] = MenuList([])
        self['infoM0'] = Label()
        self['infoM1'] = Label()
        self['infoM2'] = Label()
        self['infoM3'] = Label()
        self['infoM6'] = Label()
        self['infoM7'] = Label()
        self['infoM6'].setText('Press OK Button to change Device/Partition List.')
        self['infoM7'].setText('Select partition (where to save BackUp Image) and Exit.')
        self.deviceliste = []
        self.partitions = []
        self.SelEn = 0
        self.rereshenable = 0
        self.HDDTimer = eTimer()
        self.HDDTimer.callback.append(self.RefreshInfo)
        self.HDDTimer.start(5000, True)
        self.onLayoutFinish.append(self.drawInfo)

    
    def RefreshInfo(self):
        if self.rereshenable == 0:
            self.drawInfo()
            self.Listset()
        
        self.HDDTimer.start(5000, True)

    
    def drawInfo(self):
        self['list1'].selectionEnabled(1)
        self['list2'].selectionEnabled(0)
        os.system('/sbin/hdparm -S0 /dev/sda')
        os.system('/sbin/hdparm -S0 /dev/sdb')
        os.system('/sbin/hdparm -S0 /dev/sdc')
        os.system('/sbin/hdparm -S0 /dev/sdd')
        os.system('/sbin/hdparm -S0 /dev/sde')
        import time as time
        time.sleep(4.60268e+18)
        self.deviceliste = []
        devpath = '/sys/block/'
        for ured in listdir(devpath):
            if ured[:2] == 'sd':
                
                try:
                    f = open(devpath + ured + '/size')
                    siz = f.readline()
                    size = int(siz) * 512
                    f.close()
                except IOError:
                    size = 0

                siz1 = size / 1000000
                if int(siz1 / 1000) >= 10:
                    sizMG = '%d.%01d' % (siz1 / 1000, siz1 % 1000)
                    sizMG = sizMG + ' GB'
                else:
                    sizMG = str(siz1) + ' MB'
                DString = 'Disk /dev/' + ured + ': ' + sizMG + ', ' + str(size) + ' bytes'
                self.deviceliste.append(DString)
                continue
        self.deviceliste.sort()
        self['list1'].setList(self.deviceliste)
        if len(self.deviceliste) > 0:
            self.VendorModel()
        else:
            self['infoM0'].setText('No Devices Foond !!!')
            self['list2'].setList([])

    
    def VendorModel(self):
        self['infoM0'].setText('DEVICE LIST :')
        if len(self.deviceliste) < 1:
            return None
        p = re.compile('\\s+')
        sel = self['list1'].getSelectionIndex()
        devname = self.deviceliste[sel][5:13]
        device = self.deviceliste[sel][10:13]
        os.system('/sbin/hdparm -S 0 %s' % devname)
        
        try:
            f = open('/sys/block/' + device + '/device/vendor', 'r')
            vendor = re.sub(p, ' ', f.readline())
            f.close()
        except IOError:
            len(self.deviceliste) < 1
            vendor = ''
        except:
            len(self.deviceliste) < 1

        
        try:
            f = open('/sys/block/' + device + '/device/model', 'r')
            model = re.sub(p, ' ', f.readline())
            f.close()
        except IOError:
            len(self.deviceliste) < 1
            model = ''
        except:
            len(self.deviceliste) < 1

        deviceinfo = str(vendor) + '  ( ' + str(model) + ')'
        self['infoM1'].setText(deviceinfo)
        
        try:
            f = open('/sys/block/' + device + '/removable', 'r')
            removable = int(f.readline())
            self.removable = removable
            if removable == 0:
                devtype = 'Type: HDD'
            else:
                devtype = 'Type: Removable/PenDrive'
            f.close()
        except IOError:
            len(self.deviceliste) < 1
            devtype = 'Type: Unknown'
        except:
            len(self.deviceliste) < 1

        self['infoM2'].setText(devtype)
        
        try:
            self.partitions = []
            self['infoM3'].setText('PARTITION LIST (On selected device) :')
            devpath = '/sys/block/' + device
            for partition in listdir(devpath):
                if partition[0:len(device)] != device:
                    continue
                
                f = open('/sys/block/' + device + '/' + partition + '/size', 'r')
                cap = f.readline()
                f.close()
                
                try:
                    cap = int(cap) * 512 / 1000000
                    if int(cap / 1000) >= 10:
                        cap = '%d.%01d' % (cap / 1000, cap % 1000)
                        cap = str(cap) + ' GB '
                    else:
                        cap = str(cap) + ' MB '
                except:
                    len(self.deviceliste) < 1
                    cap = '0 MB '

                f = os.popen('sfdisk -l|grep /dev/' + partition + "| awk '{print substr($7" + '" "' + " $8,1)}'")
                ptype = re.sub(p, ' ', f.readline())
                f.close()
                ptype = ptype + '           '
                ptype = ptype[:11]
                f = os.popen('mount | grep ' + partition + "| awk '{print substr($3,1)}'")
                pmount = f.readline()
                f.close()
                if len(pmount) > 0:
                    pmount = ' - mounted on ' + pmount
                else:
                    pmount = ' - not mounted!'
                infostring = str(partition) + ': ' + str(cap) + str(ptype) + str(pmount)
                self.partitions.append(infostring)
                self.partitions.sort()
            self['list2'].setList(self.partitions)
        except:
            len(self.deviceliste) < 1
            print('Err.')


    
    def ListChange(self):
        if self.rereshenable == 1:
            return None
        if self.SelEn == 0 and len(self.partitions) > 0:
            self['list1'].selectionEnabled(0)
            self['list2'].selectionEnabled(1)
            self.SelEn = 1
        elif len(self.deviceliste) > 0:
            self['list1'].selectionEnabled(1)
            self['list2'].selectionEnabled(0)
            self.SelEn = 0
        

    
    def Listset(self):
        if len(self.partitions) == 0 or len(self.deviceliste) == 0:
            return None
        if self.SelEn == 0:
            self['list1'].selectionEnabled(1)
            self['list2'].selectionEnabled(0)
        else:
            self['list1'].selectionEnabled(0)
            self['list2'].selectionEnabled(1)

    
    def keyUp(self):
        if self.SelEn == 0:
            self['list1'].up()
            self.VendorModel()
        
        if self.SelEn == 1:
            self['list2'].up()
        

    
    def keyDown(self):
        if self.SelEn == 0:
            self['list1'].down()
            self.VendorModel()
        
        if self.SelEn == 1:
            self['list2'].down()
        

    
    def Izlez(self):
        location = self['infoM0'].getText().splitlines()[0]
        if location != 'No Devices Foond !!!':
            sel = self['list2'].getSelectionIndex()
            devline = self.partitions[sel]
            ipos = devline.find(' - mounted on ')
            if ipos == -1:
                string = '---'
            else:
                string = devline[ipos + 14:]
        else:
            string = '---'
        self.close(string)



class ChoiceBoot(Screen):
    skin = '\n\t\t<screen name="Menusimple2" position="center,center" size="160,235" title="BOOT Select" >\n\t\t\t<widget name="list" position="15,80" size="130,100" scrollbarMode="showOnDemand" foregroundColor="#aaaaaa" />\n\t\t\t<widget name="infoA" position="15,15" zPosition="2" size="130,45" font="Regular;20" foregroundColor="#aaaaaa" transparent="1" halign="center" valign="center" />\n\t\t\t<widget name="info20" position="10,200" zPosition="2" size="140,20" font="Regular;20" foregroundColor="#aaaaaa" transparent="1" halign="center" valign="center" />\n\t\t</screen>'
    
    def __init__(self, session):
        self.skinName = 'OnlineManager2'
        Screen.__init__(self, session)
        self['actions'] = ActionMap([
            'OkCancelActions',
            'ColorActions',
            'DirectionActions'], {
            'ok': self.OkPress,
            'cancel': self.Izlaz1 }, -1)
        self['list'] = MenuList([])
        self['info20'] = Label()
        self['infoA'] = Label()
        self.onLayoutFinish.append(self.openTest)

    
    def openTest(self):
        boxime = HardwareInfo().get_device_name()
        self.mountpoints = []
        self['infoA'].setText('Select BOOT Partition:')
        self['info20'].setText('And press OK')
        self.mountpoints.append('1. BOOT-0')
        self.mountpoints.append('2. BOOT-1')
        if boxime == 'me':
            self.mountpoints.append('3. BOOT-2')
        
        self.mountpoints.sort()
        self['list'].setList(self.mountpoints)

    
    def OkPress(self):
        sel = self['list'].getSelectionIndex()
        mountpoint = self.mountpoints[sel][:1]
        self.close(mountpoint)

    
    def Izlaz1(self):
        self.close('1')



def main(session, **kwargs):
    session.open(ImageBackUpScreen)


def Plugins(**kwargs):
    boxime = HardwareInfo().get_device_name()
    if boxime == 'elite' and boxime == 'premium' and boxime == 'premium+' and boxime == 'ultra' and boxime == 'me' and boxime == 'minime' or boxime == 'multimedia':
        return [
            PluginDescriptor(name = _('ImageBackUp'), description = _('ImageBackUp'), icon = 'ImageBackUp.png', where = [
                PluginDescriptor.WHERE_EXTENSIONSMENU,
                PluginDescriptor.WHERE_PLUGINMENU], fnc = main)]
    return []

