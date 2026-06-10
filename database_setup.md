# Setting Up a Remote MariaDB Database with UTM

This guide covers how to set up a MariaDB database on a UTM virtual machine (on Apple Silicon) and connect to it remotely from another machine running your application.

---

## Requirements

- Mac with Apple Silicon (M1/M2/M3)
- UTM installed
- Ubuntu Server ARM64 ISO

---

## 1. Create the VM in UTM

1. Open UTM and click **+**
2. Choose **Virtualize** (not Emulate — you are on ARM64)
3. Select **Linux**
4. Point it to your Ubuntu Server ARM64 `.iso`
   - Download from: https://ubuntu.com/download/server/arm
5. Allocate resources:
   - RAM: 1–2 GB is enough for a database VM
   - Storage: 10–20 GB
6. Finish and boot into the installer

---

## 2. Install Ubuntu Server

Go through the installer normally. Key steps:

- Set a username and password
- When asked about additional packages, select **OpenSSH server** — this lets you SSH in from your Mac instead of using the UTM window
- Complete the install, reboot, and eject the ISO when prompted

---

## 3. Install MariaDB

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install mariadb-server -y
```

Run the secure installation script:

```bash
sudo mariadb-secure-installation
```

Answer the prompts as follows:

| Prompt                               | Answer |
| ------------------------------------ | ------ |
| Switch to unix_socket authentication | y      |
| Change root password                 | n      |
| Remove anonymous users               | y      |
| Disallow root login remotely         | y      |
| Remove test database                 | y      |
| Reload privilege tables              | y      |

---

## 4. Create the Database and Remote User

Log into MariaDB:

```bash
sudo mariadb
```

Run the following SQL:

```sql
CREATE DATABASE your_database;
CREATE USER 'your_user'@'%' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON your_database.* TO 'your_user'@'%';
FLUSH PRIVILEGES;
EXIT;
```

The `%` allows connections from any host. For tighter security you can replace it with the specific IP of your application machine, for example `'your_user'@'192.168.64.1'`.

---

## 5. Allow Remote Connections in MariaDB Config

By default MariaDB only listens on localhost. Open the config file:

```bash
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```

Find this line:

```
bind-address = 127.0.0.1
```

Change it to:

```
bind-address = 0.0.0.0
```

Save with `Ctrl+O`, confirm with `Enter`, exit with `Ctrl+X`.

Restart MariaDB:

```bash
sudo systemctl restart mariadb
```

---

## 6. Configure the Firewall

```bash
sudo ufw allow 3306
sudo ufw allow OpenSSH
sudo ufw enable
```

---

## 7. Find the VM's IP Address

```bash
ip a
```

Look for the `enp0s1` interface. The IP will be in the `192.168.64.x` range, for example:

```
inet 192.168.64.7/24
```

This is the IP your application will connect to.

---

## 8. Connect From Your Application

### Using a .env file

```env
DB_HOST=192.168.64.7
DB_PORT=3306
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_database
```

### Python with mariadb connector

```python
import mariadb
import os
from dotenv import load_dotenv

load_dotenv()

conn = mariadb.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
```

### Python with pymysql / SQLAlchemy

```python
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://your_user:your_password@192.168.64.7/your_database'
)
```

---

## 9. Test the Connection

From your Mac terminal, test with the MySQL client:

```bash
mysql -u your_user -p -h 192.168.64.7
```

If you do not have it installed:

```bash
brew install mysql-client
```

If the login succeeds, your VM database is reachable and ready to use.

---

## Notes

- The VM IP (`192.168.64.x`) is assigned by UTM's virtual network and is only reachable from your Mac, not from the internet.
- If the VM restarts, it may get a different IP unless you configure a static IP or DHCP reservation.
- Never expose port 3306 directly to the public internet without a firewall restricting it to known IPs.
- Always store credentials in a `.env` file and never commit it to version control.
