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
