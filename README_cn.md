# ftp_brute_force

`ftp_brute_force` 是一个用于执行 FTP 暴力破解的工具。

## 安装

可以通过 `pip` 安装：

```bash
pip install ftp_brute
```

## 使用说明

### 基本用法

你可以通过以下方式导入并使用该工具：

```python
from ftp_brute_force import FtpBruteForce

ftp_brute(server_address, user_dict_path, password_dict_path, [server_port])
```

### 示例

```python
from ftp_brute_force import FtpBruteForce

if __name__ == '__main__':
    server_address = "192.168.1.1"
    user_dict = r"user.dic"
    password_dict = r"password.dic"
    fbf = FtpBruteForce(server_address, user_dict, password_dict)
    user_tuple, password_tuple = fbf.load_dict()
    fbf.connection()
    fbf.brute(user_tuple, password_tuple)

```

## 选项

- `server_address`：目标 FTP 服务器的 IP 地址。
- `user_dict`：用于暴力破解的用户名字典路径。
- `password_dict`：用于暴力破解的密码字典路径。

## 依赖

- Python 3.10 或更高版本
- `ftplib` (Python 内置)
- `socket` (Python内置)
- `time` (Python内置)
- `os` (Python内置)

## GitHub项目
[Github](https://github.com/jacksonjapy/ftp_brute_force)

## 变更日志
请参阅 [CHANGELOG.md](CHANGELOG_cn.md)
