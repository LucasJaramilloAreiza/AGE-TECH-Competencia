# Results

Este directorio se genera localmente al ejecutar el pipeline. Los manifests se crean automáticamente a partir de los archivos `.txt` delimitados por `|`, `.dta` y `.parquet` presentes en `staging/sabe/` y `staging/mhas/`.

No se debe subir al repositorio público si se quiere compartir solo el código y la documentación.

Se espera que aquí queden artefactos como:

- manifests de validación;
- metadatos de ejecución;
- resultados del pipeline;
- archivos de calidad y trazabilidad.

No es necesario crear los manifests antes de ejecutar. El proyecto los crea o actualiza automáticamente a partir de los datos autorizados que se hayan colocado en `staging/`.
