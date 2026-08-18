export type KnowledgeCheck = {
  question: string;
  choices: string[];
  correctIndex: number;
  rationale: string;
};

export type Lesson = {
  id: string;
  number: string;
  title: string;
  time: string;
  bloom: string;
  summary: string;
  objectives: string[];
  sections: Array<{
    heading: string;
    paragraphs?: string[];
    bullets?: string[];
    callout?: { label: string; text: string };
  }>;
  activity: { title: string; steps: string[]; artifact: string };
  check: KnowledgeCheck;
};

export const lessons: Lesson[] = [
  {
    id: "why-harmonize",
    number: "01",
    title: "Why phenotype-to-metabolome harmonization matters",
    time: "20 min",
    bloom: "Remember · Understand",
    summary:
      "Start with the scientific question, then distinguish biological signal from study context and access constraints.",
    objectives: [
      "Explain why phenotype and provenance belong beside metabolite values.",
      "Recognize open, mixed/restricted, and controlled-access data paths.",
      "State the limits of a cross-study comparison before running one.",
    ],
    sections: [
      {
        heading: "A metabolite value is not context-free",
        paragraphs: [
          "Diet, exercise, fasting state, specimen processing, collection time, and analytical platform can all shape an observed metabolomics profile. Harmonization begins by preserving those differences, not by hiding them behind a shared column name.",
          "In this module, two public Metabolomics Workbench studies provide a practical contrast. They are compared to expose design and metadata decisions; they are never treated as one randomized experiment.",
        ],
        callout: {
          label: "Boundary",
          text: "Run PCA separately within each study. Compare those patterns only after checking specimen, platform, timing, and preprocessing; do not stack uncalibrated peak-area matrices.",
        },
      },
      {
        heading: "Three questions to ask first",
        bullets: [
          "Are the specimens, timepoints, and units meaningfully comparable?",
          "Can reported metabolite names be mapped with defensible confidence?",
          "Does the resource's access tier permit the planned retrieval, analysis, and export workflow?",
        ],
      },
    ],
    activity: {
      title: "Set your comparison boundary",
      steps: [
        "Write one question the paired studies can help you explore.",
        "Write one causal claim the paired studies cannot support.",
        "Record the evidence you would need before making that stronger claim.",
      ],
      artifact: "Pre-test and comparison-boundary note",
    },
    check: {
      question: "Why does this module run PCA separately within each study?",
      choices: [
        "Separate PCA proves the interventions caused different metabolic states.",
        "The raw matrices differ in specimen, platform, timing, and study context, so stacking them would confound biological and technical structure.",
        "Separate PCA makes sample metadata unnecessary.",
      ],
      correctIndex: 1,
      rationale:
        "Within-study PCA preserves each analysis context. Its patterns still require metadata-aware interpretation and do not establish causality.",
    },
  },
  {
    id: "compare-design",
    number: "02",
    title: "Compare study design and phenotype capture",
    time: "30 min",
    bloom: "Understand · Analyze",
    summary:
      "Read two MW records as study designs: intervention, specimens, timepoints, covariates, and provenance.",
    objectives: [
      "Extract intervention, specimen, timepoint, and phenotype structure from MW metadata.",
      "Classify fields as directly, partially, or not comparable.",
      "Explain how large consortia collect more detailed phenotype data.",
    ],
    sections: [
      {
        heading: "Compare meaning before labels",
        paragraphs: [
          "Two fields named ‘timepoint’ may encode very different physiology. A post-meal sample and an immediate post-exercise sample are both post-intervention, but the interventions, kinetics, and reference states differ.",
        ],
        bullets: [
          "Intervention: exposure, dose, duration, and comparator",
          "Specimen: matrix, collection protocol, processing, and storage",
          "Time: visit, clock time, fasting/fed state, acute response, and recovery",
          "Phenotype: clinical, dietary, exercise, and behavioral covariates",
          "Provenance: source field, transformation, version, and reviewer decision",
        ],
      },
      {
        heading: "Comparability is a decision with a reason",
        callout: {
          label: "Decision rule",
          text: "Directly comparable means the fields share construct, units, and relevant context. Partially comparable means a documented transformation or caveat is required. Not comparable means merging would erase a material difference.",
        },
      },
    ],
    activity: {
      title: "Complete the study-comparison matrix",
      steps: [
        "Read the study and analysis metadata for both accessions.",
        "Populate intervention, specimen, timepoint, platform, and phenotype rows.",
        "Assign a comparability class and one-sentence justification to each row.",
      ],
      artifact: "Cohort-comparison worksheet",
    },
    check: {
      question: "Two fields both say ‘post’, but one is 30 minutes after a meal and one is immediately after exercise. How should they be classified?",
      choices: ["Directly comparable", "Partially comparable with explicit semantics", "Identical after renaming"],
      correctIndex: 1,
      rationale:
        "A shared label does not create a shared physiological meaning. Preserve the event and elapsed-time semantics.",
    },
  },
  {
    id: "harmonize",
    number: "03",
    title: "Harmonize metabolites and metadata",
    time: "35 min",
    bloom: "Apply",
    summary:
      "Use RefMet as a common naming reference while keeping unresolved mappings and field-level decisions visible.",
    objectives: [
      "Describe how mwTab organizes study, subject, factor, and analysis metadata.",
      "Map reported metabolite names to standardized identifiers with confidence labels.",
      "Create an auditable crosswalk without forcing ambiguous mappings.",
    ],
    sections: [
      {
        heading: "Identifiers solve different problems",
        paragraphs: [
          "Reported names, RefMet names, HMDB accessions, KEGG identifiers, PubChem CIDs, and InChIKeys are related but not interchangeable. A good crosswalk records the source string, chosen standardized identity, mapping method, evidence, confidence, and reviewer decision.",
        ],
      },
      {
        heading: "Flag ambiguity instead of manufacturing precision",
        bullets: [
          "Keep unmapped features in the audit table.",
          "Separate exact identifier matches from synonym or text-normalization matches.",
          "Do not collapse positional isomers unless the analytical evidence supports it.",
          "Record units and transformation history beside values.",
          "Version every external mapping source.",
        ],
        callout: {
          label: "Human review",
          text: "An unresolved mapping is a valid result. It protects downstream analysis from a false identity claim.",
        },
      },
    ],
    activity: {
      title: "Build the crosswalk",
      steps: [
        "Load the reported metabolite names from both studies.",
        "Apply the documented mapping hierarchy.",
        "Review low-confidence and one-to-many matches.",
        "Assign each mapping an accepted, review-required, or unresolved status and record the reason.",
      ],
      artifact: "Metabolite and metadata crosswalk",
    },
    check: {
      question: "A reported name maps to two plausible positional isomers with no distinguishing evidence. What should the crosswalk record?",
      choices: [
        "Choose the first RefMet result.",
        "Average the two identities.",
        "Retain the reported name and flag the standardized identity as unresolved or requiring review.",
      ],
      correctIndex: 2,
      rationale:
        "The assay evidence does not support a unique identity, so a forced mapping would add false precision.",
    },
  },
  {
    id: "analyze",
    number: "04",
    title: "Run the guided analysis",
    time: "40 min",
    bloom: "Apply · Analyze · Evaluate",
    summary:
      "Retrieve or load cached MW data, apply the crosswalk, quantify overlap, inspect PCA, and summarize metabolite classes.",
    objectives: [
      "Retrieve study data through the MW/NMDR API with a cached fallback.",
      "Build analysis-ready matrices without erasing study provenance.",
      "Interpret exploratory results within design and platform limits.",
    ],
    sections: [
      {
        heading: "A reproducible analysis path",
        bullets: [
          "Read accessions and paths from one configuration cell.",
          "Validate schemas and sample identifiers before transformation.",
          "Keep source-specific matrices and provenance columns.",
          "Normalize only within a declared analytical purpose.",
          "Run PCA within one study and analysis at a time; compare patterns descriptively only after reviewing technical context.",
        ],
      },
      {
        heading: "Review what is missing or incompatible",
        paragraphs: [
          "The non-overlapping metabolites, missing covariates, incompatible timepoints, and unresolved identifiers are part of the result. They define what the comparison cannot answer and where additional evidence is needed.",
        ],
      },
    ],
    activity: {
      title: "Complete the Python notebook",
      steps: [
        "Run the validated cached path; optionally enable live retrieval and verify its source log.",
        "Inspect validation summaries and mapping-status counts.",
        "Quantify RefMet overlap and generate both within-study PCA diagnostics.",
        "Write a three-sentence interpretation separating observation, possible explanations, and limits.",
      ],
      artifact: "Executed notebook and interpretation note",
    },
    check: {
      question: "Which notebook output should be reviewed before interpreting either within-study PCA?",
      choices: [
        "Only the explained-variance percentages",
        "Schema checks, sample roles, factor metadata, missingness, feature filtering, units, and analysis identity",
        "Only the figure colors",
      ],
      correctIndex: 1,
      rationale:
        "Interpretation depends on the provenance and quality checks that establish which samples and features entered each separate PCA.",
    },
  },
  {
    id: "transfer",
    number: "05",
    title: "Assess access tiers and transfer the workflow",
    time: "15 min",
    bloom: "Evaluate · Create",
    summary:
      "Decide what changes when a new resource is open, mixed/restricted, or controlled—and redesign the workflow accordingly.",
    objectives: [
      "Verify access at the dataset level rather than assuming one tier for an entire resource.",
      "Identify which parts of the workflow can move to a gated environment.",
      "Create a transfer plan for a resource of interest.",
    ],
    sections: [
      {
        heading: "Access tier changes architecture",
        bullets: [
          "Open: retrieval and local caching may be permitted; verify licenses and release status.",
          "Mixed or restricted: public and restricted datasets may coexist; check each dataset's terms and authentication requirements.",
          "Controlled: analysis may have to remain inside an approved cloud workspace, with limits on export and derived results.",
        ],
        callout: {
          label: "Current-state rule",
          text: "Access statements age quickly. Record the exact dataset, policy page, verification date, and permitted actions.",
        },
      },
      {
        heading: "Transfer the reasoning, not necessarily the files",
        paragraphs: [
          "The crosswalk schema, validation logic, and interpretation framework can often transfer even when raw data cannot leave a controlled environment. Rebuild retrieval, storage, and export steps around the destination's rules.",
        ],
      },
    ],
    activity: {
      title: "Create a transfer plan",
      steps: [
        "Choose a metabolomics or cohort resource.",
        "Verify its access tier and permitted actions from current documentation.",
        "Map its identifiers, metadata, compute environment, and export constraints.",
        "Name one step you can reuse and one step you must redesign.",
      ],
      artifact: "Access-tier and transfer checklist",
    },
    check: {
      question: "What is the first step when adapting the workflow to a new consortium resource?",
      choices: [
        "Download everything available.",
        "Assume the resource has one access tier.",
        "Verify the specific dataset's current access, terms, environment, and export constraints.",
      ],
      correctIndex: 2,
      rationale:
        "Resource-level labels can hide rules that apply to individual datasets. Verify the exact dataset and intended action first.",
    },
  },
];
