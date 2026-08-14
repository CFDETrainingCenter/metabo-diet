#!/usr/bin/env python3
"""Build a self-contained, accessible SCORM 1.2 package for Metabo-Diet."""

from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "module"
SCORM = MODULE / "scorm"
PACKAGE = SCORM / "package"
QA = MODULE / "qa"
DOWNLOADS = MODULE / "site" / "public" / "downloads"

LESSONS = [
    ("lesson_01", "Lesson 1 - Why harmonization matters", MODULE / "content" / "lesson_01_why_harmonization_matters.md"),
    ("lesson_02", "Lesson 2 - Comparing study design", MODULE / "content" / "lesson_02_comparing_study_design.md"),
    ("lesson_03", "Lesson 3 - Harmonizing metabolomics and metadata", MODULE / "content" / "lesson_03_harmonizing_metabolomics_metadata.md"),
    ("lesson_04", "Lesson 4 - Guided analysis and interpretation", MODULE / "content" / "lesson_04_guided_analysis_interpretation.md"),
    ("lesson_05", "Lesson 5 - Access tiers and transfer", MODULE / "content" / "lesson_05_access_tiers_transfer.md"),
]


def clean_text(value: str) -> str:
    return (
        value.replace("\u00a0", " ")
        .replace("\u2010", "-")
        .replace("\u2011", "-")
        .replace("\u2012", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2212", "-")
    )


def inline_markup(value: str) -> str:
    value = html.escape(clean_text(value), quote=True)
    value = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: '<a href="' + match.group(2) + '">' + match.group(1) + "</a>",
        value,
    )
    tick = re.escape(chr(96))
    value = re.sub(tick + r"(.+?)" + tick, r"<code>\1</code>", value)
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", value)
    return value


def parse_table_line(line: str) -> list[str]:
    return [part.strip() for part in line.strip().strip("|").split("|")]


def is_table_separator(line: str) -> bool:
    return bool(re.match(r"^\s*\|?\s*:?-{3,}", line)) and "|" in line


def markdown_to_html(source: str) -> str:
    lines = source.splitlines()
    output: list[str] = []
    index = 0
    list_tag: str | None = None
    blockquote_open = False
    in_code = False
    code_lines: list[str] = []

    def close_list() -> None:
        nonlocal list_tag
        if list_tag:
            output.append("</" + list_tag + ">")
            list_tag = None

    def close_quote() -> None:
        nonlocal blockquote_open
        if blockquote_open:
            output.append("</blockquote>")
            blockquote_open = False

    while index < len(lines):
        raw = lines[index].rstrip()
        stripped = raw.strip()
        if stripped.startswith(chr(96) * 3):
            close_list()
            close_quote()
            if in_code:
                output.append("<pre><code>" + html.escape(clean_text("\n".join(code_lines))) + "</code></pre>")
                code_lines = []
                in_code = False
            else:
                in_code = True
            index += 1
            continue
        if in_code:
            code_lines.append(raw)
            index += 1
            continue
        if not stripped or stripped == "---":
            close_list()
            close_quote()
            index += 1
            continue
        if stripped.startswith("|") and index + 1 < len(lines) and is_table_separator(lines[index + 1]):
            close_list()
            close_quote()
            rows = [parse_table_line(raw)]
            index += 2
            while index < len(lines) and lines[index].strip().startswith("|"):
                rows.append(parse_table_line(lines[index]))
                index += 1
            output.append('<div class="table-scroll" role="region" aria-label="Scrollable data table" tabindex="0"><table>')
            output.append("<thead><tr>")
            for value in rows[0]:
                output.append('<th scope="col">' + inline_markup(value) + "</th>")
            output.append("</tr></thead><tbody>")
            for row in rows[1:]:
                output.append("<tr>")
                for value in row:
                    output.append("<td>" + inline_markup(value) + "</td>")
                output.append("</tr>")
            output.append("</tbody></table></div>")
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            close_list()
            close_quote()
            level = min(6, len(heading.group(1)))
            output.append("<h" + str(level) + ">" + inline_markup(heading.group(2)) + "</h" + str(level) + ">")
            index += 1
            continue
        quote = re.match(r"^>\s?(.*)$", stripped)
        if quote:
            close_list()
            if not blockquote_open:
                output.append("<blockquote>")
                blockquote_open = True
            output.append("<p>" + inline_markup(quote.group(1)) + "</p>")
            index += 1
            continue
        close_quote()
        list_match = re.match(r"^\s*([-+*]|\d+\.)\s+(.+)$", raw)
        if list_match:
            tag = "ul" if list_match.group(1) in {"-", "+", "*"} else "ol"
            if list_tag != tag:
                close_list()
                list_tag = tag
                output.append("<" + tag + ">")
            output.append("<li>" + inline_markup(list_match.group(2)) + "</li>")
            index += 1
            continue
        close_list()
        output.append("<p>" + inline_markup(stripped) + "</p>")
        index += 1
    if in_code:
        output.append("<pre><code>" + html.escape(clean_text("\n".join(code_lines))) + "</code></pre>")
    close_list()
    close_quote()
    return "\n".join(output)


CSS = """
:root {
  color-scheme: light;
  --navy: #18354a;
  --blue: #245c85;
  --teal: #24726d;
  --gold: #9a6b12;
  --ink: #1c252c;
  --muted: #53626c;
  --paper: #ffffff;
  --surface: #f4f7f8;
  --line: #c8d3d8;
  --success: #176b44;
  --danger: #9b2c2c;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--ink);
  background: #eef3f5;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 1rem;
  line-height: 1.62;
}
a { color: #164f7a; text-underline-offset: 0.16em; }
a:hover { color: #0b3554; }
a:focus-visible, button:focus-visible, input:focus-visible, [tabindex="0"]:focus-visible {
  outline: 3px solid #d49416;
  outline-offset: 3px;
}
.skip-link {
  position: absolute;
  left: 1rem;
  top: -5rem;
  z-index: 100;
  padding: 0.7rem 1rem;
  color: #fff;
  background: #000;
}
.skip-link:focus { top: 1rem; }
.site-header {
  color: #fff;
  background: var(--navy);
  border-bottom: 5px solid var(--teal);
}
.header-inner, .page-shell, .footer-inner {
  width: min(100% - 2rem, 72rem);
  margin-inline: auto;
}
.header-inner { padding: 1rem 0; }
.brand { margin: 0; font-size: 1.08rem; font-weight: 800; letter-spacing: 0.04em; }
.mode { margin: 0.25rem 0 0; color: #e8f0f4; font-size: 0.9rem; }
.page-shell {
  display: grid;
  grid-template-columns: minmax(12rem, 15rem) minmax(0, 1fr);
  gap: 2rem;
  padding-block: 2rem 4rem;
}
.course-nav {
  align-self: start;
  position: sticky;
  top: 1rem;
  padding: 1rem;
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 0.75rem;
}
.course-nav h2 { margin-top: 0; font-size: 1rem; color: var(--navy); }
.course-nav ul { margin: 0; padding-left: 1.2rem; }
.course-nav li { margin: 0.38rem 0; }
.course-nav .status {
  margin-top: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--line);
  font-size: 0.88rem;
  color: var(--muted);
}
main {
  min-width: 0;
  padding: clamp(1.25rem, 3vw, 3rem);
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 0.9rem;
  box-shadow: 0 12px 34px rgba(24, 53, 74, 0.08);
}
h1, h2, h3, h4 { color: var(--navy); line-height: 1.23; }
h1 { margin: 0 0 1rem; font-size: clamp(2rem, 4vw, 3rem); }
h2 { margin-top: 2.2rem; font-size: 1.55rem; }
h3 { margin-top: 1.6rem; font-size: 1.22rem; }
h4 { margin-top: 1.35rem; font-size: 1.06rem; }
p, li { max-width: 76ch; }
blockquote {
  margin: 1.3rem 0;
  padding: 0.85rem 1.15rem;
  color: #193e58;
  background: #edf4f7;
  border-left: 0.35rem solid var(--blue);
}
blockquote p { margin: 0.25rem 0; }
code {
  padding: 0.08rem 0.28rem;
  color: #163448;
  background: #edf1f3;
  border-radius: 0.2rem;
  font-family: "SFMono-Regular", Consolas, monospace;
  font-size: 0.9em;
}
pre {
  overflow: auto;
  padding: 1rem;
  color: #f5f8fa;
  background: #163448;
  border-radius: 0.5rem;
}
pre code { padding: 0; color: inherit; background: transparent; }
.table-scroll { overflow-x: auto; margin: 1.25rem 0; }
table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
th, td { padding: 0.6rem 0.68rem; text-align: left; vertical-align: top; border: 1px solid #bfcbd1; }
th { color: #17364c; background: #e4edf2; }
.hero {
  margin: -0.3rem 0 2rem;
  padding: clamp(1.5rem, 4vw, 3rem);
  color: #fff;
  background: linear-gradient(135deg, #18354a, #245c85);
  border-radius: 0.75rem;
}
.hero h1 { color: #fff; }
.hero p { color: #e8f2f5; font-size: 1.08rem; }
.activity-list { display: grid; gap: 0.65rem; margin: 1.2rem 0; padding: 0; list-style: none; }
.activity-list a {
  display: block;
  padding: 0.85rem 1rem;
  color: var(--navy);
  background: #f5f8f9;
  border: 1px solid var(--line);
  border-left: 0.35rem solid var(--teal);
  border-radius: 0.45rem;
  font-weight: 700;
}
.activity-state { margin-left: 0.4rem; color: var(--muted); font-size: 0.88rem; font-weight: 400; }
.callout {
  padding: 1rem 1.1rem;
  background: #fff8e8;
  border: 1px solid #dbc17d;
  border-radius: 0.5rem;
}
.actions { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 2rem; padding-top: 1.2rem; border-top: 1px solid var(--line); }
button, .button {
  display: inline-block;
  padding: 0.68rem 1rem;
  color: #fff;
  background: var(--blue);
  border: 2px solid var(--blue);
  border-radius: 0.42rem;
  font: inherit;
  font-weight: 800;
  cursor: pointer;
  text-decoration: none;
}
button:hover, .button:hover { color: #fff; background: #183f5e; border-color: #183f5e; }
.button.secondary, button.secondary { color: var(--blue); background: #fff; }
.button.secondary:hover, button.secondary:hover { color: #fff; background: var(--blue); }
fieldset { margin: 1.3rem 0; padding: 1rem; border: 1px solid var(--line); border-radius: 0.5rem; }
legend { max-width: 75ch; padding: 0 0.35rem; color: var(--navy); font-weight: 800; }
.option { display: grid; grid-template-columns: 1.2rem 1fr; gap: 0.6rem; margin: 0.55rem 0; padding: 0.6rem; border-radius: 0.35rem; }
.option:hover { background: #f2f6f7; }
.feedback { margin-top: 0.7rem; padding: 0.7rem 0.85rem; border-radius: 0.35rem; }
.feedback.correct { color: #0e5433; background: #e7f5ed; border-left: 0.3rem solid var(--success); }
.feedback.incorrect { color: #762121; background: #faecec; border-left: 0.3rem solid var(--danger); }
.result-summary { margin: 1rem 0; padding: 1rem; background: #eef4f7; border: 2px solid var(--blue); border-radius: 0.5rem; }
.site-footer { padding: 1.5rem 0; color: #eaf1f4; background: var(--navy); }
.footer-inner p { margin: 0.2rem 0; font-size: 0.86rem; }
.visually-hidden {
  position: absolute !important;
  width: 1px; height: 1px;
  padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0, 0, 0, 0);
  white-space: nowrap; border: 0;
}
@media (max-width: 54rem) {
  .page-shell { grid-template-columns: 1fr; }
  .course-nav { position: static; }
}
@media print {
  body { background: #fff; }
  .course-nav, .site-header, .site-footer, .actions, .skip-link { display: none; }
  .page-shell { display: block; width: 100%; padding: 0; }
  main { border: 0; box-shadow: none; padding: 0; }
  a { color: inherit; }
}
"""


COURSE_JS = """
(function () {
  "use strict";
  var STORAGE_KEY = "metaboDietScormStateV1";
  var REQUIRED = ["pretest", "lesson_01", "lesson_02", "lesson_03", "lesson_04", "lesson_05", "posttest"];
  var memoryState = { activities: {}, assessments: {}, updated: null };
  var api = null;
  var initialized = false;

  function searchApiChain(win) {
    var attempts = 0;
    while (win && attempts < 50) {
      try {
        if (win.API) return win.API;
        if (win.parent && win.parent !== win) win = win.parent;
        else break;
      } catch (error) { break; }
      attempts += 1;
    }
    return null;
  }

  function findApi(win) {
    var found = searchApiChain(win);
    if (found) return found;
    try {
      if (win === window && window.opener && window.opener !== window) {
        return searchApiChain(window.opener);
      }
    } catch (error) {}
    return null;
  }

  function lms(method, argument1, argument2) {
    if (!api || typeof api[method] !== "function") return "";
    try {
      if (typeof argument2 !== "undefined") return api[method](argument1, argument2);
      return api[method](argument1 || "");
    } catch (error) { return ""; }
  }

  function safeParse(value) {
    try { return value ? JSON.parse(value) : null; } catch (error) { return null; }
  }

  function loadState() {
    var local = null;
    try { local = safeParse(window.localStorage.getItem(STORAGE_KEY)); } catch (error) {}
    if (local) memoryState = local;
    if (initialized) {
      var remote = safeParse(lms("LMSGetValue", "cmi.suspend_data"));
      if (remote && (!memoryState.updated || String(remote.updated) > String(memoryState.updated))) {
        memoryState = remote;
      }
    }
    memoryState.activities = memoryState.activities || {};
    memoryState.assessments = memoryState.assessments || {};
    return memoryState;
  }

  function calculateStatus() {
    var complete = REQUIRED.every(function (id) { return Boolean(memoryState.activities[id]); });
    if (!complete) return "incomplete";
    var post = memoryState.assessments.posttest;
    if (!post) return "completed";
    return post.percent >= 80 ? "passed" : "failed";
  }

  function saveState() {
    memoryState.updated = new Date().toISOString();
    try { window.localStorage.setItem(STORAGE_KEY, JSON.stringify(memoryState)); } catch (error) {}
    if (initialized) {
      lms("LMSSetValue", "cmi.suspend_data", JSON.stringify(memoryState));
      lms("LMSSetValue", "cmi.core.lesson_status", calculateStatus());
      if (memoryState.assessments.posttest) {
        lms("LMSSetValue", "cmi.core.score.raw", String(memoryState.assessments.posttest.percent));
        lms("LMSSetValue", "cmi.core.score.min", "0");
        lms("LMSSetValue", "cmi.core.score.max", "100");
      }
      lms("LMSCommit", "");
    }
    updateInterface();
  }

  function initialize() {
    api = findApi(window);
    if (api) initialized = String(lms("LMSInitialize", "")).toLowerCase() === "true";
    loadState();
    if (initialized) {
      var current = lms("LMSGetValue", "cmi.core.lesson_status");
      if (!current || current === "not attempted") lms("LMSSetValue", "cmi.core.lesson_status", "incomplete");
      lms("LMSSetValue", "cmi.core.lesson_location", document.body.getAttribute("data-page-id") || "index");
      lms("LMSCommit", "");
    }
    updateInterface();
  }

  function updateInterface() {
    var mode = document.getElementById("lms-mode");
    if (mode) mode.textContent = initialized ? "Connected to LMS (SCORM 1.2)" : "Local progress fallback active";
    var courseStatus = document.getElementById("course-status");
    if (courseStatus) courseStatus.textContent = "Course status: " + calculateStatus();
    var nodes = document.querySelectorAll("[data-activity-state]");
    Array.prototype.forEach.call(nodes, function (node) {
      var id = node.getAttribute("data-activity-state");
      node.textContent = memoryState.activities[id] ? "Complete" : "Not complete";
    });
    var currentId = document.body.getAttribute("data-page-id");
    var lessonButton = document.querySelector("[data-complete-lesson]");
    if (lessonButton && memoryState.activities[currentId]) {
      lessonButton.textContent = "Lesson complete";
      lessonButton.setAttribute("aria-pressed", "true");
    }
  }

  function markLessonComplete(id) {
    memoryState.activities[id] = true;
    saveState();
    var notice = document.getElementById("completion-notice");
    if (notice) {
      notice.textContent = "Saved. This lesson is marked complete.";
      notice.focus();
    }
  }

  function recordAssessment(id, correct, maximum) {
    var percent = maximum ? Math.round((correct / maximum) * 100) : 0;
    memoryState.activities[id] = true;
    memoryState.assessments[id] = {
      correct: correct,
      maximum: maximum,
      percent: percent,
      submitted: new Date().toISOString()
    };
    saveState();
    return percent;
  }

  function resetLocalProgress() {
    if (!window.confirm("Reset locally stored progress and assessment results for this course?")) return;
    memoryState = { activities: {}, assessments: {}, updated: null };
    try { window.localStorage.removeItem(STORAGE_KEY); } catch (error) {}
    saveState();
  }

  function finish() {
    if (initialized) {
      lms("LMSCommit", "");
      lms("LMSFinish", "");
      initialized = false;
    }
  }

  window.MetaboDiet = {
    getState: function () { return memoryState; },
    markLessonComplete: markLessonComplete,
    recordAssessment: recordAssessment,
    resetLocalProgress: resetLocalProgress,
    updateInterface: updateInterface
  };

  document.addEventListener("DOMContentLoaded", function () {
    initialize();
    var lessonButton = document.querySelector("[data-complete-lesson]");
    if (lessonButton) {
      lessonButton.addEventListener("click", function () {
        markLessonComplete(document.body.getAttribute("data-page-id"));
      });
    }
    var reset = document.getElementById("reset-progress");
    if (reset) reset.addEventListener("click", resetLocalProgress);
  });
  window.addEventListener("pagehide", finish);
}());
"""


ASSESSMENT_JS = """
(function () {
  "use strict";
  function make(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (typeof text !== "undefined") node.textContent = text;
    return node;
  }

  function render() {
    var dataNode = document.getElementById("assessment-data");
    var root = document.getElementById("assessment-root");
    if (!dataNode || !root) return;
    var payload = JSON.parse(dataNode.textContent);
    var form = make("form", "assessment-form");
    form.setAttribute("novalidate", "");
    payload.items.forEach(function (item, index) {
      var fieldset = document.createElement("fieldset");
      fieldset.setAttribute("data-item-id", item.id);
      var legend = make("legend", "", String(index + 1) + ". " + item.prompt);
      fieldset.appendChild(legend);
      Object.keys(item.options).forEach(function (key) {
        var label = make("label", "option");
        var input = document.createElement("input");
        input.type = "radio";
        input.name = item.id;
        input.value = key;
        input.required = true;
        var text = make("span", "", key + ". " + item.options[key]);
        label.appendChild(input);
        label.appendChild(text);
        fieldset.appendChild(label);
      });
      form.appendChild(fieldset);
    });
    var summary = make("div", "result-summary");
    summary.id = "assessment-summary";
    summary.tabIndex = -1;
    summary.hidden = true;
    summary.setAttribute("aria-live", "polite");
    var submit = make("button", "", "Submit " + payload.title.toLowerCase());
    submit.type = "submit";
    form.appendChild(submit);
    root.appendChild(form);
    root.appendChild(summary);

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var firstMissing = null;
      payload.items.forEach(function (item) {
        if (!form.querySelector('input[name="' + item.id + '"]:checked') && !firstMissing) {
          firstMissing = form.querySelector('fieldset[data-item-id="' + item.id + '"]');
        }
      });
      if (firstMissing) {
        summary.hidden = false;
        summary.textContent = "Please answer every question before submitting.";
        summary.focus();
        firstMissing.scrollIntoView({ block: "center" });
        return;
      }
      var correct = 0;
      payload.items.forEach(function (item) {
        var fieldset = form.querySelector('fieldset[data-item-id="' + item.id + '"]');
        var selected = form.querySelector('input[name="' + item.id + '"]:checked').value;
        var prior = fieldset.querySelector(".feedback");
        if (prior) prior.remove();
        var isCorrect = selected === item.answer;
        if (isCorrect) correct += 1;
        var feedback = make(
          "div",
          "feedback " + (isCorrect ? "correct" : "incorrect"),
          (isCorrect ? "Correct. " : "Not yet. Correct answer: " + item.answer + ". ") + item.rationale
        );
        feedback.setAttribute("role", "status");
        fieldset.appendChild(feedback);
      });
      var id = document.body.getAttribute("data-page-id");
      var percent = window.MetaboDiet.recordAssessment(id, correct, payload.items.length);
      summary.hidden = false;
      summary.textContent = "Submitted: " + correct + " of " + payload.items.length + " correct (" + percent + "%). Rationales now appear below each item.";
      summary.focus();
    });
  }
  document.addEventListener("DOMContentLoaded", render);
}());
"""


def course_nav() -> str:
    links = [
        ("index.html", "Course home"),
        ("pretest.html", "Pretest"),
        *[(lesson_id + ".html", title) for lesson_id, title, _ in LESSONS],
        ("posttest.html", "Posttest"),
    ]
    items = "\n".join('<li><a href="' + href + '">' + html.escape(title) + "</a></li>" for href, title in links)
    return """
<nav class="course-nav" aria-label="Course navigation">
  <h2>Course navigation</h2>
  <ul>""" + items + """</ul>
  <p class="status" id="lms-mode">Checking LMS connection...</p>
  <p class="status" id="course-status">Course status: not attempted</p>
</nav>
"""


def page_template(page_id: str, title: str, main_html: str, extra_scripts: str = "") -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>""" + html.escape(title) + """ | Metabo-Diet</title>
  <link rel="stylesheet" href="assets/course.css">
</head>
<body data-page-id=\"""" + html.escape(page_id) + """\">
  <a class="skip-link" href="#main-content">Skip to main content</a>
  <header class="site-header">
    <div class="header-inner">
      <p class="brand">METABO-DIET</p>
      <p class="mode">Harmonizing dietary and exercise phenotypes with metabolomics</p>
    </div>
  </header>
  <div class="page-shell">
    """ + course_nav() + """
    <main id="main-content" tabindex="-1">
      """ + main_html + """
    </main>
  </div>
  <footer class="site-footer">
    <div class="footer-inner">
      <p>Metabo-Diet release 1.0 | Public Metabolomics Workbench case studies ST001521 and ST003348</p>
      <p>Scientific boundary: no cross-study pooling of uncalibrated quantitative values.</p>
    </div>
  </footer>
  <script src="assets/course.js"></script>
  """ + extra_scripts + """
</body>
</html>
"""


def build_index() -> str:
    activities = [
        ("pretest", "pretest.html", "Pretest"),
        *[(lesson_id, lesson_id + ".html", title) for lesson_id, title, _ in LESSONS],
        ("posttest", "posttest.html", "Posttest"),
    ]
    items = []
    for activity_id, href, title in activities:
        items.append(
            '<li><a href="' + href + '">' + html.escape(title)
            + '<span class="activity-state" data-activity-state="' + activity_id
            + '">Not complete</span></a></li>'
        )
    resource_links = []
    resource_dir = PACKAGE / "downloads"
    if (resource_dir / "metabo_diet_learner_guide.pdf").exists():
        resource_links.append('<li><a href="downloads/metabo_diet_learner_guide.pdf">Learner guide PDF</a></li>')
    if (resource_dir / "metabo_diet_templates.zip").exists():
        resource_links.append('<li><a href="downloads/metabo_diet_templates.zip">Editable learner worksheets and checklists</a></li>')
    if (resource_dir / "metabo_diet_analysis_bundle.zip").exists():
        resource_links.append('<li><a href="downloads/metabo_diet_analysis_bundle.zip">Runnable cached analysis bundle (Python notebook, pipeline, data, figures, and R appendix)</a></li>')
    main = """
<section class="hero">
  <p>Intermediate asynchronous module | Approximately 153 minutes</p>
  <h1>Metabo-Diet</h1>
  <p>Learn to compare study designs, preserve phenotype and specimen meaning, harmonize metabolite names with RefMet, analyze two public studies safely, and transfer the workflow across access tiers.</p>
</section>
<section aria-labelledby="pathway-heading">
  <h2 id="pathway-heading">Learning pathway</h2>
  <ol class="activity-list">""" + "\n".join(items) + """</ol>
</section>
<section class="callout" aria-labelledby="guardrail-heading">
  <h2 id="guardrail-heading">Scientific guardrail</h2>
  <p>The module performs quantitative exploration within each study. It does not pool uncalibrated values across ST001521 plasma and ST003348 serum or estimate a diet-versus-exercise causal effect.</p>
</section>
<section aria-labelledby="resources-heading">
  <h2 id="resources-heading">Learner resources</h2>
  <ul>""" + ("\n".join(resource_links) if resource_links else "<li>Resources are available from the course host.</li>") + """</ul>
</section>
<div class="actions">
  <a class="button" href="pretest.html">Begin with the pretest</a>
  <button class="secondary" id="reset-progress" type="button">Reset local progress</button>
</div>
"""
    return page_template("index", "Course home", main)


def build_lesson(lesson_id: str, title: str, source: Path, previous_href: str, next_href: str) -> str:
    content = markdown_to_html(source.read_text(encoding="utf-8"))
    main = """
<article>
""" + content + """
</article>
<div class="actions">
  <button type="button" data-complete-lesson aria-pressed="false">Mark lesson complete</button>
  <a class="button secondary" href=\"""" + previous_href + """\">Previous</a>
  <a class="button secondary" href=\"""" + next_href + """\">Next</a>
</div>
<p id="completion-notice" class="callout" tabindex="-1" aria-live="polite"></p>
"""
    return page_template(lesson_id, title, main)


def build_assessment(path: Path, page_id: str, next_href: str) -> str:
    payload = json.loads(path.read_text(encoding="utf-8"))
    public_payload = {
        "title": payload["title"],
        "instructions": payload["instructions"],
        "time_minutes": payload.get("time_minutes"),
        "items": payload["items"],
    }
    intro = (
        "<h1>" + html.escape(payload["title"]) + "</h1>"
        + "<p>" + html.escape(payload["instructions"]) + "</p>"
        + "<p><strong>Estimated time:</strong> " + str(payload.get("time_minutes", "")) + " minutes.</p>"
        + '<p class="callout">Answers and rationales remain hidden until you submit all items.</p>'
        + '<div id="assessment-root"></div>'
        + '<div class="actions"><a class="button secondary" href="' + next_href + '">Continue</a></div>'
        + '<script type="application/json" id="assessment-data">'
        + json.dumps(public_payload).replace("</", "<\\/")
        + "</script>"
    )
    return page_template(
        page_id,
        payload["title"],
        intro,
        '<script src="assets/assessment.js"></script>',
    )


def copy_resources() -> None:
    shutil.copy2(ROOT / "LICENSE", PACKAGE / "LICENSE")
    target = PACKAGE / "downloads"
    target.mkdir(parents=True, exist_ok=True)
    candidates = [
        MODULE / "support" / "metabo_diet_learner_guide.pdf",
        MODULE / "support" / "metabo_diet_templates.zip",
        MODULE / "support" / "metabo_diet_analysis_bundle.zip",
    ]
    for source in candidates:
        if source.exists():
            shutil.copy2(source, target / source.name)


def build_manifest() -> None:
    files = sorted(
        str(path.relative_to(PACKAGE)).replace("\\", "/")
        for path in PACKAGE.rglob("*")
        if path.is_file() and path.name != "imsmanifest.xml"
    )
    file_nodes = "\n".join('      <file href="' + html.escape(name, quote=True) + '"/>' for name in files)
    manifest = """<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="METABO_DIET_SCORM_1_2" version="1.0"
  xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
  xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1p2 imscp_rootv1p1p2.xsd http://www.adlnet.org/xsd/adlcp_rootv1p2 adlcp_rootv1p2.xsd">
  <metadata>
    <schema>ADL SCORM</schema>
    <schemaversion>1.2</schemaversion>
  </metadata>
  <organizations default="ORG_METABO_DIET">
    <organization identifier="ORG_METABO_DIET">
      <title>Metabo-Diet</title>
      <item identifier="ITEM_METABO_DIET" identifierref="RES_METABO_DIET">
        <title>Metabo-Diet: Harmonizing Dietary and Exercise Phenotypes</title>
        <adlcp:masteryscore>80</adlcp:masteryscore>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="RES_METABO_DIET" type="webcontent" adlcp:scormtype="sco" href="index.html">
""" + file_nodes + """
    </resource>
  </resources>
</manifest>
"""
    (PACKAGE / "imsmanifest.xml").write_text(manifest, encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_archive(zip_path: Path) -> dict:
    failures: list[str] = []
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
        name_set = set(names)
        if "imsmanifest.xml" not in name_set:
            failures.append("Root imsmanifest.xml is missing.")
            return {"passed": False, "failures": failures}
        if "index.html" not in name_set:
            failures.append("Root launch page index.html is missing.")
        crc_failure = archive.testzip()
        if crc_failure:
            failures.append("CRC failure: " + crc_failure)
        root = ET.fromstring(archive.read("imsmanifest.xml"))
        namespace = {"imscp": "http://www.imsproject.org/xsd/imscp_rootv1p1p2"}
        schema = root.find("imscp:metadata/imscp:schema", namespace)
        version = root.find("imscp:metadata/imscp:schemaversion", namespace)
        if schema is None or schema.text != "ADL SCORM":
            failures.append("Manifest schema is not ADL SCORM.")
        if version is None or version.text != "1.2":
            failures.append("Manifest schema version is not 1.2.")
        href_nodes = root.findall(".//imscp:file", namespace)
        hrefs = [node.attrib.get("href", "") for node in href_nodes]
        missing = sorted(href for href in hrefs if href not in name_set)
        if missing:
            failures.append("Manifest references missing files: " + ", ".join(missing))
        required_pages = {
            "LICENSE",
            "index.html",
            "pretest.html",
            "posttest.html",
            "lesson_01.html",
            "lesson_02.html",
            "lesson_03.html",
            "lesson_04.html",
            "lesson_05.html",
            "assets/course.css",
            "assets/course.js",
            "assets/assessment.js",
        }
        absent = sorted(required_pages - name_set)
        if absent:
            failures.append("Required course files missing: " + ", ".join(absent))
        required_downloads = {
            "downloads/metabo_diet_learner_guide.pdf",
            "downloads/metabo_diet_templates.zip",
            "downloads/metabo_diet_analysis_bundle.zip",
        }
        missing_downloads = sorted(required_downloads - name_set)
        if missing_downloads:
            failures.append("Required learner downloads missing: " + ", ".join(missing_downloads))
        course_js = archive.read("assets/course.js").decode("utf-8")
        required_calls = ["LMSInitialize", "LMSSetValue", "LMSCommit", "LMSFinish", "cmi.core.score.raw", "cmi.core.lesson_status"]
        missing_calls = [token for token in required_calls if token not in course_js]
        if missing_calls:
            failures.append("LMS calls missing: " + ", ".join(missing_calls))
        accessibility_checks = {}
        for page in sorted(required_pages):
            if not page.endswith(".html") or page not in name_set:
                continue
            text = archive.read(page).decode("utf-8")
            checks = {
                "lang": '<html lang="en">' in text,
                "skip_link": 'class="skip-link"' in text,
                "main": 'id="main-content"' in text,
                "title": "<title>" in text,
                "viewport": 'name="viewport"' in text,
            }
            accessibility_checks[page] = checks
            if not all(checks.values()):
                failures.append("Accessibility shell check failed: " + page)
        return {
            "passed": not failures,
            "failures": failures,
            "archive_file_count": len(names),
            "manifest_file_count": len(hrefs),
            "required_pages_present": not absent,
            "required_downloads_present": not missing_downloads,
            "crc_passed": crc_failure is None,
            "lms_calls_present": not missing_calls,
            "accessibility_shell_checks": accessibility_checks,
            "sha256": sha256(zip_path),
            "bytes": zip_path.stat().st_size,
        }


def main() -> None:
    if PACKAGE.exists():
        shutil.rmtree(PACKAGE)
    (PACKAGE / "assets").mkdir(parents=True)
    copy_resources()
    (PACKAGE / "assets" / "course.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    (PACKAGE / "assets" / "course.js").write_text(COURSE_JS.strip() + "\n", encoding="utf-8")
    (PACKAGE / "assets" / "assessment.js").write_text(ASSESSMENT_JS.strip() + "\n", encoding="utf-8")
    (PACKAGE / "index.html").write_text(build_index(), encoding="utf-8")
    (PACKAGE / "pretest.html").write_text(
        build_assessment(MODULE / "assessments" / "pretest.json", "pretest", "lesson_01.html"),
        encoding="utf-8",
    )
    (PACKAGE / "posttest.html").write_text(
        build_assessment(MODULE / "assessments" / "posttest.json", "posttest", "index.html"),
        encoding="utf-8",
    )
    for index, (lesson_id, title, source) in enumerate(LESSONS):
        previous_href = "pretest.html" if index == 0 else LESSONS[index - 1][0] + ".html"
        next_href = "posttest.html" if index == len(LESSONS) - 1 else LESSONS[index + 1][0] + ".html"
        (PACKAGE / (lesson_id + ".html")).write_text(
            build_lesson(lesson_id, title, source, previous_href, next_href),
            encoding="utf-8",
        )
    build_manifest()
    zip_path = SCORM / "metabo_diet_scorm_1_2.zip"
    SCORM.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(PACKAGE.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(PACKAGE))
    report = validate_archive(zip_path)
    QA.mkdir(parents=True, exist_ok=True)
    (QA / "scorm_validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    shutil.copy2(zip_path, DOWNLOADS / zip_path.name)
    print(json.dumps(report, indent=2))
    if not report["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
