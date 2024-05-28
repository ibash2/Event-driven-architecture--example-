app: Основное приложение.

    api: Конечные точки API.
        router.py: Определение маршрутов и обработчиков.
        schemas.py: Модели для API. 
        exeptions.py: Определение базовых ошибок для API 

    core: Основные настройки и конфигурации.
        config.py: Конфигурации проекта (например, параметры подключения к RabbitMQ и Kafka).
        logger_config.py: Конфгурация логера (например настрока стандартного логера, также добавил Loki).
        gunicorn_config.py: Конфигурация запуска проекта (чуть переделаю в коде срач).
    
    services: Сервисы для взаимодействия с RabbitMQ и Kafka.
        rabbitmq_service.py: Реализация сервиса для работы с RabbitMQ.
        kafka_service.py: Реализация сервиса для работы с Kafka.
        redis.py: Сервис для синхронной работы с Redis (Скоро переделаю на асинхронную).

    utils: Утилиты и вспомогательные функции.
        message_broker.py: Абстракция для работы с брокерами сообщений.
        base_model.py: Улучшенная версия базовой модели Pydantic.
        logger.py: Класс для объявления логеров.
    
    database.py: Определение подключения к базе данных, объявление моделей, создание сессий.
    main.py: Точка входа в приложение.

    Если у вас микросервис, который не предоставляет API, а, например, обрабатывает сообщения 
    из очередей или выполняет фоновую работу, то логика работы вашего сервиса должна быть 
    сосредоточена в обработчиках сообщений и фоновых задачах.

    tasks: Определение обработчиков Event-ов брокера сообшений.
        consumer.py: Логика для потребления сообщений из очередей.  
        worker.py: Фоновые задачи или основная бизнес-логика.

tests: Тесты для приложения.

    test_endpoints.py: Тесты для конечных точек API.
    test_rabbitmq.py: Тесты для RabbitMQ.
    test_kafka.py: Тесты для Kafka.

requirements.txt: Зависимости проекта.

Dockerfile: Инструкция для создания Docker-образа.

docker-compose.yml: Конфигурация Docker Compose для развертывания приложения и связанных сервисов.

justfile: Объявление простых коман для удобной работы с приложением в консоли.