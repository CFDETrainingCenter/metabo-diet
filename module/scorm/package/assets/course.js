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
