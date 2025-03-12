# 🔍 Асинхронный парсер реестров НОСТРОЙ и НОПРИЗ

Этот проект представляет собой **асинхронный парсер** для сайтов:
- [reestr.nostroy.ru](https://reestr.nostroy.ru/api/sro/all/member/list)
- [reestr.nopriz.ru](https://reestr.nopriz.ru/api/sro/all/member/list)

Парсер собирает информацию о членах саморегулируемых организаций (СРО), включая:
- **Название организации** (`member_full_desc`)
- **ИНН** (`inn`)
- **Название СРО** (`sro_full_desc`)
- **Регистрационный номер СРО** (`sro_registration_number`)

Работает **асинхронно**, что позволяет быстро обрабатывать большие объёмы данных.  
Проверка SSL отключена (`verify_ssl=False`), так как серверы реестров могут использовать некорректные сертификаты.

---

## 🚀 Установка и запуск локально

### 1. Клонирование репозитория
```bash
git clone https://github.com/ai-zaytsev/sro-membres-parse.git
cd sro-membres-parse
```

### 2. Создание виртуального окружения (рекомендуется)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Запуск
```bash
python parser.py --domain both --max-pages 2
```
- `--domain`: `nostroy`, `nopriz` или `both` (по умолчанию `both`).
- `--max-pages`: ограничение количества страниц (если не указано, парсит все).

После выполнения в каталоге `output/` появятся CSV-файлы:

- `nostroy_members.csv` (если парсили `nostroy`)
- `nopriz_members.csv` (если парсили `nopriz`)

---

## 🔄 Как работает парсер?

1. Делает **асинхронные HTTP-запросы** к API НОСТРОЙ/НОПРИЗ.
2. Определяет количество страниц (`countPages`).
3. Параллельно опрашивает все страницы, получая данные о членах СРО.
4. Сохраняет результаты в папку `output/` формата CSV:
   ```
   member_full_desc;inn;sro_full_desc;sro_registration_number
   ООО "СтройГрупп";1234567890;СРО "Гильдия строителей";СРО-С-001-12345
   ООО "ПроектИнвест";0987654321;СРО "Ассоциация проектировщиков";СРО-П-002-67890
   ```

---

## 🛠 CI/CD и Docker

### Автоматическая сборка Docker-образа

- В проекте настроен **GitHub Actions**, который автоматически собирает Docker-образ при каждом пуше, если изменились файлы кода, `Dockerfile` или `requirements.txt`.
- Когда вы пушите изменения в репозиторий (кроме правок `README.md`), Actions запускается, собирает Docker-образ и публикует его в [DockerHub](https://hub.docker.com/r/aizaytsev/sro-members-parser).

> **Важно**: При изменении только `README.md` (или других файлов, перечисленных в `paths-ignore`), Actions **не** запускается, и новый образ **не** создаётся.

### Обновление Docker-образа на сервере

После того, как GitHub Actions соберёт новую версию образа и загрузит её в DockerHub, **сервер не обновляется автоматически**.  
Чтобы обновиться вручную, нужно на сервере выполнить команды:
```bash
docker pull aizaytsev/sro-members-parser:latest
docker stop sro_parser || true
docker rm sro_parser || true
docker run -d --name sro_parser aizaytsev/sro-members-parser:latest --domain both
```
*(Путь к вашему образу и параметры – по необходимости.)*

---

## ❓ Возможные проблемы и решения

### 🔹 `ModuleNotFoundError: No module named 'aiohttp'`
Установите зависимости:
```bash
pip install -r requirements.txt
```

### 🔹 `SSL: CERTIFICATE_VERIFY_FAILED`
В проекте эта проблема решается отключением проверки SSL (`verify_ssl=False`), поэтому ошибка не должна возникнуть.

### 🔹 `PermissionError: [Errno 13] Permission denied: 'output/...'`
Убедитесь, что у вас есть права на запись в папку `output/`. На Linux/Mac:
```bash
mkdir -p output
chmod 777 output
```
На Windows — запустите терминал от имени администратора.

---

## 📜 Лицензия

Проект распространяется под лицензией **MIT**.

---

## 🤝 Контакты

📌 Автор: **Алексей Зайцев**  
📌 GitHub: **[@ai-zaytsev](https://github.com/username)**  
📌 Email: **ai.zaysev89@gmail.com**
