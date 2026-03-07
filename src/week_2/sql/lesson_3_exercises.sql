-- 1. Все пользователи, отсортированные по дате регистрации (новые сверху)
select *
from users u
order by u.signup_date DESC;
-- 2. Только активные пользователи (is_active = true)
select *
from users u
where u.is_active is true;
-- 3. Пользователи, зарегистрированные в 2024 году (подсказка: EXTRACT(YEAR FROM date) или date >= '2024-01-01')
select * 
from users u
where extract('year' from u.signup_date) = 2024;
-- 4. Пользователи, у которых email содержит 'test.ru' (LIKE)
select *
from users u
where u.email like '%test.ru';
-- 5. Количество всех пользователей (COUNT)
select count(*)
from users;
-- 6. Количество активных пользователей
select count(*)
from users u
where u.is_active is true;
-- 7. Пользователи без даты регистрации (signup_date IS NULL)
select *
from users u
where u.signup_date is null;
-- 8. Уникальные домены почты (подсказка: substring + DISTINCT, или просто выведи email)
select distinct split_part(email, '@', 2)
from users u;
-- 9. Первые 3 пользователя по алфавиту имени
select *
from users u
where u.name is not null and u.name != ''
order by u.name
limit 3;
-- 10. Пользователи, зарегистрированные НЕ в 2024 году (комбинация WHERE + NOT или <> )
select *
from users u
where extract('year' from u.signup_date) <> 2024;
-- Бонус заданиe
-- "Чистых" пользователей: у которых заполнены имя, email и дата,
-- и имя не пустое, и имя не содержит пробелов только.
-- Результат: отсортирован по дате регистрации, только колонки name, email, signup_date
select u.name, u.email, u.signup_date
from users u
where 1=1 
	and u.name is not null
	and u.name != ''
	and u.email is not null
	and u.signup_date is not null
order by u.signup_date;