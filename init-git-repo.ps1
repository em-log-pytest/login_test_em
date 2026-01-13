# Скрипт для инициализации Git репозитория в текущей папке
# Запустите этот скрипт из папки J:\Ai-code\login_test_em

Write-Host "Инициализация Git репозитория..." -ForegroundColor Green

# Проверяем наличие Git
$gitCmd = $null
$gitPaths = @(
    "git",
    "C:\Program Files\Git\cmd\git.exe",
    "C:\Program Files (x86)\Git\cmd\git.exe",
    "$env:LOCALAPPDATA\GitHubDesktop\resources\app\git\cmd\git.exe"
)

foreach ($path in $gitPaths) {
    try {
        if ($path -eq "git") {
            $result = Get-Command git -ErrorAction SilentlyContinue
            if ($result) {
                $gitCmd = "git"
                break
            }
        } else {
            if (Test-Path $path) {
                $gitCmd = $path
                break
            }
        }
    } catch {
        continue
    }
}

if (-not $gitCmd) {
    Write-Host "`nGit не найден в системе!" -ForegroundColor Red
    Write-Host "Пожалуйста, используйте встроенный терминал GitHub Desktop:" -ForegroundColor Yellow
    Write-Host "1. Откройте GitHub Desktop" -ForegroundColor Yellow
    Write-Host "2. Repository -> Open in Command Prompt (или Open in Git Bash)" -ForegroundColor Yellow
    Write-Host "3. Выполните команды:" -ForegroundColor Yellow
    Write-Host "   git init" -ForegroundColor Cyan
    Write-Host "   git add ." -ForegroundColor Cyan
    Write-Host "   git commit -m 'Initial commit'" -ForegroundColor Cyan
    exit
}

Write-Host "Найден Git: $gitCmd" -ForegroundColor Green

# Инициализируем репозиторий
Write-Host "`nИнициализация репозитория..." -ForegroundColor Yellow
& $gitCmd init

# Добавляем все файлы
Write-Host "Добавление файлов..." -ForegroundColor Yellow
& $gitCmd add .

# Создаем первый коммит
Write-Host "Создание первого коммита..." -ForegroundColor Yellow
& $gitCmd commit -m "Initial commit: Selenium login tests with Docker support"

Write-Host "`nГотово! Репозиторий инициализирован." -ForegroundColor Green
Write-Host "Теперь в GitHub Desktop:" -ForegroundColor Yellow
Write-Host "1. File -> Add Local Repository" -ForegroundColor Yellow
Write-Host "2. Выберите папку: J:\Ai-code\login_test_em" -ForegroundColor Yellow
Write-Host "3. Нажмите 'Add repository'" -ForegroundColor Yellow
