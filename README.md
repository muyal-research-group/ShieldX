# ShieldX 

<div align="center">
<img src="images/shieldx.png" width=250/>
</div>

<div align=center>
<a href="https://test.pypi.org/project/mictlanx/"><img src="https://img.shields.io/badge/version-0.0.1--alpha.0-green" alt="build - 0.0.160-alpha.3"></a>
</div>

ShieldX is a secure management platform for microservices. It provides an integrated dashboard and toolset to manage, monitor, and secure your microservices environment. With robust encryption, secure communication channels, and scalable orchestration, ShieldX is designed to safeguard your infrastructure while ensuring efficient operations.
## ⚠️ Clone the repo and setup a remoto 🍴: 

1. You must clone the remote from the organization of Muyal: 
```bash
git clone git@github.com:muyal-research-group/ShieldX.git
```

2. You must create a fork (please check it up in the [Contribution](#contribution) section)

3. Add a new remote in your local git: 
   ```bash
   git remote add <remote_name> <ssh> 
   ```
You must select ```<remote_name>``` and you must copy the ```<ssh>``` uri in the github page of your 

<div align="center">
<img width=350 src="images/gitclone_ssh.png"/>
</div>

4. Remember to push all your commits to your ```<remote_name>``` to avoid github conflicts. 

Thats it!  let's get started 🚀

## Getting started

You must install the following software: 

- [Docker](https://github.com/pyenv/pyenv?tab=readme-ov-file#linuxunix)
- Poetry
    ```bash
    pip3 install poetry
    ```
- [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#linuxunix)
    ```bash
    curl -fsSL https://pyenv.run | bash
    ```


Once you get all the software, please execute the following command to install the dependencies of the project: 

```bash
poetry install
```
### How to deploy database and broker

**Install docker and docker Compose:**

- Make sure Docker is installed on your system. See [Docker's installation guide](https://docs.docker.com/get-docker/) for instructions.
- Docker Compose is usually included with Docker Desktop. Otherwise, follow [Docker Compose installation instructions](https://docs.docker.com/compose/install/).

**Navigate to your project directory:**

- Open a terminal and change to the directory where your `docker-compose.yml` file is located.

**Start the services:**

- Run the following command to start both services in detached mode:
```bash
docker compose up -d
```

**Stopping the services:**
```bash
docker compose down
```

# 🛠️ Execution Guide: FastAPI Server & RabbitMQ Consumer/Producer

This guide explains how to **run a FastAPI server** and manage **RabbitMQ consumers and producers** for event models.
1. Run the FastAPI Server
```bash
poetry run python3 ./shieldx/server.py
```
The server will be available at: http://localhost:20000, API docs can be accessed at: [http://localhost:20000/docs](http://localhost:20000/docs)

2. Run the rabbitMQ Consumer:
```bash
poetry run python3 ./shieldx/consumer.py
```
This will connect to RabbitMQ and listen for incoming messages.
3. Run the rabbitMQ Producer:
```bash
poetry run python3 ./shieldx/producer.py
```




## Running Tests

All tests for this project are located in the `tests/` folder at the root of the repository. We use [pytest](https://docs.pytest.org/) as our testing framework.

### How to Run the Tests

1. **Navigate to the project directory:**
   ```bash
   cd path/to/your/project

2. Run all tests:
    ```bash
    pytest
    ```
3. Run a specific test file: 
    ```bash
    pytest tests/test_policy_manager.py
    ```

## Contributing[](#contribution)

Please follow these steps to help improve the project:

1. **Fork the Repository:**
   - Click the "Fork" button at the top right of the repository page to create a copy under your GitHub account.

2. **Create a Feature Branch:**
   - Create a new branch from the `main` branch. Use a descriptive branch name (e.g., `feature/new-algorithm` or `bugfix/fix-issue`):
     ```bash
     git checkout -b feature/your-feature-name
     ```

3. **Make Your Changes:**
   - Implement your feature or fix the issue. Make sure to write or update tests located in the `tests/` folder as needed.

4. **Run the Tests:**
   - Verify that all tests pass by running:
     ```bash
     pytest
     ```
   - Ensure that your changes do not break any existing functionality.

5. **Commit and Push:**
   - Write clear and concise commit messages. Then push your branch to your fork:
     ```bash
     git push origin feature/your-feature-name
     ```

6. **Open a Pull Request:**
   - Navigate to the repository on GitHub and open a pull request against the `main` branch. Please include a detailed description of your changes and the motivation behind them.

7. **Review Process:**
   - Your pull request will be reviewed by the maintainers. Feedback and further changes may be requested.
