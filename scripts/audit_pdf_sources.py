"""Audit local PDF sources for reproducible methodological review.

This script checks whether project PDFs can be read reliably before they are
used as evidence in Phase 4B. It extracts only compact audit metadata and term
counts by default. It does not train models, modify competition data, generate
submissions, or perform a literature review.

Optional: pass --save-text to write extracted text to references/extracted_text/
for later local inspection.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path.cwd()
REFERENCE_DIRS = (
    PROJECT_ROOT / "references" / "books",
    PROJECT_ROOT / "references" / "papers",
    PROJECT_ROOT / "references" / "course_materials",
)
DOCS_DIR = PROJECT_ROOT / "docs"
RESEARCH_DOCS_DIR = DOCS_DIR / "04_research"
AUDIT_PATH = RESEARCH_DOCS_DIR / "pdf_review_audit.md"
FINDINGS_PATH = RESEARCH_DOCS_DIR / "pdf_key_findings.md"
EXTRACTED_TEXT_DIR = PROJECT_ROOT / "references" / "extracted_text"

MIN_NON_EMPTY_PAGE_CHARS = 20
TABLE_SAMPLE_MAX_PAGES = 25
TOP_RELEVANT_PAGE_COUNT = 5


KEY_TERM_PATTERNS: dict[str, tuple[str, ...]] = {
    "validation": ("validation", "cross-validation", "cross validation", "cv"),
    "roc_auc": ("roc-auc", "roc auc", "auc"),
    "leakage": ("leakage", "data leakage"),
    "missing_data": ("missing data", "missing values", "missing value", "missingness"),
    "categorical_encoding": ("categorical encoding", "one-hot", "one hot", "ordinal encoding"),
    "target_encoding": ("target encoding", "mean encoding"),
    "feature_selection": ("feature selection", "variable selection"),
    "feature_engineering": ("feature engineering", "feature extraction"),
    "overfitting": ("overfitting", "over-fitting", "model selection", "selection bias"),
    "xgboost": ("xgboost",),
    "lightgbm": ("lightgbm",),
    "catboost": ("catboost",),
    "optuna": ("optuna",),
    "tabular_data": ("tabular data", "tabular datasets", "tabular"),
    "leaderboard": ("leaderboard", "public leaderboard", "private leaderboard"),
    "hpo": ("hyperparameter", "hpo", "optimization", "optimisation"),
    "reproducibility": ("reproducibility", "reproducible", "replication"),
}

DECISION_CATEGORIES: dict[str, tuple[str, ...]] = {
    "validation": ("validation", "roc_auc", "leaderboard"),
    "leakage": ("leakage",),
    "feature engineering": (
        "feature_engineering",
        "feature_selection",
        "missing_data",
        "categorical_encoding",
        "target_encoding",
    ),
    "tabular models": ("tabular_data", "xgboost", "lightgbm", "catboost"),
    "HPO": ("hpo", "optuna", "overfitting"),
    "reproducibility": ("reproducibility",),
}


@dataclass(frozen=True)
class ExtractionResult:
    page_count: int
    page_texts: list[str]
    extractor: str
    errors: list[str]


def import_pymupdf_module():
    try:
        import pymupdf  # type: ignore

        return pymupdf, "pymupdf"
    except Exception as pymupdf_error:
        try:
            import fitz  # type: ignore

            return fitz, "fitz"
        except Exception as fitz_error:
            raise ImportError(
                f"Could not import pymupdf ({pymupdf_error!r}) or fitz ({fitz_error!r})."
            ) from fitz_error


def discover_pdfs() -> list[Path]:
    pdfs: list[Path] = []
    for directory in REFERENCE_DIRS:
        if directory.exists():
            pdfs.extend(directory.rglob("*.pdf"))
    return sorted(path for path in pdfs if path.is_file())


def relative_path(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def folder_group(path: Path) -> str:
    rel_parts = path.relative_to(PROJECT_ROOT).parts
    if len(rel_parts) >= 2:
        return "/".join(rel_parts[:2])
    return "Not confirmed yet"


def extract_with_pymupdf(path: Path) -> ExtractionResult:
    errors: list[str] = []
    pymupdf, module_name = import_pymupdf_module()
    try:
        with pymupdf.open(path) as document:
            page_texts = []
            for page in document:
                try:
                    page_texts.append(page.get_text("text") or "")
                except Exception as page_error:
                    page_texts.append("")
                    errors.append(f"{module_name} page extraction error: {page_error!r}")
            return ExtractionResult(
                page_count=len(document),
                page_texts=page_texts,
                extractor=module_name,
                errors=errors,
            )
    except Exception as exc:
        return ExtractionResult(page_count=0, page_texts=[], extractor=module_name, errors=[repr(exc)])


def extract_with_pypdf(path: Path) -> ExtractionResult:
    errors: list[str] = []
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        page_texts = []
        for page in reader.pages:
            try:
                page_texts.append(page.extract_text() or "")
            except Exception as page_error:
                page_texts.append("")
                errors.append(f"pypdf page extraction error: {page_error!r}")
        return ExtractionResult(
            page_count=len(reader.pages),
            page_texts=page_texts,
            extractor="pypdf",
            errors=errors,
        )
    except Exception as exc:
        return ExtractionResult(page_count=0, page_texts=[], extractor="pypdf", errors=[repr(exc)])


def summarize_text(page_texts: list[str]) -> tuple[int, float, int, float]:
    page_count = len(page_texts)
    text_chars_total = sum(len(text) for text in page_texts)
    avg_chars_per_page = text_chars_total / page_count if page_count else 0.0
    non_empty_pages = sum(1 for text in page_texts if len(text.strip()) >= MIN_NON_EMPTY_PAGE_CHARS)
    non_empty_pages_ratio = non_empty_pages / page_count if page_count else 0.0
    return text_chars_total, avg_chars_per_page, non_empty_pages, non_empty_pages_ratio


def needs_fallback(result: ExtractionResult) -> bool:
    text_chars_total, avg_chars_per_page, _, non_empty_pages_ratio = summarize_text(result.page_texts)
    return (
        not result.page_texts
        or text_chars_total < 200
        or avg_chars_per_page < 20
        or non_empty_pages_ratio < 0.10
    )


def choose_extraction(path: Path) -> tuple[ExtractionResult, bool, list[str]]:
    primary = extract_with_pymupdf(path)
    errors = [f"{primary.extractor}: {error}" for error in primary.errors]
    if not needs_fallback(primary):
        return primary, False, errors

    fallback = extract_with_pypdf(path)
    errors.extend(f"{fallback.extractor}: {error}" for error in fallback.errors)

    primary_chars = summarize_text(primary.page_texts)[0]
    fallback_chars = summarize_text(fallback.page_texts)[0]
    if fallback.page_texts and fallback_chars >= primary_chars:
        return fallback, True, errors
    return primary, True, errors


def detect_tables(path: Path, page_count: int, readable: bool) -> tuple[bool, int, str]:
    if not readable or page_count <= 0:
        return False, 0, "not_attempted"

    try:
        import pdfplumber
    except Exception as exc:
        return False, 0, f"pdfplumber import failed: {exc!r}"

    sample_pages = sorted(set(range(min(page_count, TABLE_SAMPLE_MAX_PAGES))))
    tables_found = 0
    try:
        with pdfplumber.open(path) as pdf:
            for page_index in sample_pages:
                try:
                    tables_found += len(pdf.pages[page_index].find_tables())
                except Exception:
                    continue
        return True, tables_found, f"sampled_pages={len(sample_pages)}"
    except Exception as exc:
        return True, 0, f"pdfplumber error: {exc!r}"


def compile_patterns() -> dict[str, list[re.Pattern[str]]]:
    compiled: dict[str, list[re.Pattern[str]]] = {}
    for canonical, variants in KEY_TERM_PATTERNS.items():
        compiled[canonical] = [
            re.compile(r"(?<![A-Za-z0-9_])" + re.escape(variant) + r"(?![A-Za-z0-9_])", re.IGNORECASE)
            for variant in variants
        ]
    return compiled


def count_terms(page_texts: list[str]) -> tuple[Counter[str], dict[int, Counter[str]]]:
    patterns = compile_patterns()
    total_counts: Counter[str] = Counter()
    page_counts: dict[int, Counter[str]] = {}
    for page_number, text in enumerate(page_texts, start=1):
        counts: Counter[str] = Counter()
        for canonical, regexes in patterns.items():
            count = sum(len(regex.findall(text)) for regex in regexes)
            if count:
                counts[canonical] += count
                total_counts[canonical] += count
        if counts:
            page_counts[page_number] = counts
    return total_counts, page_counts


def format_key_terms(counts: Counter[str]) -> str:
    if not counts:
        return ""
    return "; ".join(f"{term}={counts[term]}" for term in sorted(counts))


def format_top_pages(page_counts: dict[int, Counter[str]]) -> str:
    ranked = sorted(
        page_counts.items(),
        key=lambda item: (-sum(item[1].values()), item[0]),
    )[:TOP_RELEVANT_PAGE_COUNT]
    pieces = []
    for page_number, counts in ranked:
        term_summary = "; ".join(f"{term}={counts[term]}" for term in sorted(counts))
        pieces.append(f"{page_number}:{term_summary}")
    return " | ".join(pieces)


def classify_pdf(
    extraction_failed: bool,
    text_chars_total: int,
    avg_chars_per_page: float,
    non_empty_pages_ratio: float,
) -> tuple[str, bool]:
    if extraction_failed:
        return "Extraction failed", False
    if text_chars_total < 200 or avg_chars_per_page < 20 or non_empty_pages_ratio < 0.10:
        return "OCR needed", True
    if avg_chars_per_page >= 500 and non_empty_pages_ratio >= 0.70:
        return "Reviewed", False
    if (100 <= avg_chars_per_page < 500) or (0.30 <= non_empty_pages_ratio < 0.70):
        return "Partially readable", False
    return "Partially readable", False


def decision_supported(counts: Counter[str]) -> str:
    supported = []
    for decision, term_names in DECISION_CATEGORIES.items():
        if any(counts.get(term_name, 0) > 0 for term_name in term_names):
            supported.append(decision)
    return "; ".join(supported)


def markdown_escape(value: object) -> str:
    text = str(value)
    text = text.replace("\n", " ").replace("\r", " ")
    return text.replace("|", "\\|")


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(markdown_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join([header, separator, *body])


def save_text(path: Path, page_texts: list[str]) -> None:
    EXTRACTED_TEXT_DIR.mkdir(parents=True, exist_ok=True)
    output_name = path.relative_to(PROJECT_ROOT / "references").as_posix().replace("/", "__")
    output_path = EXTRACTED_TEXT_DIR / f"{output_name}.txt"
    output_path.write_text("\n\n".join(page_texts), encoding="utf-8")


def audit_pdf(path: Path, save_text_enabled: bool) -> dict[str, object]:
    extraction, fallback_used, errors = choose_extraction(path)
    text_chars_total, avg_chars_per_page, non_empty_pages, non_empty_pages_ratio = summarize_text(
        extraction.page_texts
    )
    extraction_failed = not extraction.page_texts and bool(errors)
    review_status, ocr_needed = classify_pdf(
        extraction_failed,
        text_chars_total,
        avg_chars_per_page,
        non_empty_pages_ratio,
    )
    if review_status == "Partially readable" and not (
        (100 <= avg_chars_per_page < 500) or (0.30 <= non_empty_pages_ratio < 0.70)
    ):
        errors.append(
            "classification note: extracted text did not meet Reviewed thresholds; treated as Partially readable"
        )
    readable = review_status in {"Reviewed", "Partially readable"}
    table_attempted, table_count, table_note = detect_tables(path, extraction.page_count, readable)
    term_counts, page_term_counts = count_terms(extraction.page_texts)

    if save_text_enabled and extraction.page_texts:
        save_text(path, extraction.page_texts)

    table_detail = f"{table_attempted}"
    if table_attempted:
        table_detail = f"True; tables_found_in_sample={table_count}; {table_note}"

    return {
        "file_name": path.name,
        "path": relative_path(path),
        "folder_group": folder_group(path),
        "page_count": extraction.page_count,
        "text_chars_total": text_chars_total,
        "avg_chars_per_page": round(avg_chars_per_page, 2),
        "non_empty_pages": non_empty_pages,
        "non_empty_pages_ratio": round(non_empty_pages_ratio, 4),
        "primary_extractor": extraction.extractor,
        "fallback_used": fallback_used,
        "table_detection_attempted": table_detail,
        "key_terms_found": format_key_terms(term_counts),
        "top_relevant_pages": format_top_pages(page_term_counts),
        "review_status": review_status,
        "ocr_needed": ocr_needed,
        "extraction_errors": "; ".join(errors),
        "decision_supported": decision_supported(term_counts),
    }


def summarize_by_status(rows: list[dict[str, object]]) -> Counter[str]:
    return Counter(str(row["review_status"]) for row in rows)


def top_rows_for_decision(rows: list[dict[str, object]], decision: str, limit: int = 8) -> list[dict[str, object]]:
    related_terms = DECISION_CATEGORIES[decision]

    def score(row: dict[str, object]) -> tuple[int, int, str]:
        counts = parse_key_terms(str(row["key_terms_found"]))
        term_score = sum(counts.get(term, 0) for term in related_terms)
        total_score = sum(counts.values())
        return (-term_score, -total_score, str(row["path"]))

    candidates = []
    for row in rows:
        counts = parse_key_terms(str(row["key_terms_found"]))
        if any(counts.get(term, 0) > 0 for term in related_terms):
            candidates.append(row)
    return sorted(candidates, key=score)[:limit]


def parse_key_terms(summary: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    if not summary:
        return counts
    for piece in summary.split("; "):
        if "=" not in piece:
            continue
        term, raw_count = piece.rsplit("=", 1)
        try:
            counts[term] = int(raw_count)
        except ValueError:
            continue
    return counts


def write_audit_markdown(rows: list[dict[str, object]]) -> None:
    RESEARCH_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    columns = [
        "file_name",
        "path",
        "folder_group",
        "page_count",
        "text_chars_total",
        "avg_chars_per_page",
        "non_empty_pages",
        "non_empty_pages_ratio",
        "primary_extractor",
        "fallback_used",
        "table_detection_attempted",
        "key_terms_found",
        "top_relevant_pages",
        "review_status",
        "ocr_needed",
        "extraction_errors",
        "decision_supported",
    ]
    status_counts = summarize_by_status(rows)
    content = [
        "# PDF Review Audit",
        "",
        "Purpose: reproducibly verify local PDF readability before Phase 4B methodological review.",
        "",
        "This audit does not train models, modify data, generate submissions, or perform a literature review.",
        "",
        "## Summary",
        "",
        f"- PDFs detected: {len(rows)}",
        f"- Reviewed: {status_counts.get('Reviewed', 0)}",
        f"- Partially readable: {status_counts.get('Partially readable', 0)}",
        f"- OCR needed: {status_counts.get('OCR needed', 0)}",
        f"- Extraction failed: {status_counts.get('Extraction failed', 0)}",
        "",
        "## Audit Table",
        "",
        markdown_table(rows, columns),
        "",
    ]
    AUDIT_PATH.write_text("\n".join(content), encoding="utf-8")


def rows_for_status(rows: list[dict[str, object]], status: str) -> list[dict[str, object]]:
    return [row for row in rows if row["review_status"] == status]


def compact_pdf_list(rows: Iterable[dict[str, object]], limit: int | None = None) -> list[str]:
    selected = list(rows)
    if limit is not None:
        selected = selected[:limit]
    if not selected:
        return ["- None"]
    return [
        f"- `{row['path']}` - {row['review_status']}; decisions: {row['decision_supported'] or 'Not confirmed yet'}"
        for row in selected
    ]


def write_key_findings_markdown(rows: list[dict[str, object]]) -> None:
    reviewed = rows_for_status(rows, "Reviewed")
    partial = rows_for_status(rows, "Partially readable")
    ocr_needed = rows_for_status(rows, "OCR needed")
    failed = rows_for_status(rows, "Extraction failed")

    content = [
        "# PDF Key Findings",
        "",
        "Purpose: summarize PDF readability and preliminary methodological relevance for Phase 4B.",
        "",
        "This is not a literature review. It only identifies which PDFs are readable enough to support later review.",
        "",
        "## PDFs legibles y útiles para Phase 4B",
        "",
        *compact_pdf_list(reviewed),
        "",
        "## PDFs parcialmente legibles",
        "",
        *compact_pdf_list(partial),
        "",
        "## PDFs que requieren OCR",
        "",
        *compact_pdf_list(ocr_needed),
        "",
        "## PDFs con extracción fallida",
        "",
        *compact_pdf_list(failed),
        "",
        "## Mayor evidencia preliminar por tema",
        "",
    ]

    for decision in sorted(DECISION_CATEGORIES):
        content.extend(
            [
                f"### {decision}",
                "",
                *compact_pdf_list(top_rows_for_decision(rows, decision, limit=8), limit=8),
                "",
            ]
        )

    status_counts = summarize_by_status(rows)
    limitations = [
        f"- PDFs detected: {len(rows)}",
        f"- Reviewed: {status_counts.get('Reviewed', 0)}",
        f"- Partially readable: {status_counts.get('Partially readable', 0)}",
        f"- OCR needed: {status_counts.get('OCR needed', 0)}",
        f"- Extraction failed: {status_counts.get('Extraction failed', 0)}",
        "- Table detection is exploratory and sampled; it does not extract or preserve full tables.",
        "- Key-term counts indicate likely relevance, not methodological conclusions.",
        "- Full extracted text is not saved unless the script is run with --save-text.",
    ]
    if ocr_needed:
        limitations.append("- Some PDFs may require OCR before they can support reliable Phase 4B evidence.")
    if failed:
        limitations.append("- Some PDFs failed extraction and should not be used as evidence until repaired or replaced.")

    content.extend(["## Riesgos o limitaciones de extracción", "", *limitations, ""])
    FINDINGS_PATH.write_text("\n".join(content), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit local PDF sources for reproducible review.")
    parser.add_argument(
        "--save-text",
        action="store_true",
        help="Save extracted text under references/extracted_text/. Disabled by default.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pdfs = discover_pdfs()
    rows = [audit_pdf(path, save_text_enabled=args.save_text) for path in pdfs]
    rows = sorted(rows, key=lambda row: str(row["path"]))
    write_audit_markdown(rows)
    write_key_findings_markdown(rows)

    counts = summarize_by_status(rows)
    print(f"PDFs detected: {len(rows)}")
    print(f"Reviewed: {counts.get('Reviewed', 0)}")
    print(f"Partially readable: {counts.get('Partially readable', 0)}")
    print(f"OCR needed: {counts.get('OCR needed', 0)}")
    print(f"Extraction failed: {counts.get('Extraction failed', 0)}")
    print(f"Wrote: {relative_path(AUDIT_PATH)}")
    print(f"Wrote: {relative_path(FINDINGS_PATH)}")


if __name__ == "__main__":
    main()
