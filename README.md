# FastAPI Chat Application with RabbitMQ

Это приложение на FastAPI обеспечивает обмен сообщениями между двумя пользователями в заданной комнате с использованием RabbitMQ. Приложение реализует эндпоинт для отправки сообщений и веб-сокет для получения обновлений.

## Описание проекта

Приложение позволяет двум пользователям взаимодействовать в режиме реального времени через веб-сокеты. Оно устанавливает соединение с RabbitMQ и обеспечивает обработку сообщений только для избранных комнат, позволяя сообщениям передаваться только между двумя пользователями.

## Инструменты и технологии

- **FastAPI**: Современный веб-фреймворк для создания API на Python
- **RabbitMQ**: Брокер сообщений для обеспечения общения между микросервисами
- **Pydantic**: Библиотека для проверки данных и сериализации
- **uvicorn**: Сервер для запуска FastAPI-приложения