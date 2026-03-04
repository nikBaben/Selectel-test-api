# Selectel Test API

Тестовое задание для стажировки **Python Backend Developer** в Selectel.

Проект реализует сервис для работы с вакансиями:  
парсинг данных, сохранение в базу и предоставление API для получения вакансий с фильтрацией.

---

## 📂 Структура репозитория

```
├── seletest-api-task/   # 📌 Реализованное тестовое задание
└── seletest-api/        # 📄 Описание и условия тестового задания
```
---

## ⚙️ Стек технологий

- **Python 3.11+**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **Docker / Docker Compose**
- **Pydantic**
- **AsyncIO**
- **HTTPX**

---

## 🚀 Возможности API

Сервис предоставляет следующие возможности:

### 📌 Парсинг вакансий
- загрузка вакансий из внешнего API
- сохранение данных в базу
- защита от дублирования


## Запуск проекта

### 1. Клонировать репозиторий
### 2. Запустить через Docker
docker compose up --build
## 🧪 API Testing

Для тестирования API можно использовать **Swagger** или **Postman**.

### Swagger

Интерактивная документация доступна по ссылке:

[Swagger UI](http://localhost:8000/docs)

---

### Postman

Готовая коллекция запросов для тестирования API:

[Open Postman Collection](https://elements.getpostman.com/redirect?entityId=39888884-c01a6c52-7451-4b7d-8269-c541b826a19e&entityType=collection)


