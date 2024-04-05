ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}
SHELL ["/bin/bash", "-l", "-c"]
ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 20.0.0
#####################################
# Set Timezone
#####################################
ARG TZ=UTC
ENV TZ ${TZ}
RUN apt-get update && apt-get install -y dos2unix

COPY ./docker/scraper-botasaurus-request/setup.sh /usr/local/bin/
RUN set -eu && chmod +x /usr/local/bin/setup.sh
RUN dos2unix /usr/local/bin/setup.sh

RUN curl --silent -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.2/install.sh | bash
RUN source $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default \
    && npm install -g pm2
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

RUN /usr/local/bin/python -m pip install --upgrade pip && /usr/local/bin/python -m pip install poetry
COPY ./poetry.lock ./poetry.toml ./pyproject.toml /var/app/

RUN cd /var/app/ && poetry install

ENTRYPOINT ["/bin/bash", "-l", "-c", "setup.sh"]
