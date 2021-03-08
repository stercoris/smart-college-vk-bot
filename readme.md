# Prorok SUN---Boy VkBot

### Это бот на vk-api, прикрепенный к [PHP Rest-Апишке](https://github.com/stercoris/old-tpcol-api), а в будущем [TypeScript GraphQL-Апишке](https://github.com/stercoris/tpcol-api), который,через удобный интерфейс, позволяет:
 - Подписываться на рассылку расписания
 - Смотреть экзамены
 - Смотреть расписание на Завтра/Сегодня
 - я тоже думал, что тут больше будет

Todos:
  - Менее громоздкий докер
  - token.txt => .env
  - database_create.py / ORM
  - погода

Библиотеки:

* [pyowm](https://pyowm.readthedocs.io/en/latest/) - Погода
* [vk-api](https://pypi.org/project/vk-api/) - VK-API
* [schedule](https://schedule.readthedocs.io/en/stable/) - Работа с эвентами.

### Installation

```sh
$ git clone stercoris/smart-college-vk-bot
$ echo {vk-token} > token.txt
$ pip install -r requirements.txt
$ python3 logic.py
```
