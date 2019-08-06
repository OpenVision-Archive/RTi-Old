from Screens.ChoiceBox import ChoiceBox
from Screens.Screen import Screen
from Components.ActionMap import ActionMap, NumberActionMap
from Components.MenuList import MenuList
from Components.Sources.List import List
from Components.FileList import FileList
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Plugins.Plugin import PluginDescriptor
from Components.Pixmap import Pixmap
from Tools import Notifications
from ServiceReference import ServiceReference
from Components.Button import Button
from Components.Label import Label
from Tools.LoadPixmap import LoadPixmap
import os
import urllib
from enigma import ePicLoad, eTimer, getDesktop
from Components.config import config, ConfigSubsection, ConfigInteger, ConfigSelection, ConfigText, ConfigEnableDisable, KEY_LEFT, KEY_RIGHT, KEY_0, getConfigListEntry
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Tools.HardwareInfo import HardwareInfo

class Getfolderlist(Screen):
    skin = '\n\t\t<screen name="OnlineManager0" position="center,center" size="632,400" title="Available Updates, Bootlogos, Skins..." >\n\t\t\t<ePixmap name="red"    position="10,360"   zPosition="2" size="160,40" pixmap="buttons/red.png" transparent="1" alphatest="on" />\n\t\t\t<ePixmap name="green"  position="165,360" zPosition="2" size="160,40" pixmap="buttons/green.png" transparent="1" alphatest="on" />\n\t\t\t<ePixmap name="yellow" position="320,360" zPosition="2" size="160,40" pixmap="buttons/yellow.png" transparent="1" alphatest="on" /> \n\t\t\t<ePixmap name="blue"   position="475,360" zPosition="2" size="160,40" pixmap="buttons/blue.png" transparent="1" alphatest="on" /> \n\t\t\t<widget name="key_red" position="10,360" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> \n\t\t\t<widget name="key_green" position="165,360" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> \n\t\t\t<widget name="key_yellow" position="320,360" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" />\n\t\t\t<widget name="key_blue" position="475,360" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" />\n\t\t\t<eLabel position="1,358" zPosition="-1" size="630,2" backgroundColor="#777777" />\n\n\t\t\t<widget name="list" position="240,50" size="370,255" scrollbarMode="showOnDemand" />\n\t\t\t<eLabel position="210,5" zPosition="-1" size="2,345" backgroundColor="#999999" />\n\t\t\t<widget name="info" position="230,310" zPosition="4" size="430,30" font="Regular;18" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />\n\t\t\t<widget name="thn" position="5,200" size="200,150" alphatest="on" />\n\t\t<widget name="opis" position="5,5" zPosition="4" size="200,150" font="Regular;18" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />\n\t\t</screen>'
    
    def __init__(self, session):
        self.session = session
        self.skin = Getfolderlist.skin
        self.skinName = 'OnlineManager0'
        Screen.__init__(self, session)
        self['actions'] = ActionMap([
            'OkCancelActions',
            'ColorActions',
            'DirectionActions'], {
            'ok': self.okClicked,
            'cancel': self.Izlaz,
            'red': self.openTestList,
            'green': self.okClicked,
            'yellow': self.KeyYellow,
            'blue': self.Izlaz,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.keyLeft,
            'right': self.keyRight }, -1)
        self['key_green'] = Button(_('Select'))
        self['key_blue'] = Button(_('Exit'))
        self['key_red'] = Button(_('List'))
        self['key_yellow'] = Button(_('UnInstall'))
        self['thn'] = Pixmap()
        self.list = []
        self['list'] = MenuList([])
        self['info'] = Label()
        self['opis'] = Label()
        self.icount = 0
        self.onLayoutFinish.append(self.openTestList)

    
    def openTestList(self):
        self['opis'].setText('Select group and then press OK or Red button.')
        
        try:
            self.slikanoname = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p0.png')
            self.slikaupdates = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p1.png')
            self.slikasettings = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p2.png')
            self.slikabootlogos = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p3.png')
            self.slikaskins = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p4.png')
            self.slikaplugins = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p5.png')
            self.slikapicons = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p6.png')
            self.slikatools = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p7.png')
            self.slikalanguage = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p8.png')
            self.slikacamds = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p9.png')
        except:
            self['info'].setText('Loading pixmap error !')

        self['info'].setText('Downloading list...')
        self.intgreska = 0
        xurl = 'http://www.azbox-enigma.eu/RTi_Update/folders'
        print 'xurl =', xurl
        xdest = '/tmp/folders'
        print 'xdest =', xdest
        
        try:
            xlist = urllib.urlretrieve(xurl, xdest)
            myfile = file('/tmp/folders')
            self.listfolder = []
            icount = 0
            list = []
            for line in myfile.readlines():
                if line[0:1] != '#':
                    self.listfolder.append(icount)
                    self.listfolder[icount] = line[:]
                    icount = icount + 1
                    continue
            self['info'].setText('')
            self['list'].setList(self.listfolder)
            cmd = 'rm -rf /tmp/folders &'
            os.system(cmd)
            self.vfdprint()
        except:
            self['info'].setText('Internet connection error !')
            self.intgreska = 1


    
    def Izlaz(self):
        self.close()

    
    def okClicked(self):
        sel = self['list'].getSelectionIndex()
        FolderName = self.listfolder[sel][:len(self.listfolder[sel]) - 2]
        self.session.open(Getipklist, FolderName)

    
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

    
    def vfdprint(self):
        sel = self['list'].getSelectionIndex()
        FolderName = self.listfolder[sel][:len(self.listfolder[sel]) - 2]
        
        try:
            self['thn'].instance.setPixmap(self.slikanoname)
            if FolderName == 'UPDATES':
                self['thn'].instance.setPixmap(self.slikaupdates)
            
            if FolderName == 'SETTINGS':
                self['thn'].instance.setPixmap(self.slikasettings)
            
            if FolderName == 'BOOTLOGOS':
                self['thn'].instance.setPixmap(self.slikabootlogos)
            
            if FolderName == 'SKINS':
                self['thn'].instance.setPixmap(self.slikaskins)
            
            if FolderName == 'PLUGINS':
                self['thn'].instance.setPixmap(self.slikaplugins)
            
            if FolderName == 'PICONS':
                self['thn'].instance.setPixmap(self.slikapicons)
            
            if FolderName == 'TOOLS':
                self['thn'].instance.setPixmap(self.slikatools)
            
            if FolderName == 'LANGUAGE':
                self['thn'].instance.setPixmap(self.slikalanguage)
            
            if FolderName == 'CAMDS':
                self['thn'].instance.setPixmap(self.slikacamds)
            
            self['thn'].show()
            os.system('echo "' + str(FolderName) + '" > /proc/vfd &')
        except:
            self['info'].setText('Error in show picture !')


    
    def KeyYellow(self):
        self.session.open(Ipkremove)



class Getipklist(Screen):
    skin = '\n\t\t<screen name="Menusimple2" position="center,center" size="632,400" title="Available Updates, Bootlogos, Skins..." >\n\t\t\t<ePixmap name="red"    position="10,360"   zPosition="2" size="160,40" pixmap="buttons/red.png" transparent="1" alphatest="on" />\n\t\t\t<ePixmap name="green"  position="165,360" zPosition="2" size="160,40" pixmap="buttons/green.png" transparent="1" alphatest="on" />\n\t\t\t<ePixmap name="yellow" position="320,360" zPosition="2" size="160,40" pixmap="buttons/yellow.png" transparent="1" alphatest="on" /> \n\t\t\t<ePixmap name="blue"   position="475,360" zPosition="2" size="160,40" pixmap="buttons/blue.png" transparent="1" alphatest="on" /> \n\t\t\t<widget name="key_red" position="10,360" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> \n\t\t\t<widget name="key_green" position="165,360" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> \n\t\t\t<widget name="key_yellow" position="320,360" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" />\n\t\t\t<widget name="key_blue" position="475,360" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" />\n\t\t\t<eLabel position="1,358" zPosition="-1" size="630,2" backgroundColor="#777777" />\n\n\t\t\t<widget name="list" position="230,40" size="430,275" scrollbarMode="showOnDemand" />\n\t\t\t<eLabel position="210,5" zPosition="-1" size="2,345" backgroundColor="#999999" />\n\t\t\t<widget name="info" position="210,310" zPosition="4" size="430,30" font="Regular;18" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />\n\t\t\t<widget name="thn" position="5,200" size="200,150" alphatest="on" />\n\t\t\t<widget name="opis" position="5,5" zPosition="4" size="200,150" font="Regular;18" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />\n\t\t\t<widget name="thn1" position="1,1" size="630,395" alphatest="on" />\n\t\t</screen>'
    
    def __init__(self, session, FolderName):
        self.session = session
        self.skinName = 'OnlineManager2'
        Screen.__init__(self, session)
        self['actions'] = ActionMap([
            'OkCancelActions',
            'ColorActions',
            'DirectionActions'], {
            'ok': self.okClicked,
            'cancel': self.Izlaz,
            'green': self.KeyGreen,
            'red': self.KeyRed,
            'blue': self.okClicked,
            'yellow': self.KeyYellow,
            'up': self.keyUp,
            'down': self.keyDown,
            'left': self.keyLeft,
            'right': self.keyRight }, -1)
        self['key_green'] = Button(_('Preview'))
        self['key_blue'] = Button(_('Download'))
        self['key_red'] = Button(_('List'))
        self['key_yellow'] = Button(_('UnInstall'))
        self['thn'] = Pixmap()
        self['thn1'] = Pixmap()
        self.list = []
        self['list'] = MenuList([])
        self['info'] = Label()
        self['opis'] = Label()
        self.icount = 0
        self.slikabezizmene = 0
        self.FolderName = FolderName
        self.onLayoutFinish.append(self.openTest)

    
    def GetInfo(self):
        if self.intgreska == 1:
            return None
        ipos = 0
        if self.slikabezizmene == 1:
            self['thn'].instance.setPixmap(self.slikafolder)
            self.slikabezizmene = 0
        
        self['thn'].show()
        self['thn1'].hide()
        self['opis'].show()
        self['list'].show()
        sel = self['list'].getSelectionIndex()
        
        try:
            self.praznalista = 0
            ListName = self.listname[sel]
        except:
            self.intgreska == 1
            self.praznalista = 1
            self['info'].setText('List is Empty !')
            self['opis'].setText('Press Exit button.')
            self['thn'].hide()
            return None

        os.system('echo "' + str(ListName) + '" > /proc/vfd &')
        ipk = self.names[sel]
        self['opis'].setText(self.namesexp[sel])
        itest1 = self.FolderName
        if self.FolderName != 'SKINS' and self.FolderName != 'BOOTLOGOS':
            return None
        self.slikabezizmene = 1
        ImeSlike = self.names[sel] + '_s.png'
        xurl1 = 'http://www.azbox-enigma.eu/RTi_Update/' + str(self.FolderName) + '/pixmap/'
        print 'xurl =', xurl1
        xurl2 = xurl1 + ImeSlike
        print 'xurl2 =', xurl2
        xdest2 = '/tmp/' + ImeSlike
        print 'xdest2 =', xdest2
        
        try:
            xlist = urllib.urlretrieve(xurl2, xdest2)
            self['info'].setText('')
            self['thn'].instance.setPixmapFromFile(resolveFilename(SCOPE_PLUGINS, str(xdest2)))
            self['thn'].show()
            self['thn1'].hide()
            self['opis'].show()
            self['list'].show()
            cmd = 'rm -rf ' + xdest2
            os.system(cmd)
        except:
            self.FolderName != 'BOOTLOGOS'
            self.intgreska == 1
            self['info'].setText('Internet connection error !')


    
    def KeyYellow(self):
        self.session.open(Ipkremove)

    
    def KeyGreen(self):
        if self.intgreska == 1:
            return None
        self['thn1'].instance.setPixmapFromFile(resolveFilename(SCOPE_PLUGINS, '/usr/lib/enigma2/python/RTiTeam/RTiUpdate/NoPrev.png'))
        self['thn1'].show()
        sel = self['list'].getSelectionIndex()
        if len(self.names) < 1:
            self['info'].setText('')
            self['thn'].hide()
            self['opis'].hide()
            self['list'].hide()
            return None
        ipk = self.names[sel]
        self['opis'].setText(self.namesexp[sel])
        ImeSlike = self.names[sel] + '.png'
        xurl1 = 'http://www.azbox-enigma.eu/RTi_Update/' + str(self.FolderName) + '/pixmap/'
        print 'xurl =', xurl1
        xurl2 = xurl1 + ImeSlike
        print 'xurl2 =', xurl2
        xdest2 = '/tmp/' + ImeSlike
        print 'xdest2 =', xdest2
        
        try:
            xlist = urllib.urlretrieve(xurl2, xdest2)
            self['info'].setText('')
            self['thn1'].instance.setPixmapFromFile(resolveFilename(SCOPE_PLUGINS, str(xdest2)))
            self['thn1'].show()
            self['thn'].hide()
            self['opis'].hide()
            self['list'].hide()
            cmd = 'rm -rf ' + xdest2
            os.system(cmd)
        except:
            len(self.names) < 1
            self.intgreska == 1
            self['info'].setText('Internet connection error !')


    
    def KeyRed(self):
        self['thn1'].hide()
        self['thn'].hide()
        self['opis'].hide()
        self['list'].show()
        self.openTest()
        self.GetInfo()

    
    def Izlaz(self):
        self.close()

    
    def nop(self):
        print ''

    
    def openTest(self):
        self.setTitle(_('Available ' + self.FolderName + ':'))
        
        try:
            self.slikafolder = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p0.png')
            if self.FolderName == 'UPDATES':
                self.slikafolder = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p1.png')
            
            if self.FolderName == 'SETTINGS':
                self.slikafolder = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p2.png')
            
            if self.FolderName == 'BOOTLOGOS':
                self.slikafolder = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p3.png')
            
            if self.FolderName == 'SKINS':
                self.slikafolder = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p4.png')
            
            if self.FolderName == 'PLUGINS':
                self.slikafolder = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p5.png')
            
            if self.FolderName == 'PICONS':
                self.slikafolder = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p6.png')
            
            if self.FolderName == 'TOOLS':
                self.slikafolder = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p7.png')
            
            if self.FolderName == 'LANGUAGE':
                self.slikafolder = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p8.png')
            
            if self.FolderName == 'CAMDS':
                self.slikafolder = LoadPixmap('/usr/lib/enigma2/python/RTiTeam/RTiUpdate/p9.png')
            
            self['thn'].instance.setPixmap(self.slikafolder)
            self['thn'].show()
        except:
            self['info'].setText('Error in load/show picture !')

        self['info'].setText('Downloading list...')
        self.intgreska = 0
        xurl = 'http://www.azbox-enigma.eu/RTi_Update/' + str(self.FolderName) + '/UpdList'
        print 'xurl =', xurl
        xdest = '/tmp/UpdLst'
        print 'xdest =', xdest
        
        try:
            xlist = urllib.urlretrieve(xurl, xdest)
            myfile = file('/tmp/UpdLst')
            self.data = []
            self.names = []
            self.namesexp = []
            self.listname = []
            icount = 0
            list = []
            for line in myfile.readlines():
                if line[0:1] != '#':
                    self.data.append(icount)
                    self.names.append(icount)
                    self.namesexp.append(icount)
                    self.listname.append(icount)
                    self.data[icount] = line[:]
                    ipkname = self.data[icount]
                    ipos = ipkname.find('<RTiL>')
                    remname = ipkname[:ipos]
                    ListName = ipkname[ipos + 6:len(ipkname) - 1]
                    ipos = ListName.find('<RTiD>')
                    explanation = ListName[ipos + 6:len(ListName) - 1]
                    ListName = ListName[:ipos]
                    self.namesexp[icount] = explanation
                    self.names[icount] = remname
                    self.listname[icount] = ListName
                    icount = icount + 1
                    continue
            self['info'].setText('')
            self['list'].setList(self.listname)
            cmd = 'rm -rf /tmp/UpdLst'
            os.system(cmd)
            self.GetInfo()
        except:
            self['info'].setText('Internet connection error !')
            self.intgreska = 1


    
    def okClicked(self):
        if self.intgreska == 1:
            return None
        if self.praznalista == 1:
            return None
        sel = self['list'].getSelectionIndex()
        ipk = self.names[sel]
        msg = 'Are you sure to want to install this update ?\n\n\n> ' + ipk + ' <\n\nDescription :\n\n' + self.namesexp[sel]
        self.session.openWithCallback(self.confirm, MessageBox, _(msg), MessageBox.TYPE_YESNO, timeout = 15, default = False)

    
    def confirm(self, confirmed):
        if confirmed:
            sel = self['list'].getSelectionIndex()
            ipk = self.names[sel]
            self.session.open(Getipk, ipk, self.FolderName)
        

    
    def keyLeft(self):
        self['list'].pageUp()
        self.GetInfo()

    
    def keyRight(self):
        self['list'].pageDown()
        self.GetInfo()

    
    def keyNumberGlobal(self, number):
        print 'pressed', number
        self['text'].number(number)

    
    def keyUp(self):
        self['list'].up()
        self.GetInfo()

    
    def keyDown(self):
        self['list'].down()
        self.GetInfo()

    
    def prikaziPic(self):
        print '*'



class Getipk(Screen):
    skin = '\n\t\t<screen position="center,center" size="600,480" title="Install status" >\n\t\t\t<!--widget name="text" position="0,0" size="550,25" font="Regular;20" /-->\n\t\t\t<widget name="list" position="10,0" size="630,400" scrollbarMode="showOnDemand" />\n\t\t\t<!--widget name="pixmap" position="200,0" size="190,250" /-->\n\t\t\t<eLabel position="70,100" zPosition="-1" size="100,69" backgroundColor="#222222" />\n\t\t\t<widget name="info" position="50,410" zPosition="4" size="500,60" font="Regular;22" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />\n\t\t</screen>'
    
    def __init__(self, session, ipk, FolderName):
        self.skin = Getipk.skin
        Screen.__init__(self, session)
        self['list'] = MenuList([])
        self['info'] = Label()
        self['actions'] = ActionMap([
            'OkCancelActions'], {
            'ok': self.okClicked,
            'cancel': self.close }, -1)
        self.icount = 0
        self.ipk = ipk
        self.FolderName = FolderName
        self.onLayoutFinish.append(self.openTest)

    
    def openTest(self):
        self['info'].setText('Downloading and installing...')
        xurl1 = 'http://www.azbox-enigma.eu/RTi_Update/' + str(self.FolderName) + '/'
        print 'xurl =', xurl1
        xurl2 = xurl1 + self.ipk
        print 'xurl2 =', xurl2
        xdest2 = '/tmp/' + self.ipk
        print 'xdest2 =', xdest2
        
        try:
            xlist = urllib.urlretrieve(xurl2, xdest2)
            self['info'].setText('')
            cmd = 'opkg install /tmp/' + self.ipk + '>/tmp/ipk_upd.log'
            os.system(cmd)
            self.viewLog()
        except:
            self['info'].setText('Internet connection error !')


    
    def keyLeft(self):
        self['text'].left()

    
    def keyRight(self):
        self['text'].right()

    
    def okClicked(self):
        self.close()

    
    def keyNumberGlobal(self, number):
        print 'pressed', number
        self['text'].number(number)

    
    def viewLog(self):
        print 'In viewLog'
        self['info'].setText('You must Reboot AZBox after Update,\nPress OK to continue...')
        if os.path.isfile('/tmp/ipk_upd.log') is not True:
            cmd = 'touch /tmp/ipk_upd.log'
            os.system(cmd)
        else:
            myfile = file('/tmp/ipk_upd.log')
            icount = 0
            data = []
            for line in myfile.readlines():
                data.append(icount)
                print line
                num = len(line)
                data[icount] = line[:-1]
                print data[icount]
                icount = icount + 1
            self['list'].setList(data)
            self.endinstall()

    
    def endinstall(self):
        path = '/tmp'
        tmplist = []
        ipkname = 0
        tmplist = os.listdir(path)
        print 'files in /tmp', tmplist
        icount = 0
        for name in tmplist:
            nipk = tmplist[icount]
            if nipk[-3:] == 'ipk':
                ipkname = nipk
            
            icount = icount + 1
        if ipkname != 0:
            print 'ipk name =', ipkname
            ipos = ipkname.find('_')
            remname = ipkname[:ipos]
            print 'remname =', remname
            f = open('/etc/ipklist_installed', 'a')
            f1 = remname + '\n'
            f.write(f1)
            cmd = 'rm /tmp/*.ipk'
            os.system(cmd)
        

    
    def confirmR(self, confirmed):
        if confirmed:
            cmd = 'reboot -f'
            os.system(cmd)
            self.close()
        



class Ipkremove(Screen):
    skin = '\n\t\t<screen position="100,100" size="550,400" title="Ipkremove" >\n\t\t\t<!--widget name="text" position="0,0" size="550,25" font="Regular;20" /-->\n\t\t\t<widget name="list" position="10,0" size="190,250" scrollbarMode="showOnDemand" />\n\t\t\t<widget name="pixmap" position="200,0" size="190,250" />\n\t\t</screen>'
    
    def __init__(self, session, args = None):
        self.skin = Ipkremove.skin
        Screen.__init__(self, session)
        self['list'] = FileList('/', matchingPattern = '^.*\\.(png|avi|mp3|mpeg|ts)')
        self['pixmap'] = Pixmap()
        self['actions'] = NumberActionMap([
            'WizardActions',
            'InputActions'], {
            'ok': self.ok,
            'back': self.close,
            'left': self.keyLeft,
            'right': self.keyRight,
            '1': self.keyNumberGlobal,
            '2': self.keyNumberGlobal,
            '3': self.keyNumberGlobal,
            '4': self.keyNumberGlobal,
            '5': self.keyNumberGlobal,
            '6': self.keyNumberGlobal,
            '7': self.keyNumberGlobal,
            '8': self.keyNumberGlobal,
            '9': self.keyNumberGlobal,
            '0': self.keyNumberGlobal }, -1)
        self.onShown.append(self.openTest)

    
    def openTest(self):
        
        try:
            myfile = open('/etc/ipklist_installed', 'r+')
            icount = 0
            data = []
            ebuf = []
            for line in myfile:
                data.append(icount)
                data[icount] = (_(line), '')
                ebuf.append(data[icount])
                icount = icount + 1
            myfile.close()
            ipkres = self.session.openWithCallback(self.test2, ChoiceBox, title = 'Please select ipkg to remove', list = ebuf)
            self.close()
        except:
            self.close()


    
    def test2(self, returnValue):
        if returnValue is None:
            return None
        print 'returnValue', returnValue
        nos = len
        emuname = ''
        ipkname = returnValue[0]
        print 'ipkname =', ipkname
        cmd = 'opkg remove ' + ipkname[:-1] + ' >/tmp/ipk_upd.log'
        print cmd
        os.system(cmd)
        cmd = 'touch /etc/tmpfile'
        os.system(cmd)
        myfile = open('/etc/ipklist_installed', 'r')
        f = open('/etc/tmpfile', 'w')
        icount = 0
        for line in myfile:
            if line != ipkname:
                print 'myfile line=', line
                f.write(line)
                continue
            returnValue is None
        f.close()
        f = open('/etc/tmpfile', 'r+')
        f2 = f.readlines()
        print '/etc/tmpfile', f2
        f.close()
        f = open('/etc/ipklist_installed', 'r+')
        f2 = f.readlines()
        print '/etc/ipklist_installed', f2
        f.close()
        cmd = 'rm /etc/ipklist_installed'
        os.system(cmd)
        cmd = 'mv /etc/tmpfile /etc/ipklist_installed'
        os.system(cmd)
        f = open('/etc/ipklist_installed', 'r+')
        f2 = f.readlines()
        print '/etc/ipklist_installed 2', f2
        f.close()
        return None

    
    def callback(self, answer):
        print 'answer:', answer

    
    def keyLeft(self):
        self['text'].left()

    
    def keyRight(self):
        self['text'].right()

    
    def ok(self):
        selection = self['list'].getSelection()
        if selection[1] == True:
            self['list'].changeDir(selection[0])
        else:
            self['pixmap'].instance.setPixmapFromFile(selection[0])

    
    def keyNumberGlobal(self, number):
        print 'pressed', number
        self['text'].number(number)



def mainmenu(session, **kwargs):
    session.open(Getfolderlist)


def autostart(reason, session = None, **kwargs):
    print '[Updater] Started'


def Plugins(**kwargs):
    boxime = HardwareInfo().get_device_name()
    if boxime == 'elite' and boxime == 'premium' and boxime == 'premium+' and boxime == 'ultra' and boxime == 'me' or boxime == 'minime':
        return [
            PluginDescriptor(name = _('RTi Updates, Bootlogos and Skins'), description = 'Online Update/Install Bootlogos and Skins', where = [
                PluginDescriptor.WHERE_EXTENSIONSMENU,
                PluginDescriptor.WHERE_PLUGINMENU], fnc = mainmenu)]
    return []

