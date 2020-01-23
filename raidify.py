import time # time.sleep
import sys  # sys.argv
import os   # os.path.relpath
from watchdog.observers import Observer # <--
from watchdog.events import FileSystemEventHandler # <--

# la calsse 'MyHandler' serve per gestire gli eventi registrati
# dalla libreria watchdog.
# Estende la classe 'FileSystemEventHandler' che è la classe
# più basilare presnte nella libreria, controlla ogni cambaimento
# senza filtraggio
class MyHandler(FileSystemEventHandler):
    # nel costruttore salvo il valore di path, che rappresnta
    # la directory principale da osservare
    def __init__(self, path, dest):
        self.path = path
        self.dest = dest

    # questo metodo è utilizzato unicamente per estrarre il
    # percorso relativo da un percorso assoluto, utilizzando
    # 'self.path'
    def relativePath(self, full):
        return os.path.relpath(full, self.path)

    def log(self, paths, event):
        if event == 'moved':
            print(paths[0], "moved to", paths[1])
        else :
            print(paths[0], event)

    # metodo principale, maggiori dettagli nel corpo
    def process(self, event):
        # le due variabili locali che seguono hanno lo scopo
        # di rendere il codice più leggibile, ricopiano identici
        # i valori presenti nella struttura event
        eventType = event.event_type
        srcPath = self.relativePath(event.src_path)
        if eventType == 'moved' :
            destPath = self.relativePath(event.dest_path)
            #self.log([self.relativePath(srcPath),
            #          self.relativePath(destPath)],
            #         eventType)
            self.move(srcPath, destPath)
        else:
            #self.log([self.relativePath(srcPath)],
            #         eventType)
            self.modify(srcPath)

    def move(self, srcPath, destPath):
        print("moving " + self.dest + srcPath + " to " + self.dest + destPath)

    def modify(self, srcPath):
        print("updating " + self.dest + srcPath + " as " + self.path + srcPath)

    # metodo virtuale definito nella classe principale
    # recepisce ogni evento che avviena nella directory osservata
    def on_any_event(self, event):
        # variabile locale per controllare se un evento riguarda
        # una directory
        isADir = event.is_directory
        # variabile locale per controllare se l'evento in questione
        # è una modifica
        isModified = (event.event_type == 'modified')
        # in caso si tratti di un vetento modifica di una directory
        # lo ignoriamo, non è interessante per quello che vogliamo
        # fare in questo programma
        if not (isADir and isModified):
            # chiamata alla funzione cuore della classe
            self.process(event)

if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    path = args[0] if args else '.'
    observer.schedule(MyHandler(path), path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
