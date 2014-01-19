#!/usr/bin/env python

import pexpect
import sys
import time
import datetime

#set this empty to turn off logging:
logfile = r'pexpect-hcilescan.log'


def main():
    interval = 1
    if (len(sys.argv) > 1):
        interval = sys.argv[1]
    
    
    while True:
        lf = open(logfile, 'a')
        tool = pexpect.spawn('sudo hcitool lescan',logfile=lf)
        tool.expect('LE Scan ...')
        print 'lescan started---------'
        index = tool.expect (['\n[\w:]* SensorTag\r\n', pexpect.EOF, pexpect.TIMEOUT],3)
        if index == 0:
            print "found: "
            print tool.match.group()
            tool.sendcontrol('c')
        elif index == 1 or index == 2:
            tool.sendcontrol('c')
        #    print "blorf"
        #tool.close()
        print 'lescan dead---------'
        tool.wait()
        lf.close()
        time.sleep(2)

if __name__ == '__main__':
    main()
