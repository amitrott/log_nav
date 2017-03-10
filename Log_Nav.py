class Log_Nav():

    def __init__(self,fname):
        self.x = 0
        self.y = 0
        self.A = 0
        self.B = 0
        self.current_line = None
        self.filename = fname
        return

    def __enter__(self):
        # http://stackoverflow.com/questions/865115/how-do-i-correctly-clean-up-a-python-object
        self.open_file()
        self.current_line = self.readline()
        return self

    def open_file(self):
        self.file = open(self.filename,'r')
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        return

    def go_to_start(self):
        self.x = 0
        self.y = 0
        self.file.seek(0)
        self.current_line = self.readline()
        return

    def readline(self):
        return self.file.readline()

    def move_down(self,n=1):
        i = 0
        while(i < n):
            self.current_line = self.readline()
            self.y += 1
            i += 1

    def move_up(self,n=1):
        target_pos = self.y - n
        if target_pos < 0: print("Reached start of file, cannot move up!"); return
        elif target_pos == 0:
            self.go_to_start()
            self.current_line = self.readline()
            return
        else: self.go_to_start()

        while(self.y < target_pos):
            self.y += 1
            self.current_line = self.readline()
        return


with Log_Nav("/home/angelo/PycharmProjects/log_nav/text_samples/line_counts.txt") as log_nav:
    print(log_nav.current_line)
    log_nav.move_down(3)
    print(log_nav.current_line)
    log_nav.move_up(2)
    print(log_nav.current_line)