"""지역별 수학과외 페이지(regions/*.html)를 정적 HTML로 생성한다.

실행: python _build/build_regions.py
`_` 로 시작하는 폴더는 GitHub Pages(Jekyll)에서 공개되지 않는다.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://tutorplus.kr"
PHONE = "010-2928-3614"
TEL = "tel:01029283614"
UPDATED = "2026-10-20"

# slug, 행정구역명, 검색용 지역명, 배경 글자, 영문, 대표 동네
REGIONS = [
    ("jeonju-wansan-gu", "전주시 완산구", "전주 완산구", "완산", "WANSAN-GU", ["효자동", "서신동", "평화동", "중화산동", "삼천동"]),
    ("jeonju-deokjin-gu", "전주시 덕진구", "전주 덕진구", "덕진", "DEOKJIN-GU", ["송천동", "혁신동", "인후동", "우아동", "에코시티"]),
    ("jeonju-si", "전주시", "전주", "전주", "JEONJU", ["완산구", "덕진구", "효자동", "송천동", "에코시티"]),
    ("gunsan-si", "군산시", "군산", "군산", "GUNSAN", ["나운동", "수송동", "미장동", "조촌동"]),
    ("iksan-si", "익산시", "익산", "익산", "IKSAN", ["영등동", "모현동", "어양동", "부송동"]),
    ("jeongeup-si", "정읍시", "정읍", "정읍", "JEONGEUP", ["수성동", "상동", "시기동"]),
    ("namwon-si", "남원시", "남원", "남원", "NAMWON", ["도통동", "향교동", "왕정동"]),
    ("gimje-si", "김제시", "김제", "김제", "GIMJE", ["검산동", "신풍동", "요촌동"]),
    ("wanju-gun", "완주군", "완주", "완주", "WANJU", ["삼례읍", "봉동읍", "이서면"]),
    ("jinan-gun", "진안군", "진안", "진안", "JINAN", ["진안읍"]),
    ("muju-gun", "무주군", "무주", "무주", "MUJU", ["무주읍", "안성면"]),
    ("jangsu-gun", "장수군", "장수", "장수", "JANGSU", ["장수읍", "장계면"]),
    ("imsil-gun", "임실군", "임실", "임실", "IMSIL", ["임실읍", "오수면"]),
    ("sunchang-gun", "순창군", "순창", "순창", "SUNCHANG", ["순창읍"]),
    ("gochang-gun", "고창군", "고창", "고창", "GOCHANG", ["고창읍"]),
    ("buan-gun", "부안군", "부안", "부안", "BUAN", ["부안읍"]),
]

# 지역별로 실제 안내하는 내용이 다른 부분
EXTRA_FIT = {
    "gunsan-si": "방문 수업 또는 온라인 수업을 상담하고 싶은 학생",
    "wanju-gun": "통학·학원 이동 시간이 길어 집 근처에서 1:1 수업을 찾는 학생",
}

# 같은 문장이 모든 페이지에 반복되지 않도록 지역마다 번갈아 쓰는 도입 문장
INTRO_VARIANTS = [
    "{s} 수학과외는 학생이 지금 어디에서 막혀 있는지부터 확인합니다. 초등은 기초 개념과 연산 습관을, 중등은 학교 진도와 수학내신을, 고등은 내신과 수능대비의 균형을 기준으로 수업 순서를 정합니다.",
    "같은 학년이라도 {s} 학생마다 필요한 수학 공부는 다릅니다. 초등 기초수학, 중등 내신 대비, 고등 수능수학까지 현재 실력과 목표를 먼저 진단한 뒤 1:1로 수업을 설계합니다.",
    "{s}에서 수학과외를 찾는 학생과 학부모님께 가장 먼저 드리는 것은 정확한 진단입니다. 개념 이해도, 풀이 습관, 학교 시험 결과를 함께 살펴 초등·중등·고등 학년에 맞는 수학 수업을 시작합니다.",
]

LEVELS = [
    ("초등", "ELEMENTARY", "초등 수학과외", "개념을 이해하고 스스로 설명하는 습관을 만드는 시기입니다.", [
        ("초등 수학수업", "교과서 개념을 그림과 구체적인 예로 먼저 이해한 뒤 문제로 옮깁니다. 학교 단원 진도에 맞춰 한 단원씩 정확히 마무리합니다."),
        ("초등 수학공부", "짧더라도 매일 이어지는 연산·복습 루틴을 만들고, 틀린 문제는 풀이 과정을 말로 다시 설명하게 해 이해를 확인합니다."),
        ("초등 기초수학", "곱셈구구, 나눗셈, 분수와 소수 계산처럼 이전 학년에서 놓친 기초를 진단하고 필요한 학년까지 거슬러 보완합니다."),
    ]),
    ("중등", "MIDDLE SCHOOL", "중등 수학과외", "개념과 유형을 연결해 학교 시험 점수로 이어지게 하는 시기입니다.", [
        ("중등 수학수업", "학교 진도에 맞춰 개념 → 대표 유형 → 서술형 순서로 수업하고, 단원이 끝날 때마다 이해도를 점검합니다."),
        ("중등 수학공부", "개념 정리와 오답 노트를 함께 관리해 수업 없는 날에도 혼자 다시 풀어볼 수 있는 공부 방법을 익힙니다."),
        ("중등 기초수학", "정수와 유리수 계산, 문자와 식, 방정식처럼 이후 단원의 바탕이 되는 부분에서 빈틈을 찾아 먼저 메웁니다."),
        ("중등 수학내신", "학교별 시험 범위와 교과서·학교 프린트, 기출 유형을 확인하고 서술형 감점 요인까지 점검해 중간·기말고사를 준비합니다."),
    ]),
    ("고등", "HIGH SCHOOL", "고등 수학과외", "내신과 수능 목표를 기준으로 학습 비중을 설계하는 시기입니다.", [
        ("고등 수학수업", "공식 암기보다 개념이 나온 이유와 원리를 이해하는 데 집중하고, 학교 진도와 선택 과목에 맞춰 수업합니다."),
        ("고등 수학공부", "개념 복습 → 기출 → 오답 재풀이로 이어지는 주간 학습 사이클을 만들고 학습량을 함께 관리합니다."),
        ("고등 기초수학", "인수분해, 이차함수 등 고등 수학의 바탕이 되는 중등 단원부터 다시 정리해 수학을 포기하지 않도록 돕습니다."),
        ("고등 수학내신", "학교별 출제 경향과 부교재, 서술형 문항을 분석해 내신 등급을 목표로 시험 일정에 맞춘 계획을 세웁니다."),
        ("고등 수능대비", "모의고사 결과로 취약 영역과 시간 배분 문제를 찾고, 실전 풀이 루틴을 만들어 수능까지 안정적으로 준비합니다."),
        ("고등 수능수학", "수능 수학 출제 범위의 기출 문항을 단원별로 분석하고, 고난도 문항에 접근하는 풀이 순서를 훈련합니다."),
    ]),
]

GRADES = [
    ("초등 저학년", "수와 연산, 도형의 기초를 놀이처럼 익히고 문제를 끝까지 읽는 습관을 만듭니다."),
    ("초등 고학년", "분수·소수, 비와 비율, 도형의 넓이 등 중학 수학으로 이어지는 개념을 탄탄히 다집니다."),
    ("중1", "소인수분해, 정수와 유리수, 문자와 식, 일차방정식으로 중학교 수학의 첫 단원을 안정적으로 시작합니다."),
    ("중2", "식의 계산, 연립방정식, 일차함수, 확률을 연결해 학교 내신과 서술형을 함께 준비합니다."),
    ("중3", "제곱근과 실수, 인수분해, 이차방정식, 이차함수를 다지며 예비고1 과정까지 이어지는 흐름을 만듭니다."),
    ("고1", "공통수학의 빠른 진도와 깊어진 문제 해석에 적응하고, 첫 내신과 모의고사를 준비합니다."),
    ("고2", "선택 과목과 학교별 내신 일정에 맞춰 개념과 기출을 연결하고 수능 대비의 기반을 만듭니다."),
    ("고3", "수능 수학과 내신의 비중을 목표에 맞게 정하고, 실전 시간 관리와 취약 단원 보완에 집중합니다."),
]


def faqs(s, dongs):
    area = "·".join(dongs)
    return [
        (f"{s} 어느 지역까지 수학과외 수업이 가능한가요?",
         f"{area} 등 {s} 지역 학생을 대상으로 수업을 안내합니다. 정확한 수업 장소와 가능 여부는 전화 상담({PHONE})에서 확인해 드립니다."),
        ("수학 기초가 많이 부족해도 수업을 받을 수 있나요?",
         "네. 첫 수업에서 개념 이해도와 풀이 과정을 진단하고, 필요하다면 이전 학년의 기초수학부터 다시 정리합니다. 학년보다 현재 실력에 맞춘 순서로 진행합니다."),
        ("중등 수학내신은 어떻게 준비하나요?",
         "학교별 시험 범위와 교과서, 학교 프린트, 기출 유형을 확인한 뒤 개념 정리 → 유형 연습 → 서술형 점검 순서로 중간·기말고사를 준비합니다."),
        ("고등학생 수능대비와 내신을 함께 할 수 있나요?",
         "학생의 목표와 학교 일정에 따라 내신 기간에는 학교 시험에, 그 외 기간에는 모의고사 분석과 수능수학 기출 학습에 비중을 두도록 계획합니다."),
        ("수학학원과 1:1 수학과외는 무엇이 다른가요?",
         "1:1 수학과외는 한 학생의 막힌 지점과 공부 속도에 맞춰 수업 내용을 바로 조정할 수 있습니다. 질문과 오답 관리를 수업 시간 안에서 충분히 다룰 수 있다는 점이 가장 큰 차이입니다."),
        ("무료체험수업은 어떻게 신청하나요?",
         f"{PHONE}으로 전화 주시면 학년과 학습 고민을 듣고 체험수업 일정을 안내해 드립니다."),
    ]


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def jsonld(data):
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def build(index, region):
    slug, name, s, mark, eng, dongs = region
    url = f"{SITE}/regions/{slug}.html"
    dong_text = "·".join(dongs)
    title = f"{s} 수학과외 | 초등·중등·고등 1:1 수학수업·내신·수능대비"
    desc = (f"{s} 수학과외 – {dong_text} 초등 기초수학, 중등 수학내신, 고등 수능수학까지 "
            f"학년별 1:1 맞춤 수학수업. 무료체험수업 전화 상담 {PHONE}.")
    faq_items = faqs(s, dongs)

    levels_html = "".join(
        f"""
        <article class="level">
          <span>0{i + 1} / {eng_label}</span>
          <h3>{s} {heading}</h3>
          <p class="level-lead">{lead}</p>
          <dl>{"".join(f"<dt>{s} {kw}</dt><dd>{body}</dd>" for kw, body in items)}</dl>
        </article>"""
        for i, (_, eng_label, heading, lead, items) in enumerate(LEVELS)
    )
    grades_html = "".join(
        f'<article><h3>{s} {g} 수학과외</h3><p>{body}</p></article>' for g, body in GRADES
    )
    fit_items = [
        f"{dong_text}에서 수학과외를 알아보는 학생",
        "초등·중등·고등 학년과 현재 실력에 맞춘 1:1 수업이 필요한 학생",
        "기초수학이 부족해 이전 학년 개념부터 다시 정리하고 싶은 학생",
        "중간·기말고사 수학내신과 서술형 대비가 필요한 학생",
        "모의고사 등급을 올리고 수능수학을 체계적으로 준비하고 싶은 학생",
    ]
    if slug in EXTRA_FIT:
        fit_items.insert(2, EXTRA_FIT[slug])
    fit_html = "".join(f"<li>{t}</li>" for t in fit_items)
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq_items)

    district_html = ""
    if slug.startswith("jeonju"):
        links = [("jeonju-wansan-gu", "전주 완산구 수학과외"), ("jeonju-deokjin-gu", "전주 덕진구 수학과외"), ("jeonju-si", "전주시 전체")]
        district_html = f"""
    <section class="section district-nav">
      <p class="eyebrow">JEONJU 2 DISTRICTS</p>
      <h2>거주 지역을 선택하세요.</h2>
      <div class="district-links">{"".join(f'<a href="{l}.html"' + (' aria-current="page"' if l == slug else "") + f'>{t}</a>' for l, t in links)}</div>
    </section>"""

    area_html = "".join(
        f'<a href="{r[0]}.html"' + (' aria-current="page"' if r[0] == slug else "") + f">{r[2]} 수학과외</a>"
        for r in REGIONS
    )

    schema = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "전북 수학과외", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": f"{s} 수학과외", "item": url},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": f"{s} 수학과외",
            "serviceType": "초등·중등·고등 1:1 수학과외",
            "url": url,
            "description": desc,
            "areaServed": {"@type": "AdministrativeArea", "name": f"전북특별자치도 {name}"},
            "provider": {"@type": "EducationalOrganization", "name": "전북 수학과외 TUTOR PLUS", "url": f"{SITE}/", "telephone": "+82-10-2928-3614"},
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_items
            ],
        },
    ]

    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="전북 수학과외">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/og-image.jpg?v=20261008">
  <meta property="og:locale" content="ko_KR">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="../assets/logo-mark.svg" type="image/svg+xml">
  <link rel="stylesheet" href="../region-page.css">
  {jsonld(schema)}
</head>
<body>
  <header class="site-header">
    <a class="brand" href="../">
      <span class="brand-mark" aria-hidden="true">∑</span>
      <span>전북 수학과외<small>TUTOR PLUS</small></span>
    </a>
    <a class="back-link" href="../#area">전체 지역 보기</a>
  </header>
  <main>
    <section class="hero" data-region="{mark}">
      <p class="eyebrow">{eng} MATH TUTORING</p>
      <h1>{s} 수학과외<br><em>초·중·고 1:1 맞춤 수업</em></h1>
      <p class="hero-copy">{dong_text} 등 {name} 학생의 학교 진도와 현재 실력, 목표를 살펴 초등 기초수학부터 중등 수학내신, 고등 수능대비까지 필요한 공부의 순서를 함께 설계합니다.</p>
      <div class="hero-actions">
        <a class="primary-button" href="{TEL}">무료체험수업 상담</a>
        <a class="phone-link" href="{TEL}">{PHONE}</a>
      </div>
    </section>

    <section class="section">
      <div class="intro">
        <div>
          <p class="eyebrow">{eng} 1:1 MATH</p>
          <h2>학년과 목표에 맞춰<br>수업을 설계합니다.</h2>
        </div>
        <p class="intro-copy">{INTRO_VARIANTS[index % len(INTRO_VARIANTS)].format(s=s)}</p>
      </div>
      <div class="feature-grid">
        <article><span>01 / ELEMENTARY</span><h3>{s} 초등 수학</h3><p>연산과 교과 개념을 차근차근 익히고, 풀이 과정을 자신의 말로 설명하는 습관을 만듭니다.</p></article>
        <article><span>02 / MIDDLE SCHOOL</span><h3>{s} 중등 수학</h3><p>학교 진도와 시험 범위를 살펴 핵심 개념을 정리하고, 문제 유형과 서술형에 적용하는 연습을 합니다.</p></article>
        <article><span>03 / HIGH SCHOOL</span><h3>{s} 고등 수학</h3><p>학생의 목표에 맞춰 고등 수학 개념과 내신, 모의고사·수능 학습 방향을 설계합니다.</p></article>
      </div>
    </section>

    <section class="section level-guide">
      <div class="grade-heading">
        <p class="eyebrow">CURRICULUM</p>
        <h2>{s} 초등·중등·고등<br>수학과외 수업 안내</h2>
        <p>수학수업, 수학공부 방법, 기초수학 보완, 수학내신과 수능대비까지 학교급별로 무엇을 어떻게 공부하는지 정리했습니다.</p>
      </div>
      <div class="level-grid">{levels_html}
      </div>
    </section>

    <section class="section grade-guide">
      <div class="grade-heading">
        <p class="eyebrow">GRADE PROGRAM</p>
        <h2>{s} 학년별<br>수학과외</h2>
        <p>예비중1·예비고1처럼 학년이 바뀌는 시기에는 이전 학년의 빈틈을 점검하고 다음 학년 첫 단원을 미리 준비합니다.</p>
      </div>
      <div class="transition-grid">{grades_html}</div>
    </section>

    <section class="section fit">
      <div>
        <p class="eyebrow">{eng} LESSONS</p>
        <h2>이런 수업을<br>찾고 계신가요?</h2>
      </div>
      <ul class="fit-list">{fit_html}</ul>
    </section>

    <section class="section faq">
      <p class="eyebrow">FAQ</p>
      <h2>{s} 수학과외<br>자주 묻는 질문</h2>
      <div class="faq-list">{faq_html}</div>
    </section>
{district_html}
    <section class="section area-nav">
      <p class="eyebrow">JEONBUK AREAS</p>
      <h2>전북 지역별 수학과외</h2>
      <nav class="area-links" aria-label="전북 지역별 수학과외">{area_html}</nav>
    </section>

    <section class="cta">
      <h2>{s} 수학과외 무료체험수업,<br>전화로 먼저 상담하세요.</h2>
      <a class="primary-button" href="{TEL}">{PHONE}</a>
    </section>
  </main>
  <footer class="site-footer">
    <span>전북 수학과외 · 초등·중등·고등 1:1 맞춤 수학 코칭</span>
    <span>© <span id="year">2026</span> TUTOR PLUS.</span>
  </footer>
  <a class="floating-phone" href="{TEL}">무료체험수업 상담 {PHONE}</a>
  <script src="../region-page.js"></script>
</body>
</html>
"""


def build_sitemap():
    urls = [(f"{SITE}/", "weekly", "1.0")] + [(f"{SITE}/regions/{r[0]}.html", "monthly", "0.8") for r in REGIONS]
    rows = "\n".join(
        f"  <url><loc>{loc}</loc><lastmod>{UPDATED}</lastmod><changefreq>{freq}</changefreq><priority>{prio}</priority></url>"
        for loc, freq, prio in urls
    )
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}\n</urlset>\n'


if __name__ == "__main__":
    for i, region in enumerate(REGIONS):
        (ROOT / "regions" / f"{region[0]}.html").write_text(build(i, region), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(build_sitemap(), encoding="utf-8")
    print(f"{len(REGIONS)} region pages + sitemap.xml written")
