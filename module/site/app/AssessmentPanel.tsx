"use client";

import { useMemo, useState } from "react";

type AssessmentItem = {
  id: string;
  objective_ids: string[];
  prompt: string;
  options: Record<string, string>;
  answer: string;
  rationale: string;
};

export type Assessment = {
  title: string;
  time_minutes: number;
  instructions: string;
  scoring: { maximum_points: number; suggested_mastery_threshold?: number };
  items: AssessmentItem[];
};

export function AssessmentPanel({
  assessment,
  kind,
  onBack,
  onComplete,
}: {
  assessment: Assessment;
  kind: "pretest" | "posttest";
  onBack: () => void;
  onComplete: (score: number, maximum: number) => void;
}) {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);
  const answered = Object.keys(answers).length;
  const score = useMemo(
    () => assessment.items.filter((item) => answers[item.id] === item.answer).length,
    [answers, assessment.items],
  );

  function submit() {
    if (answered !== assessment.items.length) return;
    setSubmitted(true);
    onComplete(score, assessment.scoring.maximum_points);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function reset() {
    setAnswers({});
    setSubmitted(false);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  const threshold = assessment.scoring.suggested_mastery_threshold;

  return (
    <article className="assessment-page">
      <button type="button" className="text-button" onClick={onBack}>← Return to lessons</button>
      <div className="assessment-heading">
        <span className="eyebrow">{kind === "pretest" ? "Before Lesson 1" : "After Lesson 5 and the notebook"}</span>
        <h2>{assessment.title}</h2>
        <p>{assessment.instructions}</p>
        <div className="assessment-meta">
          <span>{assessment.time_minutes} minutes</span>
          <span>{assessment.items.length} questions</span>
          <span>{answered} answered</span>
        </div>
      </div>

      {submitted && (
        <div className={threshold && score < threshold ? "score-card review" : "score-card"} role="status">
          <span>Your score</span>
          <strong>{score} / {assessment.scoring.maximum_points}</strong>
          <p>
            {kind === "pretest"
              ? "Use this as a baseline. Review the objective tags below and compare with your posttest result."
              : threshold && score >= threshold
                ? `Mastery threshold met (${threshold}/${assessment.scoring.maximum_points}).`
                : `Review the feedback by objective, then retry. Suggested mastery is ${threshold}/${assessment.scoring.maximum_points}.`}
          </p>
        </div>
      )}

      <form onSubmit={(event) => { event.preventDefault(); submit(); }}>
        <ol className="assessment-list">
          {assessment.items.map((item, index) => {
            const isCorrect = answers[item.id] === item.answer;
            return (
              <li key={item.id} className="assessment-item">
                <fieldset>
                  <legend><span>{index + 1}.</span> {item.prompt}</legend>
                  <p className="objective-tags">{item.objective_ids.join(" · ")}</p>
                  <div className="assessment-options">
                    {Object.entries(item.options).map(([key, value]) => (
                      <label key={key} className={answers[item.id] === key ? "assessment-option selected" : "assessment-option"}>
                        <input
                          type="radio"
                          name={item.id}
                          value={key}
                          checked={answers[item.id] === key}
                          disabled={submitted}
                          onChange={() => setAnswers((current) => ({ ...current, [item.id]: key }))}
                        />
                        <span className="option-key">{key}</span>
                        <span>{value}</span>
                      </label>
                    ))}
                  </div>
                </fieldset>
                {submitted && (
                  <div className={isCorrect ? "item-feedback correct" : "item-feedback review"}>
                    <strong>{isCorrect ? "Correct." : `Correct answer: ${item.answer}.`}</strong> {item.rationale}
                  </div>
                )}
              </li>
            );
          })}
        </ol>
        <div className="assessment-actions">
          {!submitted ? (
            <button type="submit" className="complete-button" disabled={answered !== assessment.items.length}>
              {answered === assessment.items.length ? "Submit assessment" : `Answer ${assessment.items.length - answered} more`}
            </button>
          ) : (
            <button type="button" className="secondary-button" onClick={reset}>Retry assessment</button>
          )}
        </div>
      </form>
    </article>
  );
}
