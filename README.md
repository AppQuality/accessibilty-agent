# OpenAI Agents SDK

This project uses the `openai-agents` package to build and manage AI agents with OpenAI's APIs. The environment is managed using [conda](https://docs.conda.io/), ensuring reproducibility and easy setup for all contributors.

> **More info at:** [DeepWiki](https://deepwiki.com/cannarocks/openai-sdk-example)

## What is `openai-agents`?

`openai-agents` is a Python package that provides tools and abstractions for building, running, and managing AI agents powered by OpenAI models. It simplifies agent orchestration, prompt management, and integration with OpenAI's API.

## Getting Started

### 1. Clone the Repository

```bash
git clone git@github.com:cannarocks/openai-sdk-example.git
cd openai-sdk-example
```

### 2. Install Conda (if you don't have it)

Download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution).

### 3. Create the Environment

Create the conda environment from the provided `environment.yml` file:

```bash
conda env create -f environment.yml
```

### 4. Activate the Environment

```bash
conda activate openai-sdk-agent
```

### 5. Install Dependencies

All dependencies, including `openai-agents`, will be installed automatically when you create the environment. If you add new dependencies, update the `environment.yml` and let your collaborators know.

### 6. Usage

You can now use the `openai-agents` package in your Python scripts:

```python
import openai_agents
# Your code here
```

## Updating Dependencies

If you install new packages, export the updated environment:

```bash
conda env export --no-builds > environment.yml
```

## Contributing

- Always activate the conda environment before working.
- Update `environment.yml` if you add or remove dependencies.
- Open issues or pull requests for improvements or bug fixes.

---

**Happy collaborating!**