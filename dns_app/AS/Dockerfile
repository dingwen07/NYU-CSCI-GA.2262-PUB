FROM python:3.11

RUN apt-get update \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN groupadd -g 799 nyu && \
    useradd -r -u 999 -g nyu nyu

# Set up a working folder and install the pre-reqs
WORKDIR /app

RUN chmod 777 /app

USER nyu

COPY --chown=nyu:nyu . .

EXPOSE 53533/udp

CMD [ "python", "./run.py" ]
