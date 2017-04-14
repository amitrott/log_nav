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

from Log_Nav import Log_Nav

with Log_Nav("/home/angelo/PycharmProjects/log_nav/text_samples/ccsip-ccapi-ccsip.txt") as log_nav:

    def extract_leg_callid():
        log_nav.move_up_until_regex("^Sent|^Received")
        if "Sent" in log_nav.current_line:
            log_nav.move_down_until_regex("Call-ID: (.*)")
            log_nav.set_property("callid",log_nav.value_from_regex("Call-ID: (.*)"))
        return

    log_nav.for_each_pattern(".*TE sip",extract_leg_callid)

    def extract_leg():
        log_nav.move_down_until_regex("Content-Length")
        length = int(log_nav.value_from_regex("Content-Length: ([0-9]+)"))
        log_nav.move_up_until_regex("^Sent|^Received")
        i = 0 if length > 0 else 1
        while log_nav.current_line is not "\n" or i == 0:
            if log_nav.current_line == "\n":
                i += 1
            log_nav.append_to_output(None,True)
            log_nav.move_down()
        log_nav.append_to_output("\n",False)
        return

    log_nav.for_each_pattern(log_nav.compile_compound_regex("Call-ID: {{callid}}"),extract_leg)

    for line in log_nav.output:
        print(line,end="")