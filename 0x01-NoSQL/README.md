# 0x01. NoSQL

## Resources
Read or watch:
- [NoSQL Databases Explained](#)
- [What is NoSQL?](#)
- [MongoDB with Python Crash Course - Tutorial for Beginners](#)
- [MongoDB Tutorial 2: Insert, Update, Remove, Query](#)
- [Aggregation](#)
- [Introduction to MongoDB and Python](#)
- [mongo Shell Methods](#)
- [Mongosh](#)

## Learning Objectives
At the end of this project, you should be able to explain the following concepts without external help:
- What NoSQL means
- The difference between SQL and NoSQL
- What ACID is
- What document storage is
- The types of NoSQL databases
- The benefits of a NoSQL database
- How to query information from a NoSQL database
- How to insert/update/delete information from a NoSQL database
- How to use MongoDB

## Requirements

### MongoDB Command File
- Files will be interpreted/compiled on Ubuntu 18.04 LTS using MongoDB (version 4.2)
- All files should end with a new line
- The first line of all files should be a comment: `// my comment`
- A `README.md` file at the root of the project is mandatory
- File lengths will be tested using `wc`

### Python Scripts
- Files will be interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7) and PyMongo (version 3.10)
- All files should end with a new line
- The first line of all files should be exactly `#!/usr/bin/env python3`
- A `README.md` file at the root of the project is mandatory
- Code should follow the pycodestyle (version 2.5.*)
- File lengths will be tested using `wc`
- All modules should have documentation (`python3 -c 'print(__import__("my_module").__doc__)'`)
- All functions should have documentation (`python3 -c 'print(__import__("my_module").my_function.__doc__)'`)
- Code should not be executed when imported (use `if __name__ == "__main__":`)

## Installation
To install MongoDB 4.2 on Ubuntu 18.04, follow these steps:

```bash
$ wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add -
$ echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org
$ sudo service mongod start
$ mongo --version
# MongoDB shell version v4.2.8
$ pip3 install pymongo
$ python3
>>> import pymongo
>>> pymongo.__version__
'3.10.1'
