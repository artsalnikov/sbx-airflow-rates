# Демо загрузки курса BTC/USD в Postgres с помощью Apache Airflow

В проекте разворачиваются контейнеры с минимальной инфраструктурой 
Apache Airflow и Postgres.

В Airflow созданы два DAG:
- `btc_usd_daily_rate` - загрузка последней информации о курсе (за сегодня);
- `btc_usd_historical_rates` - загрузка исторической ежедневной информации о курсе.


## Разорачивание и запуск

Клонируйте проект

```bash
  git clone git@github.com:artsalnikov/sbx-airflow-rates.git
```

Перейдите в репозиторий проекта

```bash
  cd sbx-airflow-rates
```

### Разворачивание

Запустите скрипт разворачивания контейнеров
- `init.sh` - на Unix;
- `init.bat` - на Windows.

### Настройка PGAdmin

Перейдите на страницу PGAdmin http://localhost:8081, 
войдите под учётной записью `admin@admin.com`/`secret`.

Добавьте новый сервер (*Add New Server*), на вкладке *Connection* укажите:
- *Hostname/address*: `postgres_container`, 
- *Username*: `airflow`,
- *Password*: `airflow`.

Раскройте базу данных `airflow` и схему `public`, далее к ней потребуется 
обращаться для проверки результатов работы Airflow.

### Запуск и проверка

Перейдите на страницу UI Airflow http://localhost:8080/home, 
войдите под учётной записью `airflow`/`airflow`.

#### Загрузка последнего курса

Найдите DAG `btc_usd_daily_rate`, снимите его с паузы и дождитесь 
запуска по расписанию, или запустите его вручную.

После успешного завершения перейдите в ранее настроенный PGAdmin 
и выберите все данные из таблицы `btc_used_rate`. 

```sql
select *
from btc_usd_rate
order by rate_date
;
```

В таблице должна быть одна строка, содержащая курс за сегодня.

#### Загрузка истории курсов стандартной глубины

В UI Airflow найдите DAG `btc_usd_historical_rates` и запустите его 
вручную.

После успешного завершения перейдите в ранее настроенный PGAdmin 
и выберите все данные из таблицы `btc_used_rate` (см. запрос выше).

В таблице должны быть курсы с 01.01.2022 по сегодня.

#### Загрузка истории курсов выбранной глубины

В UI Airflow найдите DAG `btc_usd_historical_rates` и запустите его 
вручную с указанием конфига `{"start_date": "2021-01-01"}`.

После успешного завершения перейдите в ранее настроенный PGAdmin 
и выберите все данные из таблицы `btc_used_rate` (см. запрос выше).

В таблице должны быть курсы с 01.01.2021 по сегодня.
