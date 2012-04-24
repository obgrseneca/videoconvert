class SystemCall():
    import subprocess as sp
    import os
    import re
    import sys
    import shutil
    import string

    def __init__(self,configuration):
        self.configuration = configuration
        self.outDir = self.configuration.getAppTmpDir()
        self.currentDir = self.os.getcwd()
        # FIXME: get this automatically somehow
        self.audioCodec = 'mp2'
        self.bf = '\033[0;1m'
        self.bfBlue = '\033[34;1m'
        self.bfYellow = '\033[1;33;40m'
        self.yellow = '\033[0;33;40m'
        self.nf = '\033[0;0m'
        self.prefix = ''

    def sync(self,inDir,name):
        if self.os.path.isabs(inDir):
            pass
        else:
            inDir = self.currentDir+'/'+inDir
        files = self.os.listdir(inDir)
        self.currentDir = self.os.getcwd()
        for f in files:
            if self.re.search('^[0-9]+\.vdr$',f):
                self.prefix = f.split('.')[0]
                print self.bfYellow+'Copying vdr file '+f+' to temporary directory.'+self.nf
                self.shutil.copy2(inDir+'/'+f,self.outDir+'/'+f)
                syncCommand = 'ffmpeg -i '+self.outDir+'/'+f+' -acodec copy -vcodec copy -async 2 '
                syncCommand += self.outDir+'/'+name+'-'+self.prefix+'.mpg'
                self.__callSystemCommand(syncCommand)
                self.os.remove(self.outDir+'/'+f)
        self.os.chdir(self.currentDir)
        self.joinMultipleFiles(name)
        self.convertFile(name+'.mpg',self.outDir,self.currentDir)

    def joinMultipleFiles(self,name):
        files = self.os.listdir(self.outDir)
        filesString = ''
        # TODO: just a debug output, has to be removed
        print self.bfBlue+'Anzahl der Dateien : '+str(len(files))+self.nf
        if len(files) > 1:
            for f in files:
                print self.bfBlue+f+self.nf
                if self.re.search('^'+name, f):
                    filesString += self.outDir+'/'+f+' '
            filesString = filesString.strip()
            concatCommand = 'cat '+filesString+' > '+self.outDir+'/'+name+'.mpg'
            self.__callSystemCommand(concatCommand)
        else:
            self.os.rename(self.outDir+'/'+files[0],self.outDir+'/'+name+'.mpg')

        if len(files) > 1:
            for f in files:
                if self.re.search('^'+name, f):
                    self.os.remove(self.outDir+'/'+f)

    def convertFile(self,inFile,inDir,outDir):
        nameList = inFile.split('.')
        fileEnding = nameList.pop(len(nameList)-1)
        name = self.string.join(nameList,'.')

        if fileEnding == 'wmv':
            acodec='libmp3lame'
            videoFormat='avi'
            scale=''
        elif fileEnding == 'mpg':
            if self.audioCodec == 'mp2':
                acodec = 'libmp3lame'
                videoFormat = 'avi'
            else:
                acodec = 'copy'
                videoFormat = 'mp4'
            scale = '-s '+self.configuration.getResolution()
        vcodec = 'mpeg4'
        framerate = self.configuration.getFramerate()
        outFile=name+'.'+videoFormat

        convertStringTurn1 = 'nice -5  ffmpeg -i '+inDir+'/'+inFile+' '+scale+' -vcodec '+vcodec+' -acodec '
        convertStringTurn1 += acodec+' -b:v '+str(framerate)+'k -pass 1 -f rawvideo -an -y /dev/null'
        convertStringTurn2 = 'nice -5  ffmpeg -i '+inDir+'/'+inFile+' '+scale+' -vcodec '+vcodec+' -acodec '
        convertStringTurn2 += acodec+' -b:v '+str(framerate)+'k -pass 2 -f '+videoFormat+' -y '+outDir+'/'+outFile

        self.__callSystemCommand(convertStringTurn1)
        self.__callSystemCommand(convertStringTurn2)

        self.os.remove(outDir+'/ffmpeg2pass-0.log')
        self.os.remove(inDir+'/'+inFile)

    def __callSystemCommand(self,systemCommand):
        print self.bfYellow+systemCommand+self.nf
        convert = self.sp.Popen(
          systemCommand,
          shell=True,
          stdin=self.sp.PIPE,
          stdout=self.sp.PIPE,
          stderr=self.sp.STDOUT
          )
        while True:
            out = convert.stdout.read(1)
            if out == '' and convert.poll() != None:
                break
            if out != '':
                self.sys.stdout.write(out)
                self.sys.stdout.flush()
