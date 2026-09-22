# IEEE DataPort Submission Package

## 1. Dataset title

AgeTechRegional: Regional dataset for healthy ageing, mobility, falls, and functional well-being in older adults

## 2. Dataset summary

AgeTechRegional is a reproducible, locally curated, and methodologically conservative regional dataset for research on healthy ageing, mobility, functional status, assistive technology needs, and fall risk in older adult populations. The dataset integrates locally available evidence from two major sources:

- SABE Colombia 2015
- MHAS / ENASEM Wave 7 2024

The project is intentionally designed to preserve data provenance and avoid unsupported semantic harmonization. It does not force equivalence between variables when the underlying definitions differ across surveys. Instead, it records source-specific windows, comparability status, evidence, and exclusions so the data remain transparent and scientifically defensible.

This dataset is aligned with the themes of healthy longevity, AgeTech, functional independence, mobility, care support, and older adult well-being. It is suitable for descriptive epidemiology, comparative analysis, feature preparation, and reproducible research workflows that prioritize transparency over aggressive imputation or forced standardization.

## 3. Motivation and use case

Population ageing is one of the most important demographic and public health challenges in Latin America and globally. Understanding how older adults experience mobility decline, fall risk, assistive device use, sensory limitations, cognition, and health-related functioning is essential for AgeTech innovation, digital health, and inclusive intervention design.

The dataset was constructed to support:

- comparative analysis of older adult health in Latin American and cross-regional settings;
- evaluation of mobility, falls, functionality, and assistive needs;
- feature engineering for AI and machine learning workflows;
- public health and AgeTech research with clear provenance and reproducibility;
- transparent documentation of source-specific time windows and comparability.

## 4. Scope and constraints

This package is a first-phase regional data assembly rather than a complete ETL platform or a predictive model repository. The goal is to build a high-quality, traceable analytic dataset that is honest about what can and cannot be compared across sources.

Included characteristics:

- evidence-based cataloging of variables;
- explicit time windows by source;
- separation between source-preserved tables and harmonized output;
- conservative harmonization rules;
- leakage checks and deterministic train/test partitioning;
- reproducible run manifests and quality reports.

Excluded characteristics:

- no remote download or external data acquisition;
- no OMOP conversion or forced international harmonization;
- no ETL beyond local, documented dataset preparation;
- no predictive models in this phase;
- no unsupported equivalence across surveys.

## 5. Data sources

### 5.1 SABE Colombia 2015

SABE (Salud, Bienestar y Envejecimiento) is a nationally relevant longitudinal and cross-sectional ageing survey in Colombia. In this package, it is used as a source for older adult health, mobility, functional capacity, and contextual variables with explicit documentation where relevant.

### 5.2 MHAS / ENASEM Wave 7 2024

The MHAS / ENASEM dataset provides a parallel older adult health and ageing perspective. It is integrated with explicit awareness that its temporal windows, question wording, and coding may not be equivalent to SABE.

## 6. Geographic and temporal coverage

- Countries represented: Colombia, Mexico-related MHAS/ENASEM regional alignment
- Population focus: adults older than working age, with emphasis on ageing, functional ability, falls, mobility, and care needs
- Temporal coverage: source-specific, with explicit windows preserved in the downstream harmonized table
- Primary use: comparative descriptive and analytic exploration rather than forced cross-survey causal inference

## 7. Data structure

The submission package contains the following outputs:

- `outputs/agetech_regional/source/sabe_2015/dataset.parquet`
- `outputs/agetech_regional/source/mhas_2024/dataset.parquet`
- `outputs/agetech_regional/harmonized/regional.parquet`
- `outputs/agetech_regional/all_sources.parquet`
- `outputs/agetech_regional/partitions.parquet`
- `outputs/agetech_regional/catalog/variable_catalog.csv`
- `outputs/agetech_regional/catalog/evidence_rules.csv`
- `outputs/agetech_regional/quality/coverage.csv`
- `outputs/agetech_regional/quality/exclusions.csv`
- `outputs/agetech_regional/quality/leakage_check.json`
- `outputs/agetech_regional/quality/report.json`
- `outputs/agetech_regional/run_manifest.json`

The harmonized table is organized in long format, with each row representing one observation of a specific canonical variable for a given source record.

## 8. Key variables and domains

The dataset features canonical domains such as:

- age
- sex
- ADL and functional status
- mobility limitation
- assistive device use
- falls and fall windows
- vision and hearing
- cognition
- comorbidities
- anthropometry
- context-related variables

Important note: some variables are marked as comparable and others as non-comparable across surveys. Variables marked as non-comparable are preserved as such rather than being coerced into a single, uncertain interpretation.

## 9. Data quality and governance

The package includes a documented quality control framework:

- provenance tracking by row and source file;
- missing-code handling;
- direct identifier exclusion;
- coverage statistics;
- exclusion reporting;
- leakage assessment;
- deterministic split assignment;
- reproducible run metadata.

The project explicitly tracks where variables may be influenced by temporal wording differences, source definitions, or survey instrument differences. This is a critical feature for trustworthy scientific use.

## 10. Ethics, privacy, and compliance

This project uses locally stored, non-publically sourced data and is designed to respect strict provenance and privacy boundaries. No public or unauthorized source is used for data acquisition or redistribution.

The implementation includes:

- no unsupported external linking;
- no direct identifiers in the analytic outputs;
- explicit exclusion of sensitive or non-analytic variables;
- full source traceability for quality auditing;
- no publishing of hidden or unreviewed raw identifiers.

Before any external publication or public release, the dataset owner should verify local ethics approvals, consent conditions, institutional policies, and any restrictions applicable to the original survey sources.

## 11. Reproducibility and execution

The project is fully executable from the repository and produces deterministic outputs when run against the configured local staging and manifests.

To reproduce the pipeline:

```powershell
cd AGE-TECH-Competencia
pip install -r requirements.txt
$env:PYTHONPATH="."
python -m AgeTechRegional.cli --config AgeTechRegional\config.local.json
```

To explore the outputs interactively:

```powershell
cd AGE-TECH-Competencia
streamlit run app.py
```

## 12. Data dictionary and provenance

The project includes:

- `evidence_catalog.json`: canonical variable definitions and domains
- `catalog/variable_catalog.csv`: discovered variables and evidence metadata
- `catalog/evidence_rules.csv`: patterns, evidence status, and comparability logic
- `run_manifest.json`: config and provenance of the run

This makes it possible to audit the full lifecycle of the dataset from input to final harmonized output.

## 13. Intended research applications

This dataset is intended for:

- AgeTech and healthy ageing analyses
- mobility and fall-risk descriptive studies
- functional capacity and frailty-related comparisons
- assistive technology and independence research
- AI-ready feature preparation with transparent provenance
- public-health and demographic research on older adults

## 14. Limitations

The dataset is intentionally conservative. It is not a fully standardized, international OMOP layer, nor a complete longitudinal panel. Instead, it prioritizes transparency and evidence-based comparability.

Key limitations include:

- source-specific temporal windows not uniformly aligned;
- some variables remain non-comparable by design;
- not all variables are observed in every source;
- the package is a Phase 1 regional data assembly, not a final multi-country harmonization system.

## 15. Citation recommendation

If used in a research context, an appropriate citation can be structured as:

AgeTechRegional. Regional dataset for healthy ageing, mobility, falls, and functional well-being in older adults. Local reproducible research package, 2026.

## 16. Licensing and availability

This project is distributed as a local research package with explicit provenance and documentation. Before public distribution or submission to external repositories, confirm the licensing conditions for all source datasets and any institutional restrictions.

## 17. Submission-ready overview

This package is appropriate for a competition or data-sharing context because it provides:

- domain relevance to AgeTech and healthy ageing;
- source traceability and quality reporting;
- explicit handling of temporal and semantic differences;
- reproducible processing steps;
- transparent documentation of comparability and exclusions;
- a dataset that can be responsibly reused for analytic work.

It is especially well positioned as a high-integrity regional data asset for older adult health and mobility research, rather than a low-transparency, broad, non-documented public-health dump.

## 18. Final note

The package reflects a careful balance between utility and methodological honesty. In AgeTech and health-data contexts, transparency about what is comparable, what is not, and how the data were processed is often as important as the dataset itself. This project is designed around that principle.
