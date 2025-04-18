Группа: РИ-411050  
Гуаман Вела Бруно Паоло  
Николаев Иван Сергеевич

## Цель работы

Настроить отказоустойчивую архитектуру PostgreSQL с использованием физической потоковой репликации (streaming replication) и реализовать сценарий автоматического переключения (failover) на реплику при отказе основного узла.

## Используемые технологии

- PostgreSQL 14
- Docker и Docker Compose (MacOS M1 Pro)

## Структура проекта
pg-failover-lab/
├── docker-compose.yml
├── primary/
├── standby/
├── failover.sh
├── README.md
└── screenshots/

## Этапы выполнения работы

### 1. Создан кластер из трёх контейнеров:
- primary — основной сервер PostgreSQL (порт 5433)
- standby — реплика, работает в режиме ожидания (порт 5434)
- arbiter — дополнительный контейнер для имитации арбитра

### 2. На primary были отредактированы файлы конфигурации:
- postgresql.conf (listen_addresses = '*' ; wal_level = replica ; max_wal_senders = 10 ; synchronous_standby_names = 'standby')
- pg_hba.conf (host replication all all trust)

После настройки сервер был перезапущен.

### 3. Инициализация реплики
На контейнере standby была удалена предустановленная база данных, после чего выполнена инициализация с помощью команды:
pg_basebackup -h primary -D /var/lib/postgresql/data -U postgres -Fp -Xs -P -R

### 4. На primary была создана тестовая таблица, чтобы проверять работу

Запрос: CREATE TABLE replicated_table (id INT);

Затем эта таблица отобразилась при просмотре структуры базы данных на standby через \dt .

### 5. Эмуляция отказа основного узла

Для симуляции отказа был остановлен контейнер primary через docker stop primary.

На standby отсутствовала доступность primary, что подтверждалось командой ping primary.

### 6. Проверка доступности arbiter

На standby был выполнен ping arbiter, который подтвердил наличие связи.

### 7. Реализация failover через bash-агент

Создан скрипт failover.sh, который выполняет следующие действия:
- Проверяет доступность primary через ping
- Если primary недоступен — проверяет наличие связи с arbiter
- Если arbiter доступен — выполняет pg_ctl promote, чтобы переключить standby в режим основного узла

### 8. Проверка результата failover

После успешного выполнения promote на standby, была создана новая таблица в базе данных запросом: 
CREATE TABLE after_failover (id INT);

### Выводы

В ходе выполнения лабораторной работы был развёрнут отказоустойчивый кластер PostgreSQL с физической потоковой репликацией. Проведена симуляция отказа основного узла и реализован механизм автоматического переключения на реплику. Все действия сопровождаются логикой, соответствующей условиям лабораторной работы.

### PSDT

Скриншоты, подтверждающие выполнение этапов лабораторной работы, находятся в папке screenshots/.
