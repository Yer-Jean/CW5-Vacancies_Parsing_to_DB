# Курсовая работа №5
### Курс "Работа с базами данных"


## Парсер вакансий и работа с базой данных
В результате работы программы в базе данных сохраняются данные о компаниях и их вакансиях, полученных через API
с сайта HeadHunter.ru. Так же программа позволяет выводить на экран данные из базы данных, согласно запросам:
- список всех компаний и количество вакансий у каждой компании
- список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
- среднюю зарплату по вакансиям
- список всех вакансий, у которых зарплата выше средней по всем вакансиям
- список всех вакансий, в названии которых содержатся переданные в метод слова, например python

## Требования для работы программы
- Сервер PostgreSQL (локальный или удаленный) с имеющейся на нем, установленной по умолчанию, базой данных postgres
- Отредактированный файл example.env, находящийся в корневой директории проекта, согласно параметрам доступа к
имеющемуся серверу PostgreSQL. Затем это файл необходимо переименовать в .env
- Доступ по API к сайту hh.ru авторизации не требует
- Установленные зависимости, указанные в файле pyproject.toml

## Логика работы программы
### Программа разделена на две части:

1. Поиск компаний, удовлетворяющий поисковому запросу пользователя (например: "IT company").
Поиск осуществляется в названии компании и в её описании. Для полученных компаний, выбираются размещенные ими вакансии.
Вакансии берутся те, у которых указана оплата: либо "от", либо "до", либо и то и другое.
Оба списка (компании и их вакансии) сохраняются в базу данных. Если такая база была до этого, то она удаляется.

3. Показ компаний и их вакансий, хранящихся в базе данных, согласно запросам, указанным в соответствующем меню.

### Взаимодействие с пользователем производится в диалоговом режиме:
- ввод текста запроса, ввод ключевых слов
- выбор возможных действия на разных этапах работы программы
