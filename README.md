Instagram Clone:
This is an instagram clone project for learning web development, I have tried my best to make it resemble to the real instagram.
I used Python's well known framework Flask and for frontend Bootstrap framework of css.


Prequisites:

Here i am listing the libraries and softwares you will need or you must have:
1. You should have virtualenvironment installed on your system
    for ubuntu user you can install it by typing "pip install virtualenv" on your terminal.
2. Create a virtualenv for your project using "virtualenv -p your/python3/path my_project"
3. Activate this virtualenv using "source ~/.virtualenv/venvname/bin/activate" from your root.
4. all the libraries needed for this chapter are included in requirements.txt you can install them in your virtualenv by doing pip install libraryname.
5. One more important software here is Elasticsearch if you want a full text feature, I'll list it's installment instructions below.

ELASTICSEARCH:
This does your full text search in seconds and is one of the most popular software in this area.
Here are it's installation instructions for you so that you better not get stuck there as I was.

1. Download and install the public signing key: wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
2. You may need to install the apt-transport-https package on Debian before proceeding: sudo apt-get install apt-transport-https
3. Save the repository definition to /etc/apt/sources.list.d/elastic-7.x.list: echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
4. Now you are ready with initial steps let's install elasticsearch
5. You can install the Elasticsearch Debian package with: sudo apt-get update && sudo apt-get install elasticsearch
6. The Debian package for Elasticsearch v7.3.2 can be installed as follows: wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.3.2-amd64.deb
7. wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.3.2-amd64.deb.sha512
8. shasum -a 512 -c elasticsearch-7.3.2-amd64.deb.sha512
9. sudo dpkg -i elasticsearch-7.3.2-amd64.deb
10. It is not started automically after installation starting it depends on what your system uses.
Check that by running this command: ps -p 1
11. On systemd you can start and stop elasticsearch by using:
12. sudo systemctl start elasticsearch.service
13. sudo systemctl stop elasticsearch.service
14. Now you can check by running on localhost:9200
15. If you got a output on screen that means yaya you did it.
16. Now just simply install elasticsearch in your venv using pip install elasticsearch.

Note:: This project i use only for learning web development.