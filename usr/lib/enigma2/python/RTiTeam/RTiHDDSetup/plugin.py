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

class HDDSetupScreen(Screen):
    skin = '\n\t\t<screen name="HDDSetupScreen1" position="center,center" size="560,495" title="RTi HDD Setup   v.1.0" >\n\t\t\t<widget name="red" position="0,456" size="140,40" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="green" position="140,456" size="140,40" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="yellow" position="280,456" size="140,40" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="blue" position="420,456" size="140,40" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\n\t\t\t<ePixmap name="pred" position="0,455" size="140,40" zPosition="0" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pgreen" position="140,455" size="140,40" zPosition="0" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pyellow" position="280,455" size="140,40" zPosition="0" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pblue" position="420,455" size="140,40" zPosition="0" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on"/>\n\t\t\t<widget name="list1" position="40,35" size="480,75" scrollbarMode="showOnDemand" foregroundColor="#bbbbbb" />\n\t\t\t<widget name="list2" position="10,235" size="540,75" scrollbarMode="showAlways" foregroundColor="#bbbbbb" />\n\t\t\t<widget name="infoM0" position="10,10" zPosition="2" size="540,20" font="Regular;18" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM1" position="10,130" zPosition="2" size="540,20" font="Regular;18" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM2" position="10,150" zPosition="2" size="540,20" font="Regular;18" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM3" position="10,210" zPosition="2" size="540,20" font="Regular;18" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM4" position="5,330" zPosition="2" size="550,20" font="Regular;16" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM5" position="5,350" zPosition="2" size="550,20" font="Regular;16" foregroundColor="#ffffff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM6" position="5,410" zPosition="2" size="550,20" font="Regular;16" foregroundColor="#00afff" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM1a" position="10,130" zPosition="2" size="540,20" font="Regular;18" foregroundColor="#ff0000" transparent="0" halign="center" valign="center" />\n\t\t\t<widget name="infoM2a" position="10,150" zPosition="2" size="540,20" font="Regular;18" foregroundColor="#ffbb00" transparent="0" halign="center" valign="center" />\n\t\t</screen>'
    
    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        self['red'] = Label(_('SpeedTest'))
        self['green'] = Label(_('CacheSpeed'))
        self['yellow'] = Label(_('(u)Mount'))
        self['blue'] = Label(_('Init'))
        self['actions'] = ActionMap([
            'OkCancelActions',
            'ColorActions',
            'DirectionActions',
            'NumberActions'], {
            'ok': self.ListChange,
            'cancel': self.Izlez,
            'red': self.RedBtn,
            'green': self.GreenBtn,
            'yellow': self.YellowBtn,
            'blue': self.BlueBtn,
            'up': self.keyUp,
            'down': self.keyDown,
            '0': self.drawInfo,
            '1': self.ListChange,
            '2': self.Izlez }, -2)
        self.tmp = []
        self['list1'] = MenuList(self.tmp)
        self['list2'] = MenuList([])
        self['infoM0'] = Label()
        self['infoM1'] = Label()
        self['infoM2'] = Label()
        self['infoM3'] = Label()
        self['infoM4'] = Label()
        self['infoM5'] = Label()
        self['infoM6'] = Label()
        self['infoM1a'] = Label()
        self['infoM2a'] = Label()
        self['infoM4'].setText('Read disk speed: Not Tested Yet')
        self['infoM5'].setText('Read disk cache speed: Not Tested Yet')
        self['infoM6'].setText('Press OK Button to change Device/Partition List.')
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
            self.showhide('1')
            self.drawInfo()
            self.Listset()
        
        if self.rereshenable == 1:
            self['infoM1a'].setText('INIT IS IN PROGRESS...')
            self['infoM2a'].setText('This may take some time, please be patient.')
            self.showhide('0')
        
        self.HDDTimer.start(5000, True)

    
    def drawInfo(self):
        self.showhide('1')
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
            print 'Err.'


    
    def sysfsPath(self, filename):
        return path.realpath('/sys/block/' + self.device + '/' + filename)

    
    def RedBtn(self):
        if self.rereshenable == 1:
            return None
        if len(self.deviceliste) < 1:
            return None
        dspeed = ''
        readDiskRe = re.compile('Timing buffered disk reads:\\s*(.*)')
        p = re.compile('\\s+')
        sel = self['list1'].getSelectionIndex()
        devname = self.deviceliste[sel][5:13]
        hdparm = os.popen('/sbin/hdparm -t %s' % devname)
        for line in hdparm:
            readDisk = re.findall(readDiskRe, line)
            if readDisk:
                dspeed = readDisk[0].lstrip()
                continue
            len(self.deviceliste) < 1
        hdparm.close()
        self['infoM4'].setText('Read disk speed: ' + str(dspeed))

    
    def GreenBtn(self):
        if self.rereshenable == 1:
            return None
        if len(self.deviceliste) < 1:
            return None
        dcspeed = ''
        readCacheRe = re.compile('Timing buffer-cache reads:\\s*(.*)')
        p = re.compile('\\s+')
        sel = self['list1'].getSelectionIndex()
        devname = self.deviceliste[sel][5:13]
        hdparm = os.popen('/sbin/hdparm -T %s' % devname)
        for line in hdparm:
            readCache = re.findall(readCacheRe, line)
            if readCache:
                dcspeed = readCache[0].lstrip()
                continue
            len(self.deviceliste) < 1
        hdparm.close()
        self['infoM5'].setText('Read disk cache speed: ' + str(dcspeed))

    
    def YellowBtn(self):
        if self.rereshenable == 1:
            return None
        if self.SelEn != 1:
            self.session.openWithCallback(self.callback, MessageBox, _('\nFirst you must select partition which you want to (u)Mount!'), type = 1, timeout = 20)
            return None
        sel = self['list2'].getSelectionIndex()
        ipos = self.partitions[sel].find(' - mounted on ')
        if ipos != -1:
            devname = '/dev/' + self.partitions[sel][:4]
            mountpoint = self.partitions[sel][ipos + 14:]
            odgovor = self.umount(devname)
            if odgovor == True:
                self.session.openWithCallback(self.callback, MessageBox, _('\nUmount Succesfull!'), type = 1, timeout = 20)
            else:
                self.session.openWithCallback(self.callback, MessageBox, _('Cannot umount current drive.\nA record in progress, timeshit or some external tools (like samba and nfsd) may cause this problem.\nPlease stop this actions/applications and try again'), MessageBox.TYPE_ERROR)
            self.drawInfo()
            return None
        self.session.openWithCallback(self.mnt, ChoiceMountPoint, 'aaa')

    
    def YellowPrint(self):
        sel = self['list2'].getSelectionIndex()
        ipos = self.partitions[sel].find(' - mounted on ')
        if ipos != -1:
            self['yellow'].setText('Umount')
        else:
            self['yellow'].setText('Mount')

    
    def BlueBtn(self):
        self['infoM1a'].setText('INIT IS IN PROGRESS...')
        self['infoM2a'].setText('This may take some time, please be patient.')
        self.showhide('0')
        self.rereshenable = 1
        sel = self['list2'].getSelectionIndex()
        for line in self.partitions:
            device = line[:4]
            devname = '/dev/' + device
            ipos = line.find(' - mounted on ')
            if ipos != -1:
                mountpoint = line[ipos + 14:]
                odgovor = self.umount(devname)
                if odgovor == True:
                    print 'Umount Succesfull!'
                else:
                    self.session.openWithCallback(self.callback, MessageBox, _('Cannot umount current drive.\nA record in progress, timeshit or some external tools (like samba and nfsd) may cause this problem.\nPlease stop this actions/applications and try again'), MessageBox.TYPE_ERROR)
                    self.rereshenable = 0
                    self.drawInfo()
                    return None
            odgovor == True
        self.session.openWithCallback(self.BlueBtn2, ChoicePartitionNoType, '111')

    
    def BlueBtn2(self, partno):
        if partno == '---':
            self.drawInfo()
            self.rereshenable = 0
            return None
        self.partno = partno
        self.session.openWithCallback(self.BlueBtn3, ChoicePartitionNoType, '222')

    
    def BlueBtn3(self, parttype):
        if parttype == '---':
            self.drawInfo()
            self.rereshenable = 0
            return None
        self.parttype = parttype
        self.HDDTimer1 = eTimer()
        self.HDDTimer1.callback.append(self.BlueBtn4)
        self.HDDTimer1.start(100, True)

    
    def BlueBtn4(self):
        if self.parttype == '1' or self.parttype == '2':
            cmdp = '83'
        
        if self.parttype == '3' and self.removable == 0:
            cmdp = 'c'
        
        if self.parttype == '3' and self.removable == 1:
            cmdp = '6'
        
        sel = self['list1'].getSelectionIndex()
        devname = self.deviceliste[sel][10:13]
        f = open('/sys/block/' + devname + '/size', 'r')
        cap = f.readline()
        f.close()
        
        try:
            cap = (int(cap) / 1000) * 512 / 1000
            cap = int(cap / 4.6074e+18)
        except:
            cap = 0

        sel1 = self['list1'].getSelectionIndex()
        devname1 = self.deviceliste[sel1][5:13]
        if self.partno == '1':
            cmds = str(cap)
            cmd = 'printf "0,,' + cmdp + '\n;\n;\n;\ny\n" | sfdisk -f -uM ' + devname1
        
        if self.partno == '2':
            cmds = str(int(cap / 2))
            cmd = 'printf ",' + cmds + ',' + cmdp + '\n,,' + cmdp + '\n;\n;\ny\n" | sfdisk -f -uM ' + devname1
        
        if self.partno == '3':
            cmds = str(int(cap / 3))
            cmd = 'printf ",' + cmds + ',' + cmdp + '\n,' + cmds + ',' + cmdp + '\n,,' + cmdp + '\n;\ny\n" | sfdisk -f -uM ' + devname1
        
        odgovor = self.sfdisk(cmd)
        if odgovor == True:
            print 'sfdisk Succesfull!'
        else:
            self.session.openWithCallback(self.callback, MessageBox, _('Cannot make partition!'), MessageBox.TYPE_ERROR)
            self.rereshenable = 0
            self.drawInfo()
            return None
        import time
        time.sleep(3)
        odgovor1 = True
        odgovor2 = True
        if self.partno == '1':
            devname2 = devname1 + '1'
            
            try:
                o = self.umount(devname2)
            except:
                print "can't umount " + devname2

            if self.parttype == '1':
                odgovor = self.formatext3(devname2, cmds)
            
            if self.parttype == '2':
                odgovor = self.formatext2(devname2, cmds)
            
            if self.parttype == '3' and self.removable == 0:
                odgovor = self.formatfat32(devname2)
            
            if self.parttype == '3' and self.removable == 1:
                odgovor = self.formatfat16(devname2)
            
        
        if self.partno == '2':
            devname2 = devname1 + '1'
            
            try:
                o = self.umount(devname2)
            except:
                print "can't umount " + devname2

            if self.parttype == '1':
                odgovor = self.formatext3(devname2, cmds)
            
            if self.parttype == '2':
                odgovor = self.formatext2(devname2, cmds)
            
            if self.parttype == '3' and self.removable == 0:
                odgovor = self.formatfat32(devname2)
            
            if self.parttype == '3' and self.removable == 1:
                odgovor = self.formatfat16(devname2)
            
            import time
            time.sleep(3)
            devname2 = devname1 + '2'
            
            try:
                o = self.umount(devname2)
            except:
                print "can't umount " + devname2

            if self.parttype == '1':
                odgovor1 = self.formatext3(devname2, cmds)
            
            if self.parttype == '2':
                odgovor1 = self.formatext2(devname2, cmds)
            
            if self.parttype == '3' and self.removable == 0:
                odgovor1 = self.formatfat32(devname2)
            
            if self.parttype == '3' and self.removable == 1:
                odgovor1 = self.formatfat16(devname2)
            
        
        if self.partno == '3':
            devname2 = devname1 + '1'
            
            try:
                o = self.umount(devname2)
            except:
                print "can't umount " + devname2

            if self.parttype == '1':
                odgovor = self.formatext3(devname2, cmds)
            
            if self.parttype == '2':
                odgovor = self.formatext2(devname2, cmds)
            
            if self.parttype == '3' and self.removable == 0:
                odgovor = self.formatfat32(devname2)
            
            if self.parttype == '3' and self.removable == 1:
                odgovor = self.formatfat16(devname2)
            
            import time
            time.sleep(3)
            devname2 = devname1 + '2'
            
            try:
                o = self.umount(devname2)
            except:
                print "can't umount " + devname2

            if self.parttype == '1':
                odgovor1 = self.formatext3(devname2, cmds)
            
            if self.parttype == '2':
                odgovor1 = self.formatext2(devname2, cmds)
            
            if self.parttype == '3' and self.removable == 0:
                odgovor1 = self.formatfat32(devname2)
            
            if self.parttype == '3' and self.removable == 1:
                odgovor1 = self.formatfat16(devname2)
            
            import time
            time.sleep(3)
            devname2 = devname1 + '3'
            
            try:
                o = self.umount(devname2)
            except:
                print "can't umount " + devname2

            if self.parttype == '1':
                odgovor2 = self.formatext3(devname2, cmds)
            
            if self.parttype == '2':
                odgovor2 = self.formatext2(devname2, cmds)
            
            if self.parttype == '3' and self.removable == 0:
                odgovor2 = self.formatfat32(devname2)
            
            if self.parttype == '3' and self.removable == 1:
                odgovor2 = self.formatfat16(devname2)
            
        
        if odgovor == True and odgovor1 == True and odgovor2 == True:
            print 'format Succesfull!'
        else:
            self.session.openWithCallback(self.callback, MessageBox, _('Cannot format partition!'), MessageBox.TYPE_ERROR)
            self.rereshenable = 0
            self.drawInfo()
            return None
        devname2 = (odgovor2 == True) + '1'
        odgovor1 = self.mkdir1()
        odgovor2 = self.mount(devname2, '/tmp/test0')
        odgovor3 = self.mkdir3()
        odgovor4 = self.mkdir4()
        odgovor5 = self.mkdir5()
        odgovor6 = self.umount(devname2)
        odgovor7 = self.mkdir6()
        errmsg = "Can't make dirs \n\n"
        if odgovor1 == False:
            errmsg = errmsg + "\nCan't make tmp dir."
        
        if odgovor2 == False:
            errmsg = errmsg + "\nCan't mount partition."
        
        if odgovor3 == False:
            errmsg = errmsg + "\nCan't make movie dir."
        
        if odgovor4 == False:
            errmsg = errmsg + "\nCan't make music dir."
        
        if odgovor5 == False:
            errmsg = errmsg + "\nCan't make picture dir."
        
        if odgovor6 == False:
            errmsg = errmsg + "\nCan't umount partition."
        
        if odgovor7 == False:
            errmsg = errmsg + "\nCan't remove tmp dir."
        
        if odgovor1 == True and odgovor2 == True and odgovor3 == True and odgovor4 == True and odgovor5 == True and odgovor6 == True:
            print 'All Done!'
        else:
            self.session.openWithCallback(self.callback, MessageBox, _(str(errmsg)), MessageBox.TYPE_ERROR)
            self.rereshenable = 0
            self.drawInfo()
            return None
        self.rereshenable = odgovor6 == True
        self.session.openWithCallback(self.callback, MessageBox, _('\nInit - Succesfull !'), type = 1, timeout = 20)
        self.drawInfo()

    
    def mnt(self, mountpoint):
        if mountpoint == '---':
            self.rereshenable = 0
            return None
        mountpoint = '/media/' + mountpoint
        sel = self['list2'].getSelectionIndex()
        devname = '/dev/' + self.partitions[sel][:4]
        odgovor = self.mount(devname, mountpoint)
        if odgovor == True:
            self.session.openWithCallback(self.callback, MessageBox, _('\nMount ' + devname + ' on : ' + mountpoint + ' Succesfull!'), type = 1, timeout = 20)
        else:
            self.session.openWithCallback(self.callback, MessageBox, _('\nMount ' + devname + ' on : ' + mountpoint + ' UnSuccesfull!'), MessageBox.TYPE_ERROR)
        self.drawInfo()

    
    def showhide(self, path):
        if path == '1':
            self['list1'].show()
            self['list2'].show()
            self['infoM0'].show()
            self['infoM1'].show()
            self['infoM2'].show()
            self['infoM3'].show()
            self['infoM4'].show()
            self['infoM5'].show()
            self['infoM6'].show()
            self['infoM1a'].hide()
            self['infoM2a'].hide()
        else:
            self['list1'].hide()
            self['list2'].hide()
            self['infoM0'].hide()
            self['infoM1'].hide()
            self['infoM2'].hide()
            self['infoM3'].hide()
            self['infoM4'].hide()
            self['infoM5'].hide()
            self['infoM6'].hide()
            self['infoM1a'].show()
            self['infoM2a'].show()

    
    def umount(self, path):
        return os.system('umount -f ' + path) == 0

    
    def mount(self, device, mountpoint):
        cmd = 'mount ' + device + ' ' + mountpoint
        return os.system('mount ' + device + ' ' + mountpoint) == 0

    
    def sfdisk(self, cmd):
        return os.system(cmd) == 0

    
    def formatext3(self, path, cap):
        cmd = 'mkfs.ext3 '
        if int(cap) > 4096:
            cmd += '-T largefile '
        
        cmd += '-m0 -O dir_index ' + path
        return os.system(cmd) == 0

    
    def formatext2(self, path, cap):
        cmd = 'mkfs.ext3 '
        if int(cap) > 4096:
            cmd += '-T largefile '
        
        cmd += '-m0 -O dir_index ' + path
        return os.system(cmd) == 0

    
    def formatfat32(self, path):
        print path
        return os.system('/usr/lib/enigma2/python/RTiTeam/busybox mkdosfs -F 32 ' + path) == 0

    
    def formatfat16(self, path):
        print 'Formatiram u FAT16'
        print path
        return os.system('/usr/lib/enigma2/python/RTiTeam/busybox mkfs.vfat ' + path) == 0

    
    def mkdir1(self):
        return os.system('mkdir /tmp/test0') == 0

    
    def mkdir3(self):
        return os.system('mkdir /tmp/test0/movie') == 0

    
    def mkdir4(self):
        return os.system('mkdir /tmp/test0/music') == 0

    
    def mkdir5(self):
        return os.system('mkdir /tmp/test0/picture') == 0

    
    def mkdir6(self):
        return os.system('rm -rf /tmp/test0') == 0

    
    def ListChange(self):
        if self.rereshenable == 1:
            return None
        if self.SelEn == 0 and len(self.partitions) > 0:
            self['list1'].selectionEnabled(0)
            self['list2'].selectionEnabled(1)
            self.SelEn = 1
            self.YellowPrint()
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
            self.YellowPrint()
        else:
            self['list1'].selectionEnabled(0)
            self['list2'].selectionEnabled(1)

    
    def keyUp(self):
        self['infoM4'].setText('Read disk speed: Not Tested Yet')
        self['infoM5'].setText('Read disk cache speed: Not Tested Yet')
        if self.SelEn == 0:
            self['list1'].up()
            self.VendorModel()
        
        if self.SelEn == 1:
            self['list2'].up()
            self.YellowPrint()
        

    
    def keyDown(self):
        self['infoM4'].setText('Read disk speed: Not Tested Yet')
        self['infoM5'].setText('Read disk cache speed: Not Tested Yet')
        if self.SelEn == 0:
            self['list1'].down()
            self.VendorModel()
        
        if self.SelEn == 1:
            self['list2'].down()
            self.YellowPrint()
        

    
    def Izlez(self):
        self.close()



class ChoiceMountPoint(Screen):
    skin = '\n\t\t<screen name="Menusimple2" position="center,center" size="230,355" title="HDD Onfo" >\n\t\t\t<!--widget name="text" position="0,0" size="550,25" font="Regular;20" /-->\n\t\t\t<!--widget name="pixmap" position="200,0" size="190,250" /-->\n\t\t\t<eLabel position="70,100" zPosition="-1" size="100,69" backgroundColor="#222222" />\n\t\t\t<widget name="list" position="15,35" size="200,300" scrollbarMode="showOnDemand" foregroundColor="#aaaaaa" />\n\t\t\t<widget name="infoA" position="15,15" zPosition="2" size="200,18" font="Regular;20" foregroundColor="#aaaaaa" transparent="1" halign="center" valign="center" />\n\t\t\t<widget name="info20" position="15,335" zPosition="2" size="200,18" font="Regular;20" foregroundColor="#aaaaaa" transparent="1" halign="center" valign="center" />\n\t\t</screen>'
    
    def __init__(self, session, pateka):
        self.skinName = 'OnlineManager2'
        Screen.__init__(self, session)
        self['actions'] = ActionMap([
            'OkCancelActions',
            'ColorActions',
            'DirectionActions'], {
            'ok': self.OkPress,
            'cancel': self.Izlaz1 }, -1)
        self.pateka = pateka
        self['list'] = MenuList([])
        self['info20'] = Label()
        self['infoA'] = Label()
        self.onLayoutFinish.append(self.openTest)

    
    def openTest(self):
        self['infoA'].setText('Select mountpoint:')
        self['info20'].setText('And press OK')
        self.mountpoints = []
        for mountpoint in listdir('/media'):
            if mountpoint == 'upnp':
                continue
            
            if mountpoint == 'ram':
                continue
            
            if mountpoint == 'net':
                continue
            
            if mountpoint == 'ram':
                continue
            
            if mountpoint == 'realroot':
                continue
            
            self.mountpoints.append(mountpoint)
        self.mountpoints.sort()
        self['list'].setList(self.mountpoints)

    
    def OkPress(self):
        sel = self['list'].getSelectionIndex()
        mountpoint = self.mountpoints[sel]
        self.close(mountpoint)

    
    def Izlaz1(self):
        self.close('---')



class ChoicePartitionNoType(Screen):
    skin = '\n\t\t<screen name="Menusimple2" position="center,center" size="230,355" title="HDD Onfo" >\n\t\t\t<!--widget name="text" position="0,0" size="550,25" font="Regular;20" /-->\n\t\t\t<!--widget name="pixmap" position="200,0" size="190,250" /-->\n\t\t\t<eLabel position="70,100" zPosition="-1" size="100,69" backgroundColor="#222222" />\n\t\t\t<widget name="list" position="15,65" size="200,300" scrollbarMode="showOnDemand" foregroundColor="#aaaaaa" />\n\t\t\t<widget name="infoA" position="15,15" zPosition="2" size="200,45" font="Regular;20" foregroundColor="#aaaaaa" transparent="1" halign="center" valign="center" />\n\t\t\t<widget name="info20" position="15,335" zPosition="2" size="200,18" font="Regular;20" foregroundColor="#aaaaaa" transparent="1" halign="center" valign="center" />\n\t\t</screen>'
    
    def __init__(self, session, podatok):
        self.skinName = 'OnlineManager2'
        Screen.__init__(self, session)
        self['actions'] = ActionMap([
            'OkCancelActions',
            'ColorActions',
            'DirectionActions'], {
            'ok': self.OkPress,
            'cancel': self.Izlaz1 }, -1)
        self.podatok = podatok
        self['list'] = MenuList([])
        self['info20'] = Label()
        self['infoA'] = Label()
        self.onLayoutFinish.append(self.openTest)

    
    def openTest(self):
        self.mountpoints = []
        if self.podatok == '111':
            self['infoA'].setText('Select No of partition:')
            self['info20'].setText('And press OK')
            self.mountpoints.append('1. 100%')
            self.mountpoints.append('2. 50% + 50%')
            self.mountpoints.append('3. 33% + 33% + 33%')
            self.mountpoints.sort()
        
        if self.podatok == '222':
            self['infoA'].setText('Select PartitionType:')
            self['info20'].setText('And press OK')
            self.mountpoints.append('1. EXT3')
            self.mountpoints.append('2. EXT2')
            self.mountpoints.append('3. FAT')
            self.mountpoints.sort()
        
        self['list'].setList(self.mountpoints)

    
    def OkPress(self):
        sel = self['list'].getSelectionIndex()
        mountpoint = self.mountpoints[sel][:1]
        self.close(mountpoint)

    
    def Izlaz1(self):
        self.close('---')



def main(session, **kwargs):
    session.open(HDDSetupScreen)


def Plugins(**kwargs):
    boxime = HardwareInfo().get_device_name()
    if boxime == 'elite' and boxime == 'premium' and boxime == 'premium+' and boxime == 'ultra' and boxime == 'me' and boxime == 'minime' or boxime == 'multimedia':
        return [
            PluginDescriptor(name = _('HDDSetup'), description = _('HDDSetup'), icon = 'HDDSetup.png', where = [
                PluginDescriptor.WHERE_EXTENSIONSMENU,
                PluginDescriptor.WHERE_PLUGINMENU], fnc = main)]
    return []

