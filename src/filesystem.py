"""Module containing filesystem interface logic, used to move, copy and
delete files"""

import os  # os.path.relpath
import shutil
from watchdog.events import FileSystemEventHandler  # <--


# La classe 'MyHandler' serve per gestire gli eventi registrati
# dalla libreria watchdog.
# Estende la classe 'FileSystemEventHandler', controlla ogni
# cambiamento senza distinzione


class MyHandler(FileSystemEventHandler):
    """Main filesystem watchdog class"""
    # nel costruttore salvo il valore di path, che rappresenta
    # la directory principale da osservare
    def __init__(self, path, dst, setup):
        """Class constructor, used to initialize the instance
        with correct parameters"""
        self.path = path
        self.dst = dst
        self.dry_run = (setup & 2) == 2
        self.verbose = (setup & (1 << 3)) & (1 << 3)
        if (setup & 4) == 4:  # init flag attivo
            dirs = []
            files = []
            dirs, files = self.dir_walk(path, dst, dirs, files)
            dirs, files = self.dir_walk(dst, path, dirs, files)
            if self.verbose:
                print("\nDIRS to be duplicated: ")
            for current_dir in dirs:
                test = os.path.isdir(current_dir)
                if not test:
                    if self.verbose:
                        print("\t" + current_dir)
                    os.mkdir(current_dir)

            if self.verbose:
                print("\nFILES to be duplicated: ")
            for dst_file in files:
                src = os.path.join(path,
                                   os.path.relpath(dst_file,
                                                   dst))
                if not os.path.isfile(dst_file):
                    if self.verbose:
                        print("\t" + dst_file)
                    shutil.copy2(src, dst)

    @staticmethod
    def dir_walk(main, dst, dirs, files):
        """Method used to explore a directory in order  to track file"""
        for dir_path, dir_names, file_names in os.walk(main):
            for current_dir in dir_names:
                new_path = os.path.join(dst, current_dir)
                if (new_path not in dirs) and current_dir != ".":
                    dirs.append(new_path)
            for _file in file_names:
                rel_path = os.path.relpath(dir_path, main)
                new_path = os.path.join(dst, rel_path)
                if rel_path == ".":
                    new_file = os.path.join(dst, _file)
                else:
                    new_file = os.path.join(new_path, _file)
                files.append(new_file)
        return dirs, files

    # questo metodo è utilizzato unicamente per estrarre il
    # percorso relativo da un percorso assoluto, utilizzando
    # 'self.path'
    def relative_path(self, full):
        """Wrapper method to extract relative path within a directory"""
        return os.path.relpath(full, self.path)

    @staticmethod
    def log(paths, event):
        """Static method used to log watchdog event"""
        if event == 'moved':
            print(paths[0], "moved to", paths[1])
        else:
            print(paths[0], event)

    # metodo principale, maggiori dettagli nel corpo
    def process(self, event):
        """Main method, used to decide how to respond to an event tracked by
        the watchdog"""
        # le due variabili locali che seguono hanno lo scopo
        # di rendere il codice più leggibile, ricopiano identici
        # i valori presenti nella struttura event
        event_type = event.event_type
        src_path = self.relative_path(event.src_path)
        if event_type == 'moved':
            dst_path = self.relative_path(event.dest_path)
            self.log([self.relative_path(src_path),
                      self.relative_path(dst_path)],
                     event_type)
            self.move(src_path, dst_path)
        else:
            self.log([self.relative_path(src_path)],
                     event_type)
            if not (not event.is_directory and event_type == 'created'):
                self.modify(src_path, event_type)

    def move(self, src_path, dst_path):
        """File is moved action"""
        old_path = os.path.join(self.dst, src_path)
        new_path = os.path.join(self.dst, dst_path)
        shutil.move(old_path, new_path)

    def modify(self, src_path, event):
        """File is modified action"""
        source = os.path.join(self.path, src_path)
        dst = os.path.join(self.dst, src_path)
        if event == 'creation' and os.path.isdir(source):
            os.mkdir(dst)
        elif event == 'delete':
            os.remove(dst)
        else:
            shutil.copyfile(source, dst)

    # metodo virtuale definito nella classe principale
    # recepisce ogni evento che avviene nella directory osservata
    def on_any_event(self, event):
        """Override method used as entrypoint to track filesystem events"""
        # variabile locale per controllare se un evento riguarda
        # una directory
        is_a_dir = event.is_directory
        # variabile locale per controllare se l'evento in questione
        # è una modifica
        is_modified = (event.event_type == 'modified')
        # in caso si tratti di un evento modifica di una directory
        # lo ignoriamo, non è interessante per quello che vogliamo
        # fare in questo programma
        if not (is_a_dir and is_modified):
            # chiamata alla funzione cuore della classe
            self.process(event)
