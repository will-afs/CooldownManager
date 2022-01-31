# ⌛ CooldownManager
REST Microservice to respect a cooldown between each call.

More info on this solution on 👉 [this post](https://www.linkedin.com/feed/update/urn:li:activity:6893219171723816960/) 👈

⚙️ Configuration
-----------------
The project configuration holds in the project_config.toml file.

The Flask configuration holds into the config.py file.

🔽 Installing the project on your machine
------------------------------------------
In a terminal, run the following command :

    git clone https://github.com/will-afs/PYTDelivery.git

Then build the Docker image :

    sudo docker build --tag cooldownmanager .

▶️ Usage
---------
You can now run the Docker image as a container :

    docker run cooldownmanager

By default, the microservice will run at the following address : http://172.17.0.2:5000/

You can request it, for instance from a terminal :

    curl http://172.17.0.2:5000/

You can also give a try to send concurrent requests from different terminals.
By default, the cooldown delay is set to 3 seconds, in the project_config.toml file.
So you should experiment this delay when running concurrent requests as mentionned above.

🧪 Running tests
-----------------
The tests are placed in the tests folder. They can be ran with pytests, as follows :

    python -m pytest tests
