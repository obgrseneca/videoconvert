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
        self.audioCodec = ''
        self.bf = '\033[0;1m'
        self.bfBlue = '\033[34;1m'
        self.bfYellow = '\033[1;33;40m'
        self.yellow = '\033[0;33;40m'
        self.nf = '\033[0;0m'

    def sync(self,inDir,name):
        if self.os.path.isabs(inDir):
            pass
        else:
            inDir = self.currentDir+'/'+inDir
        files = self.os.listdir(inDir)
        self.currentDir = self.os.getcwd()
        for f in files:
            if self.re.search('^[0-9]+\.vdr$',f):
                self.__demultiplex(inDir,f)
                self.__multiplex(name,f)
        self.os.chdir(self.currentDir)
        self.joinMultipleFiles(name)
        self.convertFile(name+'.mpg',self.outDir,self.currentDir)

    def __demultiplex(self,inDir,fileName):
        self.os.chdir(inDir)
        demultiplexCommand = 'projectx -out '+self.outDir+' '+fileName
        self.__callSystemCommand(demultiplexCommand)

    def __multiplex(self,name,fileName):
        self.os.chdir(self.outDir)
        prefix = fileName.split('.')[0]
        if self.os.path.exists(prefix+'.ac3'):
            self.audioCodec = 'ac3'
        else:
            self.audioCodec = 'mp2'
        multiplexCommand = 'mplex -f 9 -o '+name+'-'+prefix+'.mpg '+prefix+'.'+self.audioCodec+' '+prefix+'.m2v'
        self.__callSystemCommand(multiplexCommand)
        
        files = self.os.listdir(self.outDir)
        for f in files:
            if self.re.search('^'+prefix, f):
                self.os.remove(f)

    def joinMultipleFiles(self,name):
        files = self.os.listdir(self.outDir)
        filesString = ''
        for f in files:
            if self.re.search('^'+name, f):
                filesString += self.outDir+'/'+f+' '
        filesString = filesString.strip()
        concatCommand = 'cat '+filesString+' > '+self.outDir+'/'+name+'.mpg'
        self.__callSystemCommand(concatCommand)

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
