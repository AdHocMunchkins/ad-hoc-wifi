import subprocess
import threading
import datetime
import os

lock = threading.Lock()

times = []


def scp(username, password, ip, src_path):
    start = datetime.datetime.now()
    subprocess.check_output("sshpass -p '%s' scp %s %s@%s:~" % (password, src_path, username, ip), shell=True)
    end = datetime.datetime.now()

    time_taken = (end - start).total_seconds()

    lock.acquire()
    times.append((ip, os.path.getsize(src_path), time_taken))
    lock.release()


def main():
    path = input("Enter path to file to send: ")
    n = int(input("Enter number of recipients: "))
    l = []
    for i in range(n):
        print("Handling recipient", i + 1)
        username = input("Enter username: ")
        password = input("Enter password: ")
        ip = input("Enter ip: ")
        l.append((username, password, ip, path))

    threads = [threading.Thread(target=scp, args=params) for params in l]
    list(map(lambda thread: thread.start(), threads))

    for thread in threads:
        thread.join()

    for time in times:
        print("Transfer to", time[0], "took", time[2], "seconds, at a rate of", time[1] / time[2] / 10 ** 6, "MB/s")


main()
