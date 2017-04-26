from Log_Nav import Log_Nav
import re

with Log_Nav(r"/home/angelo/PycharmProjects/log_nav/text_samples/SHOW_FLASH.txt") as fl:

    name = "SEP.*xml"
    bytes = 0

    def count():
        bytes_regex = re.compile("[0-9]+\s+([0-9]+)")
        global bytes
        bytes += int(bytes_regex.match(fl.current_line).group(1))
        return

    fl.for_each_pattern(".*"+name,count)

    print("bytes for "+name+": "+str(bytes))
    print("kbytes for "+name+": "+str(bytes/1024))