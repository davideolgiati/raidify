import time  # time.sleep
import sys   # sys.argv
from watchdog.observers import Observer  # <--
from filesystem import MyHandler

FLAGS = {
    "--dryrun": 1,
    "--init": 2,
    "--verbose": 3
}


def logo(path="", dest=""):
    logo = """
            _     _ _  __
  _ __ __ _(_) __| (_)/ _|_   _   _ __  _   _
 | '__/ _` | |/ _` | | |_| | | | | '_ \\| | | |
 | | | (_| | | (_| | |  _| |_| |_| |_) | |_| |
 |_|  \\__,_|_|\\__,_|_|_|  \\__, (_) .__/ \\__, |
        THO 23/01/2020    |___/  |_|    |___/

    """
    print(logo)
    if path != "" and dest != "":
        print("[src ] : " + path)
        print("[dest] : " + dest)


def parseFlag(args):
    result = []
    if (len(args) < 2) or args[0] == '--help':
        logo()
        print("""python3 raidify.py [ FLAGS ] <src> <dest>

                    FLAGS:
                      --dryrun  : does nothing but print
                      --init    : make the tow folders even
                      --verbose : print almost everything
                      --help    : dispalys this help, than exit """)
    elif len(args) >= 2:
        result = args[(len(args) - 2):]
        logo(result[0], result[1])
        flagID = 0  # flag è un array di bit da mascherare
        mask = 0
        for flag in args[:(len(args) - 2)]:
            mask = (1 << FLAGS.get(flag, 0))
            if mask == 1:
                print("[ !! ] : " + flag + " flag ignored")
            else:
                flagID += mask
        result.append(flagID)

    return result


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    if args:
        result = parseFlag(args)
        if result != []:
            path = result[0]
            dest = result[1]
            observer.schedule(MyHandler(path, dest, result[2]),
                              path,
                              recursive=True)
            observer.start()

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()

            observer.join()
