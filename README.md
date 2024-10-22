# ftp_brute_force

`ftp_brute_force` is a tool designed for performing FTP brute force attacks.

## Installation

You can install it via `pip`:

```bash
pip install ftp_brute
```

## Usage Instructions

### Basic Usage

You can import and use the tool as follows:

```python
from ftp_brute_force import FtpBruteForce
```

### Example

```python
from ftp_brute_force import FtpBruteForce

if __name__ == '__main__':
    fbf = FtpBruteForce("192.168.1.1", r"user.dic", r"password.dic")
    fbf.load_dict()
    fbf.connection()
    fbf.brute()
```

## Options

- `server_address`: The IP address of the target FTP server.
- `user_dict`: Path to the user dictionary for brute forcing.
- `password_dict`: Path to the password dictionary for brute forcing.

## Dependencies

- Python 3.10 or higher
- `ftplib` (built-in Python module)
- `socket` (built-in Python module)
- `time` (built-in Python module)
- `os` (built-in Python module)
```
Let me know if you'd like to make any changes!
```
## GitHub Repository
[GitHub](https://github.com/jacksonjapy/ftp_brute_force)

## Change Log
For details, see the [CHANGELOG](CHANGELOG.md).