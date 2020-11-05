#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from enigma import eConsoleAppContainer, iServiceInformation, eActionMap
from enigma import getDesktop
from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from Components.ActionMap import ActionMap
from Components.Button import Button
from Screens.MessageBox import MessageBox
import string
from time import gmtime, strftime, localtime, mktime, time, sleep
from datetime import datetime
from Components.config import configfile, getConfigListEntry, ConfigEnableDisable, ConfigYesNo, ConfigText, ConfigDateTime, ConfigClock, ConfigNumber, ConfigSelectionNumber, ConfigSelection, config, ConfigSubsection, ConfigSubList, ConfigSubDict, ConfigIP, ConfigSlider, ConfigDirectory
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from datetime import datetime
from Components.Timezones import timezones
import timer
import time
import math
from time import localtime, mktime, time, strftime
from datetime import timedelta
import os
from os import popen
config.plugins.TimeSet = ConfigSubsection()
config.plugins.TimeSet.OSDsize = ConfigSlider(default = 425, increment = 5, limits = (320, 500))
config.plugins.TimeSet.Helligkeit = ConfigSlider(default = 5, limits = (0, 7))
config.plugins.timezone = ConfigSubsection()
config.timezone = ConfigSubsection()
config.timezone.val = ConfigSelection(default = timezones.getDefaultTimezone(), choices = timezones.getTimezoneList())

class TimeSetConfig(ConfigListScreen, Screen):
    skin = '\n\t\t\t<screen position="center,center" size="560,190" title="TimeSet Settings v.1.2" >\n\t\t\t<widget name="config" position="10,10" size="540,50" scrollbarMode="showOnDemand" />\n\n\t\t\t<widget source="poraka" render="Label" position="5,265" size="555,30" zPosition="10" font="Regular;14" halign="center" valign="center" backgroundColor="#25062748" transparent="1" />\n\t\t\t<widget source="vreme" render="Label" position="5,65" size="555,30" zPosition="10" font="Regular;22" halign="center" valign="center" backgroundColor="#25062748" transparent="1" />\n\t\t\t<widget source="introduction" render="Label" position="5,95" size="555,30" zPosition="10" font="Regular;16" halign="center" valign="center" backgroundColor="#25062748" transparent="1" />\n\t\t\t<widget source="timez" render="Label" position="5,115" size="555,30" zPosition="10" font="Regular;16" halign="center" valign="center" backgroundColor="#25062748" transparent="1" />\n\t\t\t\n\t\t\t<widget name="key_red" position="0,150" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;18" transparent="1"/> \n\t\t\t<widget name="key_green" position="140,150" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;18" transparent="1"/> \n\t\t\t<widget name="key_yellow" position="280,150" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;18" transparent="1"/> \n\t\t\t<widget name="key_blue" position="420,150" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;18" transparent="1"/> \n\t\t\t\n\t\t\t<ePixmap name="red"    position="0,150"   zPosition="2" size="140,40" pixmap="buttons/red.png" transparent="1" alphatest="on" />\n\t\t\t<ePixmap name="green"  position="140,150" zPosition="2" size="140,40" pixmap="buttons/green.png" transparent="1" alphatest="on" />\n\t\t\t<ePixmap name="yellow" position="280,150" zPosition="2" size="140,40" pixmap="buttons/yellow.png" transparent="1" alphatest="on" />\n\t\t\t<ePixmap name="blue"   position="420,150" zPosition="2" size="140,40" pixmap="buttons/blue.png" transparent="1" alphatest="on" />\n\t\t</screen>'

    def __init__(self, session, args = 0):
        self.session = session
        Screen.__init__(self, session)
        z1 = mktime(datetime.utcnow().timetuple())
        z2 = mktime(datetime.now().timetuple())
        z0 = (z2 - z1) // 3600
        if z0 >= 0:
            zz = '+' + str(z0)[:1]

        if z0 < 0:
            zz = str(z0)[:2]

        config.plugins.TimeSet.NDate = ConfigDateTime(default = z1, formatstring = _('%d.%B %Y'), increment = 86400)
        config.plugins.TimeSet.UTCTim = ConfigClock(default = z1)
        self.list = []
        self.list1 = []
        self.list1.append(getConfigListEntry(_('UTC Time'), config.plugins.TimeSet.UTCTim))
        self.list1.append(getConfigListEntry(_('Date'), config.plugins.TimeSet.NDate))
        self.list2 = []
        self.list3 = []
        ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.selectionChanged)
        self['introduction'] = StaticText()
        self['vreme'] = StaticText()
        self['poraka'] = StaticText()
        self['timez'] = StaticText()
        self['key_red'] = Button(_('Exit'))
        self['key_green'] = Button(_('Set Time'))
        self['key_yellow'] = Button(_('Get iTime'))
        self['key_blue'] = Button('Get & Set')
        self['setupActions'] = ActionMap([
            'SetupActions',
            'ColorActions'], {
            'red': self.Update,
            'green': self.Update,
            'yellow': self.ZemiVreme,
            'blue': self.Page,
            'save': self.Update,
            'cancel': self.cancel,
            'ok': self.keyOK }, -1)
        self['config'].setList(self.list1)
        self.selectionChanged()


    def selectionChanged(self):
        self['introduction'].setText(_('Your time = UTC Time + Your Time Zone'))
        self['vreme'].setText(_('*Current Your Time: ' + str(datetime.now().strftime('%H:%M:%S'))))
        saat = str(config.plugins.TimeSet.UTCTim.value[0])
        if len(saat) < 2:
            saat = '0' + saat

        minuti = str(config.plugins.TimeSet.UTCTim.value[1])
        if len(minuti) < 2:
            minuti = '0' + minuti

        sekunde = strftime('%S', localtime())
        pp = config.plugins.TimeSet.NDate.value
        import time
        TimeString = time.strftime('%Y%m%d', time.gmtime(pp)) + saat + minuti + sekunde
        TimeZoneS = config.timezone.val.value
        ipos1 = TimeZoneS.find('(GMT')
        ipos2 = TimeZoneS.find(')')
        tmp = TimeZoneS[ipos1 + 4:ipos2]
        if len(tmp) == 0:
            tmp = '+00'

        tzpredznak = tmp[:1]
        tzvalue = str(int(tmp[1:3]))
        TimeString = TimeString + tzpredznak + tzvalue
        self['timez'].setText(_('Time Zone : ' + str(TimeZoneS)))
        self['poraka'].setText(_('TimeString : ' + str(TimeString)))
        novovreme = str(int(saat) + int(tzpredznak + tzvalue))
        if len(novovreme) < 2:
            novovreme = '0' + novovreme

        novovreme = novovreme + ':' + minuti
        self['vreme'].setText(_('Your Time (After Setting): ' + str(novovreme)))


    def Update(self):
        saat = str(config.plugins.TimeSet.UTCTim.value[0])
        if len(saat) < 2:
            saat = '0' + saat

        minuti = str(config.plugins.TimeSet.UTCTim.value[1])
        if len(minuti) < 2:
            minuti = '0' + minuti

        sekunde = strftime('%S', localtime())
        pp = config.plugins.TimeSet.NDate.value
        import time
        TimeString = time.strftime('%Y%m%d', time.gmtime(pp)) + saat + minuti + sekunde
        RTCString = time.strftime('%Y.%m.%d', time.gmtime(pp)) + '-' + saat + ':' + minuti + ':' + sekunde
        TimeZoneS = config.timezone.val.value
        ipos1 = TimeZoneS.find('(GMT')
        ipos2 = TimeZoneS.find(')')
        tmp = TimeZoneS[ipos1 + 4:ipos2]
        if len(tmp) == 0:
            tmp = '+00'

        tzpredznak = tmp[:1]
        tzvalue = str(int(tmp[1:3]))
        TimeString = TimeString + tzpredznak + tzvalue
        import os as os
        cmd = 'echo "' + str(TimeString) + '" > /proc/settime'
        os.system(cmd)
        cmd = 'date -u -s "' + str(RTCString) + '"'
        os.system(cmd)
        self.session.openWithCallback(self.callback, MessageBox, _('RTC Update done! \n\nGUI Clock Update done!'), type = 1, timeout = 5)


    def ZemiVreme(self):
        plugin_path = '/usr/lib/enigma2/python/RTiTeam/TimeSet'
        print(plugin_path)
        before = 'Before: Local=' + strftime('%H:%M', localtime()) + ', UTC=' + strftime('%H:%M', gmtime())
        cmd = str('ntpdate -t 20 0.debian.pool.ntp.org')
        res = popen(cmd).read()
        if res == '':
            cmd = 'ls -l %s%s' % (plugin_path, '/ntpdate')
            res = popen(cmd).read()
            if res[3] != 'x':
                cmd = 'chmod 755 %s%s' % ('ntpdate')
                res = popen(cmd).read()
                self.session.open(MessageBox, _('ntpdate problem: attributes for ntpdate have not been correct! Fixed now! Try again!\n%s' % res), MessageBox.TYPE_INFO)
            else:
                self.session.open(MessageBox, _('ntpdate problem: Internet connection ok? Time server ok?'), MessageBox.TYPE_INFO)
        else:
            self.session.open(MessageBox, _(before + '\n\nntpdate done! ' + res + '\nAfter: Local=' + strftime('%H:%M', localtime()) + ', UTC=' + strftime('%H:%M', gmtime())), type = 1, timeout = 5)
            z1 = mktime(datetime.utcnow().timetuple())
            config.plugins.TimeSet.NDate = ConfigDateTime(default = z1, formatstring = _('%d.%B %Y'), increment = 86400)
            config.plugins.TimeSet.UTCTim = ConfigClock(default = z1)
            self.list1 = []
            self.list1.append(getConfigListEntry(_('UTC Time'), config.plugins.TimeSet.UTCTim))
            self.list1.append(getConfigListEntry(_('Date'), config.plugins.TimeSet.NDate))
            self['config'].setList(self.list1)
            self.selectionChanged()


    def Page(self):
        plugin_path = '/usr/lib/enigma2/python/RTiTeam/TimeSet'
        print(plugin_path)
        before = 'Before: Local=' + strftime('%H:%M', localtime()) + ', UTC=' + strftime('%H:%M', gmtime())
        cmd = str('ntpdate -t 20 0.debian.pool.ntp.org')
        res = popen(cmd).read()
        if res == '':
            cmd = 'ls -l %s%s' % ('ntpdate')
            res = popen(cmd).read()
            if res[3] != 'x':
                cmd = 'chmod 755 %s%s' % ('ntpdate')
                res = popen(cmd).read()
                self.session.open(MessageBox, _('ntpdate problem: attributes for ntpdate have not been correct! Fixed now! Try again!\n%s' % res), MessageBox.TYPE_INFO)
            else:
                self.session.open(MessageBox, _('ntpdate problem: Internet connection ok? Time server ok?'), MessageBox.TYPE_INFO)
        else:
            z1 = mktime(datetime.utcnow().timetuple())
            config.plugins.TimeSet.NDate = ConfigDateTime(default = z1, formatstring = _('%d.%B %Y'), increment = 86400)
            config.plugins.TimeSet.UTCTim = ConfigClock(default = z1)
            self.list1 = []
            self.list1.append(getConfigListEntry(_('UTC Time'), config.plugins.TimeSet.UTCTim))
            self.list1.append(getConfigListEntry(_('Date'), config.plugins.TimeSet.NDate))
            self['config'].setList(self.list1)
            self.selectionChanged()
            saat = str(config.plugins.TimeSet.UTCTim.value[0])
            if len(saat) < 2:
                saat = '0' + saat

            minuti = str(config.plugins.TimeSet.UTCTim.value[1])
            if len(minuti) < 2:
                minuti = '0' + minuti

            sekunde = strftime('%S', localtime())
            pp = config.plugins.TimeSet.NDate.value
            import time
            TimeString = time.strftime('%Y%m%d', time.gmtime(pp)) + saat + minuti + sekunde
            RTCString = time.strftime('%Y.%m.%d', time.gmtime(pp)) + '-' + saat + ':' + minuti + ':' + sekunde
            TimeZoneS = config.timezone.val.value
            ipos1 = TimeZoneS.find('(GMT')
            ipos2 = TimeZoneS.find(')')
            tmp = TimeZoneS[ipos1 + 4:ipos2]
            if len(tmp) == 0:
                tmp = '+00'

            tzpredznak = tmp[:1]
            tzvalue = str(int(tmp[1:3]))
            TimeString = TimeString + tzpredznak + tzvalue
            import os
            cmd = 'echo "' + str(TimeString) + '" > /proc/settime'
            os.system(cmd)
            cmd = 'date -u -s "' + str(RTCString) + '"'
            os.system(cmd)
            self.session.openWithCallback(self.callback, MessageBox, _('RTC Update done! \n\nGUI Clock Update done!\n\n' + before + '\n\nntpdate done! ' + res + '\nAfter: Local=' + strftime('%H:%M', localtime()) + ', UTC=' + strftime('%H:%M', gmtime())), type = 1, timeout = 15)


    def keyOK(self):
        print('ok')


    def save(self):
        print('save')


    def cancel(self):
        self.close(True, self.session)



def TimeSetSetupMain(session, **kwargs):
    session.open(TimeSetConfig)


def startSetup(menuid):
    if menuid != 'system':
        return []
    return [
        (_('TimeSet'), TimeSetSetupMain, 'TimeSetSetupMain_setup', 49)]


def Plugins(path, **kwargs):
    global plugin_path
    plugin_path = path
    return [
        PluginDescriptor(name = 'TimeSet', description = 'Set DateTime to RTC', where = PluginDescriptor.WHERE_MENU, fnc = startSetup)]

