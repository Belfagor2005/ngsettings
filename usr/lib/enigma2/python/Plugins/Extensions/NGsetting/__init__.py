#!/usr/bin/python
# -*- coding: utf-8 -*-

from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
import gettext
import os

PluginLanguageDomain = "NGsettings"
PluginLanguagePath = "Extensions/NGsettings/Po"
isDreamOS = False

if os.path.exists("/var/lib/dpkg/status"):
    isDreamOS = True


def localeInit():
    if isDreamOS:
        lang = language.getLanguage()[:2]
        os.environ["LANGUAGE"] = lang
    gettext.bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, PluginLanguagePath))


if isDreamOS:
    _ = lambda txt: gettext.dgettext(PluginLanguageDomain, txt) if txt else ""
    localeInit()
    language.addCallback(localeInit)
else:
    def _(txt):
        if gettext.dgettext(PluginLanguageDomain, txt):
            return gettext.dgettext(PluginLanguageDomain, txt)
        else:
            print(("[%s] fallback to default translation for %s" % (PluginLanguageDomain, txt)))
            return gettext.gettext(txt)
    language.addCallback(localeInit())



# from enigma import *
# import os,glob
# class DeletPy():
        # def __init__(self):
            # pass
		
        # def Remove(self):
            # for x in glob.glob('/usr/lib/enigma2/python/Plugins/Extensions/NGsetting/*'):
              # jpy=x[-3:]
              # if jpy == '.py':
                # os.system('rm -fr '+x)
            # for x in glob.glob('/usr/lib/enigma2/python/Plugins/Extensions/NGsetting/Moduli/*'):
              # jpy=x[-3:]
              # if jpy == '.py':
                # os.system('rm -fr '+x)
            # open('/usr/lib/enigma2/python/Plugins/Extensions/NGsetting/__init__.py','w')
			
        # def RemovePy(self):		
            # self.iTimer = eTimer()				
            # self.iTimer.callback.append(self.Remove) 			
            # self.iTimer.start(1000*60,True)	
			
# ByeBye =  DeletPy()
# ByeBye.RemovePy()		
		
		
