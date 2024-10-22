## 0.1.0 

### 2024-09-05 

#### 1. Initial Release

## 0.1.1 

### 2024-09-18 

#### 1. Fixed the error of excessively long module name during import

- Changed from

	```python
	from ftp_brute_force.ftp_brute import FtpBruteForce
	```

- To

	```python
	from ftp_brute_force import FtpBruteForce
	```

#### 2. Added Command Line Interface (CLI) Usage
- `s` Server address
- `port` FTP service port of the server, defaults to 21
- `u` Path to the user dictionary file
- `password` Path to the password dictionary file
- `v` Display version information
- `h` Display help information

##### How to usage
- Linux / Mac OS / Windows

	```shell
	ftp_brute_force -s (server_address) --port (server_port) -u (user_dict_path) --password (password_dict_path)
	```

## 0.1.2
### 2024-09-19
#### 1.Fixed known bugs.

## 0.1.3
### 2024-09-19
#### 1.Optimize the output format of the result.

## 0.1.4
### 2024-09-22
#### 1.load_dict method changed
- original
    ```python
    user_tuple, password_tuple = fbf.load_dict() # Two objects are required to receive the entire tuple of username and password.
    ```
- now
    ```python
    fbf.load_dict()
    fbf.brute() # You don't need to receive the return value, just call the brute() method.
    ```
#### 2.brute method changed
- original
    ```python
    fbf.brute(user_tuple, password_tuple)
    ```
- now
    ```python
    fbf.brute() # You no longer need to pass in parameters, you can just call them directly.
    ```
#### 3.Optimize the output format
- When the final result is printed, the username and password are displayed in yellow.
