# Команды для работы с Docker

## Сборка образа
```bash
docker build -t login-test-automation .
```

## Запуск тестов в контейнере (без веб-сервера)
```bash
docker run --rm login-test-automation
```

## Запуск тестов с Allure веб-сервером
```bash
docker run --rm -p 5050:5050 login-test-automation /app/run-tests-with-allure.sh
```
После выполнения тестов Allure веб-сервер будет доступен по адресу: **http://localhost:5050**

**Важно:** Контейнер будет работать до тех пор, пока вы не остановите его (Ctrl+C). Веб-сервер будет доступен пока контейнер запущен.

## Запуск с сохранением результатов Allure на хост
```bash
docker run --rm -v ${PWD}/allure-results:/app/allure-results login-test-automation
```
Результаты будут сохранены в папку `allure-results` на вашем хосте.

## Запуск с интерактивным режимом (для отладки)
```bash
docker run --rm -it login-test-automation /bin/bash
```

## Генерация статического Allure отчета (без веб-сервера)
```bash
docker run --rm -v ${PWD}/allure-report:/app/allure-report login-test-automation sh -c "pytest --alluredir=allure-results -v && allure generate allure-results -o allure-report --clean"
```
Отчет будет сгенерирован в папку `allure-report` на хосте.