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
Make sure that ~/.gitconfig exists as a file, not as a directory. If Docker creates a directory at this path because the Git configuration file does not exist, remove the incorrectly created directory, configure your Git name and email using the commands above, and restart the container.

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

The project requires an Ed25519 public SSH key at `~/.ssh/id_ed25519.pub`. Follow the SSH key setup and troubleshooting steps in the [README](README.md) if the key is missing or if Docker created a directory at `~/.ssh/id_ed25519.pub`.

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

### Adding or Updating Packages

If you need an additional Python package, first create or switch to a feature branch and connect to the running container. Then, use `uv add` to install the package and update the project's dependency files:

```bash
uv add package-name
```

To specify a particular version, use:

```bash
uv add package-name==1.2.3
```

After adding the package, commit both updated dependency files, pyproject.toml and uv.lock, to ensure that the project environment remains reproducible.

Next, push your branch to GitHub. The GitHub Actions workflow runs when a push to any branch changes the Dockerfile, dependency files, or workflow file, building and publishing a new Docker image and committing the updated image tag in docker-compose.yml back to that branch.

Once the workflow completes on your branch, pull the updated repository changes and Docker image by running the following commands:

```bash
git pull
docker compose pull
```
Make sure you use the image tag specified in the updated docker-compose.yml file. This ensures that your local environment uses the updated Docker image with the new dependencies.

Then, submit a Pull Request and have it reviewed and merged into main. If merging into main updates the relevant files on main and runs the workflow there as well, switch to main after the workflow completes and run:

```bash
git pull
docker compose pull
```

This ensures that the project environment on `main` uses the latest published Docker image.

## Reproducing the Analysis

To rerun the analysis, open a terminal in the project directory and execute:

```bash
docker compose run --rm analysis-env uv run quarto render analysis/videogames-regression.qmd
```

The rendered HTML report will be saved at `analysis/videogames-regression.html`.

The `--rm` option automatically removes the temporary container after the command finishes.

### Publishing the Report on GitHub Pages

After reproducing the analysis and rendering the Quarto report, contributors can publish the updated report on GitHub Pages.

The Quarto report is configured with `embed-resources: true`, which embeds the required resources into the HTML file and makes it self-contained.

From the repository root, copy the rendered HTML report to the `docs` directory as `index.html`:

```bash
mkdir -p docs
cp analysis/videogames-regression.html docs/index.html
touch docs/.nojekyll
```
Commit and push the updated report:

```bash
git add docs/index.html docs/.nojekyll
git commit -m "Update published analysis report"
git push
```

The report is published through GitHub Pages and can be accessed at:

https://ubc-mds-2026-27.github.io/DSCI-522-Group-13-Steam-Game-popularity-analysis/

Whenever you update the analysis and re-render the report, repeat these steps and commit and push the updated docs/ files so the published report on GitHub Pages stays current.

## Data and Reproducibility

All downloaded raw data should be stored in `data/raw/`, while cleaned datasets should be stored in `data/processed/`.

The analysis uses a cleaned dataset of 46,859 Steam games released between 2018 and 2022. The dataset is randomly split into training (80%) and test (20%) sets using seed 1234. The training set is used for exploratory data analysis, model development, and model selection, while the test set is reserved for final model evaluation. All preprocessing transformations must be fitted using only the training data and then applied to the test data to prevent data leakage.

Document the steps required to reproduce the analysis and avoid committing large data files that exceed GitHub's file-size limits.

## Pull Request Process

Create a new branch from an up-to-date `main` branch and choose a short, descriptive name, such as `add-eda-plot` or `fix-data-cleaning`.

Keep changes focused on one task and use meaningful commit messages. Before submitting a Pull Request, run and test the analysis inside the Docker container.

Push your branch to GitHub and open a Pull Request into `main`. Describe your changes, link any relevant GitHub Issues, and request a review from at least one teammate before merging.

The reviewer should merge the Pull Request after approval. Contributors should not push directly to `main`.
All contributors are expected to participate in the project's collaboration process by opening, reviewing, and contributing to the resolution of GitHub Issues and Pull Requests. Every change should be submitted through a Pull Request and reviewed by at least one teammate before being merged.

Python code should follow the PEP 8 style guide.

## AI Usage Policy

AI tools, including ChatGPT and GitHub Copilot, may be used to assist with debugging, documentation, code explanations, and brainstorming.

Contributors are responsible for understanding and verifying all AI-generated code or text before submitting it. AI-assisted code must be tested to ensure that it works correctly. Substantial AI assistance should be disclosed in the relevant Pull Request or documentation.

All contributors must follow UBC MDS academic integrity guidelines and ensure that contributions are reviewed by a human team member before merging. Contributors remain responsible for the accuracy and quality of their work.

## Code of Conduct

All contributors are expected to follow the project's `CODE_OF_CONDUCT.md` and communicate respectfully with teammates.

## Attribution

These guidelines were adapted from the UBC MDS Breast Cancer Predictor contributing guidelines and adjusted for our DSCI 522 Group 13 project.
