FROM python:3.9.0

RUN apt-get update && \
    apt-get install -y --no-install-recommends mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8 \
    ca-certificates \
    git \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV WORKDIR /app/

WORKDIR ${WORKDIR}

COPY Pipfile Pipfile.lock ${WORKDIR}

RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git && \
    cd mecab-ipadic-neologd && \
    ./bin/install-mecab-ipadic-neologd -n -y -p /usr/share/mecab/dic/neologd -u && \
    echo "dictdir = /usr/share/mecab/dic" > /usr/local/etc/mecabrc

RUN pip install pipenv --no-cache-dir && \
    pipenv install --system --deploy && \
    pip uninstall -y pipenv virtualenv-clone virtualenv

COPY . $WORKDIR

SHELL ["/bin/bash", "-c"]