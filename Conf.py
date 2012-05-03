# Copyright (c) 2012 Oliver Burger obgr_seneca@mageia.org
#
# This file is part of videoconvert.
#
# videoconvert is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# videoconvert is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with videoconvert.  If not, see <http://www.gnu.org/licenses/>.

class Configuration():
    import re
    import os

    def __init__(self,debug):
        self.userHome = self.os.environ['HOME']
        self.applicationDir = self.userHome+'/.videoconvert'
        self.confFile = self.applicationDir+'/config'
        self.appTmpDir = self.applicationDir+'/tmp'
        self.framerate = 890
        self.resolution = '512x384'
        self.container = 'avi'
        self.audioCodec = 'libmp3lame'
        self.videoCodec = 'mpeg4'
        self.debug = debug


        self.bf = '\033[0;1m'
        self.bfBlue = '\033[34;1m'
        self.bfYellow = '\033[1;33;40m'
        self.yellow = '\033[0;33;40m'
        self.nf = '\033[0;0m'

        if self.os.path.exists(self.appTmpDir) == False:
            self.os.makedirs(self.appTmpDir,0700)

    def readConfig(self):
        config = open(self.confFile,'r')
        lines = config.readlines()
        config.close
        for l in lines:
            if self.re.search('^#',l) == False:
                if self.re.search('^framerate',l):
                    self.framerate = l.split('=')[1].strip()
                elif self.re.search('^resolution',l):
                    self.resolution = l.split('=').strip()
                elif self.re.search('^container',l):
                    self.container = l.split('=').strip()
                elif self.re.search('^audiocodec',l):
                    self.audioCodec = l.split('=').strip()
                elif self.re.search('^videocodec',l):
                    self.videoCodec = l.split('=').strip()

    def __writeConfig(self):
        config = open(self.confFile,'w')
        config.write('# videoconvert configuration file\n')
        config.write('framerate = '+str(self.framerate)+'\n')
        config.write('resolution = '+str(self.resolution)+'\n')
        config.write('container = '+str(self.container)+'\n')
        config.write('audiocodec = '+str(self.audioCodec)+'\n')
        config.write('videocodec = '+str(self.videoCodec)+'\n')
        config.close

    def getNewConfig(self):
        if self.os.path.exists(self.confFile):
            self.readConfig()
        print self.bfYellow+'Edit configuration'+self.nf
        print ''
        print 'Enter the framerate for the video conversion'
        print '['+str(self.framerate)+']'
        userInput = raw_input(self.bfBlue+'Framerate : '+self.nf).strip()
        if userInput != '':
            self.framerate = userInput
        print 'Enter the resolution for the target video'
        print '['+self.resolution+']'
        userInput = raw_input(self.bfBlue+'Resolution : '+self.nf).strip()
        if userInput != '':
            self.resolution = userInput
        print 'Enter the container for the target video'
        print '['+self.container+']'
        userInput = raw_input(self.bfBlue+'Container : '+self.nf).strip()
        if userInput != '':
            self.container = userInput
        print 'Enter the audio codec for the target video'
        print '['+self.audioCodec+']'
        userInput = raw_input(self.bfBlue+'Audio codec : '+self.nf).strip()
        if userInput != '':
            self.audioCodec = userInput
        print 'Enter the video codec for the target video'
        print '['+self.videoCodec+']'
        userInput = raw_input(self.bfBlue+'Video codec : '+self.nf).strip()
        if userInput != '':
            self.videoCodec = userInput


        self.__writeConfig()

    def getConfFile(self):
        return self.confFile

    def getAppTmpDir(self):
        return self.appTmpDir

    def getFramerate(self):
        if self.debug:
            print self.bfBlue + 'framerate is set to ' + str(self.framerate) + self.nf
        return self.framerate

    def getResolution(self):
        if self.debug:
            print self.bfBlue + 'resolution is set to ' + str(self.resolution) + self.nf
        return self.resolution

    def getContainer(self):
        if self.debug:
            print self.bfBlue + 'container is set to ' + str(self.container) + self.nf
        return self.container

    def getAudioCodec(self):
        if self.debug:
            print self.bfBlue + 'audio codec is set to ' + str(self.audioCodec) + self.nf
        return self.audioCodec

    def getVideoCodec(self):
        if self.debug:
            print self.bfBlue + 'video codec is set to ' + str(self.videoCodec) + self.nf
        return self.videoCodec

    def setFramerate(self,framerate):
        self.framerate = framerate
        if self.debug:
            print self.bfBlue + 'Set framerate to ' + str(self.framerate) + self.nf

    def setResolution(self,resolution):
        if self.debug:
            print self.bfBlue + 'Set resolution to ' + resolution + self.nf
        self.resolution = resolution

    def setContainer(self,container):
        if self.debug:
            print self.bfBlue + 'Set container format to ' + container + self.nf
        self.container = container

    def setAudioCodec(self,audioCodec):
        if self.debug:
            print self.bfBlue + 'Set audio codec to ' + audioCodec + self.nf
        self.audioCodec = audioCodec

    def setVideoCodec(self,videoCodec):
        if self.debug:
            print self.bfBlue + 'Set video codec to ' + videoCodec + self.nf
        self.videoCodec = videoCodec

    def toString(self):
        returnString = '*****  Configuration object  *****\n'
        returnString += 'framerate      :   '+str(self.framerate)+'\n'
        returnString += 'resolution     :   '+str(self.resolution)+'\n'
        returnString += 'container      :   '+str(self.container)+'\n'
        returnString += 'audioCodec     :   '+str(self.audioCodec)+'\n'
        returnString += 'videoCodec     :   '+str(self.videoCodec)+'\n'
        returnString += 'confFile       :   '+str(self.confFile)+'\n'
        returnString += 'appTmpDir      :   '+str(self.appTmpDir)+'\n'
        return returnString
