# https://hub.docker.com/r/rasa/rasa-sdk/tags
FROM rasa/rasa_sdk:2.6.0
USER 1001

COPY actions /app
COPY requirements.txt /app
COPY workshop_data.csv /app

RUN pip install -r requirements.txt
CMD ["start", "actions", "--actions", "--debug"]

USER 1001
