#!/usr/bin/env python3

import os
import logging
import subprocess
import sys

java_export = 'export JAVA_HOME="/usr/lib/jvm/java-1.8.0-openjdk-amd64"'

# Function for install python2.7
def install_python():
    PYTHON_VERSION = os.popen('python -V 2>&1 |awk \'{ print $2 }\'', "r").read()
    if '2.7' not in PYTHON_VERSION:
        logging.info(" Installation of python ...")
        out = subprocess.run(['sudo','apt-get','-qq','-y','install','python', '>>','/dev/null','2>&1'], check=True)
        if out.returncode == 0:
            logging.info("  Python 2.7 installed [success]")
        else:
            logging.error("  Python installation failed [error]")
    return

def install_java():
    out = os.system("sudo apt-get update >> /dev/null 2>&1")
    out = os.system("sudo apt-get -qq -y install openjdk-8-jdk >> /dev/null 2>&1")
    #TODO set JAVA HOME insode /etc/environment
    '''environment_file = open('/etc/environment', 'a')
    if java_export not in environment_file.read():
        subprocess.run(['echo', java_export], stdout=environment_file, check=True)
    '''

    if out == 0:
        logging.info("  OpenJDK 8 installed [success]")
    else:
        logging.error("  OpenJDK 8 installation failed [error]")

# Function for install Java
'''
def install_java():
    JAVA_VERSION = os.popen('java -version 2>&1 |awk \'NR==1{ gsub(/"/,""); print $3 }\'', "r").read()
    if '1.8.0_112' not in JAVA_VERSION:
        logging.info(" Downloading Java ...")
        out = subprocess.run(['wget', '-q', '--no-cookies', '--no-check-certificate', '--header','Cookie: oraclelicense=accept-securebackup-cookie','http://download.oracle.com/otn-pub/java/jdk/8u112-b15/jdk-8u112-linux-x64.tar.gz'], check=True)
        if out.returncode == 0:
            logging.info("Java downloaded [success]")
        logging.info(" Installation of Java ...")
        subprocess.run(['sudo','rm','-rf','/usr/lib/java/'])
        subprocess.run(['sudo','mkdir','/usr/lib/java/'])
        out = subprocess.run(['sudo', 'tar', '-xf', 'jdk-8u112-linux-x64.tar.gz', '-C', '/usr/lib/java'], check=True)
        if out.returncode == 0:
            logging.info("Java unpacked [success]")
        subprocess.run(['rm','jdk-8u112-linux-x64.tar.gz'])
        subprocess.run(['sudo','ln', '-s', '/usr/lib/java/jdk1.8.0_112/bin/java', '/bin/java'])
        subprocess.run(['sudo','ln', '-s', '/usr/lib/java/jdk1.8.0_112/bin/javac', '/bin/javac'])
        subprocess.run(['sudo','ln', '-s', '/usr/lib/java/jdk1.8.0_112/bin/jar', '/bin/jar'])
        with open(os.path.expanduser('~/.profile'), 'a') as proFile:
            subprocess.run(['echo', 'export JAVA_HOME=/usr/lib/java/jdk1.8.0_112'], stdout=proFile, check=True)
        JAVA_VERSION = os.popen('java -version 2>&1 |awk \'NR==1{ gsub(/"/,""); print $3 }\'', "r").read()
        if '1.8.0_112' in JAVA_VERSION:
            logging.info(" Java installed [success]")
        else:
            logging.error(" Java installation failed [error]")
        return
'''

# Function for define the hostname
def define_hostname(conponent,index):
    if conponent == "hdfs":
        conponent = "spark"
    find = False
    file = open('/etc/hosts')
    for line in file:
        if get_ip() in line:
            find = True
    if not find:
        os.system('echo "'+get_ip()+' '+conponent+'-'+index+'" | sudo tee -a /etc/hosts >> /dev/null 2>&1')
        os.system('sudo hostname '+conponent+'-'+index+' >> /dev/null 2>&1')
        logging.info(" Hostname update")
    return

def install_pika() :
    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'python-pika'])

def get_ip():
    ip = os.popen('ifconfig ens3 | grep "inet ad" | cut -f2 -d: | awk \'{print $1}\'', "r").read()
    ip = ip.replace('\n', '')
    return ip

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    define_hostname(sys.argv[1],sys.argv[2])
    install_python()
    install_java()
    install_pika()
