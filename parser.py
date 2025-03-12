import asyncio
import aiohttp
import csv
import argparse

class AsyncSroParser:
    def __init__(self, domain: str, output_file: str):
        self.domain = domain
        self.output_file = output_file
        
        if self.domain == "nostroy":
            self.url = "https://reestr.nostroy.ru/api/sro/all/member/list"
            self.payload_filters = {
                "member_status": 1,
                "sro_enabled": True
            }
        elif self.domain == "nopriz":
            self.url = "https://reestr.nopriz.ru/api/sro/all/member/list"
            self.payload_filters = {
                "member_status": 1,
                "sro_enabled": True,
                "state": ["disabled"]
            }
        else:
            raise ValueError("domain должен быть 'nostroy' или 'nopriz'")

    async def parse_and_save(self, max_pages=None):
        # Отключаем проверку SSL
        connector = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            # 1. Узнаём общее число страниц
            payload = {
                "filters": self.payload_filters,
                "page": 1,
                "pageCount": "100",
                "sortBy": {}
            }
            async with session.post(self.url, json=payload) as resp:
                resp.raise_for_status()
                data_json = await resp.json()

            total_pages = int(data_json["data"]["countPages"])

            # Если указано max_pages, ограничиваемся им
            if max_pages is not None:
                total_pages = min(total_pages, max_pages)

            # 2. Собираем данные по страницам асинхронно
            tasks = []
            for page in range(1, total_pages + 1):
                tasks.append(self.fetch_page(session, page))

            results = await asyncio.gather(*tasks)

            # 3. Запись в CSV
            with open(self.output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow([
                    "member_full_desc",
                    "inn",
                    "sro_full_desc",
                    "sro_registration_number"
                ])

                for items in results:
                    for item in items:
                        member_full_description = item.get("full_description", "")
                        sro_block = item.get("sro", {})
                        sro_full_description = sro_block.get("full_description", "")
                        inn = item.get("inn", "")
                        sro_registration_number = sro_block.get("registration_number", "")

                        writer.writerow([
                            member_full_description,
                            inn,
                            sro_full_description,
                            sro_registration_number
                        ])

    async def fetch_page(self, session: aiohttp.ClientSession, page: int):
        payload = {
            "filters": self.payload_filters,
            "page": page,
            "pageCount": "100",
            "sortBy": {}
        }
        async with session.post(self.url, json=payload) as resp:
            resp.raise_for_status()
            data_json = await resp.json()
        return data_json["data"]["data"]


async def main_async(domain: str, max_pages: int = None):
    tasks = []
    if domain in ["both", "nostroy"]:
        parser_nostroy = AsyncSroParser("nostroy", "output/nostroy_members.csv")
        tasks.append(parser_nostroy.parse_and_save(max_pages))

    if domain in ["both", "nopriz"]:
        parser_nopriz = AsyncSroParser("nopriz", "output/nopriz_members.csv")
        tasks.append(parser_nopriz.parse_and_save(max_pages))

    await asyncio.gather(*tasks)


def main():
    parser = argparse.ArgumentParser(description="Асинхронный парсер reestr.nostroy.ru / reestr.nopriz.ru (SSL off).")
    parser.add_argument(
        "--domain",
        choices=["nostroy", "nopriz", "both"],
        default="both",
        help="Что парсим: 'nostroy', 'nopriz' или 'both' (по умолчанию both)."
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Ограничить кол-во страниц. Если не указано, парсим все."
    )
    args = parser.parse_args()
    asyncio.run(main_async(args.domain, args.max_pages))


if __name__ == "__main__":
    main()
