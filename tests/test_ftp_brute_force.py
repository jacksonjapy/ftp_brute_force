from ftp_brute_force import FtpBruteForce

if __name__ == '__main__':
    fbf = FtpBruteForce("192.168.1.1", r"user.dic", r"password.dic")
    fbf.connection()
    fbf.brute()
