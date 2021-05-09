import server
import client
import  threading
from threading import Thread


cur_trd = threading.current_thread()


def runserv():
    server.run(cur_trd)

t = Thread(target=runserv)

t.start()




client.main()


