# 대학·연구소 AI 모델 도감

대학과 공공·기업 연구소가 공개한 AI 모델 **167종**을 한 화면에서 찾는 정적 페이지.
"이 일을 내 PC에서 돌릴 수 있나 / 돈이 드나 / 어디서 받나"를 매번 다시 찾지 않으려고 만들었다.

👉 **https://King-cheolhee.github.io/ai-model-atlas/**

## 뭘 볼 수 있나

- **용량 산점도** — 점 하나가 모델 하나. 가로축은 내려받을 파일 크기(로그 눈금), 배경 띠는 필요한 장비. 점을 누르면 표의 해당 줄로 간다.
- **검색·필터** — 이름·기관·설명을 한국어로 검색. 분야·필요 장비·라이선스로 거른다.
- **줄 펼침** — GitHub·Hugging Face 링크, 크기별 변형, 파라미터 수, 최근 갱신일.
- **경고 배지** — 승인 필요(gated) / 비상업 / 보관됨.
- **다크모드** — 시스템 설정을 따르고, 토글하면 그 선택을 기억한다.

## 만드는 법

의존성 없음. 파이썬 표준 라이브러리만 쓴다.

```bash
python build.py
```

`data/atlas.source.json`(사실 데이터) + `data/descriptions.ko.json`(한 줄 설명)을
`src/index.template.html`에 합쳐 루트의 `index.html` 한 장을 만든다.
빌드 스크립트는 **설명 키와 모델 이름이 167개 전부 일치하는지 먼저 확인하고**, 어긋나면 중단한다.

```
build.py                     빌드 스크립트
src/index.template.html      HTML·CSS·JS 원본 (__DATA__ 자리에 데이터가 들어감)
data/atlas.source.json       사실 데이터 (모델명·기관·라이선스·용량·링크)
data/descriptions.ko.json    한 줄 설명 167개 (직접 작성)
fonts/                       나눔스퀘어 woff2 + 라이선스
index.html                   빌드 산출물 (배포되는 파일)
```

`index.html`은 빌드 산출물이지만 GitHub Pages가 그대로 서빙하므로 커밋한다.

## 출처와 한계

- **사실 데이터**(모델명·기관·라이선스·용량·파라미터·링크)는 공개 공유된 Claude 아티팩트
  「대학·연구소 AI 모델 도감」(GitHub·Hugging Face API 실측, 2026-09-11)에서 가져왔다.
- **한 줄 설명 167개는 원문을 쓰지 않고 새로 작성했다.**
- 수록된 GitHub·Hugging Face 링크 **293건을 2026-09-11에 전수 조회해 전부 정상 응답**을 확인했다.
  TiRex·TabPFN은 라이선스 원문을 직접 대조했다(GitHub API가 `NOASSERTION`으로만 표기하는 것들이다).
- 그 밖의 수치는 원 데이터를 그대로 옮긴 것이며 개별 검증하지 않았다.
- **용량·별점·라이선스는 바뀐다.** 이 페이지는 2026-09-11 시점 스냅샷이고 정본은 각 저장소다.
  내려받기 전에 링크를 열어 확인한다.

## 라이선스

- 이 저장소의 코드와 한국어 설명: MIT
- 본문 글꼴 **나눔스퀘어** © NAVER Corporation — [SIL Open Font License 1.1](fonts/LICENSE.txt).
  OFL은 재배포·임베딩을 허용하되 저작권 고지와 라이선스 전문을 함께 포함할 것을 요구하므로
  `fonts/LICENSE.txt`를 같이 둔다.
