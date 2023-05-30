import socket
from multiprocessing.pool import ThreadPool

import packages


def get_protocol(data: bytes):
    ntp_signature = b"\x1c"
    dns_signature = b"\x00\x07exa"
    smtp_signature = b"220"
    pop3_signature = b"+OK\r\n"
    imap_signature = b"\x2A\x20\x4F\x4B\x20\x49\x4D\x41\x50"
    ssh_signature = b"SSH"

    if data.startswith(ntp_signature):
        return "NTP"
    elif data.endswith(dns_signature):
        return "DNS"
    elif data.startswith(smtp_signature):
        return "SMTP"
    elif data.startswith(pop3_signature):
        return "POP3"
    elif data.startswith(imap_signature):
        return "IMAP"
    elif data.startswith(ssh_signature):
        return "SSH"
    else:
        return ""


def check_port(host: str, mode: str, port: int):
    if mode == "u":
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            try:
                sock.settimeout(0.5)
                for package in packages.get_packs():
                    sock.sendto(package, (host, port))
                    data, _ = sock.recvfrom(1024)
                    print(f"UDP {port} {get_protocol(data)}")
                    return
            except socket.timeout:
                pass
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            connected = False
            try:
                sock.settimeout(0.5)
                sock.connect((host, port))
                connected = True
                data, _ = sock.recvfrom(1024)
                print(f"TCP {port} {get_protocol(data)}")
            except socket.error:
                if connected:
                    sock.sendto(packages.HTTP_PACKET, (host, port))
                    data, _ = sock.recvfrom(1024)
                    if data.startswith(b'HTTP/1.1'):
                        print(f"TCP {port} HTTP")
                        return
                    print(f'TCP {port}')


def start_scaner(host: str, mode: str, ports: tuple):
    threadpool = ThreadPool(processes=10)
    try:
        threads = []
        for port in range(int(ports[0]), int(ports[1]) + 1):
            thread = threadpool.apply_async(check_port, args=(host, mode, port))
            threads.append(thread)
        for thread in threads:
            thread.wait()
    finally:
        threadpool.terminate()
        threadpool.join()
