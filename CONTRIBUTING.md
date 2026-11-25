# Contributing to the DSCI 522 Group 13 Project

Thank you for contributing to our DSCI 522 Group 13 project! This project analyzes Steam video game data to explore relationships between game features and outcomes.

## Fixing Typos

Small spelling or grammatical errors in documentation can be fixed directly using GitHub.

Please modify the original source files, such as `.md` or `.qmd`, rather than rendered HTML or PDF files.

## Reporting Bugs and Suggesting Improvements

Before making substantial changes, create a GitHub Issue to describe the problem or proposed improvement.

When reporting a bug, provide a clear description of the issue, the steps needed to reproduce it, the expected and actual results, and any relevant error messages or screenshots.

Before opening a new issue, check whether a similar issue has already been reported.

## Setting Up the Project

Follow the installation instructions in the [README](README.md) to clone the repository and download the Docker image.

All project work should be performed inside the Docker container to maintain a consistent and reproducible environment.

## Working in the Container

We use Docker and Positron Remote SSH to edit and run code inside the project container.

### One-time setup

Before starting, install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and [Positron](https://positron.posit.co/). Then, follow the README instructions to create an SSH key and download the Docker image.

Make sure your Git name and email are configured. You can check your current configuration by running:

```bash
git config --global user.name
git config --global user.email
```

If either value is missing, configure it using the following commands:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

The Docker Compose configuration mounts your Git configuration into the container, allowing commits made inside the container to use your Git identity.

### Starting a work session

To start a work session, open a terminal in the project directory and run:

```bash
docker compose up -d
```

You can check whether the container is running by executing:

```bash
docker compose ps
```

Next, open Positron and the Command Palette using `Ctrl + Shift + P` on Windows/Linux or `Cmd + Shift + P` on macOS. Search for and select **Remote-SSH: Show Remote Menu**, then choose **Connect to Host**.

Enter the following address:

```text
root@localhost:2222
```

If prompted, select Linux and accept the SSH host fingerprint. On your first connection, wait for Positron to connect and install its remote server.

Once connected, open the project directory:

```text
/workspace
```

### Selecting the Python environment

When working with Python, select the project's Python interpreter:

```text
/opt/venv/bin/python
```

Do not select a local `.venv` environment on your computer.

To verify that you are using the container's Python environment, run:

```python
import sys
print(sys.executable)
```

The output should be:

```text
/opt/venv/bin/python
```

### Ending a work session

When you finish working, close your remote session and stop the container from a local terminal by running:

```bash
docker compose down
```

## Troubleshooting

### SSH key not found

If Docker cannot find `~/.ssh/id_ed25519.pub`, first check whether the file exists.

If you do not have an SSH key, create one by running:

```bash
ssh-keygen -t ed25519
```

Press Enter at each prompt to accept the default settings.

If Docker has created a directory named `id_ed25519.pub` instead of finding the public key file, remove the incorrectly created directory and generate the SSH key again.

### Git configuration file issue

If Docker reports an issue with `~/.gitconfig`, check that it exists as a file rather than a directory.

You can configure your Git name and email by following the instructions in the One-time setup section.

### SSH asks for a password

If SSH asks for a password when connecting, check that your public SSH key exists at `~/.ssh/id_ed25519.pub`, Docker Desktop is running, and the project container is active. Also, make sure you are connecting to `root@localhost:2222`.

### SSH host identification has changed

If you receive an SSH host identification warning, verify that the container has been recreated. If appropriate, remove the old host entry for `localhost` from your local SSH `known_hosts` file and reconnect.

### Port 2222 is already in use

If another application is using port 2222, stop that application or change the host port mapping in `docker-compose.yml`. If you change the port, remember to use the new port when connecting through Positron.

### GitHub authentication

If GitHub asks you to authenticate when pushing changes, follow the authentication instructions provided by GitHub. Do not store passwords or access tokens in project files.

## Adding or Updating Packages

If you need an additional Python package, first create or switch to a feature branch and connect to the running container. Then, use `uv add` to install the package and update the project's dependency files:

```bash
uv add package-name
```

To specify a particular version, use:

```bash
uv add package-name==1.2.3
```

After adding the package, commit both updated dependency files, `pyproject.toml` and `uv.lock`, to ensure that the project environment remains reproducible.

Next, push your branch and open a Pull Request. After the changes are merged into `main`, the GitHub Actions workflow builds and publishes an updated Docker image.

Before starting a new work session, open a terminal in your local project directory and pull the latest repository changes and Docker image:

```bash
git pull
docker compose pull
```

Make sure you use the image tag specified in the updated `docker-compose.yml` file. This ensures that your local environment uses the latest Docker image with the updated dependencies.

## Reproducing the Analysis

To rerun the analysis, open a terminal in the project directory and execute:

```bash
docker compose run --rm analysis-env uv run quarto render
```

The `--rm` option automatically removes the temporary container after the command finishes.

For an R-only document, use:

```bash
docker compose run --rm analysis-env quarto render
```

If necessary, specify the Quarto source file after `quarto render`.

## Data and Reproducibility

All downloaded raw data should be stored in `data/raw/`, while cleaned datasets should be stored in `data/processed/`.

The analysis uses a cleaned dataset of 46,859 Steam games released between 2018 and 2022. The dataset is randomly split into training (80%) and test (20%) sets using seed 1234. The training set is used for exploratory data analysis, model development, and model selection, while the test set is reserved for final model evaluation.

Document the steps required to reproduce the analysis and avoid committing large data files that exceed GitHub's file-size limits.

## Pull Request Process

Create a new branch from an up-to-date `main` branch and choose a short, descriptive name, such as `add-eda-plot` or `fix-data-cleaning`.

Keep changes focused on one task and use meaningful commit messages. Before submitting a Pull Request, run and test the analysis inside the Docker container.

Push your branch to GitHub and open a Pull Request into `main`. Describe your changes, link any relevant GitHub Issues, and request a review from at least one teammate before merging.

The reviewer should merge the Pull Request after approval. Contributors should not push directly to `main`.

Python code should follow the PEP 8 style guide.

## AI Usage Policy

AI tools, including ChatGPT and GitHub Copilot, may be used to assist with debugging, documentation, code explanations, and brainstorming.

Contributors are responsible for understanding and verifying all AI-generated code or text before submitting it. AI-assisted code must be tested to ensure that it works correctly. Substantial AI assistance should be disclosed in the relevant Pull Request or documentation.

All contributors must follow UBC MDS academic integrity guidelines and ensure that contributions are reviewed by a human team member before merging. Contributors remain responsible for the accuracy and quality of their work.

## Code of Conduct

All contributors are expected to follow the project's `CODE_OF_CONDUCT.md` and communicate respectfully with teammates.

## Attribution

These guidelines were adapted from the UBC MDS Breast Cancer Predictor contributing guidelines and adjusted for our DSCI 522 Group 13 project.
