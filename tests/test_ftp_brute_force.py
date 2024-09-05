from ftp_brute_force import FtpBruteForce

if __name__ == '__main__':
    server_address = "192.168.1.1"
    user_dict = r"user.dic"
    password_dict = r"password.dic"
    fbf = FtpBruteForce(server_address, user_dict, password_dict)
    user_tuple, password_tuple = fbf.load_dict()
    fbf.connection()
    fbf.brute(user_tuple, password_tuple)
