const regionLinks = [
  ["전주시", "jeonju-si"], ["군산시", "gunsan-si"], ["익산시", "iksan-si"],
  ["정읍시", "jeongeup-si"], ["남원시", "namwon-si"], ["김제시", "gimje-si"],
  ["완주군", "wanju-gun"], ["진안군", "jinan-gun"], ["무주군", "muju-gun"],
  ["장수군", "jangsu-gun"], ["임실군", "imsil-gun"], ["순창군", "sunchang-gun"],
  ["고창군", "gochang-gun"], ["부안군", "buan-gun"],
];

const currentRegion = document.body.dataset.region;
document.querySelectorAll(".brand-mark").forEach((mark) => mark.setAttribute("aria-hidden", "true"));

const favicon = document.createElement("link");
favicon.rel = "icon";
favicon.type = "image/svg+xml";
favicon.href = "../assets/logo-mark.svg";
document.head.append(favicon);

document.querySelector(".area-links").innerHTML = regionLinks.map(([name, slug]) =>
  `<a href="${slug}.html"${name === currentRegion ? ' aria-current="page"' : ""}>${name}</a>`
).join("");

const gradeGuide = document.createElement("section");
gradeGuide.className = "section grade-guide";
gradeGuide.innerHTML = `
  <div class="grade-heading">
    <p class="eyebrow">GRADE PROGRAM</p>
    <h2>학년이 바뀌어도<br>흔들리지 않도록</h2>
    <p>초등은 연산과 교과 개념을 정확히 이해하는 습관부터 시작합니다. 중등은 학교 진도와 시험 범위에 맞춰 개념과 유형을 연결하고, 고등은 내신과 모의고사 목표에 따라 기출 분석과 실전 풀이 비중을 조절합니다.</p>
  </div>
  <div class="transition-grid">
    <article><span>예비중1</span><p>초등 수학의 빈틈을 점검하고 문자와 식, 정수와 유리수 등 중학교 첫 단원을 미리 준비합니다.</p></article>
    <article><span>예비중2</span><p>중1 핵심 개념을 복습한 뒤 식의 계산과 연립방정식으로 이어지는 학습 흐름을 만듭니다.</p></article>
    <article><span>예비중3</span><p>중2 취약 단원을 보완하면서 제곱근과 인수분해 등 고등 수학의 바탕이 되는 개념을 다집니다.</p></article>
    <article><span>예비고1</span><p>중등 전 범위의 연결을 확인하고 고등수학의 빠른 진도와 깊어진 문제 해석에 적응합니다.</p></article>
    <article><span>예비고2</span><p>고1 과정의 약점을 정리하고 선택 과목과 학교별 내신 일정에 맞는 학습 계획을 세웁니다.</p></article>
    <article><span>예비고3</span><p>개념과 기출을 다시 연결해 수능과 내신에서 보완할 영역을 찾고 실전 학습 순서를 정합니다.</p></article>
  </div>
`;
document.querySelector(".fit").before(gradeGuide);

document.querySelector("#year").textContent = new Date().getFullYear();