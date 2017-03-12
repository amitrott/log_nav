import re

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
        self.y += 1
        return self.file.readline()

    def move_down(self,n=1):
        i = 0
        while(i < n):
            self.current_line = self.readline()
            i += 1
        return

    def move_up(self,n=1):
        target_pos = self.y - n
        if target_pos < 0: print("Reached start of file, cannot move up!"); return
        elif target_pos == 0:
            self.go_to_start()
            self.current_line = self.readline()
            return
        else: self.go_to_start()

        while(self.y < target_pos):
            self.current_line = self.readline()
        return

    def move_down_until_regex(self,patt):
        regex = re.compile(patt)
        self.move_down()

        while(regex.match(self.current_line) is None and self.current_line is not ""):
            self.move_down()

        self.current_line = "End of file reached with no match for "+patt \
                        if self.current_line is "" else self.current_line
        return

    def move_up_until_regex(self,patt):
        regex = re.compile(patt)
        self.move_up()
        i = self.y

        while (regex.match(self.current_line) is None and i >= 0):
            self.move_up()
            i -= 1

        self.current_line = "Start of file reached with no match for " + patt \
                        if i < 0 else self.current_line
        return


with Log_Nav("/home/angelo/PycharmProjects/log_nav/text_samples/line_counts.txt") as log_nav:
    print(log_nav.current_line)
    log_nav.move_down_until_regex("fifth")
    print(log_nav.current_line)
    log_nav.move_up_until_regex(".*ir.*")
    print(log_nav.current_line)