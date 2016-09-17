import socket

def get_lan_ip():
    try:
        return ([(
            s.connect(('8.8.8.8', 80)),
            s.getsockname()[0], s.close()) for s in [socket.socket(
                socket.AF_INET,
                socket.SOCK_DGRAM
            )]
        ][0][1])
    except socket.error as e:
        sys.stderr.write(str(e) + "\n")
        sys.exit(e.errno)
