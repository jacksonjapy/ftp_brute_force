from typing import Iterator, Tuple, Optional, overload

@overload
def load_dict(user_dict_path: str, password_dict_path: str) -> Iterator[Tuple[str, str]]: ...

@overload
def load_dict(user_dict_path: None, password_dict_path: None) -> None: ...

def load_dict(user_dict_path: Optional[str], password_dict_path: Optional[str]) -> Optional[Iterator[Tuple[str, str]]]:
    """
    :param user_dict_path: The path of the username dictionary file.
    :param password_dict_path: The path of the password dictionary file.
    :return: Iterator for username and password.
    """
    ...
