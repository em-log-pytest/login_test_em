# Используем официальный образ Python 3.10
FROM python:3.10-slim

# Устанавливаем метаданные
LABEL maintainer="Test Automation"
LABEL description="Docker image for running Selenium tests with Chrome headless"

# Настраиваем зеркала для ускорения загрузки из РФ
# Используем Яндекс зеркало (Москва) - обычно быстрее всего для РФ
# Альтернативные варианты (раскомментируйте при необходимости):
#   Digital Ocean: sed -i 's/deb.debian.org/mirrors.digitalocean.com/g' /etc/apt/sources.list
#   Cloudflare: sed -i 's/deb.debian.org/debian.cloudflare.com/g' /etc/apt/sources.list
#   Германия: sed -i 's/deb.debian.org/ftp.de.debian.org/g' /etc/apt/sources.list
RUN if [ -f /etc/apt/sources.list ]; then \
        sed -i 's/deb.debian.org/mirror.yandex.ru/g' /etc/apt/sources.list; \
        sed -i 's/security.debian.org/mirror.yandex.ru/g' /etc/apt/sources.list; \
    fi && \
    if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
        sed -i 's/deb.debian.org/mirror.yandex.ru/g' /etc/apt/sources.list.d/debian.sources; \
        sed -i 's/security.debian.org/mirror.yandex.ru/g' /etc/apt/sources.list.d/debian.sources; \
    fi || true

# Устанавливаем системные зависимости для Chrome, ChromeDriver и Allure
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    ca-certificates \
    openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Google Chrome (используем новый метод без apt-key)
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем ChromeDriver
# Используем стабильную версию ChromeDriver через chrome-for-testing
RUN CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$(google-chrome --version | awk '{print $3}' | cut -d. -f1)") \
    && if [ -z "$CHROMEDRIVER_VERSION" ]; then \
        CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE"); \
    fi \
    && wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" -O chromedriver.zip \
    && unzip -q chromedriver.zip \
    && mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf chromedriver.zip chromedriver-linux64

# Создаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Устанавливаем Allure CLI
RUN ALLURE_VERSION=$(curl -s "https://api.github.com/repos/allure-framework/allure2/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/') \
    && wget -q "https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz" -O allure.tgz \
    && tar -xzf allure.tgz -C /opt/ \
    && mv /opt/allure-${ALLURE_VERSION} /opt/allure \
    && ln -s /opt/allure/bin/allure /usr/local/bin/allure \
    && rm -f allure.tgz

# Создаем директорию для результатов Allure
RUN mkdir -p /app/allure-results

# Создаем скрипт для запуска тестов с Allure serve
# Скрипт правильно обрабатывает сигналы для graceful shutdown
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Функция для обработки сигналов\n\
cleanup() {\n\
    echo ""\n\
    echo "Получен сигнал остановки. Завершение работы..."\n\
    exit 0\n\
}\n\
\n\
# Устанавливаем обработчики сигналов\n\
trap cleanup SIGTERM SIGINT\n\
\n\
echo "Запуск тестов..."\n\
pytest --alluredir=allure-results -v\n\
echo "Тесты завершены. Запуск Allure веб-сервера..."\n\
echo "Allure отчет будет доступен по адресу: http://localhost:5050"\n\
echo "Нажмите Ctrl+C для остановки"\n\
\n\
# Используем exec для замены процесса, чтобы сигналы обрабатывались правильно\n\
exec allure serve allure-results --host 0.0.0.0 --port 5050\n\
' > /app/run-tests-with-allure.sh && chmod +x /app/run-tests-with-allure.sh

# Запускаем тесты с генерацией Allure отчетов (по умолчанию без веб-сервера)
CMD ["pytest", "--alluredir=allure-results", "-v"]
