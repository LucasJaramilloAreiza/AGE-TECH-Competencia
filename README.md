# AgeTechRegional

<p align="center">
  <img src="https://img.shields.io/badge/Status-Reproducible%20pipeline-blue" alt="status" />
  <img src="https://img.shields.io/badge/Data-Official%20survey%20access-only-green" alt="access policy" />
  <img src="https://img.shields.io/badge/License-MIT-orange" alt="license" />
</p>

> **Quick Start (English)** — A local, reproducible, conservative pipeline for healthy ageing research based on SABE Colombia 2015 and MHAS/ENASEM 2024.
>
> ```powershell
> cd AGE-TECH-Competencia
> pip install -r requirements.txt
> $env:PYTHONPATH="."
> python -m AgeTechRegional.cli --config config.local.json
> ```
> Place authorized microdata in `staging/sabe/` and `staging/mhas/`. The pipeline writes results to `outputs/agetech_regional/`. **No raw data is redistributed by this repository.**

---

## Table of Contents

- [English Documentation](#english-documentation)
  - [1. Project Purpose and Data Policy](#1-project-purpose-and-data-policy)
  - [2. Scope and Principles](#2-scope-and-principles)
  - [3. Data Access Policy](#3-data-access-policy)
  - [4. Official Data Sources](#4-official-data-sources)
  - [5. Local Data Placement](#5-local-data-placement)
  - [6. Files Used and Files Excluded](#6-files-used-and-files-excluded)
  - [7. Project Structure](#7-project-structure)
  - [8. Reproduction Instructions](#8-reproduction-instructions)
  - [9. Recommended Publication Policy](#9-recommended-publication-policy)
  - [10. Observed Execution Results](#10-observed-execution-results)
  - [11. Limitations](#11-limitations)
  - [12. Closing Note](#12-closing-note)
- [Documentación en Español](#documentación-en-español)

---

# English Documentation

## 1. Project Purpose and Data Policy

**AgeTechRegional** is a local, reproducible, conservative pipeline for healthy ageing, mobility, falls, functional independence, assistive technology needs, and older-adult well-being. It uses authorized local extracts from **SABE Colombia 2015** and **MHAS / ENASEM 2024**.

Raw or restricted survey files are intentionally excluded from Git and are **never redistributed** by this repository. Researchers must download the official files through the providers' approved access procedures and place only the authorized inputs in local `staging/sabe/` and `staging/mhas/` directories.

The pipeline **preserves source semantics** instead of forcing equivalence. The evidence catalog combines historical regex discovery rules with exact source-aware mappings. Exact mappings match both the source and raw column name and emit the provenance fields:

- `evidence_reference`
- `description`
- `mapping_type`
- `raw_variable`
- `traceability_id`

…together with source-specific `time_window` and `comparable` flags.

The expanded MHAS crosswalk covers age, sex, self-rated health, hypertension, diabetes, falls, vision, hearing, memory, mobility/function, assistive devices, ADL, IADL, and care indicators. SABE mappings are intentionally conservative and limited to codes supported by the repository documentation.

---

## 2. Scope and Principles

**Included:**

- Local parquet staging files
- Local manifests
- Evidence catalog and mapping rules
- Quality and provenance artifacts
- Deterministic train/test partitions

**Not included / not relied upon:**

- Automatic download of external data
- Unauthorized authentication or access
- ELSI or other external services
- Large-scale ETL or OMOP conversion
- Forced equivalence across non-equivalent time windows

---

## 3. Data Access Policy

To analyze the data and build the regional dataset, each researcher must obtain the microdata through the **official access procedures** for each study.

This repository does **not** redistribute the raw data and does **not** require users to upload it to GitHub. Researchers must download the authorized files and place them in the correct local location.

---

## 4. Official Data Sources

### SABE Colombia 2015

Official microdata and survey access page:

> https://enlinea.minsalud.gov.co/Encuestas/Microdatos.aspx?E=SABE2015

<img width="1916" height="984" alt="SABE access portal" src="https://github.com/user-attachments/assets/62c92da3-2280-44e1-989c-1948314b20ce" />

### MHAS / ENASEM 2024

Official MHAS data products page:

> https://www.mhasweb.org/DataProducts/CoreSurveyData.aspx

Each researcher must follow the approved access or application procedure required by the data provider.

---

## 5. Local Data Placement

The project configuration already points to paths inside the repository itself. To work as intended, download the official data and place it inside the same project folder in these exact locations:

```text
AGE-TECH-Competencia/
├── staging/
│   ├── sabe/
│   │   └── <authorized SABE 2015 microdata files>
│   └── mhas/
│       └── <authorized MHAS / ENASEM microdata files>
├── results/
│   ├── manifest_sabe.json
│   └── manifest_mhas.json
├── README.md
├── ...
└── AgeTechRegional/
```

### Example layout

```text
AGE-TECH-Competencia/
├── staging/
│   ├── sabe/
│   │   ├── Base de datos y diccionario/
│   │   │   ├── Base de datos - Capitulos/
│   │   │   │   ├── Biom.txt
│   │   │   │   ├── Cap1Ident.txt
│   │   │   │   ├── Cap1Parte1.txt
│   │   │   │   ├── Cap1Parte2.txt
│   │   │   │   ├── Cap2.txt
│   │   │   │   ├── Cap2Hijos.txt
│   │   │   │   ├── Cap2PersCerc.txt
│   │   │   │   ├── Cap2PersVivHog.txt
│   │   │   │   ├── Cap3.txt
│   │   │   │   ├── Cap4.txt
│   │   │   │   ├── Cap5.txt
│   │   │   │   ├── Cap6.txt
│   │   │   │   ├── Cap7.txt
│   │   │   │   ├── Cap8.txt
│   │   │   │   ├── Cap8EnfNoTrans.txt
│   │   │   │   ├── Cap8Med.txt
│   │   │   │   ├── Cap9.txt
│   │   │   │   ├── Cap10.txt
│   │   │   │   ├── Cap11.txt
│   │   │   │   └── Cap12.TXT
│   │   │   ├── Base de datos Cuidadores/
│   │   │   │   ├── BASE_CF_20072019publicar.xlsx
│   │   │   │   └── DICCIONARIO_CF_20072019.xlsx
│   │   │   └── Diccionario de datos SABE.xlsx
│   │   └── ...
│   └── mhas/
│       ├── sect_trh_follow_up_2024.dta
│       ├── sect_trh_new_sample_2024.dta
│       ├── sect_a_c_d_e_pc_f_h_i_2024.dta
│       └── ...
└── results/
    ├── manifest_sabe.json
    └── manifest_mhas.json
```

### Important notes

- `staging/sabe/` should contain **only** the authorized SABE 2015 microdata files relevant to the study.
- `staging/mhas/` should contain **only** the files needed for the core survey and required sections.
- `results/` should contain the manifests needed for validation and pipeline traceability.
- The pipeline recursively reads pipe-delimited `.txt`, `.dta`, and `.parquet` files.
- **RAW DATA MUST NOT be stored in the public repository.**
- **Not all** files from the survey package are used — only the microdata relevant to the canonical variables.

---

## 6. Files Used and Files Excluded

### SABE 2015

Only the authorized data files relevant to the study should be used. Relevant variables include:

- Age
- Sex
- ADL and functional status
- Mobility
- Falls
- Assistive devices
- Vision / hearing
- Cognition
- Comorbidities
- Anthropometry
- Context

**Not included** in the public repository and should not be redistributed:

- PDF methodological documents
- Publication appendices
- Promotional files
- Non-essential dictionaries
- Unneeded survey files
- Any data not authorized for redistribution

### MHAS / ENASEM 2024

Only the relevant authorized files and sections should be imported. For example:

- `sect_trh_follow_up_2024`
- `sect_trh_new_sample_2024`
- `sect_a_c_d_e_pc_f_h_i_2024`

<img width="1891" height="700" alt="MHAS files" src="https://github.com/user-attachments/assets/3414053f-5f2b-475a-9822-99d7f66d81fe" />

The full auxiliary package or unrelated documentation should **not** be published or stored in this repository.

### Manifests (`results/`)

- `manifest_sabe.json`
- `manifest_mhas.json`

These files describe the source mapping, validation status, and execution traceability for the pipeline.

---

## 7. Project Structure

```text
AGE-TECH-Competencia/
├── README.md
├── __init__.py
├── app.py
├── catalog.py
├── cli.py
├── config.py
├── config.example.json
├── config.local.json
├── evidence_catalog.json
├── pipeline.py
├── requirements.txt
├── tests/
│   └── test_pipeline.py
├── outputs/
│   └── <generated locally by the run>
└── ...
```

The `outputs/` folder is generated locally after running the pipeline. It is not included in the public repository version.

---

## 8. Reproduction Instructions

```powershell
cd AGE-TECH-Competencia
pip install -r requirements.txt
$env:PYTHONPATH="."
python -m AgeTechRegional.cli --config config.local.json
```

The pipeline expects the researcher to have already placed the authorized files in `staging/`. Manifests do not need to exist beforehand — the pipeline automatically creates or updates `results/manifest_sabe.json` and `results/manifest_mhas.json`.

The command reads `.parquet`, `.dta`, and recursively discovered pipe-delimited `.txt` files. It writes generated artifacts under `outputs/agetech_regional/`:

```text
outputs/agetech_regional/
├── source/sabe_2015/dataset.parquet
├── source/mhas_2024/dataset.parquet
├── all_sources.parquet
├── harmonized/regional.parquet
├── catalog/variable_catalog.csv
├── catalog/evidence_rules.csv
├── quality/coverage.csv
├── quality/exclusions.csv
├── quality/leakage_check.json
├── quality/report.json
├── partitions.parquet
└── run_manifest.json
```

Manifests record input file names, sizes, hashes, source metadata, and configured time windows. Reproducibility requires the same authorized source extracts, catalog version, configuration, and dependency environment.

---

## 9. Recommended Publication Policy

If the project is uploaded to a public repository, the recommended approach is:

- Include only code, metadata, documentation, and reproducibility logic.
- Exclude raw microdata.
- Clearly document the sources and access procedures.
- Instruct users how to obtain the official files before running the pipeline.

This is the recommended practice when redistribution rights are not explicitly granted.

---

## 10. Observed Execution Results

The validated run produced:

| Measure | Observed result |
| --- | ---: |
| Source-preserving rows | 68,478 |
| Harmonized observations | 703,803 |
| Discovered variables | 40 |
| Quality records | 40 |
| Leakage check | passed |

The harmonized count is expected to exceed the source-row count: the source-preserving tables retain one row per input record, while the harmonized table is long format. Each non-missing evidence-backed variable in each source record becomes a separate observation, retaining its source, file, row number, raw variable, canonical variable, and provenance metadata.

The run policy explicitly records that:

- Staging was **not modified**.
- Direct identifiers were **not modeled**.
- **No cross-source linkage** was performed.
- `falls_12m` and `falls_24m` remain **separate canonical variables**; their 12-month and 24-month windows are not collapsed or treated as interchangeable.

### Age and sex comparability

Age and sex are conceptually comparable but retain source-specific coding. Health, falls, sensory, cognition, function, care, and assistive-device items remain **non-comparable** unless explicitly documented otherwise. SABE mappings are deliberately narrow because the official dictionary may not be present in every worktree; additional SABE fields must **not** be added from naming similarity alone.

---

## 11. Limitations

This package does **not** perform:

- Clinical validation
- Imputation
- OMOP conversion
- Causal inference
- International linkage

This project is a regional analytical and quality base — **not** a final clinical solution nor a trained predictive model. Interpretation of falls, mobility, and functionality must be done with the specific time window of each source.

---

## 12. Closing Note

This repository is intentionally designed as a reproducible, transparent, and legally cautious research package. It supports open science without violating data-access constraints. The actual microdata remain under official control and must be obtained separately by the researcher in accordance with the terms of the data providers.

**AgeTechRegional** represents a solid foundation for an AgeTech competition project because it combines:

- Real, locally verified sources
- Documentary evidence for each variable
- Quality and leakage checks
- Conservative harmonization
- Reproducible and traceable output

It is a useful infrastructure for serious analysis and for building a competitive case study without relying on unsupported semantic assumptions.

---
---

# Documentación en Español

## Aviso importante sobre datos y redistribución

Este repositorio **NO** incluye microdatos crudos ni archivos de encuesta redistribuibles. El proyecto se publica como un pipeline de reproducibilidad, catálogo de evidencia y documentación metodológica, pero no contiene las bases originales de SABE 2015 ni MHAS/ENASEM 2024.

La razón es estrictamente metodológica y legal: cuando no existe permiso explícito de redistribución de microdatos, la práctica recomendada es publicar únicamente:

- Código de limpieza y armonización
- Reglas de evidencia y catálogo de variables
- Metadatos, manifiestos y trazabilidad
- Documentación metodológica
- Instrucciones para que cada investigador obtenga los datos oficiales en la fuente autorizada

Esto mantiene la integridad del proyecto y evita una redistribución no autorizada de microdatos protegidos.

---

## 1. Objetivo

**AgeTechRegional** es un pipeline local, reproducible y conservador para construir una base analítica regional orientada a envejecimiento saludable, movilidad, fragilidad, caídas y bienestar funcional en adultos mayores.

El proyecto toma como base dos fuentes oficiales de investigación:

- SABE Colombia 2015
- MHAS / ENASEM Wave 7 2024

La intención no es transformar los datos para forzar equivalencias artificiales. La estrategia es **conservar la semántica de cada fuente**, registrar la evidencia local y mantener una salida analítica transparentemente conservadora.

---

## 2. Principios y alcance

El proyecto trabaja con:

- Parquet en staging local
- Manifests locales
- Catálogo de evidencia y reglas de mapeo
- Archivos de calidad y trazabilidad
- Particiones deterministas para train/test

**No se usa:**

- Descarga automática de fuentes externas
- Autenticación o acceso no autorizado
- ELSI o servicios externos
- ETL masivo o OMOP
- Conversiones forzadas de ventanas temporales no equivalentes

---

## 3. Política de acceso a los datos

Para poder analizar y construir la base regional, cada investigador debe obtener los microdatos de forma oficial en las páginas de acceso autorizado de cada estudio.

Este repositorio **no redistribuye** esos archivos y **no exige** que se suban a GitHub. El investigador debe descargarlos y colocarlos en el entorno local bajo la estructura correcta.

---

## 4. Fuentes autorizadas para obtener los datos

### SABE Colombia 2015

Portal oficial de microdatos de salud y encuestas del Ministerio de Salud de Colombia:

> https://enlinea.minsalud.gov.co/Encuestas/Microdatos.aspx?E=SABE2015

<img width="1916" height="984" alt="Portal SABE" src="https://github.com/user-attachments/assets/a7093342-374f-47f8-aceb-3bfb4d218bf8" />

### MHAS / ENASEM 2024

Portal oficial del proyecto MHAS para datos de encuesta y productos de datos:

> https://www.mhasweb.org/DataProducts/CoreSurveyData.aspx

Cada investigador debe seguir el procedimiento de acceso institucional o de solicitud oficial indicado por la fuente, según corresponda.

---

## 5. Dónde poner los datos localmente

La configuración del proyecto ya está apuntando a rutas dentro del mismo repositorio. Para que funcione tal cual, debes descargar los datos y colocarlos dentro de esta misma carpeta del proyecto, en estas ubicaciones exactas:

```text
AGE-TECH-Competencia/
├── staging/
│   ├── sabe/
│   │   └── <microdatos SABE 2015 autorizados>
│   └── mhas/
│       └── <microdatos MHAS / ENASEM autorizados>
├── results/
│   ├── manifest_sabe.json
│   └── manifest_mhas.json
├── README.md
├── ...
└── AgeTechRegional/
```

### Ejemplo real de uso

```text
AGE-TECH-Competencia/
├── staging/
│   ├── sabe/
│   │   ├── Base de datos y diccionario/
│   │   │   ├── Base de datos - Capitulos/
│   │   │   │   ├── Biom.txt
│   │   │   │   ├── Cap1Ident.txt
│   │   │   │   ├── Cap1Parte1.txt
│   │   │   │   ├── Cap1Parte2.txt
│   │   │   │   ├── Cap2.txt
│   │   │   │   ├── Cap2Hijos.txt
│   │   │   │   ├── Cap2PersCerc.txt
│   │   │   │   ├── Cap2PersVivHog.txt
│   │   │   │   ├── Cap3.txt
│   │   │   │   ├── Cap4.txt
│   │   │   │   ├── Cap5.txt
│   │   │   │   ├── Cap6.txt
│   │   │   │   ├── Cap7.txt
│   │   │   │   ├── Cap8.txt
│   │   │   │   ├── Cap8EnfNoTrans.txt
│   │   │   │   ├── Cap8Med.txt
│   │   │   │   ├── Cap9.txt
│   │   │   │   ├── Cap10.txt
│   │   │   │   ├── Cap11.txt
│   │   │   │   └── Cap12.TXT
│   │   │   ├── Base de datos Cuidadores/
│   │   │   │   ├── BASE_CF_20072019publicar.xlsx
│   │   │   │   └── DICCIONARIO_CF_20072019.xlsx
│   │   │   └── Diccionario de datos SABE.xlsx
│   │   └── ...
│   └── mhas/
│       ├── sect_trh_follow_up_2024.dta
│       ├── sect_trh_new_sample_2024.dta
│       ├── sect_a_c_d_e_pc_f_h_i_2024.dta
│       └── ...
└── results/
    ├── manifest_sabe.json
    └── manifest_mhas.json
```

### Importante

- `staging/sabe/` debe contener **solo** los archivos relevantes del microdato SABE 2015 autorizados.
- `staging/mhas/` debe contener **solo** los archivos del core survey y secciones necesarias para el estudio.
- `results/` debe contener los manifests de validación y trazabilidad del pipeline.
- El pipeline lee recursivamente archivos `.txt` delimitados por `|`, `.dta` y `.parquet`.
- **NO** se suben los microdatos al repositorio.
- **NO** se usan todos los archivos del paquete de la encuesta; solo se usan las bases requeridas para el análisis.

---

## 6. Archivos específicos que deben ir en cada carpeta

### SABE 2015 — `staging/sabe/`

En esta carpeta se espera la base de microdatos SABE 2015 y, si aplica, sus archivos auxiliares autorizados. Para esta fase del proyecto, no todos los archivos del paquete de SABE deben usarse; solo los necesarios para las variables objetivo del catálogo.

Los archivos clave de la descarga oficial son:

```text
AGE-TECH-Competencia/staging/sabe/
├── Base de datos y diccionario/
│   ├── Base de datos - Capitulos/
│   │   ├── Biom.txt
│   │   ├── Cap1Ident.txt
│   │   ├── Cap1Parte1.txt
│   │   ├── Cap1Parte2.txt
│   │   ├── Cap2.txt
│   │   ├── Cap2Hijos.txt
│   │   ├── Cap2PersCerc.txt
│   │   ├── Cap2PersVivHog.txt
│   │   ├── Cap3.txt
│   │   ├── Cap4.txt
│   │   ├── Cap5.txt
│   │   ├── Cap6.txt
│   │   ├── Cap7.txt
│   │   ├── Cap8.txt
│   │   ├── Cap8EnfNoTrans.txt
│   │   ├── Cap8Med.txt
│   │   ├── Cap9.txt
│   │   ├── Cap10.txt
│   │   ├── Cap11.txt
│   │   └── Cap12.TXT
│   ├── Base de datos Cuidadores/
│   │   ├── BASE_CF_20072019publicar.xlsx
│   │   └── DICCIONARIO_CF_20072019.xlsx
│   └── Diccionario de datos SABE.xlsx
```

La parte principal del estudio suele estar en `Base de datos - Capitulos/`.

### MHAS / ENASEM 2024 — `staging/mhas/`

Archivos típicos que suelen aparecer en esta carpeta:

- `sect_trh_follow_up_2024.dta`
- `sect_trh_new_sample_2024.dta`
- `sect_a_c_d_e_pc_f_h_i_2024.dta`
- `...`

Lo importante es que solo vayan los archivos de la base relevante para la armonización, no toda la documentación ni archivos auxiliares no usados.

### Manifests — `results/`

- `manifest_sabe.json`
- `manifest_mhas.json`

Estos archivos deben describir la validación del dataset, la fuente, el conjunto de filas y la trazabilidad del pipeline.

---

## 7. Qué archivos se usan y cuáles no

### SABE 2015

Se debe usar solo la parte autorizada de la base de microdatos y las variables que correspondan a:

- Edad
- Sexo
- Funcionalidad ADL
- Movilidad
- Caídas
- Ayudas técnicas
- Visión/audición
- Cognición
- Comorbilidades
- Antropometría
- Contexto

**No se usan, ni se publican, ni se almacenan en este repositorio:**

- Documentos PDF de metodología preliminar
- Anexos de publicación
- Materiales de difusión
- Diccionarios completos no necesarios para la fase analítica
- Archivos no usados por el pipeline
- Cualquier dato no autorizado para redistribución

### MHAS / ENASEM 2024

La base debe incluir solo los archivos y secciones requeridas para la harmonización del estudio. Como ejemplo, se pueden requerir archivos tipo:

- `sect_trh_follow_up_2024`
- `sect_trh_new_sample_2024`
- `sect_a_c_d_e_pc_f_h_i_2024`

<img width="1891" height="700" alt="Archivos MHAS" src="https://github.com/user-attachments/assets/4c4857a1-4ade-4485-8321-1fa001489194" />

Pero **no** se deben incluir ni publicar todos los archivos auxiliares o documentación general del proyecto en el repositorio.

---

## 8. Estructura lógica del proyecto

```text
AGE-TECH-Competencia/
├── README.md
├── __init__.py
├── app.py
├── catalog.py
├── cli.py
├── config.py
├── config.example.json
├── config.local.json
├── evidence_catalog.json
├── pipeline.py
├── requirements.txt
├── tests/
│   └── test_pipeline.py
├── outputs/
│   └── <generado localmente por la ejecución>
└── ...
```

La carpeta `outputs/` se genera localmente tras ejecutar el pipeline. No se incluye en la versión de repositorio pública si se desea compartir el proyecto sin microdatos.

---

## 9. Reproducción local

```powershell
cd AGE-TECH-Competencia
pip install -r requirements.txt
$env:PYTHONPATH="."
python -m AgeTechRegional.cli --config config.local.json
```

La ejecución espera que el investigador haya colocado previamente los archivos autorizados en `staging/`. Los manifests **no deben crearse manualmente**: el pipeline los genera o actualiza automáticamente en `results/manifest_sabe.json` y `results/manifest_mhas.json`.

---

## 10. Recomendación para envío o sharing

Si se va a subir a un repositorio público, la recomendación correcta es:

- Incluir solo código, metadatos, reglas, documentación y pipeline
- No subir los microdatos originales
- Documentar claramente dónde se obtienen los datos oficiales
- Mantener un README explícito que indique que la reproducción requiere acceso autorizado

---

## 11. Resultado actual

### Catálogo ampliado y crosswalk por fuente

El catálogo conserva las reglas regex históricas como descubrimiento de respaldo y añade `source_mappings` exactos en `evidence_catalog.json`. Estos mapeos requieren que coincidan la fuente y el nombre crudo, y agregan `evidence_reference`, `mapping_type`, `description`, `time_window` y `comparable` a cada observación de salida.

MHAS 2024 incluye edad, sexo, salud autopercibida, hipertensión, diabetes, caídas, visión, audición, memoria, dificultades de movilidad, ayudas técnicas, ADL, IADL e indicadores de cuidado (más de 20 columnas documentadas). SABE se limita a los códigos actualmente respaldados por la documentación local, incluyendo `P122EDAD` y `P121`.

Las caídas **no se colapsan**: `falls_12m` conserva una ventana de 12 meses y `falls_24m` una de 24 meses. Aunque edad y sexo están marcados como comparables a nivel conceptual, las respuestas, códigos y demás dominios permanecen source-specific hasta una revisión del diccionario oficial y de la redacción de cada instrumento.

### Ejecución validada

| Medida | Resultado observado |
| --- | ---: |
| Filas source-preserving | 68,478 |
| Observaciones armonizadas | 703,803 |
| Variables descubiertas | 40 |
| Registros de calidad | 40 |
| Leakage check | aprobado |

El número de observaciones armonizadas es mayor que el de filas source-preserving porque la salida armonizada está en **formato largo**: cada variable respaldada por evidencia y no faltante de cada fila de origen se convierte en una observación separada. Se conservan la fuente, archivo, número de fila, variable cruda, variable canónica y los campos de provenance `evidence_reference`, `description`, `mapping_type`, `raw_variable` y `traceability_id`.

La política de ejecución confirma que:

- No se modificó `staging`.
- No se modelaron identificadores directos.
- No se hizo linkage entre fuentes.
- `falls_12m` y `falls_24m` permanecen separadas con sus ventanas de 12 y 24 meses.

Los archivos crudos o restringidos se excluyen de Git: deben descargarse oficialmente y colocarse localmente en `staging/sabe/` y `staging/mhas/`.

La salida se genera en `outputs/agetech_regional/`, incluyendo las tablas source-preserving por fuente, `all_sources.parquet`, `harmonized/regional.parquet`, el catálogo de variables, reglas de evidencia, reportes de calidad, el leakage check, particiones y `run_manifest.json`.

---

## 12. Limitaciones

**No se hace:**

- Validación clínica
- Imputación
- Conversión OMOP
- Inferencia causal
- Linkage internacional

Las limitaciones siguen siendo explícitas: edad y sexo son comparables a nivel conceptual, pero conservan sus códigos de origen; salud, caídas, visión, audición, cognición, funcionalidad, cuidado y ayudas técnicas **no se fuerzan** como equivalentes. Los mapeos SABE son intencionalmente conservadores porque el diccionario oficial puede no estar disponible en cada worktree.

---

## 13. Conclusión

**AgeTechRegional** representa una base sólida para un proyecto de competencia AgeTech porque combina:

- Fuentes reales y verificadas localmente
- Evidencia documental para cada variable
- Calidad y leakage checks
- Armonización conservadora
- Salida reproducible y trazable

Es una infraestructura útil para análisis serio y para construir un caso de estudio competitivo sin caer en suposiciones semánticas no respaldadas.

El pipeline ya fue ejecutado y generó una salida válida en:

```text
AGE-TECH-Competencia/outputs/agetech_regional/
```

Con esto el proyecto queda listo para:

- Revisión humana
- Análisis descriptivo
- Preparación para modelado
- Documentación y presentación de la competencia

---

<p align="center"><em>Este proyecto es una base regional analítica y de calidad, no una solución clínica final ni un modelo predictivo entrenado.</em></p>
