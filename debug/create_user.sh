#!/bin/sh
curl -d "name=Alice&address=0101&skills=6" "http://127.0.0.1:5000/add_user"
curl -d "name=Bob&address=1101&skills=9" "http://127.0.0.1:5000/add_user"
curl -d "name=Catherina&address=1010&skills=2" "http://127.0.0.1:5000/add_user"
curl -d "name=Diana&address=1111&skills=3" "http://127.0.0.1:5000/add_user"
curl -d "name=Eason&address=0111&skills=9" "http://127.0.0.1:5000/add_user"
curl -d "name=Frank&address=1011&skills=4" "http://127.0.0.1:5000/add_user"
curl -d "name=George&address=0000&skills=3" "http://127.0.0.1:5000/add_user"
curl -d "name=Alice" "http://127.0.0.1:5000/del_user"
