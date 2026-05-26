# Hosting a Flask App on a UTM VM with a Remote MariaDB

## Overview

This guide covers running a Flask web app on one UTM VM, with MariaDB hosted on a separate UTM VM. The two VMs communicate over the shared UTM network.

---

## Prerequisites

- Two UTM VMs running Ubuntu Server
- Flask project on GitHub
- MariaDB already set up and running on the database VM

---

## 1. Configure MariaDB to Accept Remote Connections

On the **database VM**, edit the MariaDB config:

```bash
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```

Change this line:

```
bind-address = 127.0.0.1
```

To:

```
bind-address = 0.0.0.0
```

Restart MariaDB:

```bash
sudo systemctl restart mariadb
```

---

## 2. Create a Remote MariaDB User

Still on the **database VM**, log into MariaDB and create a user that allows remote login:

```sql
sudo mariadb

CREATE USER 'flask_user'@'%' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON your_database.* TO 'flask_user'@'%';
FLUSH PRIVILEGES;
```

---

## 3. Open Port 3306 on the Database VM

Allow the Flask VM to reach MariaDB:

```bash
sudo ufw allow from 192.168.64.0/24 to any port 3306
```

Replace the subnet with whatever your UTM network uses.

---

## 4. Find the Database VM's IP

```bash
ip a
```

Note the `192.168.x.x` address. This is what Flask will connect to.

---

## 5. Set Up the Flask VM

### Install dependencies

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
sudo apt install libmariadb3 libmariadb-dev -y
```

### Clone your project

```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo
```

### Set up a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Python packages

```bash
pip install flask python-dotenv mariadb
```

Add any other packages your project requires.

---

## 6. Create the .env File

On the Flask VM, inside your project folder:

```bash
nano .env
```

Fill in your values:

```
DB_HOST=192.168.64.7
DB_PORT=3306
DB_USER=flask_user
DB_PASSWORD=yourpassword
DB_NAME=your_database
```

---

## 7. Make Flask Listen on All Interfaces

In `app.py`, make sure the run call looks like this:

```python
app.run(host="0.0.0.0", port=5000, debug=True)
```

This allows devices on the network to reach Flask, not just the VM itself.

---

## 8. Test the Database Connection

Before running Flask, verify the two VMs can talk:

```bash
mariadb -h 192.168.64.7 -u flask_user -p your_database
```

If you get a MariaDB prompt, the connection works.

---

## 9. Run the Flask App

```bash
source venv/bin/activate
python3 app.py
```

Flask will start and be accessible from your Mac or any device on the same network at:

```
http://192.168.64.X:5000
```

Where `192.168.64.X` is the Flask VM's IP.
