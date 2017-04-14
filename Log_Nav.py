import re
import math

class Log_Nav():

    def __init__(self,fname):

        self.BUFFER_SIZE = 10 # lines
        self.buffer_y = 0
        self.buffer = []

        self.x = 0
        self.y = -1
        self.A = 0
        self.B = 0
        self.current_line = None
        self.filename = fname
        self.output = []
        self.dict = {}
        return

    def __enter__(self):
        # http://stackoverflow.com/questions/865115/how-do-i-correctly-clean-up-a-python-object
        self.open_file()
        self.readline()
        return self

    def open_file(self):
        self.file = open(self.filename,'r')
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        return

    def load_buffer(self,new_y):
        if (new_y == self.y or new_y <= self.buffer_y) and self.buffer_y > 0:
            return
        elif new_y < self.y:
            groups_to_read = math.ceil(new_y / self.BUFFER_SIZE)
            self.file.seek(0)
            self.buffer_y = 0
            while groups_to_read > 0:
                self.buffer = []
                for _ in range(0,self.BUFFER_SIZE):
                    self.buffer.append(self.file.readline())
                    self.buffer_y += 1
                groups_to_read -= 1
        else:
            groups_to_read = math.ceil((new_y - self.y) / self.BUFFER_SIZE)
            while groups_to_read > 0:
                self.buffer = []
                for _ in range(0,self.BUFFER_SIZE):
                    self.buffer.append(self.file.readline())
                    self.buffer_y += 1
                groups_to_read -= 1
        return

    def go_to_start(self):
        self.x = 0
        self.y = -1
        self.buffer_y = 0
        self.file.seek(0)
        self.readline()
        return

    def go_to_end(self):
        while(self.current_line is not ""):
            self.readline()
            self.y += 1
        self.move_up()
        return

    def go_to_line(self,l,starts_in_one = True):
        l = l - 1 if starts_in_one else l
        if l == self.y:
            return
        elif l < self.y:
            self.go_to_start()
            self.move_down(l)
        else:
            self.move_down(l - self.y)
        return

    def readline(self):
        self.load_buffer(self.y + 1)
        if self.y < 0:
            self.y += 1
        if self.BUFFER_SIZE > 0 and self.buffer_y > 0:
            self.current_line = self.buffer[abs(self.buffer_y - self.y - self.BUFFER_SIZE)]
        else:
            self.current_line = self.buffer[0]
        return

    def move_down(self,n=1):
        i = 0
        while(i < n):
            self.y += 1
            self.readline()
            i += 1
            if self.current_line is "":
                print("End of file reached, cannot move down!")
                break
        return

    def move_up(self,n=1):
        target_pos = self.y - n
        if target_pos < 0: print("Reached start of file, cannot move up!"); self.go_to_start(); return
        elif target_pos == 0:
            self.go_to_start()
            return

        if target_pos >= self.buffer_y:
            while target_pos < self.y:
                self.y -= 1
                self.current_line = self.buffer[abs(self.buffer_y - ( self.y + 1 ) - self.BUFFER_SIZE)]
        else:
            self.go_to_start()
            self.move_down(target_pos)
        return

    def move_down_until_regex(self,patt,max_lines=0):
        regex = re.compile(patt)

        i = 0
        while(regex.match(self.current_line) is None and self.current_line is not ""):
            if(max_lines > 0 and i >= max_lines):
                break
            self.move_down()
            i += 1

        if self.current_line is "":
            print("End of file reached with no match for " + patt)
        return

    def move_up_until_regex(self,patt,max_lines=0):
        regex = re.compile(patt)
        i = self.y

        top = self.y - max_lines

        while (regex.match(self.current_line) is None and i >= 0):
            if(max_lines != 0 and i <= top):
                break
            self.move_up()
            i -= 1

        if i < 0:
            print("Start of file reached with no match for " + patt)
        return

    def iter_tabbed(self):
        regex = re.compile("^\s+(.*)")

        self.move_down()
        while(regex.search(self.current_line) is not None):
            result = regex.match(self.current_line)
            self.move_down()
            yield result.group(1)

        return

    def exit_tabbed(self):
        regex = re.compile("^[^\s]")

        while(regex.search(self.current_line) is not None):
            self.move_down()

        return

    def tabbed_regex(self,patt,name="regex_0",group=1,reset_position=False):
        if reset_position:
            original_line = self.y
        regex = re.compile(patt)
        for line in self.iter_tabbed():
            if(regex.search(line) is not None):
                result = regex.match(line)
                self.set_property(name,result.group(group))
                self.exit_tabbed()
                break
        if reset_position:
            self.go_to_line(original_line,False)
        return

    def append_to_output(self,text=None,whole_line=True):
        if whole_line:
            self.output.append(self.current_line)
        else:
            self.output.append(text)
        return

    def get_output(self):
        return self.output

    def get_dict(self):
        return self.dict

    def set_property(self,name,value):
        self.dict[name] = value
        return

    def get_property(self,name):
        return self.dict[name]

    def value_from_regex(self,patt,group=1):
        regex = re.compile(patt)
        result = regex.match(self.current_line)
        return result.group(group)

    def compile_compound_regex(self,patt):
        # .*dest={{name}}.*
        find_properties_regex = re.compile(".*\{\{(.*)\}\}.*")
        properties = find_properties_regex.findall(patt)
        for prop in properties:
            patt = str(patt).replace("{{"+prop+"}}",self.dict[prop])
        return patt

    def for_each_pattern(self,patt,cb_fn):
        orig_line = self.y

        self.go_to_start()
        while self.current_line is not "":
            self.move_down_until_regex(patt)
            curr_line = self.y
            cb_fn()
            self.go_to_line(curr_line + 1,False)

        self.go_to_line(orig_line,False)

        return


with Log_Nav("/home/angelo/PycharmProjects/log_nav/text_samples/ccsip-ccapi-ccsip.txt") as log_nav:

    def callback_function():
        log_nav.move_up_until_regex("(?!Via).*SIP/2\.0.*")
        print(log_nav.current_line + "  line: "+str(log_nav.y))
        return

    log_nav.for_each_pattern("Call-ID",callback_function)

    exit()

with Log_Nav("/home/angelo/PycharmProjects/log_nav/text_samples/ccsip-ccapi-ccsip.txt") as log_nav:
    log_nav.move_down_until_regex("zzzzzzz")
    #print(log_nav.current_line)
    print(log_nav.current_line+" "+str(log_nav.y))
    log_nav.move_up_until_regex("zzzzzzz",5)
    print(log_nav.current_line+" "+str(log_nav.y))
    exit()

with Log_Nav("/home/angelo/PycharmProjects/log_nav/text_samples/ccsip-ccapi-ccsip.txt") as log_nav:
    log_nav.move_down_until_regex("INVITE sip")
    log_nav.set_property("called",log_nav.value_from_regex("INVITE sip:(.*)@"))
    log_nav.move_down_until_regex(log_nav.compile_compound_regex(".*dest={{called}}"))
    log_nav.move_up_until_regex(".*//.*/[A-F0-9]+/CCAPI")

    print(log_nav.current_line)
    log_nav.tabbed_regex("dest=(.*)","destination",reset_position=True)
    print(log_nav.get_property("destination"))
    print(log_nav.current_line)
    log_nav.tabbed_regex(".*ani=(.*)","cisco-ani",reset_position=True)
    print(log_nav.get_property("cisco-ani"))
    print(log_nav.current_line)
    exit()

    log_nav.set_property("ccapi_id", log_nav.value_from_regex(".*//.*/([A-F0-9]+)/CCAPI"))
    log_nav.move_down_until_regex(log_nav.compile_compound_regex(".*//.*/{{ccapi_id}}/CCAPI/cc_api_call_disconnected"))
    log_nav.tabbed_regex("Cause Value=([0-9]+)","release_code",1)
    print(log_nav.get_property("release_code"))

with Log_Nav("/home/angelo/PycharmProjects/log_nav/text_samples/line_counts_tabbed.txt") as log_nav:
    log_nav.append_to_output()#print(log_nav.current_line)
    log_nav.go_to_end()
    log_nav.move_down()
    log_nav.append_to_output()#print(log_nav.current_line)
    log_nav.move_up_until_regex(".*ir.*")
    log_nav.append_to_output()#print(log_nav.current_line)
    print(log_nav.get_output())

    log_nav.set_property("test",log_nav.value_from_regex(".*(rd).*"))
    print(log_nav.get_dict())

    '''log_nav.go_to_start()
    for match in log_nav.iter_tabbed():
        print(match)'''

    log_nav.go_to_start()
    log_nav.tabbed_regex(".*dest=(.*)")

    log_nav.append_to_output(log_nav.get_property("regex_0"),False)
    print(log_nav.get_output())

    print(log_nav.compile_compound_regex("this is test's value: {{test}}"))

    log_nav.go_to_start()
    log_nav.go_to_line(7)
    print(log_nav.current_line)