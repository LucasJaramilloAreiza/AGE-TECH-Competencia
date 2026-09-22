# AgeTechRegional

<p align="center">
  <img src="https://img.shields.io/badge/Status-Reproducible%20pipeline-blue" alt="status" />
  <img src="https://img.shields.io/badge/Data-Official%20survey%20access-only-green" alt="access policy" />
  <img src="https://img.shields.io/badge/License-MIT-orange" alt="license" />
</p>

## Aviso importante sobre datos y redistribución

Este repositorio NO incluye microdatos crudos ni archivos de encuesta redistribuibles. El proyecto se publica como un pipeline de reproducibilidad, catálogo de evidencia y documentación metodológica, pero no contiene las bases originales de SABE 2015 ni MHAS/ENASEM 2024.

La razón es estrictamente metodológica y legal: cuando no existe permiso explícito de redistribución de microdatos, la práctica recomendada es publicar únicamente:

- código de limpieza y armonización;
- reglas de evidencia y catálogo de variables;
- metadatos, manifiestos y trazabilidad;
- documentación metodológica;
- instrucciones para que cada investigador obtenga los datos oficiales en la fuente autorizada.

Esto mantiene la integridad del proyecto y evita una redistribución no autorizada de microdatos protegidos.

## Versión en español

### 1. Objetivo

AgeTechRegional es un pipeline local, reproducible y conservador para construir una base analítica regional orientada a envejecimiento saludable, movilidad, fragilidad, caídas y bienestar funcional en adultos mayores.

El proyecto toma como base dos fuentes oficiales de investigación:

- SABE Colombia 2015
- MHAS / ENASEM Wave 7 2024

La intención no es transformar los datos para forzar equivalencias artificiales. La estrategia es conservar la semántica de cada fuente, registrar la evidencia local y mantener una salida analítica transparentemente conservadora.

### 2. Principios y alcance

El proyecto trabaja con:

- parquet en staging local;
- manifests locales;
- catálogo de evidencia y reglas de mapeo;
- archivos de calidad y trazabilidad;
- particiones deterministas para train/test.

No se usa:

- descarga automática de fuentes externas;
- autenticación o acceso no autorizado;
- ELSI o servicios externos;
- ETL masivo o OMOP;
- conversiones forzadas de ventanas temporales no equivalentes.

### 3. Política de acceso a los datos

Para poder analizar y construir la base regional, cada investigador debe obtener los microdatos de forma oficial en las páginas de acceso autorizado de cada estudio.

Este repositorio no redistribuye esos archivos y no exige que se suban a GitHub. El investigador debe descargarlos y colocarlos en el entorno local bajo la estructura correcta.

### 4. Fuentes autorizadas para obtener los datos

#### SABE Colombia 2015

Portal oficial de microdatos de salud y encuestas del Ministerio de Salud de Colombia:

https://enlinea.minsalud.gov.co/Encuestas/Microdatos.aspx?E=SABE2015

#### MHAS / ENASEM 2024

Portal oficial del proyecto MHAS para datos de encuesta y productos de datos:

https://www.mhasweb.org/DataProducts/CoreSurveyData.aspx

Cada investigador debe seguir el procedimiento de acceso institucional o de solicitud oficial indicado por la fuente, según corresponda.

### 5. Dónde poner los datos localmente

Una vez descargados, los archivos deben colocarse en una estructura local de trabajo, no dentro del repositorio público. La convención recomendada es la siguiente:

```text
<carpeta-de-trabajo-local>/
├── staging/
│   ├── sabe/
│   │   └── <microdatos SABE 2015 autorizados>
│   └── mhas/
│       └── <microdatos MHAS / ENASEM autorizados>
├── results/
│   ├── manifest_sabe.json
│   └── manifest_mhas.json
└── AGE-TECH-Competencia/
    └── <este repositorio>
```

Importante:

- `staging/sabe/` debe contener solo los archivos relevantes del microdato SABE 2015 autorizados.
- `staging/mhas/` debe contener solo los archivos del core survey y secciones necesarias para el estudio.
- `results/` debe contener los manifests de validación y trazabilidad del pipeline.
- NO se suben los microdatos al repositorio.
- NO se usan todos los archivos del paquete de la encuesta; solo se usan las bases requeridas para el análisis y los datos relevantes para las variables canónicas del catálogo.

### 6. Qué archivos se usan y cuáles no

#### SABE 2015

Se debe usar solo la parte autorizada de la base de microdatos y las variables que correspondan a:

- edad
- sexo
- funcionalidad ADL
- movilidad
- caídas
- ayudas técnicas
- visión/audición
- cognición
- comorbilidades
- antropometría
- contexto

No se usan, ni se publican, ni se almacenan en este repositorio:

- documentos pdf de metodología preliminar
- anexos de publicación
- materiales de difusión
- diccionarios completos no necesarios para la fase analítica
- archivos no usados por el pipeline
- cualquier dato no autorizado para redistribución

#### MHAS / ENASEM 2024

La base debe incluir solo los archivos y secciones requeridas para la harmonización del estudio. Como ejemplo, se pueden requerir archivos tipo:

- `sect_trh_follow_up_2024`
- `sect_trh_new_sample_2024`
- `sect_a_c_d_e_pc_f_h_i_2024`

Pero no se deben incluir ni publicar todos los archivos auxiliares o documentación general del proyecto en el repositorio.

### 7. Estructura lógica del proyecto

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

### 8. Reproducción local

```powershell
cd AGE-TECH-Competencia
pip install -r requirements.txt
$env:PYTHONPATH="."
python -m AgeTechRegional.cli --config AgeTechRegional\config.local.json
```

La ejecución espera que el investigador haya colocado previamente los archivos autorizados en `staging/` y que los manifests existan en `results/`.

### 9. Recomendación para envío o sharing

Si se va a subir a un repositorio público, la recomendación correcta es:

- incluir solo código, metadatos, reglas, documentación y pipeline;
- no subir los microdatos originales;
- documentar claramente dónde se obtienen los datos oficiales;
- mantener un README explícito que indique que la reproducción requiere acceso autorizado.

## English version

### 1. Objective

AgeTechRegional is a local, reproducible, and conservative pipeline designed to build a regional analytical dataset for healthy ageing, mobility, frailty, falls, and functional well-being among older adults.

The project is based on two official research sources:

- SABE Colombia 2015
- MHAS / ENASEM Wave 7 2024

The goal is not to force artificial comparability. The strategy is to preserve each source’s semantics, document local evidence, and produce a transparent and conservative analytical output.

### 2. Scope and principles

The project works with:

- local parquet staging files;
- local manifests;
- evidence catalog and mapping rules;
- quality and provenance artifacts;
- deterministic train/test partitions.

It does not rely on:

- automatic download of external data;
- unauthorized authentication or access;
- ELSI or other external services;
- large-scale ETL or OMOP conversion;
- forced equivalence across non-equivalent time windows.

### 3. Data access policy

To analyze the data and build the regional dataset, each researcher must obtain the microdata through the official access procedures for each study.

This repository does not redistribute the raw data and does not require users to upload it to GitHub. Researchers must download the authorized files and place them in the correct local location.

### 4. Official data sources

#### SABE Colombia 2015

Official microdata and survey access page:

https://enlinea.minsalud.gov.co/Encuestas/Microdatos.aspx?E=SABE2015

#### MHAS / ENASEM 2024

Official MHAS data products page:

https://www.mhasweb.org/DataProducts/CoreSurveyData.aspx

Each researcher must follow the approved access or application procedure required by the data provider.

### 5. Where to place the data locally

After download, the files should be placed in a local workspace outside the public repository. Recommended layout:

```text
<local-workspace>/
├── staging/
│   ├── sabe/
│   │   └── <authorized SABE 2015 microdata files>
│   └── mhas/
│       └── <authorized MHAS / ENASEM microdata files>
├── results/
│   ├── manifest_sabe.json
│   └── manifest_mhas.json
└── AGE-TECH-Competencia/
    └── <this repository>
```

Important:

- `staging/sabe/` should contain only the authorized SABE 2015 microdata files relevant to the study.
- `staging/mhas/` should contain only the files needed for the core survey and required sections.
- `results/` should contain the manifests needed for validation and pipeline traceability.
- RAW DATA MUST NOT be stored in the public repository.
- NOT all files from the survey package are used; only the microdata relevant to the study and the canonical variables of the project should be ingested.

### 6. Which files are used and which are not

#### SABE 2015

Only the authorized data files relevant to the study should be used. The relevant variables are those tied to:

- age
- sex
- ADL and functional status
- mobility
- falls
- assistive devices
- vision/hearing
- cognition
- comorbidities
- anthropometry
- context

The following are not included in the public repository and should not be redistributed:

- pdf methodological documents
- publication appendices
- promotional files
- non-essential dictionaries
- unneeded survey files
- any data not authorized for redistribution

#### MHAS / ENASEM 2024

Only the relevant authorized files and sections should be imported. For example, files such as:

- `sect_trh_follow_up_2024`
- `sect_trh_new_sample_2024`
- `sect_a_c_d_e_pc_f_h_i_2024`

may be required, but the full auxiliary package or unrelated documentation should not be published or stored in this repo.

### 7. Reproduction instructions

```powershell
cd AGE-TECH-Competencia
pip install -r requirements.txt
$env:PYTHONPATH="."
python -m AgeTechRegional.cli --config AgeTechRegional\config.local.json
```

The pipeline expects the researcher to have already placed the authorized files in `staging/` and the manifests in `results/`.

### 8. Recommended publication policy

If the project is uploaded to a public repository, the correct approach is:

- include only code, metadata, documentation, and reproducibility logic;
- exclude raw microdata;
- clearly document the sources and access procedures;
- instruct users how to obtain the official files before running the pipeline.

This is the recommended practice when redistribution rights are not explicitly granted.

## Closing note

This repository is intentionally designed as a reproducible, transparent, and legally cautious research package. It supports open science without violating data-access constraints. The actual microdata remain under official control and must be obtained separately by the researcher in accordance with the terms of the data providers.


Este proyecto es una base regional analítica y de calidad, no una solución
clínica final ni un modelo predictivo entrenado. Además:

- no se ha hecho modelado final;
- no se ha construido OMOP;
- no se ha realizado linkage internacional o equivalencia forzada;
- la interpretación de caídas, movilidad y funcionalidad debe hacerse con la
  ventana temporal específica de cada fuente.

## Resultado actual

El pipeline ya fue ejecutado y generó una salida válida en la carpeta:

```text
AGE-TECH-Competencia/outputs/agetech_regional/
```

Con esto el proyecto queda listo para:

- revisión humana;
- análisis descriptivo;
- preparación para modelado;
- documentación y presentación de la competencia.

## Conclusión

AgeTechRegional representa una base sólida para un proyecto de competencia AgeTech
porque combina:

- fuentes reales y verificadas localmente;
- evidencia documental para cada variable;
- calidad y leakage checks;
- armonización conservadora;
- salida reproducible y trazable.

Es una infraestructura útil para análisis serio y para construir un caso de
estudio competitivo sin caer en suposiciones semánticas no respaldadas.
