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

---

## 🚀 Установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/ai-zaytsev/sro-membres-parse.git
cd sro_parser
```

### 2. Создание виртуального окружения (рекомендуется)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

---

## 🔧 Использование

Скрипт поддерживает аргументы командной строки, позволяя управлять парсингом.

### 📌 Примеры запуска:

📌 **Спарсить только `nostroy` (все страницы)**:
```bash
python parser.py --domain nostroy
```

📌 **Спарсить только `nopriz` (все страницы)**:
```bash
python parser.py --domain nopriz
```

📌 **Спарсить оба реестра (по умолчанию)**:
```bash
python parser.py --domain both
```

📌 **Протестировать парсер, ограничив количество страниц (например, 2 страницы):**
```bash
python parser.py --domain both --max-pages 2
```

---

## 📂 Где сохраняются результаты?

После выполнения работы в каталоге `output/` появятся файлы:

- **`output/nostroy_members.csv`** (если парсился `nostroy`)
- **`output/nopriz_members.csv`** (если парсился `nopriz`)

Формат CSV:
```
member_full_desc;inn;sro_full_desc;sro_registration_number
ООО "СтройГрупп";1234567890;СРО "Гильдия строителей";СРО-С-001-12345
ООО "ПроектИнвест";0987654321;СРО "Ассоциация проектировщиков";СРО-П-002-67890
...
```

---

## 🔄 Как работает парсер?

1. Делает **асинхронные HTTP-запросы** к API НОСТРОЙ и НОПРИЗ.
2. Определяет количество страниц, необходимых для парсинга.
3. Параллельно запрашивает данные со всех страниц.
4. Сохраняет результаты в CSV-файл.

⚠️ **Обратите внимание:**  
Проверка SSL отключена (`verify_ssl=False`), так как серверы реестров могут использовать некорректные сертификаты.

---

## ❓ Возможные проблемы и решения

### 🔹 `ModuleNotFoundError: No module named 'aiohttp'`
📌 Установите зависимости:
```bash
pip install -r requirements.txt
```

### 🔹 `SSL: CERTIFICATE_VERIFY_FAILED`
Проблема с сертификатами на сервере. В этом проекте она решена отключением проверки (`verify_ssl=False`), так что ошибки быть не должно.

### 🔹 `PermissionError: [Errno 13] Permission denied: 'output/nostroy_members.csv'`
📌 Проверьте права доступа к папке `output/`:
```bash
mkdir -p output
chmod 777 output  # Linux/Mac
```
На Windows попробуйте запустить командную строку **от имени администратора**.

---

## 🛠 Требования

- Python 3.8+  
- Установленный `pip`  
- Библиотеки из `requirements.txt` (`aiohttp`)

---

## 📜 Лицензия

Проект распространяется под лицензией **MIT**.

---

## 🤝 Контакты

📌 Автор: **Алексей Зайцев**  
📌 GitHub: **[@ai-zaytsev](https://github.com/username)**  
📌 Email: **ai.zaysev89@gmail.com**

