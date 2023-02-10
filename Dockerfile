# Define custom function directory
ARG LAMBDA_TASK_ROOT="/var/task"

# =========== #
# BUILD IMAGE #
# =========== #
FROM python:3.11-slim-bullseye as build-image

# Include global arg in this stage of the build
ARG LAMBDA_TASK_ROOT
RUN mkdir -p ${LAMBDA_TASK_ROOT}

# Setting poetry envs
# POETRY_HOME: installs poetry to the specified location
# POETRY_VIRTUALENVS_IN_PROJECT: creates the .venv in the project's root
# POETRY_NO_INTERACTION: do not ask any interactive questions
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

# Add poetry to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install aws-lambda-cpp build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    cmake \
    curl \
    g++ \
    libcurl4-openssl-dev \
    make \
    unzip && \
    curl -sSL https://install.python-poetry.org | python3 -

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy required files for the build
COPY poetry.lock pyproject.toml ./

# Installs poetry project dependencies
RUN poetry install --no-root --no-ansi --without dev

# ============= #
# RUNTIME IMAGE #
# ============= #
FROM python:3.11-slim-bullseye

# Include global arg in this stage of the build
ARG LAMBDA_TASK_ROOT
RUN mkdir -p ${LAMBDA_TASK_ROOT}

# PYTHONDONTWRITEBYTECODE: prevents writing bytecode to disk
# PYTHONUNBUFFERED: ensures that the Python are sent to the terminal
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="${LAMBDA_TASK_ROOT}/.venv/bin:$PATH"

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy the built dependencies
COPY --from=build-image ${LAMBDA_TASK_ROOT}/.venv ${LAMBDA_TASK_ROOT}/.venv

# Copy the application
COPY json_dataset_faker ${LAMBDA_TASK_ROOT}

# Set Lambda Runtime Interface Client as the Python entrypoint
ENTRYPOINT [ "/var/task/.venv/bin/python", "-m", "awslambdaric" ]

# Specifies the function handler
CMD [ "main.handler" ]
