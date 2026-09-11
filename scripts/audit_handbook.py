"""Lightweight structural audit for a generated travel-handbook HTML file.

This is a guardrail, not a fact checker. It reports obvious missing UI markers;
the handbook author must still verify actual venues, links, routes and behavior.
"""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED_TAB_IDS = ("home", "itinerary", "stay", "sights", "check", "notes")
REQUIRED_MARKERS = {
    "左上角目录按钮": ("☰ 目录", "menuButton"),
    "本地勾选状态": ("localStorage",),
    "照片上传": ("上传照片",),
    "照片查看": ("查看照片",),
    "照片删除": ("删除当前照片",),
    "Google Maps": ("Google Maps",),
    "小红书搜索": ("小红书搜索",),
}


def any_marker(text: str, choices: tuple[str, ...]) -> bool:
    return any(choice in text for choice in choices)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a static travel handbook HTML file.")
    parser.add_argument("html", type=Path, help="absolute or relative path to the handbook HTML")
    args = parser.parse_args()

    try:
        text = args.html.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.html}")
        return 2
    except UnicodeDecodeError:
        print(f"ERROR: {args.html} is not UTF-8 HTML")
        return 2

    errors: list[str] = []
    warnings: list[str] = []

    for tab_id in REQUIRED_TAB_IDS:
        if f'id="{tab_id}"' not in text and f"id='{tab_id}'" not in text:
            errors.append(f"missing required tab id: {tab_id}")

    for label, choices in REQUIRED_MARKERS.items():
        if not any_marker(text, choices):
            errors.append(f"missing required marker: {label}")

    if "官网购票" in text and "查看检查清单" not in text:
        warnings.append("ticket button found but no visible checklist-jump marker")
    if "餐厅" in text and "tel:" not in text and "电话待确认" not in text:
        warnings.append("restaurant content found but neither tel: nor 电话待确认 appears")
    if "当地体验" in text and "Google Maps" not in text:
        warnings.append("local-experience tab found but no Google Maps marker")
    if "route-map" not in text and "路线示意" not in text:
        warnings.append("no obvious local route-map marker found")

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")

    if errors:
        print(f"FAIL: {len(errors)} structural requirement(s) missing")
        return 1

    print("PASS: core handbook markers found")
    if warnings:
        print("Review warnings manually; this script cannot verify real-world facts or interaction behavior.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
