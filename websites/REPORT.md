# Sprint 004 — завершение двух многоязычных сайтов

Дата отчёта: **26 октября 2026**. Бюджет: **$0**. Канонический основатель: **Alexander Romaskevich — Александр Николаевич Ромаскевич — RomaskevicH**.

## DONE

Опубликованы два новых самостоятельных сайта: профиль основателя и обзор IMPERIAL Core. Каждый содержит 10 полноценных языковых страниц (EN, UK, RU, DE, FR, ES, PT, JA, ZH, AR), отдельные URL, title/description, self-canonical, взаимные hreflang и x-default. Фото перенесено без изменения байтов. Сайты связаны друг с другом и с девятью публичными проектами GitHub. Ни один старый сайт не заменён и не опубликован повторно.

Новые адреса рассчитаны на GitHub Pages: `https://oromaskevic23-cmd.github.io/oromaskevic23-cmd/` и `https://oromaskevic23-cmd.github.io/IMPERIAL-Core-Public/`. Это бесплатный поддомен GitHub и два пути проектов. Сначала оба адреса возвращали **404**. После создания веток `gh-pages` GitHub завершил два успешных запуска `pages build and deployment`; опубликованные файлы проверены по HTTP и SHA-256. Оба сайта теперь **PUBLISHED / CRAWLABLE**. Это не означает индексацию Google.

Дизайны различаются: личный профиль — тёмный фон, золотые акценты, шрифт с засечками и крупный портрет; IMPERIAL Core — светлый фон, синие акценты, строгий шрифт без засечек, центральный заголовок и отдельные карточки направлений.

Исходная архитектура и название IMPERIAL Core сохранены. Упоминания юридического статуса, оценок, доходов, клиентов и наград не выдуманы. NDB/IMPERIUM сопровождаются точной квалификацией авторства как заявления основателя. IMPERIUM описан как долгосрочная архитектурная цифровая валюта для ИИ-агентов всего мира.

## TESTED

- 9 автоматических групп проверок успешно проверили все 20 страниц: HTML, метаданные, reciprocal hreflang, граф сущностей, файлы/ссылки/якоря, sitemap, SHA-256 и ограниченный поиск распространённых форматов секретов.
- Google Rich Results Test в режиме CODE: **1 valid item detected — Profile page — Alexander Romaskevich**. [Результат Google](https://search.google.com/test/rich-results/result/r%2Fprofile-page?id=lFnvHeACGPv_96ZzVTGKaw). Проверена английская страница основателя; остальные языки прошли локальную структурную проверку. Это была проверка исходного HTML. Дополнительно Google проверил опубликованный RU URL: **1 valid Profile page**, crawl allowed **Yes**, page fetch **Successful**, indexing allowed **Yes**. [Live URL test](https://search.google.com/test/rich-results/result?id=4BWD3AIsziG8uK45YmJ1ww). Это успешная загрузка Google Inspection Tool, не подтверждение индексации.
- В браузере проверены все 20 страниц на ширине 320 px (доступная ширина 305 px с полосой прокрутки): горизонтального переполнения нет. Исправлены декоративный фон и ширина меню в UK/PT. Арабские страницы имеют RTL.
- Переход English → Русский выполнен через меню и привёл на отдельный URL. Основное содержимое существует в HTML и доступно без JavaScript.
- 9 репозиториев, профиль и маршрут public issues: **11 HTTP 200**. Записи: [external-links.json](evidence/external-links.json).
- Фотография: 1122 × 1402, 360546 байт; SHA-256 `7758dacaa2b08ee3b305489297714d23ec4c6f819b546ea7c8e79e4fd54e7b07`. Форматы 1:1/4:3/16:9 не создавались, чтобы сохранить весь исходный кадр. Они были рекомендацией, а не обязательным условием.

## BEFORE / AFTER

| Проверка | BEFORE: исходный профиль | AFTER: новые сборки |
|---|---|---|
| Публичная доступность | HTTP 200 | Оба новых сайта HTTP 200; опубликованные файлы совпали с SHA-256 манифестами |
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
| BUILT / TESTED | Сборки, тесты и SHA-256 манифесты существуют |
| PUBLISHED | Да: HTTP 200 и совпадение опубликованных байтов |
| CRAWLABLE | Да: live HTML/фото/sitemap доступны, нет noindex; root robots.txt — 404, запрета нет |
| INDEXING_REQUESTED | Нет |
| GOOGLE_CRAWLED | Не подтверждено |
| GOOGLE_INDEXED | Не подтверждено |
| RANKING_MEASURED | Нет |
| TOP_3_VERIFIED | Нет |

## BLOCKED

Google Search Console не предоставил подтверждённый ресурс, поэтому отправка sitemap и URL Inspection не выполнены. Вход через защищённую форму GitHub не был выполнен: автоматическая проверка согласования завершилась ошибкой лимита использования. Это не оценка безопасности действия. Затем read-only проверка выявила успешные штатные Pages deployments для уже созданных веток; повторный вход для этой публикации не потребовался. Пароли, токены и фиктивные коды подтверждения не добавлены в исходники.

## NEXT — конкретная последовательность

1. Публикация двух веток `gh-pages` завершена; сохранять бесплатные адреса `github.io` и HTTPS.
2. После будущих изменений повторять `python3 websites/tools/verify_live.py`; текущая публикация прошла проверку HTTP, SHA-256 и корневого robots.txt.
3. Подтвердить два URL-prefix ресурса в Search Console по [инструкции](README.md), отправить sitemap и однократно запросить индексирование ключевых страниц. Сохранить фактические результаты URL Inspection.
4. Обновить URL сайта в GitHub account settings и согласовать переход со старых сайтов: один канонический источник, без конкурирующих копий. Пины репозиториев и био аккаунта не изменялись в этой работе.
5. Еженедельно после появления данных записывать GSC показы, клики, CTR и среднюю позицию по запросам: Alexander Romaskevich; RomaskevicH; Александр Ромаскевич; Олександр Ромаскевич; IMPERIAL Core founder; Alexander Romaskevich AI; RomaskevicH GitHub; NDB IMPERIUM creator. Наблюдение Top 3 фиксировать с датой, страной, устройством, запросом и URL; не выводить Top 3 из среднего значения позиции.
6. На следующие 30 дней: один воспроизводимый инженерный отчёт в неделю, документация реальных приложений, архитектурная статья с ограничениями, затем демонстрация подтверждённых функций. Независимое признание фиксировать только при реальном появлении.

Нет гарантии сроков индексации или позиции. Финальное решение принадлежит поисковой системе. Нет платных сервисов, рекламы, покупки ссылок или фиктивных публикаций.

## Репозитории и CI

- [Основной Draft PR #5](https://github.com/oromaskevic23-cmd/IMPERIAL-Core-Public/pull/5).
- [Профиль основателя: Draft PR #2](https://github.com/oromaskevic23-cmd/oromaskevic23-cmd/pull/2).
- [Первый зелёный CI исходников](https://github.com/oromaskevic23-cmd/IMPERIAL-Core-Public/actions/runs/40277296015); [CI профиля](https://github.com/oromaskevic23-cmd/oromaskevic23-cmd/actions/runs/40277389722).
- [Первая успешная публикация профиля](https://github.com/oromaskevic23-cmd/oromaskevic23-cmd/actions/runs/40277448810); [публикация экосистемы](https://github.com/oromaskevic23-cmd/IMPERIAL-Core-Public/actions/runs/40277453314).
- Полное имя с отчеством включено в RU title, description, подпись фото и alt; все версии содержат полное имя в видимом содержимом и alternateName Person. Индексация по ФИО остаётся задачей Google, а не заявленным результатом.

Финальная версия с разными дизайнами: [коммит исходников](https://github.com/oromaskevic23-cmd/IMPERIAL-Core-Public/commit/dbc95fe9c467a0bd20712607efaedf121bee0a73), [коммит профиля](https://github.com/oromaskevic23-cmd/oromaskevic23-cmd/commit/960a69028820fdc388c110302eac8c09fa2c18fa). Оба CI и оба Pages deployment завершились успешно. 34 публичных файла совпали с манифестами SHA-256; доказательства — [live-verification.json](evidence/live-verification.json) и [release.json](evidence/release.json). Изменения README профиля остаются в Draft PR, основные ветки не слиты.
