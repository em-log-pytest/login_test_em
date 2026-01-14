# Решение проблемы "port is already allocated"

## Проблема
Порт 5050 уже занят другим контейнером или процессом.

## Решение

### Шаг 1: Найти контейнер, использующий порт 5050
```bash
docker ps -a | grep 5050
# или
docker ps --filter "publish=5050"
```

### Шаг 2: Остановить все контейнеры с портом 5050
```bash
# Найти ID контейнера
docker ps --format "table {{.ID}}\t{{.Ports}}" | grep 5050

# Остановить контейнер (замените CONTAINER_ID на реальный ID)
docker stop CONTAINER_ID

# Или остановить все контейнеры
docker stop $(docker ps -q)
```

### Шаг 3: Проверить, что порт освободился
```bash
# Проверить, что порт свободен
netstat -tlnp | grep 5050
# или
ss -tlnp | grep 5050
```

### Шаг 4: Если порт все еще занят, найти процесс
```bash
# Найти процесс, использующий порт 5050
sudo lsof -i :5050
# или
sudo fuser -k 5050/tcp
```

### Шаг 5: Убить процесс (если нужно)
```bash
# Найти PID процесса
sudo lsof -i :5050 | grep LISTEN

# Убить процесс (замените PID на реальный)
sudo kill -9 PID
```

## Быстрое решение (остановить все контейнеры)
```bash
docker stop $(docker ps -q)
```

## Альтернатива: использовать другой порт
Если нужно запустить несколько экземпляров:
```bash
docker run --rm -p 5051:5050 login-test-automation /app/run-tests-with-allure.sh
# Тогда доступ будет по http://<IP>:5051
```
