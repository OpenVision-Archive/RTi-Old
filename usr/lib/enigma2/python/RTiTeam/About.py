#!/usr/bin/python
# -*- coding: utf-8 -*-
from enigma import *
from Screens.Screen import Screen
from Components.Button import Button
from Components.Label import Label
from Components.ActionMap import ActionMap


class AboutTeam(Screen):
    skin = '\n\t\t<screen position="center,center" size="210,430" title="About" >\n\t\t<widget name="about" position="5,10" zPosition="4" size="200,400" font="Regular;18" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />\n\t\t</screen>'

    def __init__(self, session, args=0):
        Screen.__init__(self, session)
        abouttxt = 'Many thanks to all developers :\n- The-Ripper\n- telesat\n- MickeySa\n- Thempra\n- joseba\n- sattomy\n\nand betatesters:\n- Roger_Rabbit\n- Dona\n- BEBI\n- dvlajkovic\n- nenadx\n- looney\n- kultor\n- green1975\n- Nalbantic\n'
        self['about'] = Label(abouttxt)
        self['key_green'] = Button('')
        self['key_red'] = Button('')
        self['key_blue'] = Button(_('Exit'))
        self['key_yellow'] = Button('')
        self['actions'] = ActionMap([
            'OkCancelActions',
            'ColorActions'], {
            'blue': self.quit,
            'ok': self.quit,
            'cancel': self.quit}, -2)

    def quit(self):
        self.close()
