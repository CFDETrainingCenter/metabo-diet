"use client";

import { useEffect, useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";
import pretest from "../public/assessments/pretest.json";
import posttest from "../public/assessments/posttest.json";
import { AssessmentPanel, type Assessment } from "./AssessmentPanel";
import { lessons } from "./course-data";
import { lessonMarkdown } from "./lesson-markdown";

const STORAGE_KEY = "metabo-diet-progress-v1";

type SavedProgress = {
  completed: string[];
  answers: Record<string, number>;
  scores?: Record<string, { score: number; maximum: number }>;
};

const emptyProgress: SavedProgress = { completed: [], answers: {} };

export function CourseApp() {
  const [activeId, setActiveId] = useState(lessons[0].id);
  const [progress, setProgress] = useState<SavedProgress>(emptyProgress);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    const restoreFrame = window.requestAnimationFrame(() => {
      try {
        const stored = window.localStorage.getItem(STORAGE_KEY);
        if (stored) setProgress(JSON.parse(stored) as SavedProgress);
      } catch {
        setProgress(emptyProgress);
      } finally {
        setHydrated(true);
      }
    });
    return () => window.cancelAnimationFrame(restoreFrame);
  }, []);

  useEffect(() => {
    if (hydrated) window.localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  }, [hydrated, progress]);

  const assessmentKind = activeId === "pretest" || activeId === "posttest" ? activeId : null;
  const lesson = lessons.find((item) => item.id === activeId) ?? lessons[0];
  const activeIndex = lessons.findIndex((item) => item.id === lesson.id);
  const percent = Math.round((progress.completed.length / lessons.length) * 100);
  const selectedAnswer = progress.answers[lesson.id];
  const answerSubmitted = selectedAnswer !== undefined;
  const answerCorrect = selectedAnswer === lesson.check.correctIndex;
  const completedSet = useMemo(() => new Set(progress.completed), [progress.completed]);

  function chooseAnswer(index: number) {
    setProgress((current) => ({
      ...current,
      answers: { ...current.answers, [lesson.id]: index },
    }));
  }

  function toggleComplete() {
    setProgress((current) => {
      const isComplete = current.completed.includes(lesson.id);
      return {
        ...current,
        completed: isComplete
          ? current.completed.filter((id) => id !== lesson.id)
          : [...current.completed, lesson.id],
      };
    });
  }

  function move(direction: -1 | 1) {
    const next = activeIndex + direction;
    if (next >= 0 && next < lessons.length) {
      setActiveId(lessons[next].id);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }

  return (
    <>
      <a className="skip-link" href="#lesson-content">Skip to lesson content</a>
      <header className="course-header">
        <a className="brand" href="#top" aria-label="Metabo-Diet course home">
          <span className="brand-mark" aria-hidden="true">MD</span>
          <span>
            <strong>Metabo-Diet</strong>
            <small>CFDE training module</small>
          </span>
        </a>
        <div className="header-progress" aria-label={`${percent}% of lessons complete`}>
          <span>{progress.completed.length} of {lessons.length} lessons</span>
          <div className="progress-track" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={percent}>
            <span style={{ width: `${percent}%` }} />
          </div>
        </div>
      </header>

      <div className="course-layout" id="top">
        <aside className="course-rail" aria-label="Course lessons">
          <div className="rail-intro">
            <span className="eyebrow">Intermediate · 2.5 hours</span>
            <h1>Harmonize phenotype metadata with public metabolomics data.</h1>
            <p>Compare two public Metabolomics Workbench studies with an auditable workflow that preserves their differences.</p>
          </div>
          <nav>
            <button
              type="button"
              className={activeId === "pretest" ? "assessment-link active" : "assessment-link"}
              onClick={() => setActiveId("pretest")}
            >
              <span>Start here</span>
              <strong>Pretest · 5 min</strong>
            </button>
            <ol className="lesson-list">
              {lessons.map((item) => (
                <li key={item.id}>
                  <button
                    type="button"
                    className={item.id === activeId ? "lesson-link active" : "lesson-link"}
                    aria-current={item.id === activeId ? "page" : undefined}
                    onClick={() => setActiveId(item.id)}
                  >
                    <span className="lesson-number">{item.number}</span>
                    <span className="lesson-label">
                      <strong>{item.title}</strong>
                      <small>{item.time}</small>
                    </span>
                    <span className={completedSet.has(item.id) ? "status-dot complete" : "status-dot"}>
                      <span className="sr-only">{completedSet.has(item.id) ? "Complete" : "Not complete"}</span>
                    </span>
                  </button>
                </li>
              ))}
            </ol>
            <button
              type="button"
              className={activeId === "posttest" ? "assessment-link post active" : "assessment-link post"}
              onClick={() => setActiveId("posttest")}
            >
              <span>Finish here</span>
              <strong>Posttest · 8 min</strong>
            </button>
          </nav>
          <div className="rail-downloads">
            <p className="eyebrow">Course files</p>
            <a href="/downloads/metabo_diet_analysis_bundle.zip" download>Runnable analysis bundle</a>
            <a href="/downloads/metabo_diet_learner_guide.pdf" download>Learner guide PDF</a>
            <a href="/downloads/metabo_diet_templates.zip" download>Worksheets + templates</a>
          </div>
        </aside>

        <main className="lesson-main" id="lesson-content" tabIndex={-1}>
          {assessmentKind ? (
            <AssessmentPanel
              assessment={(assessmentKind === "pretest" ? pretest : posttest) as Assessment}
              kind={assessmentKind}
              onBack={() => setActiveId(assessmentKind === "pretest" ? lessons[0].id : lessons[lessons.length - 1].id)}
              onComplete={(score, maximum) => setProgress((current) => ({
                ...current,
                scores: { ...current.scores, [assessmentKind]: { score, maximum } },
              }))}
            />
          ) : (
          <article>
            <div className="lesson-heading">
              <div>
                <span className="eyebrow">Lesson {lesson.number} · {lesson.bloom}</span>
                <h2>{lesson.title}</h2>
                <p className="dek">{lesson.summary}</p>
              </div>
              <div className="time-card" aria-label={`Estimated time ${lesson.time}`}>
                <span>Estimated time</span>
                <strong>{lesson.time}</strong>
              </div>
            </div>

            <section className="objective-card" aria-labelledby="objectives-heading">
              <p className="section-kicker" id="objectives-heading">By the end, you can</p>
              <ul>{lesson.objectives.map((objective) => <li key={objective}>{objective}</li>)}</ul>
            </section>

            {lesson.sections.map((section) => (
              <section className="content-section" key={section.heading}>
                <h3>{section.heading}</h3>
                {section.paragraphs?.map((paragraph) => <p key={paragraph}>{paragraph}</p>)}
                {section.bullets && <ul>{section.bullets.map((bullet) => <li key={bullet}>{bullet}</li>)}</ul>}
                {section.callout && (
                  <aside className="callout">
                    <strong>{section.callout.label}</strong>
                    <p>{section.callout.text}</p>
                  </aside>
                )}
              </section>
            ))}

            <section className="activity-card" aria-labelledby="activity-heading">
              <div>
                <span className="eyebrow">Hands-on activity</span>
                <h3 id="activity-heading">{lesson.activity.title}</h3>
              </div>
              <ol>{lesson.activity.steps.map((step) => <li key={step}>{step}</li>)}</ol>
              <p className="artifact"><strong>Takeaway:</strong> {lesson.activity.artifact}</p>
            </section>

            <details className="full-lesson" open>
              <summary>Complete lesson text, worked examples, and sources</summary>
              <div className="markdown-body">
                <ReactMarkdown
                  components={{
                    h1: ({ children }) => <p className="markdown-title">{children}</p>,
                    a: ({ children, href }) => <a href={href} target="_blank" rel="noreferrer">{children}</a>,
                    table: ({ children }) => <div className="table-scroll"><table>{children}</table></div>,
                  }}
                >
                  {lessonMarkdown[lesson.id]}
                </ReactMarkdown>
              </div>
            </details>

            <section className="knowledge-check" aria-labelledby="check-heading">
              <span className="eyebrow">Knowledge check</span>
              <h3 id="check-heading">{lesson.check.question}</h3>
              <div className="answer-list" role="radiogroup" aria-labelledby="check-heading">
                {lesson.check.choices.map((choice, index) => (
                  <button
                    type="button"
                    role="radio"
                    aria-checked={selectedAnswer === index}
                    className={selectedAnswer === index ? "answer selected" : "answer"}
                    onClick={() => chooseAnswer(index)}
                    key={choice}
                  >
                    <span>{String.fromCharCode(65 + index)}</span>
                    {choice}
                  </button>
                ))}
              </div>
              {answerSubmitted && (
                <div className={answerCorrect ? "feedback correct" : "feedback review"} role="status">
                  <strong>{answerCorrect ? "Correct." : "Review this one."}</strong> {lesson.check.rationale}
                </div>
              )}
            </section>

            <div className="lesson-actions">
              <button type="button" className="secondary-button" onClick={() => move(-1)} disabled={activeIndex === 0}>Previous lesson</button>
              <button type="button" className={completedSet.has(lesson.id) ? "complete-button done" : "complete-button"} onClick={toggleComplete}>
                {completedSet.has(lesson.id) ? "Marked complete" : "Mark lesson complete"}
              </button>
              <button type="button" className="secondary-button" onClick={() => move(1)} disabled={activeIndex === lessons.length - 1}>Next lesson</button>
            </div>
          </article>
          )}
          <footer className="course-footer">
            <p>
              Metabo-Diet · Public-data training with explicit provenance and interpretation limits. Original
              training materials are available under <a href="/downloads/LICENSE">CC BY 4.0</a>.
            </p>
          </footer>
        </main>
      </div>
    </>
  );
}
