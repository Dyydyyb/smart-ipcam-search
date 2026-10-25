import socket

def test():
    ports = [80, 443, 5199, 8000, 8554, 1935, 8888, 8889]
    for p in ports:
        s = socket.socket()
        s.settimeout(2.0)
        res = s.connect_ex(('66.97.44.166', p))
        s.close()
        status = "OPEN" if res == 0 else f"BLOCKED ({res})"
        print(f"Port {p}: {status}")

if __name__ == '__main__':
    test()
