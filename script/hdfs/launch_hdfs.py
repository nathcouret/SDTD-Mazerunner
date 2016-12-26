#!/usr/bin/env python3

import logging, sys, subprocess, configparser, socket


version='hadoop-2.7.3'


def format():
	logging.info('Formatting HDFS namenode')
	subprocess.run(['/home/xnet/'+version+'/bin/hdfs', 'namenode', '-format', '-force'], check=True)

def launch():
	logging.info('Launching HDFS cluster')
	subprocess.run(['/home/xnet/'+version+'/sbin/start-dfs.sh'], check=True)

def startJournalNode():
	logging.info('Starting JournalNode')
	subprocess.run(['/home/xnet/'+version+'/sbin/hadoop-daemon.sh', 'start', 'journalnode'], check=True)

def startZK():
	logging.info('Starting ZooKeeper (hdfs)')
	subprocess.run(['/home/xnet/hdfs_zk/bin/zkServer.sh', 'start'], check=True)

def isNameNode():
	config = configparser.ConfigParser()
	config.read("/home/xnet/hdfs/conf.ini")
	masters = getHostsByKey(config, "Master")
	hostname = socket.gethostname()

	return hostname in masters


# Recover all ip for one component. Return format ip
def getHostsByKey(config, key):
    hosts = config.get(key, "hosts").split(',')
    return [host.strip(' \n') for host in hosts]

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

	startJournalNode()
	format()

	#startZK()

	if isNameNode():
		launch()

