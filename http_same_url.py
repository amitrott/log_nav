from Log_Nav import Log_Nav

# http://www.isi.csic.es/dataset/
with Log_Nav("/home/angelo/Downloads/http-dataset/normalTrafficTraining.txt") as http_log:

    '''
    Extract all HTTP messages that include URL 'tienda1/publico/miembros.jsp'
    
    The resulting output is reduced from ~20MB to ~500kB, containing only POST/GET requests to this URL
    '''

    def each_postget():
        while http_log.current_line is not "\n":
            print(http_log.current_line, end="")
            http_log.move_down()
        print()

    http_log.for_each_pattern("^POST.*tienda1/publico/miembros\.jsp|^GET.*tienda1/publico/miembros\.jsp",each_postget)