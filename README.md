Goal
=====
To construct a fog-computing framework based on Raspberry Pi.


Install
=====
```bash  
$ sudo git clone https://github.com/wenbo1188/distribute.git 
$ cd project_path
$ sudo pip install -e .
``` 


Usage Guide
=====
Running distribute app: 
```bash 
$ export FLASK_APP=distribute
$ export FLASK_DEBUG=1
$ flask run #for locally debugging or
$ flask run --host=0.0.0.0 #for public using 
``` 