import re
import math

class Log_Nav():

    def __init__(self,fname):
        self.x = 0
        self.y = 0
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

    def go_to_start(self):
        self.x = 0
        self.y = 0
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
        self.current_line = self.file.readline()
        return

    def move_down(self,n=1):
        i = 0
        while(i < n):
            self.readline()
            self.y += 1
            i += 1
            if self.current_line is "":
                print("End of file reached, cannot move down!")
                break
        return

    def move_up(self,n=1):
        target_pos = self.y - n
        if target_pos < 0: print("Reached start of file, cannot move up!"); return
        elif target_pos == 0:
            self.go_to_start()
            self.readline()
            return
        else: self.go_to_start()

        while(self.y < target_pos):
            self.readline()
            self.y += 1
        return

    def move_down_until_regex(self,patt):
        regex = re.compile(patt)

        while(regex.match(self.current_line) is None and self.current_line is not ""):
            self.move_down()

        if self.current_line is "":
            print("End of file reached with no match for " + patt)
        return

    def move_up_until_regex(self,patt):
        regex = re.compile(patt)
        i = self.y

        while (regex.match(self.current_line) is None and i >= 0):
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

    def tabbed_regex(self,patt,name="regex_0",group=1):
        regex = re.compile(patt)
        for line in self.iter_tabbed():
            if(regex.search(line) is not None):
                result = regex.match(line)
                self.set_property(name,result.group(group))
                self.exit_tabbed()
                break
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


with Log_Nav("/home/angelo/PycharmProjects/log_nav/text_samples/ccsip-ccapi-ccsip.txt") as log_nav:
    log_nav.move_down_until_regex("INVITE sip")
    log_nav.set_property("called",log_nav.value_from_regex("INVITE sip:(.*)@"))
    log_nav.move_down_until_regex(log_nav.compile_compound_regex(".*dest={{called}}"))
    log_nav.move_up_until_regex(".*//.*/[A-F0-9]+/CCAPI")
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