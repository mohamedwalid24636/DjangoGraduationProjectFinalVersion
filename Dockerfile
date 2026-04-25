FROM python:3.11

RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    unixodbc \
    unixodbc-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg \
    && install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/ \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

WORKDIR /app/backend

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
