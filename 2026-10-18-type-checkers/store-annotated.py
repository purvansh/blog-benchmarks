"""A small inventory service. Ten type errors are planted in here.

They are deliberately not obvious: no bare `1 + "x"`, nothing a reader spots in
a second. Each one is the shape of a mistake that survives review, and each is
annotated in the test harness by line number rather than by a comment here, so
a checker cannot find them by reading a marker.
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Item:
    sku: str
    name: str
    qty: int
    tags: list[str] = field(default_factory=list)


class Inventory:
    def __init__(self) -> None:
        self._items: dict[str, Item] = {}

    def add(self, item: Item) -> None:
        self._items[item.sku] = item

    def find(self, sku: str) -> Optional[Item]:
        return self._items.get(sku)

    def label(self, sku: str) -> str:
        item = self.find(sku)
        return item.name.upper()                      # BUG 1: item may be None

    def restock(self, sku: str, qty: str) -> int:
        item = self._items[sku]
        item.qty += qty                               # BUG 2: int += str
        return item.qty

    def rename(self, sku: str, name: str) -> None:
        item = self._items[sku]
        item.title = name                             # BUG 3: no such attribute

    def total(self) -> int:
        running = 0
        for item in self._items.values():
            running += item.qty
        if running > 0:
            return running                            # BUG 4: falls through to None

    def by_tag(self, tag: str) -> list[Item]:
        out = {}
        for item in self._items.values():
            if tag in item.tags:
                out[item.sku] = item
        return out                                    # BUG 5: dict, not list

    def bulk_add(self, items: list[Item]) -> None:
        for sku in items:
            self.add(sku, sku.sku)                    # BUG 6: add takes 1 arg

    def quantities(self) -> dict[str, int]:
        return {item.name: str(item.qty)              # BUG 7: values are str
                for item in self._items.values()}


async def fetch_remote(sku: str) -> Item:
    await asyncio.sleep(0)
    return Item(sku=sku, name="remote", qty=1)


async def sync_one(inv: Inventory, sku: str) -> None:
    item = fetch_remote(sku)                          # BUG 8: missing await
    inv.add(item)


def summarise(inv: Inventory, skus: list[str]) -> str:
    parts = []
    for sku in skus:
        parts.append(inv.find(sku))
    return ", ".join(parts)                           # BUG 9: joining Optional[Item]


def apply_discount(price: float, pct: int = 10) -> float:
    return price * (1 - pct / 100)


def checkout(prices: list[float]) -> float:
    return sum(apply_discount(p, "10") for p in prices)   # BUG 10: str for int
