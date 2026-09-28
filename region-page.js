const regionLinks = [
  ["전주시", "jeonju-si"], ["군산시", "gunsan-si"], ["익산시", "iksan-si"],
  ["정읍시", "jeongeup-si"], ["남원시", "namwon-si"], ["김제시", "gimje-si"],
  ["완주군", "wanju-gun"], ["진안군", "jinan-gun"], ["무주군", "muju-gun"],
  ["장수군", "jangsu-gun"], ["임실군", "imsil-gun"], ["순창군", "sunchang-gun"],
  ["고창군", "gochang-gun"], ["부안군", "buan-gun"],
];

const currentRegion = document.body.dataset.region;
document.querySelector(".area-links").innerHTML = regionLinks.map(([name, slug]) =>
  `<a href="${slug}.html"${name === currentRegion ? ' aria-current="page"' : ""}>${name}</a>`
).join("");
document.querySelector("#year").textContent = new Date().getFullYear();