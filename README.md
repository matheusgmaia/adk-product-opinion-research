# Product Opinions Research Multiagent System


## Overview

This is a Product Opinion Research Assistant. The main functionality is to analyze Youtube videos to gather relevant information and opinions about products.


### Agent architecture:

This diagram shows the detailed architecture of the agents and tools used
to implement this workflow.
<img src="multi_agent_diagram.png" alt="multi agent diagram" width="800"/>

## Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/matheusgmaia/adk-product-opinion-research.git
    cd adk-product-opinion-research
    ```

2.  **Install `uv`:** If you haven't already, install `uv` following the instructions on their website.

3.  **Create Virtual Environment:**
    ```bash
    uv venv
    ```
    This creates a `.venv` directory. You don't typically need to activate it manually, as `uv run` handles it.

4.  **Install Dependencies:**
    ```bash
    uv sync
    ```
    This command installs all dependencies listed in `pyproject.toml` and `uv.lock` into the `.venv`.


5.  **Configuration**

    *   Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    *   Review the `.env` file and adjust settings if necessary

    *   Authenticate your GCloud account.

        ```bash
        gcloud auth application-default login
        gcloud auth application-default set-quota-project $GOOGLE_CLOUD_PROJECT
        ```

## Running the Agent

**Using `adk`**

ADK provides convenient ways to bring up agents locally and interact with them.
You may talk to the agent using the CLI:

```bash
adk run product-research-agent
```

Or on a web interface:

```bash
 adk web
```

The command `adk web` will start a web server on your machine and print the URL.
You may open the URL, select "academic_research" in the top-left drop-down menu, and
a chatbot interface will appear on the right. The conversation is initially
blank.

## Customization

The Product Opinions Research Agent can be customized and extended to better suit your requirements. For example:
 1. Integrate Specialized Search Tools: Augment the agent's discovery capabilities by incorporating additional  search functionalities, such as an google search tool.
 2. Implement Output Visualization: Enhance the presentation of research findings by adding modules and instruction to better visualize the results.
 3. Develop with price search functionality.
 4. Reset needed state informations at each interaction.