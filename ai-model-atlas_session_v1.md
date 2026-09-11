# ai-model-atlas 세션 기록 v1 — 초판 제작·배포

작성일: 2026-09-12
출처: `C:\()안티그래비티\()안티그래비티_session_v18 ~ v23` 조사 세션. 이 폴더는 그 결과물을 열람용 정적 페이지로 만든 것이다.

🔗 **https://king-cheolhee.github.io/ai-model-atlas/**

---

## 이번에 한 일

공개 공유된 Claude 아티팩트 「대학·연구소 AI 모델 도감」을 레퍼런스로, 같은 구조·정렬의 정적 페이지를 만들어 GitHub Pages에 배포했다.

### 사용자가 정한 것 (다시 논의하지 말 것)

| 항목 | 결정 |
|---|---|
| 배포 | **공개 저장소 + GitHub Pages** |
| 설명 문구 | **원문을 쓰지 않고 새로 작성** (재배포 문제 제거) |
| 폰트 | **나눔스퀘어** |
| 디자인 | 세컨드브레인 UI/UX 노트를 근거로 |

### 디자인 토큰 — `skillui` 스킬 경로가 막혀 소스 직접 파싱

- `skillui --dir`로 레퍼런스 HTML을 스캔 → **색 0 / 폰트 0 / 컴포넌트 0**. 스타일이 인라인 `<style>` 한 덩어리라 정적 분석이 놓친다.
- 스킬 안내대로면 `--mode ultra`(Playwright)인데 **미설치**였고, 새 패키지 설치는 승인 대상이라 진행하지 않았다.
- 대신 **원본 CSS를 직접 파싱**했다. 스킬의 원칙("추측 금지, 실측")은 이 방법이 더 정확히 지킨다.
- 확보: CSS 변수 21개(라이트/다크 각각), 분야색 4종, 테마 전환 구조(`prefers-color-scheme` + `[data-theme]`).

### 볼트에서 가져온 설계 제약 (전부 반영)

- [[development/korean-webfont-sourcing-pitfalls]] — **폰트는 CDN 링크에 의존하지 말고 파일을 저장소에 고정**한다. 받은 뒤 `file`로 진짜 폰트 바이너리인지 확인한다(과거 62바이트 ASCII 오류 응답 사례).
  → 네이버 공식 CSS(`hangeul.pstatic.net/hangeul_static/css/nanum-square.css`)는 **woff2가 없어** eot/woff/ttf뿐이었다. woff2는 커뮤니티 미러에서 받아 `fonts/`에 커밋했고, `file` 검증으로 3종 모두 `Web Open Font Format (Version 2)` 확인.
- [[development/css-token-ui-polish-darkmode]] — 다크는 토큰 오버라이드로만, **FOUC 방지 인라인 스크립트를 `<head>` 최상단**에, 하드코딩 색 금지.
- [[development/ui-visual-style-catalog]] — 이 페이지는 **반복 열람형 목록**이라 벤토가 아니라 세로 리스트가 맞다(NN/g). 미니멀의 함정 두 개를 피했다: 무테 컨트롤 3:1(SC 1.4.11) → 칩·입력에 보이는 테두리, 타깃 24×24(SC 2.5.8) → `--tap:32px`. `clamp()`의 preferred 값에 rem을 섞어 **F94**(줌 200%에서 안 커지는 실패 기법)를 피했다.

### 만든 것

```
build.py                     빌드(표준 라이브러리만)
src/index.template.html      HTML·CSS·JS 원본
data/atlas.source.json       사실 데이터 167종
data/descriptions.ko.json    한 줄 설명 167개 (직접 작성)
fonts/                       나눔스퀘어 woff2 3종 + SIL OFL 전문
index.html                   빌드 산출물 115KB (배포본)
```

기능: 용량 로그 산점도(98종, 점 클릭 → 해당 행 펼침) · 한국어 검색 · 분야/장비/라이선스 필터 · 4종 정렬 · 행 펼침(링크·변형·수치·비고) · 경고 배지(승인필요/비상업/보관됨) · 다크모드.

### 검증 (전부 실행 결과)

| 검사 | 결과 |
|---|---|
| 설명 키 대조 | **167/167 일치**, 누락 0·오타 0. 빌드가 강제한다(어긋나면 중단) |
| 폰트 바이너리 | 3종 모두 `Web Open Font Format (Version 2)` |
| 라이브 폰트 로드 | `NanumSquare 400/700/800 → loaded` |
| 렌더 | 표 **167행**, 산점도 **98점** |
| 단위 정합 | 제목 `207 KB에서 328 GB까지` = 표의 `weights` 문자열과 일치 |
| 검색 | "시계열" → 23종 |
| 필터 | 노트북 CPU 36종 → +라이선스 주의 8종 |
| 행 펼침 | 링크 5개 표시, 접기 정상 |
| 테마 | 토글 → `data-theme=dark` + `localStorage` 저장, 복귀 정상 |
| 산점도 클릭 | MatterGen 점 → 같은 행 자동 펼침(일치 확인) |
| 콘솔 오류 | 0건 |
| 라이브 배포 | `https://king-cheolhee.github.io/ai-model-atlas/` **HTTP 200** |

### 고친 것

- **단위 불일치**: 처음엔 `fmtBytes`가 1024 기준이라 제목이 "202 KB~306 GB"인데 표는 "207 KB·328 GB"였다. 원본 `weights` 문자열이 1000 기준(SI)이므로 맞췄다.
- **제목 줄바꿈**: `.sec-head` 첫 칸이 좁아 "328 / GB까지"로 끊겼다. `auto` + `nowrap`으로 수정.
- **커밋 메시지 오염**: bash에서 PowerShell 히어스트링(`@'...'@`)을 써서 메시지 앞에 `@`가 붙었다. 푸시 전이라 `--amend`로 교정.

---

## 남은 일

- 데이터 갱신 절차가 없다. 원본 아티팩트가 다시 측정되면 `data/atlas.source.json`을 갈아 끼우고 `python build.py`를 돌려야 하는데, **새 모델이 추가되면 설명이 없어 빌드가 중단된다**(의도된 동작). 그때 `data/descriptions.ko.json`에 항목을 추가한다.
- 모바일 화면 실기기 확인은 하지 않았다. CSS 미디어쿼리(760px)만 작성한 상태다.
- 검색이 단순 부분일치다. 초성 검색·오타 허용은 없다(필요해지면 그때).

## 주의사항

- **`index.html`은 빌드 산출물인데 커밋한다.** GitHub Pages가 그대로 서빙하기 때문이다. 손으로 고치지 말 것 — 다음 빌드에 덮어쓰인다. 수정은 `src/index.template.html`에서 한다.
- **폰트는 SIL OFL 1.1이다.** 재배포·임베딩은 허용되지만 **저작권 고지와 라이선스 전문을 함께 둬야** 한다. `fonts/LICENSE.txt`를 지우면 라이선스 위반이다. 푸터와 README에도 고지가 들어가 있다.
- **한 줄 설명 167개는 직접 쓴 것**이고 사실 데이터만 원본에서 가져왔다. 출처는 푸터·README에 명시했다. 설명을 원본 문구로 되돌리면 이 구분이 깨진다.
- 저장소가 **공개**다. 여기에 비밀·개인정보를 넣지 않는다(`.gitignore`에 `.env`류 등록).
- 페이지는 2026-09-11 스냅샷이다. 용량·별점·라이선스는 바뀌므로 푸터에 그 사실을 적어 뒀다.
- 상위 폴더 `C:\()안티그래비티`는 git 저장소가 아니다(깨진 `.git` 껍데기). 이 폴더만 독립 저장소다.

## 다음 단계

1. 실사용하며 불편한 점을 모아 다음 버전에 반영한다. 지금은 관찰 단계.
2. 데이터 갱신이 필요해지면 `atlas.source.json` 교체 → `python build.py` → 커밋·푸시.
3. 페이지에 손댈 때는 `src/index.template.html`만 고치고 반드시 `python build.py`를 다시 돌린다.
4. 관련 지식: [[development/local-ai-model-atlas-2026-09]](167종 전체 스냅샷) · [[development/stock-automation-model-stack]](주식 자동화 후보).
