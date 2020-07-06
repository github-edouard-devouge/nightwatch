### multistage-build dockerfile for nightwatch-all-in-one

# Build vuejs app
FROM node:latest as build-vuejs
ARG projectName=nightwatch
ARG appRoot=/app/$projectName
ARG jsProjectRoot=./webui/$projectName
WORKDIR $appRoot
COPY $jsProjectRoot .
# Install deps and compile artifacts
RUN npm install
RUN npm run build

# Build python3 app
FROM python:3.8-buster as build-python
ARG projectName=nightwatch
ARG appRoot=/app/$projectName
WORKDIR $appRoot
COPY . .
RUN make build-py


# Production image
FROM python:3.8-buster as production
# Define some default variables (overwritten with build extra-args)
ARG projectName=nightwatch
ARG appRoot=/app/$projectName
ARG webUiRoot=$appRoot/webui

# Set workdir
WORKDIR $appRoot

# Copy conf
ADD conf/* /etc/$projectName/

# Copy static website builded artifacts
COPY --from=build-vuejs $appRoot/dist $webUiRoot

# Copy python builded artifacts to dist directory
COPY --from=build-python $appRoot/dist $appRoot/dist

# Install system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Install all python wheel files in dist directory
RUN pip install --upgrade pip && \
    pip install --find-links=$appRoot/dist $(cd $appRoot/dist; ls -1 *.whl | awk -F - '{ gsub("_", "-", $1); print $1 }' | uniq)

# Clean package artifacts directory
RUN rm -rf $appRoot/dist

# Set few env vars
ENV AWS_DEFAULT_REGION='eu-west-1'
ENV APP_ROOT=$appRoot
ENV WEBUI_ROOT=$webUiRoot

# Run entrypoint script
CMD ["uvicorn", "nightwatch:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
