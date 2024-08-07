import re
import secrets
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def generate_api_key() -> str:
    api_key = ""
    while len(api_key) < 32:
        # One iteration suffices 99.4992% of the time.
        api_key += secrets.token_urlsafe(3 * 9).replace("_", "").replace("-", "")
    return api_key[:32]


def has_api_key_format(key: str) -> bool:
    return bool(re.fullmatch(r"([A-Za-z0-9]){32}", key))


def assert_is_not_none(value: T | None) -> T:
    assert value is not None
    return value


def process_list_in_batches(
    lst: list[T], chunk_size: int, process_batch: Callable[[list[T]], None]
) -> None:
    offset = 0

    while True:
        items = lst[offset : offset + chunk_size]
        if not items:
            break
        process_batch(items)
        offset += chunk_size


def optional_bytes_to_mib(value: int | None) -> int | None:
    if value is None:
        return None
    else:
        return value >> 20
