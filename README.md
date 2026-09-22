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
<img width="1916" height="984" alt="image" src="https://github.com/user-attachments/assets/a7093342-374f-47f8-aceb-3bfb4d218bf8" />


#### MHAS / ENASEM 2024

Portal oficial del proyecto MHAS para datos de encuesta y productos de datos:

https://www.mhasweb.org/DataProducts/CoreSurveyData.aspx

Cada investigador debe seguir el procedimiento de acceso institucional o de solicitud oficial indicado por la fuente, según corresponda.

### 5. Dónde poner los datos localmente

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

Ejemplo real de uso:

```text
AGE-TECH-Competencia/
staging/
├── sabe/
│   ├── Base de datos y diccionario/
│   │   ├── Base de datos - Capitulos/
│   │   │   ├── Biom.txt
│   │   │   ├── Cap1Ident.txt
│   │   │   ├── Cap1Parte1.txt
│   │   │   ├── Cap1Parte2.txt
│   │   │   ├── Cap2.txt
│   │   │   ├── Cap2Hijos.txt
│   │   │   ├── Cap2PersCerc.txt
│   │   │   ├── Cap2PersVivHog.txt
│   │   │   ├── Cap3.txt
│   │   │   ├── Cap4.txt
│   │   │   ├── Cap5.txt
│   │   │   ├── Cap6.txt
│   │   │   ├── Cap7.txt
│   │   │   ├── Cap8.txt
│   │   │   ├── Cap8EnfNoTrans.txt
│   │   │   ├── Cap8Med.txt
│   │   │   ├── Cap9.txt
│   │   │   ├── Cap10.txt
│   │   │   ├── Cap11.txt
│   │   │   └── Cap12.TXT
│   │   ├── Base de datos Cuidadores/
│   │   │   ├── BASE_CF_20072019publicar.xlsx
│   │   │   └── DICCIONARIO_CF_20072019.xlsx
│   │   └── Diccionario de datos SABE.xlsx
│   └── ...
└── mhas/
    ├── sect_trh_follow_up_2024.dta
    ├── sect_trh_new_sample_2024.dta
    ├── sect_a_c_d_e_pc_f_h_i_2024.dta
    └── ...

results/
├── manifest_sabe.json
└── manifest_mhas.json
```

Importante:

- `staging/sabe/` debe contener solo los archivos relevantes del microdato SABE 2015 autorizados.
- `staging/mhas/` debe contener solo los archivos del core survey y secciones necesarias para el estudio.
- `results/` debe contener los manifests de validación y trazabilidad del pipeline.
- El pipeline lee recursivamente archivos `.txt` delimitados por `|`, `.dta` y `.parquet`.
- NO se suben los microdatos al repositorio.
- NO se usan todos los archivos del paquete de la encuesta; solo se usan las bases requeridas para el análisis y los datos relevantes para las variables canónicas del catálogo.

### 6. Archivos específicos que deben ir en cada carpeta

#### SABE 2015: archivos que deben ir en `staging/sabe/`

Los archivos que normalmente corresponden a la base autorizada de SABE 2015 deben colocarse en esta ruta dentro del repositorio:

```text
AGE-TECH-Competencia/staging/sabe/
```

En esta carpeta se espera la base de microdatos SABE 2015 y, si aplica, sus archivos auxiliares autorizados. Para esta fase del proyecto, no todos los archivos del paquete de SABE deben usarse; solo los necesarios para las variables objetivo del catálogo.

Los archivos clave de la descarga oficial, tal como aparecen en la estructura real del paquete de SABE 2015, son estos:

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

Este conjunto es el que normalmente viene en la descarga oficial de SABE 2015. No todos esos archivos son obligatorios para el análisis final, pero son los que debes tener claros y no perder de vista. La parte principal del estudio suele estar en `Base de datos - Capitulos/`.

#### MHAS / ENASEM 2024: archivos que deben ir en `staging/mhas/`

Los archivos del estudio MHAS / ENASEM que correspondan a la encuesta core o secciones requeridas deben ir en esta ruta:

```text
AGE-TECH-Competencia/staging/mhas/
```

Archivos típicos que suelen aparecer en esta carpeta:

- `sect_trh_follow_up_2024.dta`
- `sect_trh_new_sample_2024.dta`
- `sect_a_c_d_e_pc_f_h_i_2024.dta`
- `...`

Lo importante es que solo vayan los archivos de la base relevante para la armonización, no toda la documentación ni archivos auxiliares no usados.

#### Manifests: archivos que deben ir en `results/`

La carpeta esperada es:

```text
AGE-TECH-Competencia/results/
```

Con archivos como:

- `manifest_sabe.json`
- `manifest_mhas.json`

Estos archivos deben describir la validación del dataset, la fuente, el conjunto de filas y la trazabilidad del pipeline.

### 7. Qué archivos se usan y cuáles no

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
<img width="1891" height="700" alt="image" src="https://github.com/user-attachments/assets/4c4857a1-4ade-4485-8321-1fa001489194" />

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
python -m AgeTechRegional.cli --config config.local.json
```

La ejecución espera que el investigador haya colocado previamente los archivos autorizados en `staging/`. Los manifests no deben crearse manualmente: el pipeline los genera o actualiza automáticamente en `results/manifest_sabe.json` y `results/manifest_mhas.json`.

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
<img width="1916" height="984" alt="image" src="https://github.com/user-attachments/assets/62c92da3-2280-44e1-989c-1948314b20ce" />

#### MHAS / ENASEM 2024

Official MHAS data products page:

https://www.mhasweb.org/DataProducts/CoreSurveyData.aspx

Each researcher must follow the approved access or application procedure required by the data provider.

### 5. Where to place the data locally

The project configuration already points to paths inside the repository itself. To work as intended, you should download the official data and place it inside the same project folder, in these exact locations:

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

Example:

```text
AGE-TECH-Competencia/
staging/
├── sabe/
│   ├── base_sabe_2015.dta
│   └── diccionario_sabe_2015.xlsx
└── mhas/
    ├── sect_trh_follow_up_2024.dta
    ├── sect_trh_new_sample_2024.dta
    ├── sect_a_c_d_e_pc_f_h_i_2024.dta
    └── ...

results/
├── manifest_sabe.json
└── manifest_mhas.json
```

Important:

- `staging/sabe/` should contain only the authorized SABE 2015 microdata files relevant to the study.
- `staging/mhas/` should contain only the files needed for the core survey and required sections.
- `results/` should contain the manifests needed for validation and pipeline traceability.
- The pipeline recursively reads pipe-delimited `.txt`, `.dta`, and `.parquet` files.
- RAW DATA MUST NOT be stored in the public repository.
- NOT all files from the survey package are used; only the microdata relevant to the study and the canonical variables of the project should be ingested.

### 6. Specific files to place in each folder

#### SABE 2015: files to place in `staging/sabe/`

Place the official, authorized SABE 2015 microdata inside:

```text
AGE-TECH-Competencia/staging/sabe/
```

This folder should contain the subset of SABE files actually needed for analysis. The project does not require all files from the full download package; only those necessary for the target variables and harmonization workflow should be kept.

Typical examples include:

- `base_sabe_2015.dta`
- `diccionario_sabe_2015.xlsx`
- `Base de datos - Capitulos/*.txt`
- other authorized microdata files used by the analysis

#### MHAS / ENASEM 2024: files to place in `staging/mhas/`

Place the authorized MHAS / ENASEM survey files in:

```text
AGE-TECH-Competencia/staging/mhas/
```

Examples of relevant files often included here:

- `sect_trh_follow_up_2024.dta`
- `sect_trh_new_sample_2024.dta`
- `sect_a_c_d_e_pc_f_h_i_2024.dta`
- other required core sections only

Do not include unrelated or non-essential documentation files in the repo.

#### Manifests: files to place in `results/`

Place the required manifests in:

```text
AGE-TECH-Competencia/results/
```

Examples:

- `manifest_sabe.json`
- `manifest_mhas.json`

These files describe the source mapping, validation status, and execution traceability for the pipeline.

### 7. Which files are used and which are not

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
<img width="1891" height="700" alt="image" src="https://github.com/user-attachments/assets/3414053f-5f2b-475a-9822-99d7f66d81fe" />

- `sect_trh_follow_up_2024`
- `sect_trh_new_sample_2024`
- `sect_a_c_d_e_pc_f_h_i_2024`

may be required, but the full auxiliary package or unrelated documentation should not be published or stored in this repo.

### 7. Reproduction instructions

```powershell
cd AGE-TECH-Competencia
pip install -r requirements.txt
$env:PYTHONPATH="."
python -m AgeTechRegional.cli --config config.local.json
```

The pipeline expects the researcher to have already placed the authorized files in `staging/`. Manifests do not need to exist beforehand: the pipeline automatically creates or updates `results/manifest_sabe.json` and `results/manifest_mhas.json`.

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
