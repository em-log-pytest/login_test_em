# Команды для работы с Docker

## Сборка образа
```bash
docker build -t login-test-automation .
```

## Запуск тестов в контейнере
```bash
docker run --rm login-test-automation
```

## Запуск с сохранением результатов Allure
```bash
docker run --rm -v ${PWD}/allure-results:/app/allure-results login-test-automation
```

## Запуск с интерактивным режимом (для отладки)
```bash
docker run --rm -it login-test-automation /bin/bash
```

## Просмотр логов
```bash
docker run --rm login-test-automation pytest --alluredir=allure-results -v -s
```
