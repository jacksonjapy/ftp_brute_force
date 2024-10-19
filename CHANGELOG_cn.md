## 0.1.0

### 2024-09-05

#### 1. 初次发布

## 0.1.1

### 2024-09-18

#### 1. 修复了import时模块名过长的错误

   - 由
     ```python
     from ftp_brute_force.ftp_brute import FtpBruteForce
     ```
   - 改为
     ```python
     from ftp_brute_force import FtpBruteForce
     ```

#### 2. 增加命令行的使用方式
 - `s` 服务器地址
 - `port` 服务器FTP服务的端口，默认为21
 - `u` 用户名字典文件的路径
 - `password` 密码字典文件的路径
 - `v`  版本信息
 - `h`  帮助信息
##### 使用方法
  - Linux / Mac OS / Windows

	```shell
	ftp_brute_force -s (server_address) --port (server_port) -u (user_dict_path) --password (password_dict_path)
	```

## 0.1.2
### 2024-09-19
#### 1.修复已知Bug