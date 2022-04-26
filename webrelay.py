#!/usr/bin/env python3
import smbus
import time as t
from flask import Flask


class Relay:
    
    def __init__(self,dev_bus, dev_addr):
        self.dev_bus = dev_bus
        self.dev_addr = dev_addr
        self.bus=smbus.SMBus(self.dev_bus)
        
    def TurnOn(self,ch):
        self.bus.write_byte_data(self.dev_addr,ch,0xFF)
        return 1

    def TurnOff(self, ch):
        self.bus.write_byte_data(self.dev_addr,ch,0x00)
        return 1

    def GetStatus(self,ch):
        st = self.bus.read_byte_data(self.dev_addr,ch)
        if st == 0x00:
            retval = 0
        elif st == 0xFF:
            retval = 1
        return retval

app = Flask(__name__)
# main page
#def get_ch(any_string):
#    c1,ch = any_string.split('_')
#    return int(ch)

def workers(cmd,ch):
    r1 = Relay(1,0x10)
    if cmd == 'on':
        # ch = get_ch(any_string)
        if r1.GetStatus(int(ch)):
            r1.TurnOff(int(ch))
        r1.TurnOn(int(ch))
        retval = "turn on channel {}".format(ch)
    elif cmd == 'off':
        # ch = get_ch(any_string)
        r1.TurnOff(int(ch))
        retval = "turn off channel {}".format(ch)
    elif cmd == 'stat':
        # ch = get_ch(any_string)
        st = r1.GetStatus(int(ch))
        if st == 0:
            retval ="OFF"
        else:
            retval ="ON"
        # retval = "status channel {} {}".format(ch,st)
    else:
        retval="NOT a command"
    return retval

@app.route('/')
def root():
    return workers("")
@app.route('/<command>/<ch>',methods =['POST','GET'])
def Fun(command,ch):
    return workers(command,ch)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0', port=8080)
