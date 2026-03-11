CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    order_date DATE NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('new', 'paid', 'shipped', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Тестовые данные
INSERT INTO orders (user_id, order_date, amount, status) VALUES
    (1, '2024-01-20', 1500.00, 'paid'),
    (1, '2024-02-15', 3200.50, 'shipped'),
    (3, '2024-01-10', 890.00, 'cancelled'),
    (4, '2024-03-01', 5000.00, 'new'),
    (5, '2024-02-28', 1200.00, 'paid'),
    (5, '2024-03-05', 750.00, 'paid');

-- 1. INNER JOIN: Пользователи + их заказы (только у кого есть заказы)
select u.id as user_id, u.name, o.order_date, o.amount, o.status
from users u
inner join orders o
on u.id = o.user_id;
-- 2. LEFT JOIN: Все пользователи + их заказы (если есть), включая тех, у кого заказов нет
select u.id as user_id, u.name, o.order_date, o.amount, o.status
from users u
left join orders o
on u.id = o.user_id;
-- 3. Агрегация: Сколько заказов и на какую сумму сделал каждый пользователь (по имени)
select u.name, COUNT(o.order_date) as cnt_orders, SUM(o.amount) as total_sum
from users u
left join orders o
on u.id = o.user_id
group by u.name;
-- 4. Фильтрация после агрегации: Пользователи, потратившие > 2000 руб (подсказка: HAVING)
select u.name, COUNT(o.order_date) as cnt_orders, SUM(o.amount) as total_sum
from users u
left join orders o
on u.id = o.user_id
group by u.name
having SUM(o.amount) > 2000;
-- 5. Статусы: Количество заказов по каждому статусу (группировка по status)
select status, count(*) as cnt_orders
from orders
group by status;
-- 6. Месячная метрика: Новые пользователи по месяцам (используй DATE_TRUNC)
select date_trunc('month', signup_date) as months, count(distinct id) as mau
from users
group by date_trunc('month', signup_date);
-- 7. "Брошенные корзины": Пользователи, у которых есть заказ со статусом 'new', но нет 'paid'
select distinct u.id, u.name
from users u
where exists (
    select 1
from orders o1
where o1.user_id = u.id
and o1.status = 'new'
)
and not exists (
    select 1
from orders o2
where o2.user_id = u.id
and o2.status = 'paid'
);
-- 8. Бонус: Топ-3 пользователя по сумме заказов за 2024 год (имя, общая сумма, кол-во заказов)
select u.name, count(o.order_date) as cnt_orders, sum(o.amount) as total_amount
from users u
left join orders o
on u.id = o.user_id
where o.order_date >= '2024-01-01' and o.order_date < '2025-01-01'
group by u.name
order by sum(o.amount) desc
limit 3;

-- Анализ запроса
EXPLAIN analyze
select u.id as user_id, u.name, o.order_date, o.amount, o.status
from users u
left join orders o
on u.id = o.user_id;