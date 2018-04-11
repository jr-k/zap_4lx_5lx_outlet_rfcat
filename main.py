#!/usr/bin/python

# Send a PWM String using RfCat

import rflib
import bitstring
import time

# That prefix string. This was determined by literally
# just looking at the waveform, and calculating it relative
# to the clock signal value.
# Your remote may not need this.
prefix = '0000000000000000'

# The key from our static key remote.

remotes = {
   '0303': '1111101010',
   '0308': '1010101110'
}

options = {
   '4LX': {
       'channels': {
           'C1': '1010101100',
           'C2': '1010100011',
           'C3': '1010001111',
           'C4': '1000101111',
           'C5': '0010101111'
       },
       'actions': {
           'ON': '1100',
           'OFF': '0011'
       },
       'suffix': '1'
   },
   '5LX': {
       'channels': {
           'C1': '0101010011',
           'C2': '0101011100',
           'C3': '0101110000',
           'C4': '0111010000',
           'C5': '1101010000'
       },
       'actions': {
           'ON': '0011',
           'OFF': '1100'
       },
       'suffix': ''
   }
}

def getPayload(remote, model, channel, action):
   return remotes[remote] + options[model]['channels'][channel] + options[model]['actions'][action] + options[model]['suffix']

def getPacket(remote, model, channel, action):
   payload = getPayload(remote, model, channel, action)

   print "Send payload : " + str(payload)

   # Convert the data to a PWM key by looping over the
   # data string and replacing a 1 with 1000 and a 0
   # with 1110
   pwm_key = ''.join(['1000' if b == '1' else '1110' for b in payload])

   # Join the prefix and the data for the full pwm key
   full_pwm = '{}{}'.format(prefix, pwm_key)
   print('Sending full PWM key: {}'.format(full_pwm))

   # Convert the data to hex
   rf_data = bitstring.BitArray(bin=full_pwm).tobytes()

   return rf_data

def sendPacket(remote, model, channel, action):
   packet = getPacket(remote, model, channel, action)

   # Send the data string a few times
   device.RFxmit(packet, repeat=25)
   device.setModeIDLE()


def init():
   d = rflib.RfCat()

   # Set Modulation. We using On-Off Keying here
   d.setMdmModulation(rflib.MOD_ASK_OOK)

   # Configure the radio
   #d.makePktFLEN(len(rf_data)) # Set the RFData packet length
   d.setMdmDRate(5500)         # Set the Baud Rate
   d.setMdmSyncMode(0)         # Disable preamble
   d.setFreq(433920000)        # Set the frequency

   return d

device = init()

for i in range(0,10):
   sendPacket('0303', '4LX', 'C4', 'ON' if i%2 == 0 else 'OFF')

   #time.sleep(0.0005)