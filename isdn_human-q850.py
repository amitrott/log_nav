from Log_Nav import Log_Nav

with Log_Nav(r"/home/angelo/PycharmProjects/log_nav/text_samples/deoli_debugs.txt") as q850:

    '''
    https://supportforums.cisco.com/discussion/11690201/help-needed-connecting-isdn-bri-channel-isdn-pri-e1-channel-all-debugs-and
    
    Print calling/called numbers and human-readable Q.850 code
    '''

    def handle():
        isdn_id = q850.value_from_regex(".*0x[0-9A-F]([0-9A-F]+)")

        print(q850.current_line,end="")

        orig_pos = q850.y
        def x_calling_ed(ing_ed,l):
            q850.move_down_until_regex(".*all"+ing_ed+".*'",stop_patt="ISDN(?!.*0x."+str(isdn_id)+").*0x")
            if q850.test_regex(".*all.*'") is not None:
                print(q850.current_line)
            q850.go_to_line(l)

        x_calling_ed("ing",orig_pos)
        x_calling_ed("ed",orig_pos)

        q850.move_down_until_regex(".*(RELE.*|DISCO.*)0x."+str(isdn_id))
        print(q850.current_line,end="")
        q850.move_down_until_regex(".*ause i")
        print(q850.current_line)

    q850.for_each_pattern(".*X.*SETUP(?!.*ACK)",handle)



with Log_Nav(r"/home/angelo/PycharmProjects/log_nav/text_samples/34004-sh_and_debug.txt") as q850:
    '''
    Reuse code:
    https://supportforums.cisco.com/discussion/9602911/please-help-me-i-have-probleme-call-pstn
    
    Print calling/called numbers and human-readable Q.850 code
    
    NOTE: fine-tuning might be needed when reusing scripts, to generalize correctly
    '''

    print()
    print("Reusing Code ...")
    print()

    def handle():
        isdn_id = q850.value_from_regex(".*0x[0-9A-F]([0-9A-F]+)")

        print(q850.current_line, end="")

        orig_pos = q850.y

        def x_calling_ed(ing_ed, l):
            q850.move_down_until_regex(".*all" + ing_ed + ".*'", stop_patt="ISDN(?!.*0x." + str(isdn_id) + ").*0x")
            if q850.test_regex(".*all.*'") is not None:
                print(q850.current_line)
            q850.go_to_line(l)

        x_calling_ed("ing", orig_pos)
        x_calling_ed("ed", orig_pos)

        q850.move_down_until_regex(".*(RELE.*|DISCO.*)0x." + str(isdn_id))
        print(q850.current_line, end="")
        q850.move_down_until_regex(".*ause i")
        print(q850.current_line)


    q850.for_each_pattern(".*X.*SETUP(?!.*ACK)", handle)