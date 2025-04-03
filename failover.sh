#!/bin/bash

PRIMARY_HOST="primary"
ARBITER_HOST="arbiter"
PG_DATA="/var/lib/postgresql/data"
PG_CTL="/usr/lib/postgresql/14/bin/pg_ctl"

# Пингуем primary (1 попытка, таймаут 2 сек)
ping -c1 -W2 $PRIMARY_HOST &> /dev/null
if [ $? -ne 0 ]; then
    echo "Primary недоступен. Проверяем arbiter..."

    ping -c1 -W2 $ARBITER_HOST &> /dev/null
    if [ $? -eq 0 ]; then
        echo "Arbiter доступен. Выполняем promote..."
        $PG_CTL promote -D "$PG_DATA"
    else
        echo "Нет связи с arbiter. Promote не выполнен."
    fi
else
    echo "Primary доступен. Ничего не делаем."
fi
