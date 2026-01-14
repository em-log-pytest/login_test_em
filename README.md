# Selenium Login Automation Tests

Автоматизированные тесты для проверки функциональности логина на [saucedemo.com](https://www.saucedemo.com/) с использованием Selenium, Python и Docker.

## Описание проекта

Проект демонстрирует:
- Чистую архитектуру с использованием Page Object Pattern
- Стабильные UI ожидания через WebDriverWait
- Allure отчетность
- Запуск тестов локально и в Docker без изменений кода

## Технологический стек

- Python 3.10
- Selenium WebDriver
- pytest
- Allure
- Chrome (headless)
- Docker

## Требования

- Docker (для запуска в контейнере)
- Или Python 3.10+ с установленными зависимостями (для локального запуска)




## Установка и запуск

### Вариант 1: Копирование проекта через файловый менеджер

1. **Скопируйте проект** в нужную директорию на вашем сервере/LXC контейнере:
   ```bash
   # Например, в /home/login_test_em
   cp -r /path/to/login_test_em /home/login_test_em
   ```

2. **Перейдите в директорию проекта**:
   ```bash
   cd /home/login_test_em
   ```

3. **Соберите Docker образ**:
   ```bash
   docker build -t login-test-automation .
   ```

4. **Запустите тесты**:
   
   **Только тесты (без веб-сервера)**:
   ```bash
   docker run --rm login-test-automation
   ```
   
   **Тесты с Allure веб-сервером**:
   ```bash
   docker run --rm --init -p 5050:5050 login-test-automation /app/run-tests-with-allure.sh
   ```
   
   После выполнения тестов Allure веб-сервер будет доступен по адресу: **http://<IP_вашего_сервера>:5050**






### Вариант 2: Клонирование проекта из GitHub

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/em-log-pytest/login_test_em.git
   cd login_test_em
   ```

2. **Соберите Docker образ**:
   ```bash
   docker build -t login-test-automation .
   ```

3. **Запустите тесты**:
   
   **Только тесты (без веб-сервера)**:
   ```bash
   docker run --rm login-test-automation
   ```
   
   **Тесты с Allure веб-сервером**:
   ```bash
   docker run --rm --init -p 5050:5050 login-test-automation /app/run-tests-with-allure.sh
   ```
   
   После выполнения тестов Allure веб-сервер будет доступен по адресу: **http://localhost:5050** (или **http://<IP_вашего_сервера>:5050**)





## Структура проекта

```
login_test_em/
├── pages/              # Page Objects
│   ├── base_page.py    # Базовый класс для всех страниц
│   └── login_page.py   # Page Object для страницы логина
├── tests/              # Тесты
│   └── test_login.py   # Тесты логина
├── conftest.py         # Настройки pytest и WebDriver
├── requirements.txt    # Python зависимости
├── Dockerfile          # Docker образ для запуска тестов
└── README.md           # Документация
```

## Тесты

Проект содержит 5 тестов для проверки различных сценариев авторизации:

1. **Успешный логин** (standard_user / secret_sauce)
2. **Логин с неверным паролем**
3. **Логин заблокированного пользователя** (locked_out_user)
4. **Логин с пустыми полями**
5. **Логин пользователем performance_glitch_user** (проверка работы при задержках)

## Дополнительные команды

### Сохранение результатов Allure на хост

```bash
docker run --rm -v $(pwd)/allure-results:/app/allure-results login-test-automation
```

### Интерактивный режим (для отладки)

```bash
docker run --rm -it login-test-automation /bin/bash
```

### Генерация статического Allure отчета

```bash
docker run --rm -v $(pwd)/allure-report:/app/allure-report login-test-automation sh -c "pytest --alluredir=allure-results -v && allure generate allure-results -o allure-report --clean"
```

## Остановка контейнера

Для остановки контейнера с Allure веб-сервером:
- Нажмите `Ctrl+C` в терминале
- Или используйте `docker stop <container_id>`

Если контейнер не останавливается по `Ctrl+C`, используйте флаг `--init` при запуске (как показано в примерах выше).

## Решение проблем

### Порт 5050 уже занят

```bash
# Остановите все запущенные контейнеры
docker stop $(docker ps -q)

# Или используйте другой порт
docker run --rm --init -p 5051:5050 login-test-automation /app/run-tests-with-allure.sh
```

### Медленная сборка образа

Dockerfile настроен на использование Яндекс зеркала для ускорения загрузки из РФ. Если возникают проблемы, можно изменить зеркало в Dockerfile.

## Архитектура

- **Page Object Pattern**: Все локаторы и методы работы со страницами вынесены в отдельные классы
- **WebDriverWait**: Используются только явные ожидания, `time.sleep()` запрещен
- **Headless режим**: Браузер работает в headless режиме для работы в Docker
- **Фиксированный размер окна**: 1920x1080 для стабильности тестов

## Лицензия

Проект создан в рамках тестового задания.

## Ссылки

- Репозиторий: https://github.com/em-log-pytest/login_test_em
- Тестируемый сайт: https://www.saucedemo.com/
