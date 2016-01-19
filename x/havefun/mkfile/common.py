#!/usr/bin/env python
#coding=utf-8

import sys
import re
import os
from ftplib import FTP
def svnupdate(path,reversion="HEAD"):

    if os.system("svn cleanup "+path)!=0:
        print "svn cleanup fail"
    if os.system("svn revert -R "+path)!=0:
        print "svn revert fail"    
    if os.system("svn update -r "+reversion +" "+path)==0:
        print "svn update success "+ path
        return 1
    else:
         print "svn update fail，update again "+ path
         if os.system("svn cleanup "+path)!=0:
             print "svn cleanup fail"
         if os.system("svn revert -R "+path)!=0:
             print "svn revert fail"
         if os.system("svn update -r "+reversion +" "+path)==0:
             print "svn update success "+ path
             return 1
         else:
             print "svn update fail "+ path
             return 0
    
def svncommit(file,message):
    
    message=str(message)
    print message
    if os.system("svn commit "+file +" -m " +message)==0:
       print "svn commit success" + file
       return 1
    else:
       print "svn commit fail" + file
       return 0
    
def modifycs(filepath,version,GM_ENABLE,UPDATE_ENABLE,DEBUGMODE_ENABLE,GONGGAO_COMMON):
    
    version = version.split('.')
    pWriteFile1 = open(filepath, 'r')
    lines = pWriteFile1.readlines()
    pWriteFile1.close()

    index = 0
    for curline in lines:

        if(curline.strip().find("GAME_VERSION=")==0):
            tempcontent = "GAME_VERSION=" +version[0]+"\n"
            lines[index]=tempcontent
        elif (curline.strip().find("PROGRAM_VERSION=")==0):
            tempcontent = "PROGRAM_VERSION=" +version[1]+"\n"
            lines[index]=tempcontent
        elif (curline.strip().find("GM_ENABLE=")==0):
            tempcontent = "GM_ENABLE=" +GM_ENABLE+"\n"
            lines[index]=tempcontent
        elif (curline.strip().find("UPDATE_ENABLE=")==0):
            tempcontent = "UPDATE_ENABLE=" +UPDATE_ENABLE+"\n"
            lines[index]=tempcontent
        elif (curline.strip().find("DEBUGMODE_ENABLE=")==0):
            tempcontent = "DEBUGMODE_ENABLE=" +DEBUGMODE_ENABLE+"\n"
            lines[index]=tempcontent
        elif (curline.strip().find("GONGGAO_COMMON=")==0):
            tempcontent = "GONGGAO_COMMON=" +GONGGAO_COMMON+"\n"
            lines[index]=tempcontent
        index = index +1
    pWriteFile = open(filepath,'w')
    pWriteFile.writelines(lines)
    pWriteFile.close()
    return 1
def modifyios(filepath,version):

    version = version.split('.')
    pWriteFile1 = open(filepath, 'r')
    lines = pWriteFile1.readlines()
    pWriteFile1.close()

    index = 0
    for curline in lines:

        if(curline.strip().find("GameVersion = ")==0):
            tempcontent = "    GameVersion = " +version[0]+",\n"
            lines[index]=tempcontent
        elif(curline.strip().find("ProgramVersion = ")==0):
            tempcontent = "    ProgramVersion = " +version[1]+",\n"
            lines[index]=tempcontent
        index = index +1
    pWriteFile = open(filepath,'w')
    pWriteFile.writelines(lines)
    pWriteFile.close()
    return 1

def targzip(sourcepath,targetpath):
    os.system("cd "+sourcepath +" && tar zcf "+targetpath +" *")

def ungzip(sourcefile,targetpath):
    os.system("cd "+targetpath +" && tar zxf "+sourcefile)
    
class Xfer(object):
    def __init__(self):  
        self.ftp = None
      
    def __del__(self):  
        pass
        #self.ftp.close()
      
    def setFtpParams(self, ip = "10.2.4.29", uname = "happy", pwd = "happy", port = 888, timeout = 60):          
        self.ip = ip  
        self.uname = uname  
        self.pwd = pwd  
        self.port = port  
        self.timeout = timeout  
      
    def initEnv(self):  
        if self.ftp is None:  
            self.ftp = FTP()  
            print '### connect ftp server: %s ...'%self.ip  
            self.ftp.connect(self.ip, self.port, self.timeout)  
            self.ftp.login(self.uname, self.pwd)   
            print self.ftp.getwelcome()

    def clearEnv(self):  
        if self.ftp:  
            self.ftp.close()  
            print '### disconnect ftp server: %s!'%self.ip   
            self.ftp = None
    
    def uploadDir(self, localdir='./', remotedir='./'):  
        if not os.path.isdir(localdir):    
            return  
        self.ftp.cwd(remotedir)   
        for file in os.listdir(localdir):  
            src = os.path.join(localdir, file)  
            if os.path.isfile(src):  
                self.uploadFile(src, file)  
            elif os.path.isdir(src):  
                try:    
                    self.ftp.mkd(file)    
                except:    
                    sys.stderr.write('the dir is exists %s'%file)  
                self.uploadDir(src, file)  
        self.ftp.cwd('..')  
      
    def uploadFile(self, localpath, remotepath='./'):  
        if not os.path.isfile(localpath):    
            return  
        print '+++ upload %s to %s:%s'%(localpath, self.ip, remotepath)  
        self.ftp.storbinary('STOR ' + remotepath, open(localpath, 'rb'))  
      
    def __filetype(self, src):  
        if os.path.isfile(src):  
            index = src.rfind('\\')  
            if index == -1:  
                index = src.rfind('/')                  
            return 'FILE', src[index+1:]  
        elif os.path.isdir(src):  
            return 'DIR', ''          
      
    def upload(self, src,remotepath):
        if (os.path.isfile(src) or os.path.isdir(src)):
            filetype, filename = self.__filetype(src)  
            self.initEnv()
            self.ftp.cwd(remotepath) 
            if filetype == 'DIR':  
               self.srcDir = src              
               self.uploadDir(self.srcDir)  
            elif filetype == 'FILE':  
               self.uploadFile(src, filename)  
            self.clearEnv()
        else:
            print '+++file not find %s'%src
        
    def creatdir(self,dirname,remotepath):
        self.initEnv()
        dirpath=remotepath+'/'+dirname
        print dirpath
        try:
            self.ftp.cwd(dirpath)
        except:
            try:
                self.ftp.cwd(remotepath)
                self.ftp.mkd(dirname)
            except:
                print "Creat directory failed!"
        self.clearEnv()

    def create_dir_tree(self,dirname,remotepath):


    def download_file(self, localfile, remotefile):          
        #return     
        file_handler = open(localfile, 'wb')     
        self.ftp.retrbinary('RETR %s'%(remotefile), file_handler.write)     
        file_handler.close()     

    def download_files(self, localdir='./', remotedir='./'):     
        try:
           #print '--------%s' %(remotedir)
           self.ftp.cwd(remotedir)
        except:        
           return    
        if not os.path.isdir(localdir):     
           os.makedirs(localdir)         
        self.file_list = []     
        self.ftp.dir(self.get_file_list)     
        remotenames = self.file_list     
        #print(remotenames)     
        #return     
        for item in remotenames:     
             filetype = item[0]     
             filename = item[1]     
             local = os.path.join(localdir, filename)     
             if filetype == 'd':     
                 self.download_files(local, filename)     
             elif filetype == '-':     
                 self.download_file(local, filename)
        #print '--------pwd--1--%s' %self.ftp.pwd()
        self.ftp.cwd('..')
        #print '--------pwd---2-%s' %self.ftp.pwd()

    def download(self,localfile, remotefile):    
        self.initEnv()
        try:     
           self.ftp.cwd(remotefile)     
        except:
           print 'wenjian-------%s' %(remotefile)      
           self.download_file(localfile, remotefile)
        else:
           print "lujing-------"
           self.download_files(localfile, remotefile)
        finally:
           self.clearEnv()
    
    def get_file_list(self, line):     
         ret_arr = []     
         file_arr = self.get_filename(line)     
         if file_arr[1] not in ['.', '..']:     
            self.file_list.append(file_arr)     
                     
    def get_filename(self, line):     
         pos = line.rfind(':')     
         while(line[pos] != ' '):     
           pos += 1    
         while(line[pos] == ' '):     
           pos += 1    
         file_arr = [line[0], line[pos:]]     
         return file_arr     

if __name__ == '__main__':
    if sys.argv[1]=="svnupdate":
        print "svn update begin"
        svnupdate(sys.argv[2],sys.argv[3])
    if sys.argv[1]=="svncommit":
        svncommit(sys.argv[2],sys.argv[3])
    if sys.argv[1]=="modifycs":
        modifycs(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7])
    if sys.argv[1]=="modifyios":
        modifyios(sys.argv[2],sys.argv[3])
    if sys.argv[1]=="ftp_up": 
        xfer = Xfer()  
        xfer.setFtpParams()
        xfer.upload(sys.argv[2],sys.argv[3])
    if sys.argv[1]=="ftp_creatdir":
        xfer = Xfer()  
        xfer.setFtpParams()
        xfer.creatdir(sys.argv[2],sys.argv[3])
    if sys.argv[1]=="download":
        xfer = Xfer()  
        xfer.setFtpParams()
        xfer.download(sys.argv[2],sys.argv[3])
    if sys.argv[1]=="targzip":
        targzip(sys.argv[2],sys.argv[3])
    if sys.argv[1]=="ungzip":
        ungzip(sys.argv[2],sys.argv[3])
