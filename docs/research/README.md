# Research report

**User Requirements Prioritization Based on Crisp and Fuzzy Approaches**  
Viktor Fedorov · Research term project · Software Engineering, Higher School of Economics

- [Read the full English report on GitHub](requirements-prioritization.en.md)
- [Open the original English PDF](requirements-prioritization.en.pdf)
- [Run the software and the reproducible demo](../../README.md)

## Research focus

The project studies how requirements can be ranked when stakeholder judgments differ and the inputs contain uncertainty. It implements and compares established crisp, interval, and fuzzy approaches through worked examples, then exposes the calculations through software.

The report covers:

- MoSCoW with stakeholder weights and variative category assessments.
- The Kano model with traditional and weighted aggregation.
- TOPSIS with crisp, interval, trapezoidal fuzzy, and intuitionistic ratings.
- Fuzzy Delphi Type-2 and intuitionistic approaches to expert uncertainty.
- Fuzzy AHP Type-1 and Type-2, including pairwise comparisons and consistency checks.
- A Python desktop application, CSV input formats, and PDF report generation.
- A later FastAPI/React web interface and an optional generative-AI interpretation layer.

The comparative examples explore how aggregation, stakeholder influence, and the treatment of uncertainty affect rankings. The report includes 41 tables and a 37-entry bibliography. The original document is a research term-project report; its worked examples and claims should be read in that academic context.

## Relationship to this repository

The original desktop implementation is retained in `prioritization_tool/`. The web application in `backend/` and `frontend/` exposes the method implementations through an API and a browser interface.

The [fintech onboarding case](../../examples/fintech-quarter/README.md) is a separate reproducible demonstration with authored synthetic data. It should be distinguished from the examples and results in the historical research report. The report's descriptions of UI behavior, AI model configuration, and implementation details reflect its source version; the root README describes how to run the current repository.

## Source and edition notes

The English PDF was recovered from `Report User Requirements Prioritization.pdf`. Its embedded creation timestamp is **27 May 2026**. It contains **63 pages**; its title page retains the original **2025** academic-project context.

The Markdown edition was assembled from the recovered English LaTeX parts dated **26–27 May 2026**, including the updated front matter, AI/web chapter, conclusion, bibliography, and software appendix. It adapts section navigation, multi-row table headings, equation formatting, and bibliography links for GitHub. The original PDF is included unchanged as the reference for pagination and typesetting.

Known editorial inconsistencies in the source are preserved:

- The abstract states 75 pages, while the PDF contains 63.
- Some introductory and web-chapter passages refer to eight methods or earlier section numbers; the final contents contain ten method-analysis sections followed by the web-application chapter.

These are historical source notes. The publication of this edition does not change the implementation, recalculate the examples, or introduce new experimental results.
