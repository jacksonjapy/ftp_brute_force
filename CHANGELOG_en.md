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
