"""지역×학교급 수학과외 페이지(regions/<지역>-<elementary|middle|high>.html)를 생성한다.

build_regions.py 실행 시 함께 호출된다.
"""
from build_regions import (PHONE, REGIONS, ROOT, SCHOOL_IDS, SCHOOLS, SITE, TEL,
                           esc, jsonld)
from build_schools import LEVEL_INFO

LEVEL_KEYS = ["elementary", "middle", "high"]
LEVEL_ENG = {"elementary": "ELEMENTARY", "middle": "MIDDLE SCHOOL", "high": "HIGH SCHOOL"}

FAQS = {
    "elementary": [
        ("{s} 초등 수학과외는 어떤 학생에게 맞나요?",
         "연산 실수가 잦거나 교과 개념을 문제에 적용하기 어려운 학생, 학교 진도는 따라가지만 서술형 풀이를 어려워하는 학생에게 특히 도움이 됩니다."),
        ("연산 실수가 많은데 어떻게 보완하나요?",
         "실수가 나오는 계산 유형을 먼저 찾고, 풀이 과정을 줄 맞춰 쓰는 습관과 짧은 매일 연산 루틴으로 정확도를 높입니다."),
        ("{s} 초등 고학년인데 예비중1 준비도 하나요?",
         "초등 과정의 빈틈을 점검한 뒤 정수와 유리수, 문자와 식 등 중학교 첫 단원을 미리 익히는 예비중1 과정을 함께 진행합니다."),
    ],
    "middle": [
        ("{s} 중등 수학내신은 어떻게 준비하나요?",
         "다니는 학교의 시험 범위와 교과서, 학교 프린트, 기출 유형을 확인한 뒤 개념 정리 → 유형 연습 → 서술형 점검 순서로 중간·기말고사를 준비합니다."),
        ("중학생인데 수학 기초가 많이 부족해요.",
         "첫 수업에서 개념 이해도를 진단하고, 필요하면 초등·이전 학년의 기초수학부터 다시 정리한 뒤 학교 진도를 따라갑니다."),
        ("{s} 중3 학생은 예비고1 준비를 언제 시작하나요?",
         "중3 2학기 내신 이후 중등 전 범위의 빈틈을 점검하고, 공통수학의 빠른 진도에 대비해 고1 첫 단원을 미리 준비합니다."),
    ],
    "high": [
        ("{s} 고등 수학과외는 내신과 수능대비를 함께 하나요?",
         "내신 기간에는 학교 시험에, 그 외 기간에는 모의고사 분석과 수능수학 기출 학습에 비중을 두도록 학생의 목표에 맞춰 계획합니다."),
        ("고등학생인데 수학을 거의 포기한 상태예요.",
         "인수분해, 이차함수 등 고등 수학의 바탕이 되는 중등 단원부터 다시 정리하고, 학교 진도에서 꼭 필요한 개념을 우선순위대로 익힙니다."),
        ("모의고사 등급을 올리려면 무엇부터 해야 하나요?",
         "최근 모의고사에서 틀린 문항을 단원과 원인별로 나눠 취약 영역을 찾고, 시간 배분과 풀이 순서를 정하는 실전 루틴을 만듭니다."),
    ],
}


def page_name(slug, level):
    return f"{slug}-{level}.html"


def build(region, level):
    slug, region_name, s, mark, eng, dongs = region
    info = LEVEL_INFO[level]
    short, label = info["short"], info["label"]
    url = f"{SITE}/regions/{page_name(slug, level)}"
    schools = SCHOOLS[slug][level]
    _, _, _, lead, items = info["levels"]
    keywords = "·".join(kw.split(" ", 1)[1] for kw, _ in items[-3:])
    title = f"{s} {short} 수학과외 | {keywords} 1:1"
    desc = (f"{s} {short} 수학과외 – {s} {label} {len(schools)}곳 학생을 위한 1:1 {keywords} 맞춤 수업. "
            f"무료체험수업 전화 상담 {PHONE}.")
    faq_items = [(q.format(s=s), a) for q, a in FAQS[level]]
    faq_items.append(("무료체험수업은 어떻게 신청하나요?", f"{PHONE}으로 전화 주시면 학년과 학습 고민을 듣고 체험수업 일정을 안내해 드립니다."))

    items_html = "".join(f"<dt>{s} {kw}</dt><dd>{body}</dd>" for kw, body in items)
    grades_html = "".join(f"<article><h3>{s} {g} 수학과외</h3><p>{body}</p></article>" for g, body in info["grades"])
    schools_html = "".join(f'<li><a href="../schools/{SCHOOL_IDS[n]}.html">{n}</a></li>' for n in schools)
    sibling_html = "".join(
        f'<a href="{page_name(slug, k)}"' + (' aria-current="page"' if k == level else "") + f'>{s} {LEVEL_INFO[k]["short"]} 수학과외</a>'
        for k in LEVEL_KEYS
    ) + f'<a href="{slug}.html">{s} 수학과외 전체</a>'
    area_html = "".join(
        f'<a href="{page_name(r[0], level)}"' + (' aria-current="page"' if r[0] == slug else "") + f'>{r[2]} {short} 수학과외</a>'
        for r in REGIONS
    )

    schema = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "전북 수학과외", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": f"{s} 수학과외", "item": f"{SITE}/regions/{slug}.html"},
            {"@type": "ListItem", "position": 3, "name": f"{s} {short} 수학과외", "item": url},
        ]},
        {"@context": "https://schema.org", "@type": "Service", "name": f"{s} {short} 수학과외",
         "serviceType": f"{short} 1:1 수학과외", "url": url, "description": desc,
         "areaServed": {"@type": "AdministrativeArea", "name": f"전북특별자치도 {region_name}"},
         "provider": {"@type": "EducationalOrganization", "name": "전북 수학과외 TUTOR PLUS", "url": f"{SITE}/", "telephone": "+82-10-2928-3614"}},
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
    <a class="back-link" href="{slug}.html">{s} 수학과외</a>
  </header>
  <main>
    <nav class="breadcrumb" aria-label="현재 위치"><a href="../">전북 수학과외</a> › <a href="{slug}.html">{s} 수학과외</a> › <span>{s} {short} 수학과외</span></nav>
    <section class="hero school-hero" data-region="{mark}">
      <p class="eyebrow">{eng} {LEVEL_ENG[level]} MATH</p>
      <h1>{s} {short} 수학과외<br><em>{info['focus']} 1:1 맞춤 수업</em></h1>
      <p class="hero-copy">{"·".join(dongs)} 등 {region_name} {label} 학생을 위한 1:1 수학과외입니다. {info['copy']}</p>
      <div class="hero-actions">
        <a class="primary-button" href="{TEL}">무료체험수업 상담</a>
        <a class="phone-link" href="{TEL}">{PHONE}</a>
      </div>
    </section>

    <section class="section level-guide">
      <div class="grade-heading">
        <p class="eyebrow">CURRICULUM</p>
        <h2>{s} {short}<br>수학 수업 안내</h2>
        <p>{lead} {s} {short} 학생의 현재 실력과 학교 진도를 먼저 진단한 뒤 아래 순서로 수업합니다.</p>
      </div>
      <dl class="level-single">{items_html}</dl>
    </section>

    <section class="section grade-guide">
      <div class="grade-heading">
        <p class="eyebrow">GRADE PROGRAM</p>
        <h2>{s} {short}<br>학년별 수학과외</h2>
        <p>학년마다 배우는 단원과 시험 부담이 다르기 때문에 학년에 맞춰 수업의 중심을 바꿉니다.</p>
      </div>
      <div class="transition-grid grade-{len(info['grades'])}">{grades_html}</div>
    </section>

    <section class="section schools">
      <div class="grade-heading">
        <p class="eyebrow">{eng} SCHOOLS</p>
        <h2>{s} {label}<br>학교별 수학과외</h2>
        <p>{region_name} {label} {len(schools)}곳 학생을 대상으로, 다니는 학교의 진도와 시험 범위에 맞춰 수업을 준비합니다. 학교를 누르면 학교별 안내를 볼 수 있습니다.</p>
      </div>
      <ul class="school-list level-schools">{schools_html}</ul>
      <p class="school-source">학교 목록 출처: 전국초중등학교위치표준데이터(2026.10 기준)</p>
    </section>

    <section class="section faq">
      <p class="eyebrow">FAQ</p>
      <h2>{s} {short} 수학과외<br>자주 묻는 질문</h2>
      <div class="faq-list">{"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq_items)}</div>
    </section>

    <section class="section district-nav">
      <p class="eyebrow">{eng} LEVELS</p>
      <h2>{s} 학교급별 수학과외</h2>
      <div class="district-links">{sibling_html}</div>
    </section>

    <section class="section area-nav">
      <p class="eyebrow">JEONBUK AREAS</p>
      <h2>전북 지역별 {short} 수학과외</h2>
      <nav class="area-links" aria-label="전북 지역별 {short} 수학과외">{area_html}</nav>
    </section>

    <section class="cta">
      <h2>{s} {short} 수학과외 무료체험수업,<br>전화로 먼저 상담하세요.</h2>
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
    urls = []
    for region in REGIONS:
        for level in LEVEL_KEYS:
            (ROOT / "regions" / page_name(region[0], level)).write_text(build(region, level), encoding="utf-8")
            urls.append(f"{SITE}/regions/{page_name(region[0], level)}")
    return urls
