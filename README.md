# AgeTechRegional

Programa local y reproducible para construir una base analítica regional de
envejecimiento saludable, fragilidad motriz, movilidad y caídas a partir de SABE
Colombia 2015 y MHAS/ENASEM Wave 7 2024.

## Alcance

Lee exclusivamente Parquet de staging y manifests locales. No descarga, autentica,
usa ELSI ni modifica los Parquet de origen. La salida conserva tablas por fuente y
una tabla larga armonizada; la armonización es conservadora y no transforma
caídas de último año de SABE en caídas de dos años de MHAS. No hay modelos
predictivos, OMOP ni linkage internacional en esta fase.

## Ejecución

Instalar dependencias (`pandas`, `pyarrow`) en el entorno local y copiar
`config.example.json` a una ruta de configuración. Ajustar las rutas externas:

```powershell
python -m AgeTechRegional.cli --config AgeTechRegional\config.local.json
```

Si falta una ruta, manifest o una columna respaldada por evidencia, el programa
falla de forma explícita. Las salidas contienen `run_manifest.json`, Parquet
fuente-preservados, Parquet armonizado, catálogo/crosswalk CSV, cobertura,
exclusiones, particiones y reporte de leakage/calidad.

Los patrones del catálogo son un detector inicial reproducible, no una afirmación
de equivalencia. Antes de usar una variable en un análisis se debe confirmar su
definición, código, unidad, población elegible y ventana en los diccionarios
locales; las variables no comparables permanecen identificadas como tales.
