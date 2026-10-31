"""수학 공부 가이드 글(guides/*.html), 목록(guides/index.html), RSS(rss.xml)를 생성한다.

build_regions.py 실행 시 함께 호출된다. 새 글은 GUIDES 맨 앞에 추가한다.
"""
from build_regions import FONT_LINKS, PHONE, ROOT, SITE, TEL, esc, jsonld


# slug, 제목, 요약, 날짜, 대상 학교급 페이지(slug 접미사), 본문 HTML
GUIDES = [
    ("pre-high1-winter-math", "예비고1 겨울방학 수학 준비, 무엇부터 해야 할까",
     "중3 겨울방학은 고등 수학의 첫 단추입니다. 중등 복습과 공통수학 선행의 비중, 주간 계획 예시를 정리했습니다.",
     "2026-10-31", "high", """
<p>중학교 3학년 2학기 기말고사가 끝나면 고등학교 입학까지 약 3개월이 남습니다. 이 시기를 어떻게 보내느냐에 따라 고1 첫 중간고사의 부담이 크게 달라집니다. 무작정 선행 진도를 빼기보다 <strong>중등 핵심 단원 복습과 고1 첫 단원 준비</strong>를 함께 가져가는 것이 중요합니다.</p>
<h2>1. 먼저 중등 수학의 빈틈을 확인하세요</h2>
<p>고1 공통수학은 중학교에서 배운 다항식 계산, 인수분해, 이차방정식, 이차함수를 바탕으로 시작합니다. 이 네 단원에서 계산이 느리거나 실수가 잦다면 선행보다 복습이 먼저입니다.</p>
<ul>
<li><strong>인수분해:</strong> 공식만 외우지 말고 어떤 식에 어떤 방법을 쓰는지 스스로 고를 수 있어야 합니다.</li>
<li><strong>이차방정식:</strong> 근의 공식과 판별식의 의미를 설명할 수 있는지 확인합니다.</li>
<li><strong>이차함수:</strong> 그래프의 꼭짓점, 축, 평행이동을 식과 그림으로 오갈 수 있어야 합니다.</li>
</ul>
<h2>2. 공통수학 첫 단원은 '깊이' 있게</h2>
<p>고1 1학기 초반에는 다항식의 연산, 나머지정리, 인수분해, 복소수와 이차방정식이 이어집니다. 겨울방학에는 이 범위를 개념서 한 권으로 정확히 이해하는 것을 목표로 하세요. 여러 권을 빠르게 훑는 것보다 한 권을 오답까지 완전히 정리하는 편이 실제 내신에 훨씬 도움이 됩니다.</p>
<h2>3. 주간 계획 예시</h2>
<ul>
<li>주 3일: 공통수학 개념 학습 + 기본 문제</li>
<li>주 2일: 중등 핵심 단원 복습 + 계산 연습</li>
<li>주 1일: 한 주 동안 틀린 문제 다시 풀기</li>
</ul>
<p>하루 공부량보다 중요한 것은 <strong>매주 오답을 다시 푸는 날을 비워 두는 것</strong>입니다. 다시 풀었을 때 맞히는 문제가 늘어나야 실력이 쌓입니다.</p>
<h2>4. 이런 경우에는 1:1 수업을 고려해 보세요</h2>
<p>중등 개념의 빈틈이 커서 어디서부터 다시 해야 할지 모르겠거나, 혼자서는 오답 정리가 잘 이어지지 않는다면 학생의 현재 실력에 맞춰 순서를 잡아 주는 1:1 수업이 효율적입니다.</p>
"""),
    ("middle-school-exam-4weeks", "중학교 수학 내신, 시험 4주 전부터 준비하는 방법",
     "중간·기말고사 4주 전부터 시험 당일까지, 주차별로 무엇을 해야 하는지 정리한 중등 수학 내신 대비 계획입니다.",
     "2026-10-31", "middle", """
<p>중학교 수학 내신은 '얼마나 많이 풀었는가'보다 <strong>학교 시험 범위를 얼마나 정확하게 정리했는가</strong>로 결정됩니다. 시험 4주 전부터 아래 순서로 준비하면 막판에 몰아서 공부하는 부담을 줄일 수 있습니다.</p>
<h2>4주 전: 시험 범위와 자료 확인</h2>
<p>학교에서 공지한 시험 범위를 교과서 쪽수 단위로 적어 두고, 수업 시간에 받은 프린트와 학습지를 모두 모읍니다. 학교 선생님이 강조한 예제와 서술형 문항은 따로 표시해 둡니다.</p>
<h2>3주 전: 개념 정리와 교과서 문제</h2>
<p>교과서의 개념 설명과 예제, 확인 문제를 다시 풉니다. 교과서 문제를 막힘없이 풀 수 있어야 그다음 유형 문제집이 의미가 있습니다. 공식은 왜 그렇게 되는지 한 줄로 설명할 수 있는지 확인하세요.</p>
<h2>2주 전: 유형 연습과 서술형</h2>
<p>문제집으로 단원별 대표 유형을 연습하고, 서술형은 풀이 과정을 처음부터 끝까지 써 봅니다. 서술형 감점은 대부분 <strong>중간 과정 생략, 단위·조건 누락, 마지막 답 미기재</strong>에서 나옵니다.</p>
<h2>1주 전: 기출과 오답 재풀이</h2>
<p>같은 학교의 이전 기출 문제를 시간을 재고 풀어 봅니다. 그 뒤에는 새 문제를 늘리기보다 지금까지 틀린 문제를 다시 풀어 같은 실수를 반복하지 않도록 합니다.</p>
<h2>시험 전날</h2>
<p>오답 노트와 학교 프린트의 표시한 문제만 가볍게 확인하고 충분히 잡니다. 전날 새로운 어려운 문제를 붙잡는 것은 오히려 자신감을 떨어뜨립니다.</p>
<p>학교마다 시험 범위와 출제 경향이 다르기 때문에, 다니는 학교의 자료를 기준으로 계획을 세우는 것이 가장 중요합니다.</p>
"""),
    ("elementary-calculation-mistakes", "초등 수학 연산 실수, 습관부터 바꾸는 5가지 방법",
     "알면서도 틀리는 초등 연산 실수는 대부분 습관에서 나옵니다. 집에서도 바로 해볼 수 있는 연산 실수 줄이는 방법입니다.",
     "2026-10-31", "elementary", """
<p>"아는 문제인데 계산에서 틀렸어요." 초등 수학에서 가장 많이 듣는 이야기입니다. 연산 실수는 실력 부족이라기보다 <strong>풀이 습관</strong>에서 생기는 경우가 많아서, 습관을 바꾸면 눈에 띄게 줄어듭니다.</p>
<h2>1. 어떤 실수인지 먼저 분류하기</h2>
<p>받아올림·받아내림을 빠뜨리는지, 자릿수를 잘못 맞추는지, 문제의 숫자를 잘못 옮겨 적는지 틀린 문제를 모아 종류별로 나눠 보세요. 실수의 종류가 보이면 고칠 방법도 분명해집니다.</p>
<h2>2. 풀이를 줄 맞춰 쓰기</h2>
<p>연습장 아무 곳에나 계산하면 자릿수가 어긋나기 쉽습니다. 세로셈은 칸을 맞춰 쓰고, 한 문제의 풀이는 한곳에 모아 쓰는 습관을 들입니다.</p>
<h2>3. 짧게, 매일 하기</h2>
<p>한 번에 많은 양을 푸는 것보다 하루 10~15분이라도 매일 이어가는 것이 정확도를 높이는 데 효과적입니다. 속도보다 정확도를 먼저 목표로 합니다.</p>
<h2>4. 검산하는 방법 익히기</h2>
<p>덧셈은 뺄셈으로, 곱셈은 나눗셈으로 거꾸로 확인하는 방법을 알려 주세요. 모든 문제를 검산할 필요는 없지만, 시험에서는 자신이 자주 틀리는 유형만이라도 다시 확인하게 합니다.</p>
<h2>5. 틀린 문제를 말로 설명하게 하기</h2>
<p>틀린 문제를 다시 풀 때 "왜 이렇게 계산했는지"를 말로 설명하게 하면, 단순 실수인지 개념을 헷갈린 것인지 구분할 수 있습니다. 분수·소수 계산에서 실수가 반복된다면 개념부터 다시 짚어 보는 것이 좋습니다.</p>
"""),
    ("high-school-wrong-answer-note", "고등 수학 오답노트, 쓰는 것보다 다시 푸는 것이 중요합니다",
     "시간만 많이 드는 오답노트 대신, 내신과 모의고사 점수로 이어지는 고등 수학 오답 관리 방법을 소개합니다.",
     "2026-10-31", "high", """
<p>고등학생이 되면 문제 수가 많아지고 시험 범위도 넓어집니다. 그래서 틀린 문제를 예쁘게 옮겨 적는 오답노트는 시간이 너무 많이 들어 오래 이어가기 어렵습니다. 중요한 것은 노트의 모양이 아니라 <strong>틀린 문제를 다시 풀어서 맞히는 경험</strong>입니다.</p>
<h2>1. 틀린 이유를 한 줄로 적기</h2>
<p>문제를 옮겨 적는 대신 문제집에 표시하고, 옆에 틀린 이유를 한 줄로 적습니다. "개념을 몰랐다", "조건을 놓쳤다", "계산 실수", "시간 부족"처럼 이유를 나누면 나중에 약점이 한눈에 보입니다.</p>
<h2>2. 3일 뒤, 1주 뒤 다시 풀기</h2>
<p>틀린 직후 해설을 보고 이해한 것은 아직 내 실력이 아닙니다. 며칠 뒤 해설 없이 다시 풀어 맞혀야 비로소 실력이 됩니다. 두 번 다시 풀어도 틀리는 문제만 따로 모아 시험 전에 집중적으로 봅니다.</p>
<h2>3. 모의고사는 단원별로 다시 나누기</h2>
<p>모의고사에서 틀린 문항은 단원과 틀린 이유별로 분류해 보세요. 특정 단원에 오답이 몰려 있다면 그 단원의 개념부터 다시 정리하고, 시간 부족이 원인이라면 풀이 순서와 시간 배분을 바꿔야 합니다.</p>
<h2>4. 내신 기간에는 학교 자료 위주로</h2>
<p>내신 시험이 다가오면 오답 재풀이도 학교 교과서, 부교재, 학교 프린트 문제를 우선합니다. 학교 시험은 수업에서 다룬 자료에서 나오는 경우가 많기 때문입니다.</p>
<p>오답 관리가 혼자 잘 이어지지 않는다면, 수업 시간 안에서 오답을 함께 점검하는 1:1 수업이 도움이 됩니다.</p>
"""),
    ("tutoring-vs-academy", "수학과외와 수학학원, 우리 아이에게 맞는 선택 기준",
     "수학학원과 1:1 수학과외는 장단점이 다릅니다. 학생의 성향과 현재 실력에 따라 무엇이 맞는지 판단하는 기준을 정리했습니다.",
     "2026-10-31", None, """
<p>수학 공부를 도와줄 곳을 찾을 때 가장 먼저 고민하는 것이 학원과 과외 중 무엇을 선택할지입니다. 어느 한쪽이 무조건 좋은 것이 아니라, <strong>학생의 현재 실력과 공부 성향</strong>에 따라 맞는 방식이 다릅니다.</p>
<h2>수학학원이 잘 맞는 경우</h2>
<ul>
<li>학교 진도를 무리 없이 따라가고, 정해진 커리큘럼에 맞춰 공부하는 것이 편한 학생</li>
<li>또래와 함께 공부할 때 동기 부여가 잘 되는 학생</li>
<li>질문이 생기면 스스로 손을 들고 해결할 수 있는 학생</li>
</ul>
<h2>1:1 수학과외가 잘 맞는 경우</h2>
<ul>
<li>이전 학년 개념에 빈틈이 있어 반 진도를 따라가기 어려운 학생</li>
<li>질문을 잘 하지 못하거나, 모르는 부분을 그냥 넘기는 습관이 있는 학생</li>
<li>다니는 학교의 시험 범위와 출제 경향에 맞춘 내신 대비가 필요한 학생</li>
<li>목표 등급이 분명해 학습 계획을 개인에 맞게 세워야 하는 고등학생</li>
</ul>
<h2>선택하기 전에 확인할 것</h2>
<p>어떤 방식을 선택하든 <strong>첫 상담에서 현재 실력을 어떻게 진단하는지</strong>, 수업 이후 숙제와 오답을 어떻게 관리하는지 꼭 물어보세요. 진단 없이 바로 진도를 시작하거나, 수업 이후 관리 방법이 불분명하다면 다시 생각해 보는 것이 좋습니다.</p>
<p>체험수업을 통해 학생이 설명 방식을 편하게 느끼는지 직접 확인해 보는 것도 좋은 방법입니다.</p>
"""),
]

LEVEL_LABEL = {"elementary": "초등", "middle": "중등", "high": "고등"}


def head(title, desc, url, prefix, schema, og_type="article"):
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="전북 수학과외">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/og-image.jpg?v=20261008">
  <meta property="og:locale" content="ko_KR">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="alternate" type="application/rss+xml" title="전북 수학과외 수학 공부 가이드" href="{SITE}/rss.xml">
  <link rel="icon" href="{prefix}favicon.ico" sizes="any">
  <link rel="icon" href="{prefix}assets/logo-mark.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="{prefix}assets/apple-touch-icon.png">
{FONT_LINKS}
  <link rel="stylesheet" href="{prefix}region-page.css">
  {jsonld(schema)}
</head>"""


def shell_top(prefix):
    return f"""<body>
  <header class="site-header">
    <a class="brand" href="{prefix}">
      <span class="brand-mark" aria-hidden="true">∑</span>
      <span>전북 수학과외<small>TUTOR PLUS</small></span>
    </a>
    <a class="back-link" href="{prefix}guides/">수학 공부 가이드</a>
  </header>"""


def shell_bottom(prefix):
    return f"""  <footer class="site-footer">
    <span>전북 수학과외 · 초등·중등·고등 1:1 맞춤 수학 코칭</span>
    <span>© <span id="year">2026</span> TUTOR PLUS.</span>
  </footer>
  <a class="floating-phone" href="{TEL}">무료체험수업 상담 {PHONE}</a>
  <script src="{prefix}region-page.js"></script>
</body>
</html>
"""


def build_article(guide):
    slug, title, summary, date, level, body = guide
    url = f"{SITE}/guides/{slug}.html"
    others = [g for g in GUIDES if g[0] != slug]
    schema = [
        {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": summary,
         "datePublished": date, "dateModified": date, "mainEntityOfPage": url, "inLanguage": "ko",
         "image": f"{SITE}/assets/og-image.jpg",
         "author": {"@type": "Organization", "name": "전북 수학과외 TUTOR PLUS", "url": f"{SITE}/"},
         "publisher": {"@type": "Organization", "name": "전북 수학과외 TUTOR PLUS",
                       "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/apple-touch-icon.png"}}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "전북 수학과외", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "수학 공부 가이드", "item": f"{SITE}/guides/"},
            {"@type": "ListItem", "position": 3, "name": title, "item": url}]},
    ]
    related = ""
    if level:
        lv = LEVEL_LABEL[level]
        related = (f'<p class="article-related">{lv} 수학과외 지역별 안내: '
                   f'<a href="../regions/jeonju-si-{level}.html">전주 {lv} 수학과외</a> · '
                   f'<a href="../regions/gunsan-si-{level}.html">군산 {lv} 수학과외</a> · '
                   f'<a href="../regions/iksan-si-{level}.html">익산 {lv} 수학과외</a></p>')
    return f"""{head(f"{title} | 전북 수학과외", summary, url, "../", schema)}
{shell_top("../")}
  <main>
    <nav class="breadcrumb" aria-label="현재 위치"><a href="../">전북 수학과외</a> › <a href="./">수학 공부 가이드</a> › <span>{title}</span></nav>
    <article class="section article">
      <p class="eyebrow">MATH STUDY GUIDE</p>
      <h1>{title}</h1>
      <p class="article-meta"><time datetime="{date}">{date.replace("-", ".")}</time> · 전북 수학과외</p>
      <p class="article-summary">{summary}</p>
      <div class="article-body">{body}</div>
      {related}
    </article>
    <section class="section district-nav">
      <p class="eyebrow">MORE GUIDES</p>
      <h2>다른 수학 공부 가이드</h2>
      <div class="guide-list">{"".join(f'<a href="{g[0]}.html"><strong>{g[1]}</strong><span>{g[2]}</span></a>' for g in others)}</div>
    </section>
    <section class="cta">
      <h2>우리 아이에게 맞는 공부 순서,<br>전화로 먼저 상담하세요.</h2>
      <a class="primary-button" href="{TEL}">{PHONE}</a>
    </section>
  </main>
{shell_bottom("../")}"""


def build_index():
    url = f"{SITE}/guides/"
    title = "수학 공부 가이드 | 초등·중등·고등 수학 공부법 – 전북 수학과외"
    desc = "초등 연산 실수, 중학교 수학 내신 대비, 예비고1 준비, 고등 오답노트까지 학년별 수학 공부 방법을 정리했습니다."
    schema = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "수학 공부 가이드", "url": url, "description": desc,
              "hasPart": [{"@type": "Article", "headline": g[1], "url": f"{SITE}/guides/{g[0]}.html"} for g in GUIDES]}
    return f"""{head(title, desc, url, "../", schema, "website")}
{shell_top("../")}
  <main>
    <nav class="breadcrumb" aria-label="현재 위치"><a href="../">전북 수학과외</a> › <span>수학 공부 가이드</span></nav>
    <section class="section article">
      <p class="eyebrow">MATH STUDY GUIDE</p>
      <h1>수학 공부 가이드</h1>
      <p class="article-summary">{desc}</p>
      <div class="guide-list">{"".join(f'<a href="{g[0]}.html"><strong>{g[1]}</strong><span>{g[2]}</span><time datetime="{g[3]}">{g[3].replace("-", ".")}</time></a>' for g in GUIDES)}</div>
    </section>
    <section class="cta">
      <h2>전북 초·중·고 1:1 수학과외,<br>전화로 먼저 상담하세요.</h2>
      <a class="primary-button" href="{TEL}">{PHONE}</a>
    </section>
  </main>
{shell_bottom("../")}"""


def build_rss():
    from email.utils import format_datetime
    from datetime import datetime, timezone, timedelta
    kst = timezone(timedelta(hours=9))
    items = "".join(f"""
    <item>
      <title>{esc(g[1])}</title>
      <link>{SITE}/guides/{g[0]}.html</link>
      <guid>{SITE}/guides/{g[0]}.html</guid>
      <description>{esc(g[2])}</description>
      <pubDate>{format_datetime(datetime.fromisoformat(g[3]).replace(hour=9, tzinfo=kst))}</pubDate>
    </item>""" for g in GUIDES)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>전북 수학과외 수학 공부 가이드</title>
    <link>{SITE}/guides/</link>
    <description>전북 초등·중등·고등 1:1 수학과외 TUTOR PLUS의 학년별 수학 공부 방법</description>
    <language>ko</language>{items}
  </channel>
</rss>
"""


def index_block():
    """index.html 의 <!-- guides:start --> ~ <!-- guides:end --> 구간."""
    cards = "".join(f'<a href="guides/{g[0]}.html"><strong>{g[1]}</strong><span>{g[2]}</span></a>' for g in GUIDES[:4])
    return f"""<!-- guides:start -->
    <section class="guides section" id="guides" aria-labelledby="guides-title">
      <div class="section-title reveal">
        <p class="eyebrow">STUDY GUIDE</p>
        <h2 id="guides-title">학년별<br>수학 공부 가이드</h2>
      </div>
      <div class="guide-cards reveal">{cards}</div>
      <a class="school-more" href="guides/">수학 공부 가이드 전체 보기 →</a>
    </section>
    <!-- guides:end -->"""


def write_all():
    out = ROOT / "guides"
    out.mkdir(exist_ok=True)
    for guide in GUIDES:
        (out / f"{guide[0]}.html").write_text(build_article(guide), encoding="utf-8")
    (out / "index.html").write_text(build_index(), encoding="utf-8")
    (ROOT / "rss.xml").write_text(build_rss(), encoding="utf-8")
    return [f"{SITE}/guides/"] + [f"{SITE}/guides/{g[0]}.html" for g in GUIDES]
