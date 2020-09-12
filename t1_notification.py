from threading import Thread
from time import sleep as ResidentSleeper
from tribes import TribesMasterClient
from tooltip import WindowsBalloonTip
from sys import exc_info
from traceback import format_exc
import os

if os.name == 'nt':
    from  winsound import PlaySound, SND_FILENAME
def snd(name):
    if os.name == 'nt':
        PlaySound("sound\\%s.wav" % name, SND_FILENAME)

if __name__ == '__main__':
    tool_tip = WindowsBalloonTip(icon="tribes.ico")

    def checkTribesAll():
        global tool_tip

        lastcnt = {}

        tribes_list = [
            TribesMasterClient('67.222.138.46', 28006),
            TribesMasterClient('52.188.16.233', 28001)
        ]
        while True:
            os.system("cls")
            for tribes_srv in tribes_list:
                srvhash = "%s_%s" % (tribes_srv.ip, tribes_srv.port)
                lastplayercnt = lastcnt.get(srvhash, 0)
                try:
                    tribes_srv.Query(readplayerdata=False)
                    if  tribes_srv.playerCount >= 3 and lastplayercnt < 3 :
                        snd("ir_end")
                        tool_tip.show("%d/%d" % (tribes_srv.playerCount, tribes_srv.maxPlayers), tribes_srv.serverName.decode(), 5)
                    lastcnt[srvhash] = tribes_srv.playerCount
                except:
                    print(srvhash)
                    print(str(format_exc()))
                    print(str(exc_info()[0]))
            ResidentSleeper(120)


    def starttasks():
        ___tlist = [
            #Thread(target=webserv),
            #Thread(target=ffmpegWatcher),
            Thread(target=checkTribesAll),
            ]
        for ___t in ___tlist:
            ___t.start()
        for ___t in ___tlist:
            ___t.join()
    starttasks()
