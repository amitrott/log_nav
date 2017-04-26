from Log_Nav import Log_Nav

with Log_Nav("/home/angelo/PycharmProjects/log_nav/text_samples/ccsip-ccapi-ccsip.txt") as ccapi:

    calling = '1001'
    called  = '3000'

    ccapi.move_down_until_regex(".*dest="+called)
    ccapi.move_up_until_regex(".*ani="+calling,stop_patt=".*/CCAPI/")

    ccapi.move_up_until_regex(".*/CCAPI/",stop_patt="[0-9]+:")
    ccapi.set_property("call_id",ccapi.value_from_regex(".*/([A-F0-9]+)/CCAPI/"))

    ccapi.move_down_until_regex(ccapi.compile_compound_regex(".*{{call_id}}.*cc_api_call_disconnected"))
    ccapi.tabbed_regex(".*Cause Value=([0-9]+)","cc")

    if int(ccapi.get_property("cc")) > 0:
        print(ccapi.get_property("cc"))
    else:
        print("no release code found")