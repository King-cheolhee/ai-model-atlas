# -*- coding: utf-8 -*-
"""atlas 원본 + 직접 작성한 한국어 설명 -> 배포용 index.html 한 장.

사용법:  python build.py [atlas.json 경로]
기본 입력 경로는 data/atlas.source.json 이다.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src", "index.template.html")
DESC = os.path.join(ROOT, "data", "descriptions.ko.json")
OUT = os.path.join(ROOT, "index.html")
DEFAULT_ATLAS = os.path.join(ROOT, "data", "atlas.source.json")

# 11개 세부 분야를 레퍼런스와 같은 4개 묶음으로
GROUP = {
    "시계열·표 데이터 예측": "예측",
    "금융·경제 예측": "예측",
    "날씨·기후·환경": "예측",
    "건강·의료 예측": "예측",
    "생명과학(단백질·DNA·세포)": "과학",
    "화학·신소재": "과학",
    "월드 모델·영상 예측": "세계·로봇",
    "로봇 AI": "세계·로봇",
    "AI 훈련 환경·시뮬레이터": "세계·로봇",
    "인간 행동·사회 시뮬레이션": "세계·로봇",
    "범용 AI 도구·경량화": "도구",
}

# GitHub API가 NOASSERTION으로만 표기하지만 LICENSE 원문을 직접 대조해 확인한 것
LICENSE_FIX = {
    "TiRex": "NXAI Community",
    "TabPFN": "Prior Labs",
}

# 코드는 자유 라이선스인데 가중치만 비상업이거나, 별도 협의가 필요한 것
NONCOMMERCIAL = {
    "Pangu-Weather", "SleepFM (sleepfm-clinical)", "OlmoEarth v1 (Nano/Tiny/Base/Large)",
    "InternVLA-M1", "LongLive", "Delphi-2M", "AgentTorch (Large Population Models)",
    "Centaur", "life2vec", "AlphaFold 3",
}
NC_PAT = re.compile(r"비상업|BY-NC|NonCommercial|별도 라이선스|승인받아야")


def lean(item, desc):
    gh = item.get("gh") or {}
    name = item["name"]
    note = item.get("note")
    out = {
        "name": name,
        "category": item["category"],
        "group": GROUP[item["category"]],
        "org": item["org"],
        "org_type": item["org_type"],
        "desc": desc[name],
        "license": LICENSE_FIX.get(name) or gh.get("license") or None,
        "weights": item.get("weights"),
        "bytes": item.get("weights_bytes"),
        "tier": item.get("tier"),
        "params_ko": item.get("params_ko"),
        "variant_range": item.get("variant_range"),
        "hf_downloads": item.get("hf_downloads"),
        "stars": gh.get("stars"),
        "gh_url": gh.get("url"),
        "pushed": (gh.get("pushed_at") or "")[:10] or None,
        "variants": [
            {"id": v["id"], "url": v["url"], "size": v.get("size")}
            for v in (item.get("variants") or [])
        ],
        "gated": bool(item.get("gated")),
        "archived": bool(gh.get("archived")),
        "noncommercial": name in NONCOMMERCIAL or bool(note and NC_PAT.search(note)),
        "note": note,
    }
    if out["license"] == "NOASSERTION":
        out["license"] = None
    return {k: v for k, v in out.items() if v not in (None, [], False)}


def main():
    atlas_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ATLAS
    raw = json.load(open(atlas_path, encoding="utf-8"))
    items = raw["items"]
    desc = {k: v for k, v in json.load(open(DESC, encoding="utf-8")).items()
            if not k.startswith("_")}

    names = {i["name"] for i in items}
    missing = names - set(desc)
    extra = set(desc) - names
    if missing or extra:
        print("설명 키 불일치 — 빌드 중단")
        for m in sorted(missing):
            print("  설명 없음:", m)
        for e in sorted(extra):
            print("  대상 없음:", e)
        return 1

    unknown = {i["category"] for i in items} - set(GROUP)
    if unknown:
        print("분류 매핑 누락 — 빌드 중단:", unknown)
        return 1

    payload = {"measured": raw["measured"],
               "items": [lean(i, desc) for i in items]}
    blob = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    # </script> 로 스크립트 블록이 조기 종료되는 것을 막는다
    blob = blob.replace("</", "<\\/")

    html = open(SRC, encoding="utf-8").read()
    if "__DATA__" not in html:
        print("템플릿에 __DATA__ 자리표시자가 없다 — 빌드 중단")
        return 1
    html = html.replace("__DATA__", blob)
    open(OUT, "w", encoding="utf-8", newline="\n").write(html)

    with_w = sum(1 for i in payload["items"] if i.get("bytes"))
    nc = sum(1 for i in payload["items"] if i.get("noncommercial"))
    print("빌드 완료:", OUT)
    print("  모델 %d종 / 설명 %d개 / 가중치 보유 %d종 / 비상업·조건부 %d종"
          % (len(items), len(desc), with_w, nc))
    print("  데이터 %.1f KB, 최종 HTML %.1f KB"
          % (len(blob.encode()) / 1024, os.path.getsize(OUT) / 1024))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
