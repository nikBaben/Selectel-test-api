import logging
from typing import Optional

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import upsert_external_vacancies
from app.schemas import ExternalVacanciesResponse


logger = logging.getLogger(__name__)

API_URL = "https://api.selectel.ru/proxy/public/employee/api/public/vacancies"


async def fetch_page(client: httpx.AsyncClient, page: int) -> ExternalVacanciesResponse:
    response = await client.get(
        API_URL,
        params={"per_page": 1000, "page": page},
    )
    response.raise_for_status()
    return ExternalVacanciesResponse.model_validate(response.json())


def safe_name(obj: object | None) -> str | None:
    if obj is None:
        return None

    name = getattr(obj, "name", None)
    if not name:
        return None

    return str(name).strip()

def map_item_to_payload(item) -> dict:
    return {
        "external_id": item.id,
        "title": item.title,
        "timetable_mode_name": safe_name(item.timetable_mode),
        "tag_name": safe_name(item.tag),
        "city_name": safe_name(item.city),
        "published_at": item.published_at,
        "is_remote_available": item.is_remote_available,
        "is_hot": item.is_hot,
    }


async def parse_and_store(session: AsyncSession) -> int:
    logger.info("Старт парсинга вакансий")

    timeout = httpx.Timeout(10.0, read=20.0)
    created_total = 0
    page = 1

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            while True:
                payload = await fetch_page(client, page)

                parsed_payloads = [map_item_to_payload(item) for item in payload.items]

                if parsed_payloads:
                    created_total += await upsert_external_vacancies(session, parsed_payloads)

                if page >= payload.page_count:
                    break

                page += 1

    except httpx.HTTPStatusError as exc:
        logger.exception(
            "HTTPStatusError при парсинге вакансий: status=%s url=%s",
            getattr(exc.response, "status_code", None),
            getattr(exc.request, "url", None),
        )
        return 0
    except httpx.RequestError as exc:
        logger.exception("RequestError при парсинге вакансий: %s", exc)
        return 0
    except Exception:
        logger.exception("Неожиданная ошибка парсинга вакансий")
        return 0

    logger.info("Парсинг завершен, новых вакансий: %s", created_total)
    return created_total
