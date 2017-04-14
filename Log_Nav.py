'''
Copyright 2017 Angelo Mitrotti

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

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
        self.move_down_until_regex(patt)
        while self.current_line is not "":
            curr_line = self.y
            cb_fn()
            self.go_to_line(curr_line + 1,False)
            self.move_down_until_regex(patt)

        self.go_to_line(orig_line,False)

        return

    def test_regex(self,patt):
        regex = re.compile(patt)
        return regex.search(self.current_line)


