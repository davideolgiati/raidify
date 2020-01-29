import os   # os.path.relpath
import shutil
from watchdog.events import FileSystemEventHandler # <--

# la calsse 'MyHandler' serve per gestire gli eventi registrati
# dalla libreria watchdog.
# Estende la classe 'FileSystemEventHandler' che è la classe
# più basilare presnte nella libreria, controlla ogni cambaimento
# senza filtraggio
class MyHandler(FileSystemEventHandler):
    # nel costruttore salvo il valore di path, che rappresnta
    # la directory principale da osservare
    def __init__(self, path, dest, setup):
        self.path = path
        self.dest = dest
        self.dryrun = (setup & 2) == 2
        self.verbose = (setup & (1 << 3)) & (1 << 3)
        if (setup & 4) == 4: # init flag attivo
            dirs = []
            files = []
            dirs, files = self.dirWalk(path, dest, dirs, files)
            dirs, files = self.dirWalk(dest, path, dirs, files)
            if self.verbose : print("\nDIRS to be duplicated: ")
            for dir in dirs:
                test = os.path.isdir(dir)
                if not test:
                    if self.verbose : print("\t" + dir)
                    os.mkdir(dir)

            if self.verbose : print("\nFILES to be duplicated: ")
            for dst in files:
                src = os.path.join(path,
                                   os.path.relpath(dst,
                                                   dest))
                test = os.path.isfile(dst)
                if not test:
                    if self.verbose : print("\t" + dst)
                    shutil.copy2(src, dst)

    def dirWalk(self, main, dest, dirs, files):
        for dir_path, dir_names, file_names in os.walk(main):
            for dir in dir_names:
                new_path = os.path.join(dest, dir)
                if (not new_path in dirs) and dir != ".":
                    dirs.append(new_path)
            for f in file_names:
                rel_path = os.path.relpath(dir_path, main)
                new_path = os.path.join(dest, rel_path)
                if rel_path == "." :
                    new_file = os.path.join(dest ,f)
                else :
                    new_file = os.path.join(new_path ,f)
                files.append(new_file)
        return dirs, files

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
            self.log([self.relativePath(srcPath),
                      self.relativePath(destPath)],
                     eventType)
            self.move(srcPath, destPath)
        else:
            self.log([self.relativePath(srcPath)],
                     eventType)
            if not (not event.is_directory and eventType == 'created'):
                self.modify(srcPath, eventType)

    def move(self, srcPath, destPath):
        oldPath = os.path.join(self.dest, srcPath)
        newPath = os.path.join(self.dest, destPath)
        shutil.move(oldPath, newPath)

    def modify(self, srcPath, event):
        source = os.path.join(self.path, srcPath)
        dest = os.path.join(self.dest, srcPath)
        shutil.copyfile(source, dest)

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
