# A website using mariaDB

## A website that displays the most common adjective describing the website

The dashboard:

<img src="/images/dashboard.png" alt="Image of the dashboard on startup" width="400">

The wordcloud:

<img src="/images/wordcloud.png" alt="Image of the wordcloud" width="300">

Lightmode:

<img src="/images/image_light.png" alt="Lightmode" width="400">

This website uses python as backend. `app.py` is connected to the HTML. `app.py` then sends this info to `mariadb_python.py`, this script then takes the adjective and stores it in the database. The database is to be updated.

Also planned to do a wordcloud for all the adjectives, instead of just a word

## TODO's

- [x] Update database
- [x] wordcloud (both for light- and dark mode)
- [x] Dark / light mode
- [x] Styling
- [ ] Get some other feature in

### Far fetched ideas

- [ ] Docker
- [x] AI to accept only adjectives

# The installation

## Create an environment

Create a project folder and a `.venv` folder within, with this command:

```
mkdir myproject
cd myproject
python3 -m venv .venv
```

## Install Flask

- Open a `terminal` or use the one in Visual Studio Code
- Navigate to your project folder using `cd`
- Run the command bellow to install Flask

```
pip install Flask
```

## Install mariaDB for Mac

[If you are using Windows, go to mariaDB's website and follow the guide there](https://mariadb.com/docs/server/server-management/install-and-upgrade-mariadb/installing-mariadb/binary-packages/installing-mariadb-msi-packages-on-windows)

Run this command to install mariaDB and update to latest version

```
brew install mariadb
brew upgrade mariadb
```

## Start mariaDB for Mac

Navigate to your local `terminal`.

Start mariaDB

```
brew services start mariadb
```

If you later want to stop the database you can run

```
brew services stop mariadb
```

## Windows

.....

## Setup mariaDB

If it is your first time using mariaDB, you need to login without a password to setup a password

```
sudo mariadb -u root
```

This now puts you inside mariaDB, if you want to exit mariaDB, just type `EXIT;`, `QUIT;` or just `Ctrl + D`

### Setup your user

```
CREATE USER 'username'@'localhost' IDENTIFIED BY 'secure_password';
```

#### The pythonscript uses `pythonuser` as username and `pythonpass`as password

```
CREATE USER 'pythonuser'@'localhost' IDENTIFIED BY 'pythonpass';
```

You should now be logged in as root user, even though you just created a new one. The root user has all the privileges, if you want your user that you just created to also have all privileges, you can run

```
GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost';
```

#### Give privileges to a specific database (Recommended)

```
GRANT SELECT, INSERT, UPDATE ON database_name.* TO 'username'@'localhost';
```

#### For my script

```
GRANT SELECT, INSERT, UPDATE ON adjectives.* TO 'pythonuser'@'localhost';
```

#### After you have done that, you need to save the changes

```
FLUSH PRIVILEGES;
```

#### If you are unsure that you have done it correctly you can run

```
SHOW GRANTS FOR 'pythonuser'@'localhost';
```

And you should see something like

| Grants for pythonuser@localhost                                                                                |
| -------------------------------------------------------------------------------------------------------------- |
| GRANT USAGE ON _._ TO pythonuser@localhost IDENTIFIED BY PASSWORD '\_C85F42CED428CAE393E47738770729D0657BB541' |
| GRANT SELECT, INSERT, UPDATE ON database_name.\* TO pythonuser@localhost;                                      |

### Complete user-generation

```
CREATE USER 'pythonuser'@'localhost' IDENTIFIED BY 'pythonpass';
GRANT SELECT, INSERT UPDATE ON ON adjectives.* TO 'pythonuser'@'localhost';
FLUSH PRIVILEGES;
```

# Making the database

### Run this command to create the database used in this project

```
CREATE DATABASE adjectives;
```

#### Use the database

```
USE adjectives;
```

#### The code bellow will create all the neccesary information to get started

```
CREATE TABLE adjectives (
    id INT AUTO_INCREMENT PRIMARY KEY,
    adjective VARCHAR(50) NOT NULL UNIQUE,
    counter INT NOT NULL
);

```

#### To be extra sure, run this command

```
DESCRIBE adjectives;
```

#### It should look like this, you can now `QUIT;`, `EXIT;` or `Ctrl + D` to get out of the terminal, and close it

| Field     |    Type     | Null | Key | Default |          Extra |
| --------- | :---------: | ---: | --: | ------: | -------------: |
| id        |   int(11)   |   NO | PRI |    NULL | auto_increment |
| adjective | varchar(50) |   NO |     |    NULL |                |
| counter   |   int(11)   |   NO |     |    NULL |                |

## Install wordcloud

Wordcloud is the program that makes them word-pictures. Run the commands bellow in the terminal

```
pip install wordcloud
pip install nympy matplotlib pillow
```

## Other miscellaneous commands you need to run

```
pip install spacy # Only adjectives allowed
python -m spacy download en_core_web_sm # Only a spesific liberary is required
pip install flask-limiter # This is for people not to spam your website

pip install gunicorn # for a more robust online server
```
