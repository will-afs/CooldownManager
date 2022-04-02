# <img src="https://github.com/will-afs/AdvancedAcademicProject/blob/main/doc/Icons/CooldownManager.png" width="30"> CooldownManager
Make your processes respect a cooldown between each call to this REST Microservice

<img src="https://github.com/will-afs/CooldownManager/blob/main/doc/CooldownManager%20sequence%20diagram.JPG" width="700">

More info on this solution on 👉 [this post](https://www.linkedin.com/feed/update/urn:li:activity:6893219171723816960/) 👈

This is a sub-project of the [AdvancedAcademicProject](https://github.com/will-afs/AdvancedAcademicProject/)

⚙️ Configuration
-----------------
The project configuration holds in the [project_config.toml file](https://github.com/will-afs/CooldownManager/blob/main/project_config.toml)

The Flask configuration holds into the [flask_config.py file](https://github.com/will-afs/CooldownManager/blob/main/flask_config.py)

🐇 Quickly run the service as a container
-----------------------------------------

    sudo docker run --name cooldownmanager -d -p 80:80 williamafonso/cooldownmanager
    
By default, the container will listen to any IPv4. Thus, it can be accessed locally at the following address : http://172.17.0.2:80/

So it can directly be tested by sending it a local request :

    curl http://172.17.0.2:80/

You can also give a try to send concurrent requests from different terminals.
By default, the cooldown delay is set to 3 seconds, in the project_config.toml file.
So you should experiment this delay when running concurrent requests as mentionned above.

🧪 Developing and running tests
--------------------------------
In a terminal, run the following command :

    git clone https://github.com/will-afs/cooldownmanager.git

Go into the cloned repository (stay at the root) - it will be the working directory:

    cd CooldownManager

Add the working directory to the Python PATH environment variable:

    export PYTHONPATH=$(pwd)
    
Create a virtual environment:

    python3 -m venv .venv

Activate the virtual environment:
    
    source .venv/bin/activate
    
Install the dependencies:
    
    pip install -r requirements.txt

Run the main python file:

    python src.arxivparser.core.arxiv_parser.py

The tests are placed in the tests folder. They can be ran with pytests, as follows :

    python -m pytest tests
 
🐋 Containerizing the application 
----------------------------------
To build a Docker image :

    sudo docker build --tag cooldownmanager .
    
Or if you want to be able to push it to your DockerHub:

    sudo docker build --tag <your_docker_username>/cooldownmanager .

Pushing the Docker image to your registry :

    sudo docker push <your_docker_user_name>/cooldownmanager

You can now run the Docker image as a container :

    sudo docker run -d -p 80:80 cooldownmanager

☁️ Deploying on EC2
--------------------

Create an AWS EC2 instance (ideally Ubuntu Server 20.04 LTS) - keep your KeyPair.pem file safe !

Configure Security Group so that the machine is reachable via SSH and HTTP
    
By default, permissions on the keypair.pem file are too open and must be restricted:

    chmod 600 <path_to_your_key_pair>

You should now be able to connect to your EC2 instance:

    sudo ssh -i <path_to_your_key_pair> ubuntu@<ec2_instance_public_ipv4>

From there, run the service as a container:

    sudo docker run --name cooldownmanager -d -p 80:80 williamafonso/cooldownmanager
    
The service should now be able from the internet:

    curl "http://15.188.144.230:80/"

You should obtain the following response:

    {"message":"authorized"}
