"""학교별 수학과외 페이지(schools/<학교ID>.html)를 생성한다.

build_regions.py 실행 시 함께 호출된다. 데이터: _build/school_details.json
(전국초중등학교위치표준데이터 2026-10-26, 전북 운영 학교)
"""
import json
import math
from pathlib import Path

from build_regions import (GRADES, LEVELS, PHONE, REGIONS, ROOT, SITE, TEL, UPDATED,
                           esc, jsonld)

SCHOOLS = json.loads((ROOT / "_build" / "school_details.json").read_text(encoding="utf-8"))
BY_ID = {s["id"]: s for s in SCHOOLS}
REGION = {r[0]: r for r in REGIONS}

LEVEL_INFO = {
    "elementary": {
        "label": "초등학교", "short": "초등", "levels": LEVELS[0], "grades": GRADES[0:2],
        "focus": "기초수학·수학공부",
        "copy": "교과 진도에 맞춰 연산과 개념을 정확히 익히고, 풀이 과정을 스스로 설명하는 습관을 만듭니다. 중학교 수학으로 이어지는 기초까지 함께 다집니다.",
    },
    "middle": {
        "label": "중학교", "short": "중등", "levels": LEVELS[1], "grades": GRADES[2:5],
        "focus": "수학내신·기초수학",
        "copy": "학교 진도와 중간·기말고사 범위에 맞춰 개념과 유형, 서술형을 준비합니다. 기초가 부족한 단원은 이전 학년 개념부터 다시 정리합니다.",
    },
    "high": {
        "label": "고등학교", "short": "고등", "levels": LEVELS[2], "grades": GRADES[5:8],
        "focus": "수학내신·수능대비",
        "copy": "학교별 내신 출제 경향과 모의고사 결과를 함께 살펴, 내신과 수능수학의 비중을 목표에 맞게 설계합니다.",
    },
}
NEXT_LEVEL = {"elementary": "middle", "middle": "high"}


def distance_km(a, b):
    lat1, lon1, lat2, lon2 = map(math.radians, (a["lat"], a["lon"], b["lat"], b["lon"]))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def nearest(school, level, count):
    others = [s for s in SCHOOLS if s["level"] == level and s["id"] != school["id"]]
    return sorted(((distance_km(school, s), s) for s in others), key=lambda x: x[0])[:count]


def school_link(school, prefix=""):
    return f'{prefix}schools/{school["id"]}.html'


def faqs(school, s):
    name, level = school["name"], school["level"]
    exam = "단원평가와 교과 진도" if level == "elementary" else "중간·기말고사 범위와 교과서·학교 프린트"
    items = [
        (f"{name} 시험 범위와 진도에 맞춰 수업하나요?",
         f"네. {name}의 학년별 {exam}를 확인하고, 그에 맞춰 개념 정리와 문제 연습 계획을 세웁니다."),
        (f"{name} 근처에서 수학과외 수업이 가능한가요?",
         f"{school['address']} 인근을 포함한 {s} 지역 학생을 대상으로 안내합니다. 정확한 수업 장소와 가능 여부는 전화 상담({PHONE})에서 확인해 드립니다."),
    ]
    if level == "elementary":
        items.append((f"{name} 고학년인데 중학교 수학 준비도 할 수 있나요?",
                      "초등 과정의 빈틈을 먼저 점검한 뒤 정수와 유리수, 문자와 식 등 중학교 첫 단원을 예비중1 과정으로 준비합니다."))
    elif level == "middle":
        items.append((f"{name} 학생인데 수학 기초가 부족해도 괜찮나요?",
                      "첫 수업에서 개념 이해도를 진단하고 필요하면 초등·이전 학년 개념부터 다시 정리한 뒤 학교 진도를 따라갑니다."))
    else:
        items.append((f"{name} 학생도 내신과 수능대비를 함께 할 수 있나요?",
                      "내신 기간에는 학교 시험에, 그 외 기간에는 모의고사 분석과 수능수학 기출 학습에 비중을 두도록 목표에 맞춰 계획합니다."))
    items.append(("무료체험수업은 어떻게 신청하나요?", f"{PHONE}으로 전화 주시면 학년과 학습 고민을 듣고 체험수업 일정을 안내해 드립니다."))
    return items


def build(school):
    region = REGION[school["region"]]
    slug, region_name, s = region[0], region[1], region[2]
    info = LEVEL_INFO[school["level"]]
    name = school["name"]
    url = f"{SITE}/{school_link(school)}"
    title = f"{name} 수학과외 | {s} {info['short']} 1:1 {info['focus']}"
    desc = f"{name}({school['address']}) 학생을 위한 1:1 수학과외. {info['copy'].split('.')[0]}. 무료체험수업 상담 {PHONE}."
    faq_items = faqs(school, s)
    type_text = school["type"] + (" · 분교" if school["branch"] else "")

    _, eng_label, _, lead, items = info["levels"]
    level_html = "".join(f"<dt>{name} {kw.split(' ', 1)[1]}</dt><dd>{body}</dd>" for kw, body in items)
    grades_html = "".join(f"<article><h3>{name} {g} 수학</h3><p>{body}</p></article>" for g, body in info["grades"])

    near_same = nearest(school, school["level"], 6)
    near_html = "".join(
        f'<a href="{s2["id"]}.html">{s2["name"]} 수학과외 <small>약 {d:.1f}km</small></a>' for d, s2 in near_same
    )
    next_html = ""
    if school["level"] in NEXT_LEVEL:
        nxt = NEXT_LEVEL[school["level"]]
        near_next = nearest(school, nxt, 4)
        next_html = f"""
      <h3 class="nearby-title">{name} 주변 {LEVEL_INFO[nxt]['label']}</h3>
      <div class="nearby-links">{"".join(f'<a href="{s2["id"]}.html">{s2["name"]} 수학과외 <small>약 {d:.1f}km</small></a>' for d, s2 in near_next)}</div>"""

    schema = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "전북 수학과외", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": f"{s} 수학과외", "item": f"{SITE}/regions/{slug}.html"},
            {"@type": "ListItem", "position": 3, "name": f"{s} {info['short']} 수학과외", "item": f"{SITE}/regions/{slug}-{school['level']}.html"},
            {"@type": "ListItem", "position": 4, "name": f"{name} 수학과외", "item": url},
        ]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_items]},
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
  <link rel="icon" href="../favicon.ico" sizes="any">
  <link rel="icon" href="../assets/logo-mark.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="../assets/apple-touch-icon.png">
  <link rel="stylesheet" href="../region-page.css">
  {jsonld(schema)}
</head>
<body>
  <header class="site-header">
    <a class="brand" href="../">
      <span class="brand-mark" aria-hidden="true">∑</span>
      <span>전북 수학과외<small>TUTOR PLUS</small></span>
    </a>
    <a class="back-link" href="../regions/{slug}.html">{s} 수학과외</a>
  </header>
  <main>
    <nav class="breadcrumb" aria-label="현재 위치"><a href="../">전북 수학과외</a> › <a href="../regions/{slug}.html">{s} 수학과외</a> › <a href="../regions/{slug}-{school['level']}.html">{s} {info['short']} 수학과외</a> › <span>{name}</span></nav>
    <section class="hero school-hero" data-region="{info['short']}">
      <p class="eyebrow">{eng_label} MATH TUTORING</p>
      <h1>{name} 수학과외<br><em>{info['focus']} 1:1 맞춤 수업</em></h1>
      <p class="hero-copy">{s} {name} 학생을 위한 1:1 수학과외입니다. {info['copy']}</p>
      <div class="hero-actions">
        <a class="primary-button" href="{TEL}">무료체험수업 상담</a>
        <a class="phone-link" href="{TEL}">{PHONE}</a>
      </div>
    </section>

    <section class="section school-info">
      <div class="grade-heading">
        <p class="eyebrow">SCHOOL INFO</p>
        <h2>{name}<br>학교 정보</h2>
        <p>다니는 학교의 진도와 시험 일정에 맞춰 수업 계획을 세우기 위해 학교 정보를 함께 확인합니다.</p>
      </div>
      <dl class="info-table">
        <div><dt>학교명</dt><dd>{name}</dd></div>
        <div><dt>학교급</dt><dd>{info['label']}</dd></div>
        <div><dt>설립 형태</dt><dd>{type_text}</dd></div>
        <div><dt>지역</dt><dd><a href="../regions/{slug}.html">전북특별자치도 {region_name}</a></dd></div>
        <div><dt>도로명 주소</dt><dd>{school['address']}</dd></div>
      </dl>
      <p class="school-source">출처: 전국초중등학교위치표준데이터(2026.10 기준)</p>
    </section>

    <section class="section level-guide">
      <div class="grade-heading">
        <p class="eyebrow">CURRICULUM</p>
        <h2>{name}<br>수학 수업 안내</h2>
        <p>{lead}</p>
      </div>
      <dl class="level-single">{level_html}</dl>
    </section>

    <section class="section grade-guide">
      <div class="grade-heading">
        <p class="eyebrow">GRADE PROGRAM</p>
        <h2>{name}<br>학년별 수학</h2>
        <p>학년마다 배우는 단원과 시험 부담이 다르기 때문에 학년에 맞춰 수업의 중심을 바꿉니다.</p>
      </div>
      <div class="transition-grid grade-{len(info['grades'])}">{grades_html}</div>
    </section>

    <section class="section nearby">
      <p class="eyebrow">NEARBY SCHOOLS</p>
      <h2>{name} 근처<br>학교 수학과외</h2>
      <h3 class="nearby-title">가까운 {info['label']}</h3>
      <div class="nearby-links">{near_html}</div>{next_html}
    </section>

    <section class="section faq">
      <p class="eyebrow">FAQ</p>
      <h2>{name} 수학과외<br>자주 묻는 질문</h2>
      <div class="faq-list">{"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq_items)}</div>
    </section>

    <section class="cta">
      <h2>{name} 수학과외 무료체험수업,<br>전화로 먼저 상담하세요.</h2>
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


def write_all():
    out = ROOT / "schools"
    out.mkdir(exist_ok=True)
    for old in out.glob("*.html"):
        old.unlink()
    for school in SCHOOLS:
        (out / f"{school['id']}.html").write_text(build(school), encoding="utf-8")
    return [f"{SITE}/{school_link(s)}" for s in SCHOOLS]
