"""
Copyright (c) 2012, Thomas Recouvreux
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import sys
import socket
import string
import time 
import threading

HOST="localhost"
PORT=9095
NICK="flooder_"
IDENT="flooder_"
REALNAME="Flood"
readbuffer=""

def envoyer(commande):
#    print(commande) # "bracelets" autour du print (T.R.)
    commande = commande + "\r\n"
    s.send(commande.encode())

def loop():
    while 1:
        data = s.recv(1024)

        lines = data.decode().split("\n")
        
        for line in lines:
            line = line.strip()
            #print(line)
            line = line.split()
            if(line and line[0] == "PING"):
                envoyer("PONG %s\r\n" % line[1])

s = socket.socket()
print("connected")
s.connect((HOST, PORT))

envoyer("NICK %s\r\n" % NICK)
envoyer("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
envoyer("JOIN #test")

print("start boucle")

# Lancement du thread
t = threading.Thread(target=loop)
t.setDaemon(True)
t.start()

while 1:
    m = input()
    if m == "flood":
        last = round(time.time())
        count = 0
        while 1:
            envoyer("privmsg #test :Je flood !") #" %f" % time.time())
            if time.time() - last > 1:
                print("%s messages par seconde" % count)
                last = round(time.time())
                count = 0
            else:
                count = count + 1
            
            time.sleep(.001)
        print(time.time())
    else:
        envoyer(m)
