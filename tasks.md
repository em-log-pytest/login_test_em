# AQA Python — Login automation (saucedemo)

## Goal
Automate login tests for https://www.saucedemo.com/ using Selenium and Python.

Project must demonstrate:
- clean architecture
- Page Object pattern
- stable UI waits
- basic Allure reporting
- ability to run locally and in Docker without code changes

---

## Tech stack
- Python 3.10
- Selenium
- pytest
- Allure
- Chrome (headless)
- Docker

---

## Architecture rules (mandatory)
- Tests MUST NOT contain Selenium calls
- Page Objects MUST NOT contain assertions
- All locators MUST be stored inside Page Objects
- One Page Object per page
- Explicit waits only (`WebDriverWait`)
- `time.sleep()` is forbidden
- Browser must run in headless mode both locally and in Docker
- Window size must be fixed (1920x1080)

---

## Project structure
```text
project/
├── pages/
│   ├── base_page.py
│   └── login_page.py
├── tests/
│   └── test_login.py
├── conftest.py
├── requirements.txt
├── Dockerfile
├── README.md
└── tasks.md
