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
    log_nav.move_down_until_regex(".*CCAPI.*",stop_patt="[0-9]+:")
    print(log_nav.current_line)
    log_nav.move_down_until_regex(".*term def len.*")
    print(log_nav.current_line)
    log_nav.move_up_until_regex(".*CCAPI.*",stop_patt="[0-9]+:")
    print(log_nav.current_line)
    exit()

with Log_Nav("/home/angelo/PycharmProjects/log_nav/text_samples/ccsip-ccapi-ccsip.txt") as log_nav:

    def callback_function():
        log_nav.move_up_until_regex("(?!Via).*SIP/2\.0.*")
        if not log_nav.test_regex("SIP/2\.0 1") and not log_nav.test_regex("SIP/2\.0 2"):
            print(log_nav.current_line + "  line: "+str(log_nav.y))
        return

    log_nav.move_down_until_regex("Call-ID")
    log_nav.set_property("callid",log_nav.value_from_regex("Call-ID: (.*)"))

    log_nav.for_each_pattern(log_nav.compile_compound_regex("Call-ID: {{callid}}"),callback_function)

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