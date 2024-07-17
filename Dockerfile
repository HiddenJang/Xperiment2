# Используем базовый образ Python
FROM python:3.10
# Устанавливаем переменные окружения для Python (для логирования и вывода в консоль)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
SHELL ["/bin/bash", "-c"]
RUN pip install --upgrade pip
RUN apt update

RUN useradd -rms /bin/bash xperiment2 && chmod 777 /opt /run
# Устанавливаем рабочую директорию контейнера
WORKDIR /xperiment2
# Копируем все файлы проекта в рабочую директорию контейнера
COPY . /xperiment2/
#сменить владельца и скопировать все файлы из текущей директории(где лежит файл Dockerfile) в рабочую(WORKDIR)
#COPY --chown=cryptomonkey:cryptomonkey . .
# Устанавливаем зависимости из requirements.txt
#COPY requirements.txt /app/
RUN pip install -r requirements.txt
RUN python manage.py collectstatic
USER xperiment2
CMD ["gunicorn", "-b", "0.0.0.0:8000", "Xperiment2.wsgi:application"]