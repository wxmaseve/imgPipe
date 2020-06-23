import time
import datetime
import os

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

except ModuleNotFoundError as e:
    print (e)
    os.system("pip install watchdog")

class Handler(FileSystemEventHandler):

    def on_created(self, event): # 파일 생성시

        if event.is_directory:
            realPath = os.path.realpath(event.src_path)
            baseName = os.path.basename(event.src_path)

            print(f'event type : {event.event_type}\n'
                  f'event src_path : {realPath}\n'
                  f'base name : {baseName}')

            if baseName.startswith('RQ') > 0:
                file_list = os.listdir(event.src_path)
                file_list_png = [file for file in file_list if file.lower().endswith(".png")]

                print("png file lists : {}".format(file_list_png))

    def on_moved(self, event): # 파일 이동시
        
        if event.is_directory:
            realPath = os.path.realpath(event.dest_path)
            baseName = os.path.basename(event.dest_path)

            print(f'event type : {event.event_type}\n'
                  f'event src_path : {realPath}\n'
                  f'base name : {baseName}')

            if baseName.startswith('RQ') > 0:
                file_list = os.listdir(event.dest_path)
                file_list_png = [file for file in file_list if file.lower().endswith(".png")]

                print("png file lists : {}".format(file_list_png))

    #def on_deleted(self, event):

class Watcher:

    def __init__(self, path):

        print("감시 중 ...")

        self.event_handler = None      # Handler
        self.observer = Observer()     # Observer 객체 생성
        self.target_directory = path   # 감시대상 경로
        self.currentDirectorySetting() # instance method 호출 func(1)

    def currentDirectorySetting(self):

        print ("====================================")
        print ("현재 작업 디렉토리:  ", end=" ")
        os.chdir(self.target_directory)
        print ("{cwd}".format(cwd = os.getcwd()))
        print ("====================================")

    def run(self):

        self.event_handler = Handler() # 이벤트 핸들러 객체 생성
        self.observer.schedule(
            self.event_handler,
            self.target_directory,
            recursive=True
        )

        self.observer.start() # 감시 시작

        try:
            while True: # 무한 루프
                time.sleep(0.1) # 1초 마다 대상 디렉토리 감시

        except KeyboardInterrupt as e: # 사용자에 의해 "ctrl + z" 발생시
            print ("감시 중지...")
            self.observer.stop() # 감시 중단

myWatcher = Watcher("./")

myWatcher.run()

