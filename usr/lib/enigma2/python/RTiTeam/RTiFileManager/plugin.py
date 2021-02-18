#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from Plugins.Plugin import PluginDescriptor
from Components.config import config, ConfigSubList, ConfigSubsection, ConfigInteger, ConfigYesNo, ConfigText, getConfigListEntry
from Components.FileList import FileList
from Components.ConfigList import ConfigListScreen
from Screens.Console import Console
from Screens.ChoiceBox import ChoiceBox
from Screens.InputBox import InputBox
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Scanner import openFile
from os.path import isdir as os_path_isdir
from mimetypes import guess_type
import os.path as os
import stat
import sys
import os
import string
from Tools.HardwareInfo import HardwareInfo
from enigma import eTimer
from Components.MenuList import MenuList
from Components.Sources.List import List
pname = _('RTi FileManager')
pdesc = _('File Manager')
config.plugins.RTiFileManager = ConfigSubsection()
config.plugins.RTiFileManager.savedirs = ConfigYesNo(default=True)
config.plugins.RTiFileManager.add_mainmenu_entry = ConfigYesNo(default=True)
config.plugins.RTiFileManager.add_extensionmenu_entry = ConfigYesNo(default=True)
config.plugins.RTiFileManager.path_left = ConfigText(default='/')
config.plugins.RTiFileManager.path_right = ConfigText(default='/')

class RTiFileManagerScreen(Screen):
    skin = '\n\t\t<screen position="center,center" size="720,495" title="">\n\t\t\t<widget name="list_left" position="0,45" size="356,370" scrollbarMode="showOnDemand" />\n\t\t\t<widget name="list_right" position="364,45" size="356,370" scrollbarMode="showOnDemand" />\n\n\t\t\t<widget name="red" position="20,456" size="140,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="green" position="200,456" size="140,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="yellow" position="380,456" size="140,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="blue" position="560,456" size="140,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\n\t\t\t<ePixmap name="pred" position="20,455" size="140,30" zPosition="0" pixmap="buttons/red.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pgreen" position="200,455" size="140,30" zPosition="0" pixmap="buttons/green.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pyellow" position="380,455" size="140,30" zPosition="0" pixmap="buttons/yellow.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pblue" position="560,455" size="140,30" zPosition="0" pixmap="buttons/blue.png" transparent="1" alphatest="on"/>\n\t\t\t<widget name="infoA" position="10,430" zPosition="2" size="700,18" font="Regular;20" foregroundColor="#aaaaaa" transparent="1" halign="center" valign="center" />\n\t\t\t<widget name="infoB" position="10,25" zPosition="2" size="350,18" font="Regular;15" foregroundColor="#aaaaaa" transparent="1" halign="center" valign="center" />\n\t\t\t<widget name="infoC" position="360,25" zPosition="2" size="350,18" font="Regular;15" foregroundColor="#aaaaaa" transparent="1" halign="center" valign="center" />\n\t\t\t<widget name="infoD" position="10,5" zPosition="2" size="700,15" font="Regular;15" foregroundColor="#aaaaaa" transparent="1" halign="center" valign="center" />\n\t\t\t<eLabel position="361,45" zPosition="-1" size="3,370" backgroundColor="#999999" />\n\t\t</screen>'

    def __init__(self, session, path_left=None):
        if path_left is None:
            if os_path_isdir(config.plugins.RTiFileManager.path_left.value) and config.plugins.RTiFileManager.savedirs.value:
                path_left = config.plugins.RTiFileManager.path_left.value
            else:
                path_left = '/'

        if os_path_isdir(config.plugins.RTiFileManager.path_right.value) and config.plugins.RTiFileManager.savedirs.value:
            path_right = config.plugins.RTiFileManager.path_right.value
        else:
            path_right = '/'
        self.session = session
        Screen.__init__(self, session)
        self['list_left'] = FileList(path_left, matchingPattern='^.*')
        self['list_right'] = FileList(path_right, matchingPattern='^.*')
        self['red'] = Label(_('Delete'))
        self['green'] = Label(_('Attributes'))
        self['yellow'] = Label(_('Copy'))
        self['blue'] = Label(_('Rename'))
        self['actions'] = ActionMap([
            'ChannelSelectBaseActions',
            'WizardActions',
            'DirectionActions',
            'MenuActions',
            'NumberActions',
            'ColorActions'], {
            'ok': self.ok,
            'back': self.exit,
            'nextMarker': self.listRight,
            'prevMarker': self.listLeft,
            'up': self.goUp,
            'down': self.goDown,
            'left': self.goLeft,
            'right': self.goRight,
            'red': self.goRed,
            'green': self.goGreen,
            'yellow': self.goYellow,
            'blue': self.goBlue,
            '0': self.doRefresh,
            '1': self.doView,
            '2': self.doMKFile,
            '3': self.doMKDir}, -1)
        self.onLayoutFinish.append(self.listLeft)
        self['infoA'] = Label()
        self['infoB'] = Label()
        self['infoC'] = Label()
        self['infoD'] = Label()
        self.setTitle('RTi FileManager   v.1.0')
        self.strana = 1
        self.msgno = 0
        self.msgTimer = eTimer()
        self.msgTimer.callback.append(self.updateMsg)
        self.msgTimer.start(1000, True)


    def updateMsg(self):
        self.msgno = self.msgno + 1
        if self.msgno == 1:
            self['infoA'].setText('Use buttons : |<< and >>| to switch left/right browser.')

        if self.msgno == 2:
            self['infoA'].setText("Press Button '0' to refresh.")

        if self.msgno == 3:
            self['infoA'].setText("Press Button '1' to View & Edit File.")

        if self.msgno == 4:
            self['infoA'].setText("Press Button '2' to Create a File.")

        if self.msgno == 5:
            self['infoA'].setText("Press Button '3' to Create a Directory.")

        if self.msgno > 4:
            self.msgno = 0

        self.msgTimer.start(3000, True)


    def exit(self):
        if self['list_left'].getCurrentDirectory() and config.plugins.RTiFileManager.savedirs.value:
            config.plugins.RTiFileManager.path_left.value = self['list_left'].getCurrentDirectory()
            config.plugins.RTiFileManager.path_left.save()

        if self['list_right'].getCurrentDirectory() and config.plugins.RTiFileManager.savedirs.value:
            config.plugins.RTiFileManager.path_right.value = self['list_right'].getCurrentDirectory()
            config.plugins.RTiFileManager.path_right.save()

        self.close()


    def ok(self):
        if self.SOURCELIST.canDescent():
            self.SOURCELIST.descent()
            if self.SOURCELIST.getCurrentDirectory():
                aaa = self.SOURCELIST.getCurrentDirectory()
                if len(aaa) > 40:
                    aaa = '...' + aaa[len(aaa) - 40:]

                if self.strana == 1:
                    self['infoB'].setText(aaa)

                if self.strana == 2:
                    self['infoC'].setText(aaa)

            else:
                self.onFileAction()



    def goLeft(self):
        self.SOURCELIST.pageUp()


    def goRight(self):
        self.SOURCELIST.pageDown()


    def goUp(self):
        self.SOURCELIST.up()
        self.GetCHMod()


    def goDown(self):
        self.SOURCELIST.down()
        self.GetCHMod()


    def GetCHMod(self):
        filename = self.SOURCELIST.getFilename()
        LL = 0
        LLp = 0
        LLk = 0

        try:
            if os.path.isdir(self.SOURCELIST.getFilename()) == True:
                pattern = self.SOURCELIST.getFilename()
            else:
                pattern = self.SOURCELIST.getCurrentDirectory() + self.SOURCELIST.getFilename()
            findResults = []
            findResults.append(pattern)
            self['infoD'].setText('Attributes: ')
            self.fileright = 0
            for file in findResults:
                mode = stat.S_IMODE(os.lstat(file)[stat.ST_MODE])
                for level in ('USR', 'GRP', 'OTH'):
                    for perm in ('R', 'W', 'X'):
                        if mode & getattr(stat, 'S_I' + perm + level):
                            if perm == 'R':
                                LLp = 4

                            if perm == 'W':
                                LLp = 2

                            if perm == 'X':
                                LLp = 1

                        else:
                            LLp = 0
                        if level == 'USR':
                            LLk = 100

                        if level == 'GRP':
                            LLk = 10

                        if level == 'OTH':
                            LLk = 1

                        if perm == 'R':
                            LL = LL + LLp * LLk

                        if perm == 'W':
                            LL = LL + LLp * LLk

                        if perm == 'X':
                            LL = LL + LLp * LLk
                            continue
        except:
            pass

        self['infoD'].setText('Attributes: ' + str(LL))
        self.fileright = LL


    def goYellow(self):
        filename = self.SOURCELIST.getFilename()
        sourceDir = self.SOURCELIST.getCurrentDirectory()
        targetDir = self.TARGETLIST.getCurrentDirectory()

        try:
            if os.path.isdir(filename) == True:
                self.session.openWithCallback(self.doCopyDir, ChoiceBox, title=_('Do you really want to copy directory: ') + '%s ?\nfrom: %s\nto: %s' % (filename, sourceDir, targetDir), list=[
                    (_('yes'), True),
                    (_('no'), False)])
            else:
                self.session.openWithCallback(self.doCopy, ChoiceBox, title=_('Do you really want to copy file: ') + '%s ?\nfrom: %s\nto: %s' % (filename, sourceDir, targetDir), list=[
                    (_('yes'), True),
                    (_('no'), False)])
        except:
            pass



    def doCopy(self, result):
        if result is not None:
            if result[1]:
                filename = self.SOURCELIST.getFilename()
                sourceDir = self.SOURCELIST.getCurrentDirectory()
                targetDir = self.TARGETLIST.getCurrentDirectory()
                src = self.SOURCELIST.getCurrentDirectory() + self.SOURCELIST.getFilename()
                dst = self.TARGETLIST.getCurrentDirectory()
                self.session.openWithCallback(self.callback, MessageBox, _('Copying...'), type=1, timeout=1)
                shutil.copy2(src, dst)
                self.doRefresh()




    def doCopyDir(self, result):
        if result is not None:
            if result[1]:
                self.session.openWithCallback(self.callback, MessageBox, _('Copying ...'), type=1, timeout=1)
                symlinks = False
                aaa = self.SOURCELIST.getCurrentDirectory()
                src = self.SOURCELIST.getFilename()
                bbb = src[len(aaa):]
                dst = self.TARGETLIST.getCurrentDirectory() + bbb
                names = os.listdir(src)

                try:
                    os.makedirs(dst)
                except:
                    pass

                errors = []
                for name in names:
                    srcname = os.path.join(src, name)
                    dstname = os.path.join(dst, name)

                    try:
                        if symlinks and os.path.islink(srcname):
                            linkto = os.readlink(srcname)
                            os.symlink(linkto, dstname)
                        elif os.path.isdir(srcname):
                            shutil.copytree(srcname, dstname, symlinks)
                        else:
                            shutil.copy2(srcname, dstname)
                    except (IOError, os.error):
                        why = None
                        errors.append((srcname, dstname, str(why)))
                        continue



                try:
                    copystat(src, dst)
                except:
                    pass

                self.doRefresh()




    def doCopyCB(self):
        self.doRefresh()


    def goRed(self):
        if os.path.isdir(self.SOURCELIST.getFilename()) == True:
            pattern = self.SOURCELIST.getFilename()
        else:
            pattern = self.SOURCELIST.getCurrentDirectory() + self.SOURCELIST.getFilename()
        self.session.openWithCallback(self.doDelete, MessageBox, _('Are you sure you want to delete : ' + str(pattern)), MessageBox.TYPE_YESNO, timeout=20, default=False)


    def doDelete(self, result):
        if result:
            if os.path.isdir(self.SOURCELIST.getFilename()) == True:
                pattern = self.SOURCELIST.getFilename()
                for root, dirs, files in os.walk(pattern, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(pattern)
            else:
                pattern = self.SOURCELIST.getCurrentDirectory() + self.SOURCELIST.getFilename()
                os.remove(pattern)
            self.doRefresh()



    def doDelete0(self, result):
        if result is not None:
            if result[1]:
                filename = self.SOURCELIST.getFilename()
                sourceDir = self.SOURCELIST.getCurrentDirectory()
                self.session.openWithCallback(self.doDeleteCB, Console, title=_('executing file ...'), cmdlist=[
                    '"' + sourceDir + filename + '"'])




    def doDeleteCB(self):
        self.doRefresh()


    def doView(self):

        try:
            if os.path.isdir(self.SOURCELIST.getFilename()) == True:
                pattern = self.SOURCELIST.getFilename()
            else:
                pattern = self.SOURCELIST.getCurrentDirectory() + self.SOURCELIST.getFilename()
            self.session.open(SubView, str(pattern))
        except:
            pass



    def goGreen(self):
        self.GetCHMod()
        if os.path.isdir(self.SOURCELIST.getFilename()) == True:
            pattern = self.SOURCELIST.getFilename()
        else:
            pattern = self.SOURCELIST.getCurrentDirectory() + self.SOURCELIST.getFilename()
        self.session.open(SubAtributes, str(pattern), str(self.fileright))
        self.GetCHMod()


    def doCHMod(self, chmod):
        if chmod:
            if os.path.isdir(self.SOURCELIST.getFilename()) == True:
                pattern = self.SOURCELIST.getFilename()
            else:
                pattern = self.SOURCELIST.getCurrentDirectory() + self.SOURCELIST.getFilename()
            chmod = int(str(chmod), 10)
            if chmod > 777:
                chmod == 777

            if chmod < 0:
                chmod == 0

            os.chmod(pattern, int(str(chmod), 8))
            self.GetCHMod()



    def doMove(self, result):
        if result is not None:
            if result[1]:
                filename = self.SOURCELIST.getFilename()
                sourceDir = self.SOURCELIST.getCurrentDirectory()
                targetDir = self.TARGETLIST.getCurrentDirectory()
                self.session.openWithCallback(self.doMoveCB, Console, title=_('unzip file ...'), cmdlist=[
                    'tar zxvf "' + sourceDir + filename + '" -C "' + targetDir + '"'])




    def doMoveCB(self):
        self.doRefresh()


    def goBlue(self):
        filename = self.SOURCELIST.getFilename()
        sourceDir = self.SOURCELIST.getCurrentDirectory()
        if os.path.isdir(self.SOURCELIST.getFilename()) == False:
            self.session.openWithCallback(self.doRename, InputBox, text=filename, title=filename, windowTitle=_('Rename file'))
        else:
            dirname = os.path.dirname(filename)[len(sourceDir):]
            self.session.openWithCallback(self.doRenameDir, InputBox, text=dirname, title=dirname, windowTitle=_('Rename file'))


    def doRename(self, newname):
        if newname:
            src = self.SOURCELIST.getCurrentDirectory() + self.SOURCELIST.getFilename()
            dst = self.SOURCELIST.getCurrentDirectory() + newname

            try:
                os.rename(src, dst)
            except:
                pass

            self.doRefresh()



    def doRenameDir(self, newname):
        if newname:
            src = self.SOURCELIST.getFilename()
            dst = self.SOURCELIST.getCurrentDirectory() + newname

            try:
                os.rename(src, dst)
            except:
                pass

            self.doRefresh()



    def doMKDir(self):
        self.session.openWithCallback(self.doMKDir1, InputBox, text='', title='Enter Name of New Dir :', windowTitle=_('Make Directory'))


    def doMKDir1(self, newname):
        if newname:
            newdir = self.SOURCELIST.getCurrentDirectory() + newname

            try:
                os.mkdir(newdir)
            except:
                pass

            self.doRefresh()



    def doMKFile(self):
        self.session.openWithCallback(self.doMKFile1, InputBox, text='', title='Enter Name of New File :', windowTitle=_('Make File'))


    def doMKFile1(self, newname):
        if newname:
            newfile = self.SOURCELIST.getCurrentDirectory() + newname

            try:
                if os.path.exists(newfile) == False:
                    open(newfile, 'w').close()
            except:
                pass

            self.doRefresh()



    def doRefresh(self):
        self.SOURCELIST.refresh()
        self.TARGETLIST.refresh()
        self.GetCHMod()


    def listRight(self):
        self['list_left'].selectionEnabled(0)
        self['list_right'].selectionEnabled(1)
        self.SOURCELIST = self['list_right']
        self.TARGETLIST = self['list_left']
        aaa = self.SOURCELIST.getCurrentDirectory()
        if len(aaa) > 40:
            aaa = '...' + aaa[len(aaa) - 40:]

        self['infoC'].setText(aaa)
        self.strana = 2
        self.GetCHMod()


    def listLeft(self):
        self['infoA'].setText('Use buttons : |<< and >>| to switch left/right browser.')
        self['list_left'].selectionEnabled(1)
        self['list_right'].selectionEnabled(0)
        self.SOURCELIST = self['list_left']
        self.TARGETLIST = self['list_right']
        aaa = self.SOURCELIST.getCurrentDirectory()
        if len(aaa) > 40:
            aaa = '...' + aaa[len(aaa) - 40:]

        self['infoB'].setText(aaa)
        self.strana = 1
        self.GetCHMod()


    def onFileAction(self):

        try:
            x = openFile(self.session, guess_type(self.SOURCELIST.getFilename())[0], self.SOURCELIST.getCurrentDirectory() + self.SOURCELIST.getFilename())
            print('RESULT OPEN FILE', x)
        except TypeError:
            e = None
            print('ok')




class SubAtributes(Screen):
    skin = '\n\t\t<screen position="center,center" size="560,110" title="">\n\t\t\t<widget name="red" position="0,80" size="140,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="green" position="140,80" size="140,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="yellow" position="280,80" size="140,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="blue" position="420,80" size="140,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\n\t\t\t<ePixmap name="pred" position="0,80" size="140,30" zPosition="0" pixmap="buttons/red.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pgreen" position="140,80" size="140,30" zPosition="0" pixmap="buttons/green.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pyellow" position="280,80" size="140,30" zPosition="0" pixmap="buttons/yellow.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pblue" position="420,80" size="140,30" zPosition="0" pixmap="buttons/blue.png" transparent="1" alphatest="on"/>\n\t\t\t<widget name="infoA" position="10,5" zPosition="2" size="540,18" font="Regular;18" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />\n\t\t\t<widget name="infoB" position="10,25" zPosition="2" size="540,18" font="Regular;18" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />\n\t\t\t<widget name="infoC" position="10,55" zPosition="2" size="540,18" font="Regular;16" foregroundColor="#888888" transparent="1" halign="center" valign="center" />\n\t\t</screen>'

    def __init__(self, session, pateka, fileright):
        self.session = session
        Screen.__init__(self, session)
        self['red'] = Label(_('600'))
        self['green'] = Label(_('644'))
        self['yellow'] = Label(_('755'))
        self['blue'] = Label(_('777'))
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
        self['infoA'] = Label()
        self['infoB'] = Label()
        self['infoC'] = Label()
        self.setTitle('RTi FileManager   v.1.0')
        self.pateka = pateka
        self.fileright = fileright
        self.onLayoutFinish.append(self.openTest)


    def openTest(self):
        self['infoA'].setText('Filename : ' + str(self.pateka))
        self['infoB'].setText('Current Attributes : ' + str(self.fileright))
        self['infoC'].setText('Please choose one of coloured buttons , to change attributes.')


    def doCHMod(self, chmod):
        if chmod:
            chmod = int(str(chmod), 10)
            if chmod > 777:
                chmod == 777

            if chmod < 0:
                chmod == 0

            os.chmod(self.pateka, int(str(chmod), 8))
            self.close()



    def ok(self):
        print('ok')


    def exit(self):
        self.close()


    def goRed(self):
        self.doCHMod(600)


    def goGreen(self):
        self.doCHMod(644)


    def goYellow(self):
        self.doCHMod(755)


    def goBlue(self):
        self.doCHMod(777)



class SubView(Screen):
    skin = '\n\t\t<screen position="center,center" size="720,495" title="">\n\t\t\t<widget name="red" position="20,456" size="140,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="green" position="200,456" size="140,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="yellow" position="380,456" size="140,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\t\t\t<widget name="blue" position="560,456" size="140,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>\n\n\t\t\t<ePixmap name="pred" position="20,455" size="140,30" zPosition="0" pixmap="buttons/red.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pgreen" position="200,455" size="140,30" zPosition="0" pixmap="buttons/green.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pyellow" position="380,455" size="140,30" zPosition="0" pixmap="buttons/yellow.png" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="pblue" position="560,455" size="140,30" zPosition="0" pixmap="buttons/blue.png" transparent="1" alphatest="on"/>\n\t\t\t<widget name="infoA" position="10,5" zPosition="2" size="700,18" font="Regular;18" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />\n\t\t\t<widget name="list" position="10,30" size="710,405" scrollbarMode="showOnDemand" foregroundColor="#aaaaaa" />\n\t\t</screen>'

    def __init__(self, session, pateka):
        self.session = session
        Screen.__init__(self, session)
        self['red'] = Label(_('Edit Line'))
        self['green'] = Label(_('Save'))
        self['yellow'] = Label(_(' '))
        self['blue'] = Label(_('Exit'))
        self['actions'] = ActionMap([
            'ChannelSelectBaseActions',
            'WizardActions',
            'DirectionActions',
            'MenuActions',
            'NumberActions',
            'ColorActions'], {
            'back': self.exit,
            'ok': self.doEdit,
            'red': self.doEdit,
            'green': self.doSave,
            'yellow': self.exit,
            'blue': self.exit}, -1)
        self['infoA'] = Label()
        self.setTitle('RTi FileManager   v.1.0')
        self.pateka = pateka
        self.encname = []
        self['list'] = MenuList(self.encname)
        self.onLayoutFinish.append(self.openTest)


    def openTest(self):
        self['infoA'].setText('Filename : ' + str(self.pateka))

        try:
            sfile = open(str(self.pateka), 'r')
            for line in sfile:
                self.encname.append(line)
            self['list'].setList(self.encname)
        except Exception:
            return None



    def exit(self):
        self.close()


    def doEdit(self):
        sel = self['list'].getSelectionIndex()
        self.session.openWithCallback(self.doEdit1, InputBox, text=str(self.encname[sel]), title='Use |<< , >>| to del , back', windowTitle=_('Edit Line'))


    def doEdit1(self, res):
        if res:
            sel = self['list'].getSelectionIndex()
            self.encname[sel] = res
            self['list'].setList(self.encname)



    def doSave(self):
        self.session.openWithCallback(self.doSave1, MessageBox, _('Are you sure you want to save changes in file : ' + str(self.pateka)), MessageBox.TYPE_YESNO, timeout=20, default=False)


    def doSave1(self, result):
        if result is not None:

            try:
                sfile = open(str(self.pateka), 'w')
                for line in self.encname:
                    sfile.write(line)
            except Exception:
                return None





def main(session, **kwargs):
    session.open(RTiFileManagerScreen)


def Plugins(**kwargs):
    boxime = HardwareInfo().get_device_name()
    if boxime == 'elite' and boxime == 'premium' and boxime == 'premium+' and boxime == 'ultra' and boxime == 'me' and boxime == 'minime' or boxime == 'multimedia':
        return [
            PluginDescriptor(name=_('RTi FileManager'), description=_('FileManager'), icon='FileManager.png', where=[
                PluginDescriptor.WHERE_EXTENSIONSMENU,
                PluginDescriptor.WHERE_PLUGINMENU], fnc=main)]
    return []

