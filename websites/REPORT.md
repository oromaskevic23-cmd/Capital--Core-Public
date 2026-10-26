# Sprint 004 — завершение двух многоязычных сайтов

Дата отчёта: **26 октября 2026, Europe/Kyiv**. Бюджет: **$0**. Канонический основатель: **Alexander Romaskevich — Александр Николаевич Ромаскевич — RomaskevicH**.

## DONE

Подготовлены два новых самостоятельных сайта: профиль основателя и обзор IMPERIAL Core. Каждый содержит 10 полноценных языковых страниц (EN, UK, RU, DE, FR, ES, PT, JA, ZH, AR), отдельные URL, title/description, self-canonical, взаимные hreflang и x-default. Фото перенесено без изменения байтов. Сайты связаны друг с другом и с девятью публичными проектами GitHub. Ни один старый сайт не заменён и не опубликован повторно.

Новые адреса рассчитаны на GitHub Pages: `https://oromaskevic23-cmd.github.io/oromaskevic23-cmd/` и `https://oromaskevic23-cmd.github.io/IMPERIAL-Core-Public/`. Это бесплатный поддомен GitHub и два пути проектов. На момент проверки до включения Pages оба адреса возвращали **404**; сами адреса пока не считаются работающими сайтами.

Исходная архитектура и название IMPERIAL Core сохранены. Упоминания юридического статуса, оценок, доходов, клиентов и наград не выдуманы. NDB/IMPERIUM сопровождаются точной квалификацией авторства как заявления основателя. IMPERIUM описан как долгосрочная архитектурная цифровая валюта для ИИ-агентов всего мира.

## TESTED

- 8 автоматических групп проверок успешно проверили все 20 страниц: HTML, метаданные, reciprocal hreflang, граф сущностей, файлы/ссылки/якоря, sitemap, SHA-256 и ограниченный поиск распространённых форматов секретов.
- Google Rich Results Test в режиме CODE: **1 valid item detected — Profile page — Alexander Romaskevich**. [Результат Google](https://search.google.com/test/rich-results/result/r%2Fprofile-page?id=lFnvHeACGPv_96ZzVTGKaw). Проверена английская страница основателя; остальные языки прошли локальную структурную проверку. Это не проверка опубликованного URL и не подтверждение индексации.
- В браузере проверены все 20 страниц на ширине 320 px (доступная ширина 305 px с полосой прокрутки): горизонтального переполнения нет. Исправлены декоративный фон и ширина меню в UK/PT. Арабские страницы имеют RTL.
- Переход English → Русский выполнен через меню и привёл на отдельный URL. Основное содержимое существует в HTML и доступно без JavaScript.
- 9 репозиториев, профиль и маршрут public issues: **11 HTTP 200**. Записи: [external-links.json](evidence/external-links.json).
- Фотография: 1122 × 1402, 360546 байт; SHA-256 `7758dacaa2b08ee3b305489297714d23ec4c6f819b546ea7c8e79e4fd54e7b07`. Форматы 1:1/4:3/16:9 не создавались, чтобы сохранить весь исходный кадр. Они были рекомендацией, а не обязательным условием.

## BEFORE / AFTER

| Проверка | BEFORE: исходный профиль | AFTER: новые сборки |
|---|---|---|
| Публичная доступность | HTTP 200 | До включения Pages: HTTP 404; локальная сборка проверена |
| Canonical | Отсутствовал | Свой HTTPS URL для каждой из 20 страниц |
| Person / ProfilePage | Отсутствовали | Единый Person ID; ProfilePage на 10 страницах основателя |
| Organization | На разных источниках разные домены | Единый Organization ID и founder → Person |
| Языки | JS-переключатель EN/UK/RU в исходнике | 10 полноценных URL на каждом сайте |
| Hreflang | Не найден | 10 языков + x-default, взаимные ссылки |
| Sitemap | 404 | Два XML sitemap по 10 страниц с фото |
| Фото | Уже опубликовано на образце | Тот же файл, SHA-256 совпадает |
| Телефон / RTL | В этой работе ранее не подтверждено | 20 страниц проверены, Arabic RTL |
| Google indexing | Не подтверждено | Не подтверждено |

### Датированный аудит исходных публичных URL

Ниже сохранены наблюдения 25 октября 2026. Они не выдаются за повторную live-проверку 26 октября. Полные title, description, robots, noindex, изображения и метаданные — в [before.json](evidence/before.json).

| Публичный URL | HTTP | Canonical | H1 | Имя видно | JSON-LD | Sitemap HTTP |
|---|---|---|---|---|---|---|
| https://imperialcore.netlify.app/ | 200 | https://imperialcore-github.val.run/ | 1 | Да | Нет | 200 |
| https://imperialcore.val.run/ | 404 | Нет | 1 | Нет | Нет | None |
| https://constructor-ai-imperial.floot.app/ | 200 | Нет | 1 | Да | Нет | 403 |
| https://imperial-core-cheat-sheet.oromaskevic23.chatgpt.site/ | 200 | https://imperialcore.eu.org/ | 1 | Да | [['ProfilePage', 'Person', 'Organization', 'WebSite']] | 200 |
| https://alexander-romaskevich-architect.oromaskevic23.chatgpt.site/ | 200 | Нет | 1 | Да | Нет | 404 |
| https://romaskevich-authorship.oromaskevic23.chatgpt.site/ | 200 | https://romaskevich-authorship.oromaskevic23.chatgpt.site/ | 1 | Да | [['WebSite', 'ProfilePage', 'Person', 'Organization', 'CreativeWork', 'CreativeWork', 'CreativeWork']] | 200 |
| https://ndb-imperium-verify.oromaskevic23.chatgpt.site/en-US | 200 | https://ndb-imperium-verify.oromaskevic23.chatgpt.site/en-US | 1 | Да | ['WebPage'] | 200 |
| https://imperial-core-official.oromaskevic23.chatgpt.site/ | 200 | https://imperial-core-official.oromaskevic23.chatgpt.site/ | 1 | Да | [['Organization', 'Person', 'WebPage', 'WebSite']] | 200 |
| https://imperial-core-architect.oromaskevic23.chatgpt.site/ | 200 | https://imperial-core-architect.oromaskevic23.chatgpt.site/ | 1 | Да | [['WebSite', 'Organization', 'Person']] | 200 |
| https://human-protection-constitution.oromaskevic23.chatgpt.site/ | 200 | Нет | 1 | Да | Нет | 404 |
| https://github.com/oromaskevic23-cmd | 200 | https://github.com/oromaskevic23-cmd | 3 | Да | Нет | None |

Критичные найденные расхождения: старый Netlify-сайт указывает canonical/sitemap на `imperialcore-github.val.run`, который возвращал 404; cheat-sheet указывает `imperialcore.eu.org`, который возвращал 503; профиль-образец не имел canonical, JSON-LD и sitemap. По последнему указанию владельца старые сайты оставлены образцами, поэтому эти live-конфигурации не изменены. Их перенос/редиректы остаются отдельным следующим этапом после работающих новых URL.

## PUBLISHED / CRAWLABLE / INDEXED

| Статус | Доказательство |
|---|---|
| DRAFTED | Сборки и SHA-256 манифесты существуют |
| PUBLISHED | Пока не подтверждено: Pages требуется включить |
| CRAWLABLE | Подготовлено в коде; live-проверка после включения |
| INDEXING_REQUESTED | Нет |
| GOOGLE_CRAWLED | Не подтверждено |
| GOOGLE_INDEXED | Не подтверждено |
| RANKING_MEASURED | Нет |
| TOP_3_VERIFIED | Нет |

## BLOCKED

GitHub-подключение позволяет записывать код и Draft PR, но не предоставляет операцию включения GitHub Pages. В браузере настройки Pages требуют входа в GitHub. Google Search Console также не предоставил подтверждённый ресурс. Пароли, токены и фиктивные коды подтверждения не добавлены в исходники.

## NEXT — конкретная последовательность

1. Включить Pages для двух подготовленных веток `gh-pages`, корень `/`, бесплатные адреса `github.io`, HTTPS.
2. Выполнить `python3 websites/tools/verify_live.py`; поднять статус до PUBLISHED/CRAWLABLE только после HTTP 200, совпадения SHA-256 и проверки корневого robots.txt.
3. Подтвердить два URL-prefix ресурса в Search Console по [инструкции](README.md), отправить sitemap и однократно запросить индексирование ключевых страниц. Сохранить фактические результаты URL Inspection.
4. После публикации обновить URL сайта в GitHub account settings и согласовать переход со старых сайтов: один канонический источник, без конкурирующих копий. Пины репозиториев и био аккаунта не изменялись в этой работе.
5. Еженедельно после появления данных записывать GSC показы, клики, CTR и среднюю позицию по запросам: Alexander Romaskevich; RomaskevicH; Александр Ромаскевич; Олександр Ромаскевич; IMPERIAL Core founder; Alexander Romaskevich AI; RomaskevicH GitHub; NDB IMPERIUM creator. Наблюдение Top 3 фиксировать с датой, страной, устройством, запросом и URL; не выводить Top 3 из среднего значения позиции.
6. На следующие 30 дней: один воспроизводимый инженерный отчёт в неделю, документация реальных приложений, архитектурная статья с ограничениями, затем демонстрация подтверждённых функций. Независимое признание фиксировать только при реальном появлении.

Нет гарантии сроков индексации или позиции. Финальное решение принадлежит поисковой системе. Нет платных сервисов, рекламы, покупки ссылок или фиктивных публикаций.
