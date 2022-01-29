"""raidify.py is a python script to keep 2 folders synced."""
import os.path
import time  # time.sleep
import sys   # sys.argv
from watchdog.observers import Observer  # <--
from filesystem import MyHandler

FLAGS = {
    "--dryrun": 1,
    "--init": 2,
    "--verbose": 3
}


def logo(source="", destination=""):
    """Function used to print the script banner (from file banner.txt)."""
    if os.path.abspath(os.curdir).endswith('/src'):
        file = "banner.txt"
    elif os.path.abspath(os.curdir).endswith('/tests'):
        file = "../src/banner.txt"
    else:
        file = "src/banner.txt"

    with open(os.path.join(os.path.abspath(os.curdir), file),
              "r",
              encoding="UTF-8") as banner_source:
        banner = banner_source.read()

    print(banner)
    if source != "" and destination != "":
        print("[src] : " + source)
        print("[dst] : " + destination)


def parse_flag(flags):
    """Function used to parse script flags."""
    output = []
    if (len(flags) < 2) or flags[0] == '--help':
        logo()
        print("""python3 raidify.py [ FLAGS ] <src> <dest>

                    FLAGS:
                      --dryrun  : does nothing but print
                      --init    : make two folders equal
                      --verbose : print everything about execution
                      --help    : displays this help, than exit """)
        return [-1]

    output = flags[(len(flags) - 2):]
    logo(output[0], output[1])
    flag_id = 0  # flag è un array di bit da mascherare

    for flag in flags[:(len(flags) - 2)]:
        mask = (1 << FLAGS.get(flag, 0))
        if mask == 1:
            print("[ !! ] : " + flag + " flag ignored")
        else:
            flag_id += mask
    output.append(flag_id)

    return output


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    if args:
        result = parse_flag(args)
        if result:
            source_path = result[0]
            destination_path = result[1]
            observer.schedule(
                MyHandler(
                    source_path,
                    destination_path,
                    result[2]
                ),
                source_path,
                recursive=True)
            observer.start()

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()

            observer.join()
