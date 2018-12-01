## Streaming Event Compliance
A system that is able to check event compliance over streaming event data in python, 
which can enhance online process mining result.

There are two provided services:
  - compliance checking [http://127.0.0.1:5000/compliance-checker?uuid=user_name]
  - show deviation pdf [http://127.0.0.1:5000/show-deviation-pdf?uuid=user_name]


Client is a another small system, trying to simulating the streaming event data. 


### Virtual Environment Setting(using anaconda)
1. create own environment naming StreamEC

`conda create -n StreamEC python=3.6 anaconda`

2. activate and enter the environment 

`source activate StreamEC` in Linux or Mac


`activate StreamEC` in Windows

3. execute the requirements.txt

`pip install -r requirements.txt`

4. deactivate and enter the environment

`source deactivate StreamEC` in Linux or Mac

`source deactivate StreamEC` in Windows

5. start the project with this enviroment


### Database
username: compliancechecker
password: compliancechecker
mysql-db: compliancechecker


### Execute

We provide both server and client
  use `python server.py` in command to run the server
  
  use `python client.py user_name Example.xes` in command with two extra parameters to run client
