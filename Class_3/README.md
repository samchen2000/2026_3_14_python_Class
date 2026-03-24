# 2020/3/28 上課影片
## 2026/3/28 課程
### 2026_03_28_早上


### 2026_03_28_下午


### **Linux 常用指令列表**

#### **一、文件和目录操作 (Files and Directories)**

1.  **`ls`** (list)
    *   **说明**: 列出当前目录或指定目录下的文件和目录。
    *   **常用选项**:
        *   `-l`: 以长格式显示详细信息 (权限、所有者、大小、修改日期等)。
        *   `-a`: 显示所有文件，包括隐藏文件 (以 `.` 开头的文件)。
        *   `-h`: (配合 `-l`) 以人类可读的格式显示文件大小 (如 1K, 234M, 2G)。
    *   **范例**: `ls -lah`

2.  **`cd`** (change directory)
    *   **说明**: 改变当前工作目录。
    *   **常用范例**:
        *   `cd /home/user/documents`: 进入指定目录。
        *   `cd ..`: 返回上一级目录。
        *   `cd ~`: 进入当前用户的主目录。
        *   `cd`: 等同于 `cd ~`。
        *   `cd -`: 返回上次所在的目录。

3.  **`pwd`** (print working directory)
    *   **说明**: 显示当前所在的完整目录路径。

4.  **`mkdir`** (make directory)
    *   **说明**: 创建新目录。
    *   **常用选项**:
        *   `-p`: 递归创建目录 (如果父目录不存在，则一并创建)。
    *   **范例**: `mkdir mydir`, `mkdir -p /path/to/new/dir`

5.  **`rmdir`** (remove directory)
    *   **说明**: 删除空目录。 (如果目录非空，此命令会失败。通常建议使用 `rm -r` 来删除非空目录)。
    *   **范例**: `rmdir myemptydir`

6.  **`cp`** (copy)
    *   **说明**: 复制文件或目录。
    *   **常用选项**:
        *   `-r` 或 `-R`: 递归复制目录及其内容。
        *   `-i`: 覆盖前提示。
    *   **范例**: `cp file1 file2` (复制文件), `cp -r dir1 dir2` (复制目录)

7.  **`mv`** (move)
    *   **说明**: 移动文件或目录，也可以用于重命名文件或目录。
    *   **常用范例**:
        *   `mv file1 /path/to/new/location`: 移动文件。
        *   `mv oldname newname`: 重命名文件或目录。

8.  **`rm`** (remove)
    *   **说明**: 删除文件或目录。
    *   **常用选项**:
        *   `-r` 或 `-R`: 递归删除目录及其内容 (非常危险，请谨慎使用)。
        *   `-f`: 强制删除，不提示。
        *   `-i`: 交互式删除，每次删除前提示。
    *   **范例**: `rm myfile`, `rm -rf mydir` (慎用!)

9.  **`touch`**
    *   **说明**: 创建一个空文件，或者更新文件的访问和修改时间。
    *   **范例**: `touch newfile.txt`

#### **二、查看文件内容 (Viewing File Content)**

1.  **`cat`** (concatenate)
    *   **说明**: 查看文件内容，将文件内容输出到标准输出。如果文件很大，内容会快速滚动。
    *   **范例**: `cat myfile.txt`

2.  **`less`**
    *   **说明**: 分页查看文件内容，支持向上/向下滚动，比 `more` 功能更强大。按 `q` 退出。
    *   **范例**: `less largefile.log`

3.  **`head`**
    *   **说明**: 显示文件头部内容，默认显示前10行。
    *   **常用选项**:
        *   `-n N`: 显示前N行。
    *   **范例**: `head -n 5 myfile.txt`

4.  **`tail`**
    *   **说明**: 显示文件尾部内容，默认显示最后10行。常用于查看日志文件。
    *   **常用选项**:
        *   `-n N`: 显示最后N行。
        *   `-f`: 实时跟踪文件末尾的添加内容 (常用于监控日志)。
    *   **范例**: `tail -n 20 error.log`, `tail -f access.log`

#### **三、文件权限和所有权 (File Permissions and Ownership)**

1.  **`chmod`** (change mode)
    *   **说明**: 改变文件或目录的权限。
    *   **常用范例**:
        *   `chmod 755 script.sh`: 设置文件所有者可读写执行，组用户和其他用户可读执行。
        *   `chmod u+x script.sh`: 给文件所有者添加执行权限。
        *   `chmod -R 755 mydir`: 递归地改变目录及其内容的权限。

2.  **`chown`** (change owner)
    *   **说明**: 改变文件或目录的所有者。
    *   **常用范例**: `chown user1 file.txt`, `chown user1:group1 file.txt`

3.  **`chgrp`** (change group)
    *   **说明**: 改变文件或目录的所属组。
    *   **范例**: `chgrp group1 file.txt`

#### **四、系统信息和监控 (System Info and Monitoring)**

1.  **`df`** (disk free)
    *   **说明**: 显示磁盘分区的使用情况。
    *   **常用选项**:
        *   `-h`: 以人类可读的格式显示大小。
    *   **范例**: `df -h`

2.  **`du`** (disk usage)
    *   **说明**: 显示目录或文件占用的磁盘空间。
    *   **常用选项**:
        *   `-h`: 以人类可读的格式显示大小。
        *   `-s`: 只显示总计大小。
    *   **范例**: `du -sh mydir`

3.  **`free`**
    *   **说明**: 显示内存使用情况。
    *   **常用选项**:
        *   `-h`: 以人类可读的格式显示大小。
    *   **范例**: `free -h`

4.  **`top`**
    *   **说明**: 实时显示系统中运行的进程信息，包括CPU、内存使用情况等。按 `q` 退出。
    *   **替代**: `htop` (功能更强大，通常需要额外安装)

5.  **`ps`** (process status)
    *   **说明**: 显示当前运行的进程快照。
    *   **常用选项**:
        *   `aux`: 显示所有用户的所有进程。
    *   **范例**: `ps aux | grep nginx` (查找Nginx进程)

6.  **`uname`**
    *   **说明**: 显示操作系统信息。
    *   **常用选项**:
        *   `-a`: 显示所有信息 (内核名称、主机名、内核版本等)。

7.  **`uptime`**
    *   **说明**: 显示系统运行时间、当前用户数和平均负载。

#### **五、进程管理 (Process Management)**

1.  **`kill`**
    *   **说明**: 向进程发送信号，通常用于终止进程。
    *   **常用范例**:
        *   `kill PID`: 终止指定PID的进程 (默认发送TERM信号)。
        *   `kill -9 PID`: 强制终止指定PID的进程 (发送KILL信号，进程无法捕获，无法清理)。

2.  **`killall`**
    *   **说明**: 根据进程名称终止所有匹配的进程。
    *   **范例**: `killall firefox`

#### **六、文本处理 (Text Processing)**

1.  **`grep`** (global regular expression print)
    *   **说明**: 在文件中搜索指定模式的文本。
    *   **常用选项**:
        *   `-i`: 忽略大小写。
        *   `-r` 或 `-R`: 递归搜索目录。
        *   `-n`: 显示匹配行的行号。
        *   `-v`: 反向匹配，显示不包含模式的行。
    *   **范例**: `grep "error" /var/log/syslog`, `grep -rn "config" .`

2.  **`echo`**
    *   **说明**: 在终端上显示文本或变量的值。
    *   **范例**: `echo "Hello, Linux!"`, `echo $PATH`

3.  **`wc`** (word count)
    *   **说明**: 计算文件中的行数、单词数和字符数。
    *   **常用选项**:
        *   `-l`: 只计算行数。
        *   `-w`: 只计算单词数。
        *   `-c`: 只计算字符数。
    *   **范例**: `wc -l myfile.txt`

4.  **`sort`**
    *   **说明**: 对文本文件内容进行排序。

5.  **`uniq`**
    *   **说明**: 报告或忽略文件中重复的行。

#### **七、网络操作 (Networking)**

1.  **`ping`**
    *   **说明**: 测试网络连接性，向目标主机发送ICMP回显请求。
    *   **范例**: `ping google.com`

2.  **`ip`** (Internet Protocol)
    *   **说明**: (现代Linux推荐使用，替代旧的 `ifconfig` 和 `route`) 配置和显示网络设备信息。
    *   **常用范例**: `ip a` (显示所有网络接口信息), `ip route` (显示路由表)

3.  **`ssh`** (Secure Shell)
    *   **说明**: 安全地远程登录到另一台计算机。
    *   **范例**: `ssh user@remote_host`

4.  **`scp`** (Secure Copy)
    *   **说明**: 在本地和远程主机之间安全地复制文件。
    *   **范例**: `scp localfile.txt user@remote_host:/path/to/remote/dir`

5.  **`wget`**
    *   **说明**: 从Web下载文件。
    *   **范例**: `wget https://example.com/file.zip`

6.  **`curl`**
    *   **说明**: 传输数据，支持多种协议。常用于测试API或下载文件。
    *   **范例**: `curl https://example.com/api/data`, `curl -O https://example.com/file.zip`

#### **八、软件包管理 (Package Management)**

(根据不同的Linux发行版，包管理器不同)

**Debian/Ubuntu (APT):**
1.  **`sudo apt update`**: 更新软件包列表。
2.  **`sudo apt upgrade`**: 升级已安装的软件包。
3.  **`sudo apt install package_name`**: 安装软件包。
4.  **`sudo apt remove package_name`**: 卸载软件包。
5.  **`sudo apt search keyword`**: 搜索软件包。

**Red Hat/CentOS/Fedora (YUM/DNF):**
1.  **`sudo dnf update`** (或 `sudo yum update`): 更新软件包。
2.  **`sudo dnf install package_name`** (或 `sudo yum install package_name`): 安装软件包。
3.  **`sudo dnf remove package_name`** (或 `sudo yum remove package_name`): 卸载软件包。
4.  **`sudo dnf search keyword`** (或 `sudo yum search keyword`): 搜索软件包。

#### **九、用户和组管理 (User and Group Management)**

1.  **`sudo`** (superuser do)
    *   **说明**: 以超级用户或其他用户的身份执行命令。
    *   **范例**: `sudo apt update`, `sudo vi /etc/hosts`

2.  **`su`** (switch user)
    *   **说明**: 切换用户身份，如果未指定用户，则切换到 root 用户。
    *   **范例**: `su -` (切换到root并加载root的环境变量), `su user2`

3.  **`useradd`**
    *   **说明**: 添加新用户。
    *   **范例**: `sudo useradd -m newuser` (-m 自动创建家目录)

4.  **`passwd`**
    *   **说明**: 更改用户密码。
    *   **范例**: `passwd` (更改自己的密码), `sudo passwd newuser` (更改其他用户密码)

#### **十、归档和压缩 (Archiving and Compression)**

1.  **`tar`** (tape archive)
    *   **说明**: 归档和解归档文件，常用于打包和解包。
    *   **常用选项**:
        *   `-c`: 创建归档文件。
        *   `-x`: 解开归档文件。
        *   `-v`: 显示详细过程。
        *   `-f`: 指定归档文件名。
        *   `-z`: 通过 gzip 压缩/解压 (生成 `.tar.gz` 或 `.tgz`)。
        *   `-j`: 通过 bzip2 压缩/解压 (生成 `.tar.bz2` 或 `.tbz`)。
        *   `-J`: 通过 xz 压缩/解压 (生成 `.tar.xz` 或 `.txz`)。
    *   **范例**:
        *   `tar -czvf archive.tar.gz /path/to/dir`: 压缩目录。
        *   `tar -xzvf archive.tar.gz`: 解压 `.tar.gz` 文件。

2.  **`gzip`** / **`gunzip`**
    *   **说明**: 压缩/解压缩 `.gz` 文件。
    *   **范例**: `gzip myfile.txt`, `gunzip myfile.txt.gz`

3.  **`zip`** / **`unzip`**
    *   **说明**: 创建/解压缩 `.zip` 文件 (与Windows兼容)。
    *   **范例**: `zip archive.zip file1 file2`, `unzip archive.zip`

---

### **重要提示**

*   **`man command_name`**: 这是您最好的朋友！它会显示任何命令的完整手册页，包括所有选项和用法。
*   **Tab 键自动补全**: 在终端输入命令或文件路径时，多按几次 Tab 键，系统会尝试自动补全或显示可能的选项，可以大大提高效率并减少输入错误。
*   **历史命令**: 使用 `history` 命令查看您执行过的所有命令。使用上下箭头键可以快速翻阅历史命令。
*   **`Ctrl+C`**: 终止当前正在运行的命令。
*   **`Ctrl+D`**: 通常表示输入结束 (EOF)，或退出当前 shell 会话。
*   **`clear`**: 清空终端屏幕。
*   **`sudo` 权限**: 许多系统管理操作需要 `sudo` 权限。请务必谨慎使用 `rm -rf` 和其他破坏性命令，尤其是在 `sudo` 下，因为它们可能导致不可逆的数据丢失或系统损坏。