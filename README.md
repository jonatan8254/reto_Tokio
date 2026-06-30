# Reto Tokio / GCI World NFL Draft Prediction

**Proyecto academico de machine learning para la hackathon Reto Tokio GCI: prediccion reproducible, auditable y sin leakage de atletas seleccionados en el NFL Draft.**

Autor: **Jonatan Estiven Sanchez Vargas**
Institucion: **Universidad Nacional de Colombia**
Programa: **Ingenieria de Sistemas e Informatica**
Modalidad: **Proyecto academico / hackathon / competencia de ciencia de datos**
Tarea: **clasificacion binaria**
Variable objetivo: **`Drafted`**
Metrica oficial: **ROC-AUC sobre la probabilidad de la clase positiva (`Drafted = 1`)**

---

## 1. Contexto Del Reto

Este repositorio documenta y ejecuta una solucion completa para el reto **GCI World NFL Draft Prediction**, desarrollado dentro del marco academico del **Reto Tokio GCI**. La actividad propone un problema realista de aprendizaje supervisado: a partir de informacion historica de atletas universitarios, mediciones fisicas, posicion, tipo de jugador y variables de perfil deportivo, construir un modelo capaz de estimar la probabilidad de que un atleta sea seleccionado en el **NFL Draft**.

El objetivo inmediato de la competencia es generar un archivo de prediccion con el formato oficial `Id,Drafted`, donde `Drafted` debe ser una probabilidad numerica entre 0 y 1. Sin embargo, el objetivo tecnico de este proyecto fue deliberadamente mas amplio: construir una solucion defendible bajo auditoria, reproducible desde codigo, metodologicamente clara y resistente a los errores comunes en competencias de machine learning, especialmente:

- uso indebido de datos externos;
- leakage por preprocesamiento global;
- seleccion de modelos guiada por el leaderboard publico;
- validacion local inestable;
- manipulacion manual de predicciones;
- notebooks dependientes de estado oculto;
- resultados sin trazabilidad experimental.

Por esa razon, el proyecto no se limito a entrenar un modelo. Se diseno como una investigacion aplicada de ciencia de datos, con fases, reglas, aceptaciones, contratos de datos, controles de leakage, comparacion de familias de modelos, diagnosticos por slices, optimizacion controlada y preparacion final de submissions.

---

## 2. Definicion Del Problema

La competencia plantea una tarea de **clasificacion binaria**:

> Predecir si un atleta sera seleccionado en el NFL Draft.

La variable objetivo es `Drafted`:

- `Drafted = 1`: atleta seleccionado.
- `Drafted = 0`: atleta no seleccionado.

La metrica principal es **ROC-AUC**, calculada sobre la probabilidad predicha de la clase positiva. Esta metrica evalua la calidad del ranking probabilistico del modelo, no una decision binaria fija. Esto es especialmente importante porque el archivo de entrega no requiere etiquetas duras, sino probabilidades.

### Datos oficiales

El proyecto utiliza exclusivamente los archivos oficiales de la competencia ubicados en `data/input/`:

| Archivo | Rol | Dimensiones verificadas |
|---|---:|---:|
| `data/input/train.csv` | Entrenamiento con variable objetivo | 2,781 filas x 16 columnas |
| `data/input/test.csv` | Datos para inferencia final | 696 filas x 15 columnas |
| `data/input/sample_submission.csv` | Plantilla oficial de entrega | 696 filas x 2 columnas |

Columnas principales:

- identificador: `Id`;
- objetivo: `Drafted`;
- variables temporales y demograficas: `Year`, `Age`;
- variables institucionales y posicionales: `School`, `Player_Type`, `Position_Type`, `Position`;
- mediciones fisicas: `Height`, `Weight`, `Sprint_40yd`, `Vertical_Jump`, `Bench_Press_Reps`, `Broad_Jump`, `Agility_3cone`, `Shuttle`.

Distribucion de clases en entrenamiento:

| Clase | Filas |
|---|---:|
| `Drafted = 0` | 978 |
| `Drafted = 1` | 1,803 |

La tasa positiva aproximada es 0.6483. Por eso, la exactitud simple no es una metrica suficiente; el proyecto se alinea con la competencia usando ROC-AUC.

---

## 3. Reglas De Gobernanza Y Competencia

Una parte central del trabajo fue tratar la competencia como un entorno con restricciones formales. Las reglas mas importantes aplicadas durante todo el proyecto fueron:

- usar solo los archivos oficiales en `data/input/`;
- no usar datos externos de atletas, escuelas, conferencias, rankings, geografia, historia del draft ni resultados deportivos;
- no etiquetar ejemplos manualmente;
- no editar manualmente valores de prediccion;
- no ajustar imputation, encoding, scaling, seleccion de features, seleccion de modelos ni hiperparametros usando `test.csv`;
- no usar el leaderboard publico como sistema principal de validacion;
- generar toda submission desde codigo reproducible;
- usar semillas fijas siempre que exista aleatoriedad;
- conservar los notebooks oficiales en `notebooks/_official/` como evidencia, sin modificarlos.

Estas restricciones no fueron tratadas como una formalidad. Se convirtieron en decisiones de diseno: cada experimento importante produjo artefactos, reportes, predicciones out-of-fold, diagnosticos y registros separados, de modo que el resultado pudiera revisarse sin depender de memoria, intuicion o ejecuciones informales.

---

## 4. Enfoque Academico Y De Ingenieria

El proyecto se desarrollo como un flujo **notebook-first**, pero con disciplina de ingenieria de machine learning. Esto significa que los notebooks fueron el medio principal de analisis y ejecucion, mientras que la trazabilidad se mantuvo mediante documentos, logs, artefactos y reglas de validacion.

El trabajo priorizo:

- **reproducibilidad:** todo resultado importante debe poder regenerarse desde codigo;
- **auditabilidad:** cada decision relevante queda documentada con evidencia;
- **validacion local confiable:** ROC-AUC sobre folds estratificados y predicciones out-of-fold;
- **prevencion de leakage:** todo transformador que aprende estadisticas se ajusta solo dentro del fold de entrenamiento;
- **simplicidad progresiva:** iniciar con baseline, luego feature engineering controlado, despues comparacion de modelos y solo al final HPO;
- **separacion entre decision y diagnostico:** los diagnosticos informan, pero no sustituyen reglas de seleccion predefinidas;
- **honestidad experimental:** los modelos con warnings se reportan como tales, incluso si tienen mejor ROC-AUC global.

---

## 5. Estructura Del Repositorio

```text
data/input/                  Archivos oficiales de la competencia.
notebooks/_official/         Notebooks oficiales originales. No se editan.
notebooks/                   Notebooks de trabajo, validacion, comparacion y readiness.
docs/                        Contratos, planes, metodologia, aceptaciones y runbooks.
references/                  Materiales academicos, libros, papers, slides y tutoriales.
outputs/folds/               Asignaciones de folds reproducibles.
outputs/oof/                 Predicciones out-of-fold por experimento.
outputs/validation/          Reportes tabulares de validacion, slices y resumenes.
outputs/reports/             Reportes narrativos, manifests y candidate logs.
outputs/submissions/         CSVs de submission generados por codigo.
outputs/figures/             Figuras de EDA y reporte.
logs/experiment_log.csv      Registro principal de experimentos importantes.
```

La organizacion refleja la evolucion del proyecto: no solo hay notebooks de entrenamiento, sino tambien contratos, protocolos, reportes de validacion, evidencias de comparacion y controles de preparacion de submission.

---

## 6. Flujo De Trabajo Por Fases

El desarrollo se ejecuto en fases, cada una con objetivo, alcance y artefactos. Esta estrategia permitio avanzar sin mezclar exploracion, seleccion de modelos, HPO y submission en una sola ejecucion opaca.

| Fase | Objetivo | Resultado |
|---|---|---|
| 0 | Contrato del reto y reglas | Se documentaron objetivo, formato, metricas, restricciones y archivos oficiales. |
| 1 | Setup y reproducibilidad | Se definio la estructura del proyecto, entorno local, carpetas y politica notebook-first. |
| 2 | Reproduccion del baseline oficial | Se reprodujo un RandomForest baseline historico con CV 0.812964 y LB publico 0.80792; se marco como referencia historica, no como ancla futura por su preprocessing global. |
| 3 | EDA y contrato de datos | Se verificaron shapes, target, missingness, columnas, riesgos de leakage y familias de senales. |
| 4 | Sintesis metodologica | Se revisaron materiales tecnicos sobre validacion, leakage, feature engineering, modelos tabulares, HPO y reproducibilidad. |
| 5 | Congelamiento metodologico | Se fijo ROC-AUC, `StratifiedKFold(5, shuffle=True, random_state=42)`, fit-scope seguro y reglas de artefactos. |
| 6 | Harness de validacion | Se implemento validacion leakage-safe con folds congelados y OOF predictions. |
| 6A | Reconciliacion del baseline | Se explico la diferencia entre baseline historico y validacion limpia; se aislo el papel de missingness informativo. |
| 7 | Feature engineering | Se adopto el feature set F2 con missingness flags y availability count. |
| 7B | Probe de interacciones por rol | Se evaluo y rechazo una interaccion adicional; F2 quedo como feature set final. |
| 8 | Comparacion de familias | Se compararon Logistic Regression, RandomForest, ExtraTrees, HistGradientBoosting, XGBoost, LightGBM y CatBoost bajo reglas fijas. |
| 9A | Diagnosticos de ranking | Se verifico el orden de candidatos con diagnosticos complementarios y slices. |
| 10 | Optimizacion controlada | Se ejecuto HPO acotado; CatBoost tuned alcanzo mejor OOF global, pero con warnings. |
| 11 | Submission readiness | Se generaron y validaron dos submissions candidatas, sin subir ni declarar ganador automatico. |
| 12 | Integracion final | Se planifico el paquete portable y el notebook final integrado como entrega academica. |

Esta secuencia muestra el caracter academico del proyecto: cada mejora fue tratada como una hipotesis, no como un cambio arbitrario. La progresion fue de baseline a validacion, de validacion a features, de features a modelos, de modelos a optimizacion y de optimizacion a readiness.

---

## 7. Notebooks Principales

| Notebook | Proposito |
|---|---|
| `notebooks/01_baseline_reproduction.ipynb` | Reproduce el baseline oficial y genera una submission baseline valida. |
| `notebooks/02_eda_and_data_contract.ipynb` | Inspecciona datos, target, ID, missingness, tipos, grupos de features y riesgos. |
| `notebooks/03_validation_harness_phase6.ipynb` | Implementa el harness de validacion leakage-safe con folds y OOF. |
| `notebooks/04_phase6a_baseline_reconciliation.ipynb` | Reconciliacion entre baseline historico y pipeline seguro. |
| `notebooks/07_phase7_missingness_availability_feature_block.ipynb` | Evalua missingness flags y availability features. |
| `notebooks/08_phase8_model_family_comparison.ipynb` | Compara familias de modelos sklearn bajo folds y features fijos. |
| `notebooks/08c_phase8_wave2_external_gbdt_comparison.ipynb` | Compara XGBoost, LightGBM y CatBoost bajo el mismo protocolo. |
| `notebooks/09a_auc_ranking_diagnostics.ipynb` | Diagnostica estabilidad de ranking, slices y distribucion de scores. |
| `notebooks/10_phase10_model_optimization.ipynb` | Ejecuta HPO controlado y acotado. |
| `notebooks/11_phase11_submission_readiness.ipynb` | Refit final, inferencia sobre test y validacion de submissions candidatas. |

Los notebooks oficiales en `notebooks/_official/` son evidencia de origen y no deben editarse.

---

## 8. Protocolo De Validacion

El protocolo de validacion fue uno de los componentes mas importantes del proyecto.

Decision congelada:

```python
StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
```

Principios:

- todos los experimentos comparables usan los mismos folds;
- la metrica principal es ROC-AUC sobre probabilidades, no etiquetas duras;
- las predicciones out-of-fold se guardan para diagnostico y comparacion;
- la clase positiva se identifica mediante `estimator.classes_`, no mediante `predict_proba(X)[:, 1]` asumido a ciegas;
- los resultados se reportan como OOF ROC-AUC, fold mean y fold std;
- los slices se usan como diagnostico, no como sustituto de la metrica principal.

El archivo de folds congelados tiene SHA-256 parcial reportado en los artefactos:

```text
96937649526bcadb
```

Este enfoque permite comparar modelos sobre exactamente las mismas particiones, reduciendo el ruido de comparacion y evitando que un modelo parezca mejor solo por haber recibido folds mas favorables.

---

## 9. Prevencion De Leakage

El proyecto identifico como operaciones de alto riesgo:

- imputacion;
- scaling;
- one-hot encoding;
- ordinal encoding;
- target encoding;
- feature selection;
- hyperparameter tuning;
- missing-value indicators si se calculan de forma no controlada;
- frequency encoding;
- rare-category grouping;
- cualquier transformacion que aprenda estadisticas de filas.

Regla central:

> Toda operacion que aprende de los datos debe ajustarse solo en el fold de entrenamiento durante cross-validation, o en todo `train.csv` durante el refit final. Nunca se ajusta usando `test.csv`.

Aplicaciones concretas:

- `test.csv` se usa solo para checks estructurales e inferencia final;
- `School` se excluye de las matrices de modelado por riesgo de cardinalidad, inestabilidad y leakage;
- no se usa target encoding;
- no se hace feature selection automatica con informacion global;
- no se optimiza contra el leaderboard publico;
- los reportes distinguen diagnosticos de resultados seleccionables.

---

## 10. Feature Engineering

El feature engineering se construyo de forma gradual y bajo ablation controlado.

### Feature set final F2

El feature set F2 contiene 21 features:

| Grupo | Features |
|---|---|
| Base numerica/categorica | `Year`, `Age`, `Height`, `Weight`, `Sprint_40yd`, `Vertical_Jump`, `Bench_Press_Reps`, `Broad_Jump`, `Agility_3cone`, `Shuttle`, `Player_Type`, `Position_Type`, `Position` |
| Missingness flags | Indicadores binarios para mediciones fisicas faltantes |
| Availability count | `available_measurement_count` |

Features excluidas:

- `Id`: identificador, no senal predictiva valida;
- `Drafted`: target;
- `School`: diagnostico solamente, no feature de modelado;
- features externas: prohibidas por regla de competencia.

### Razonamiento

El EDA mostro que la ausencia de mediciones no era simplemente ruido. La missingness podia capturar patrones asociados con tipos de jugador, posiciones y procesos de medicion. Por eso, la solucion no se limito a imputar valores faltantes; incorporo explicitamente banderas de missingness y conteos de disponibilidad como senales row-wise, sin aprender estadisticas globales.

Resultado relevante de Phase 7:

| Variante | OOF ROC-AUC | Decision |
|---|---:|---|
| F0 anchor recheck | 0.726616 | Referencia limpia inicial |
| F1 median + flags | 0.811568 | Escalada |
| F5 mean + flags | 0.813066 | Escalada |
| **F2 median + flags + count** | **0.811650** | **Adoptada** |
| F3 median + flags + count bins | 0.810606 | Escalada, no adoptada |

F2 fue adoptada no solo por score, sino por equilibrio entre rendimiento, simplicidad, estabilidad de slices y bajo riesgo de leakage.

---

## 11. Modelos Evaluados

El proyecto siguio una ruta progresiva:

1. baseline oficial con RandomForest;
2. baseline leakage-safe;
3. feature engineering controlado;
4. comparacion de modelos sklearn;
5. comparacion externa de GBDTs;
6. optimizacion acotada;
7. refit final y validacion de submissions.

Familias evaluadas:

- RandomForest;
- Logistic Regression;
- ExtraTrees;
- HistGradientBoosting;
- XGBoost;
- LightGBM;
- CatBoost.

La comparacion se hizo sobre:

- mismos folds;
- mismo feature set F2;
- misma metrica;
- mismo criterio de extraccion de probabilidades;
- preprocessing fold-safe;
- sin HPO durante la fase de comparacion inicial;
- sin leaderboard;
- sin submissions.

---

## 12. Resultados Principales

Los resultados mas relevantes registrados en los reportes aceptados son:

| Modelo / candidato | OOF ROC-AUC | Rol |
|---|---:|---|
| M0 RandomForest congelado | 0.8116502602 | Ancla / referencia limpia |
| M1 LogisticRegression baseline | 0.8270821070 | Candidato simple y fuerte; fallback |
| CatBoost baseline | 0.8202943969 | Comparacion externa GBDT |
| M1 LogisticRegression tuned | 0.8274819178 | Mejora pequena, tratada como ruido |
| **CatBoost tuned** | **0.8303208581** | Mejor OOF global, warning-heavy |

Interpretacion:

- Logistic Regression fue sorprendentemente competitiva y robusta como candidato simple.
- CatBoost tuned obtuvo el mejor score global out-of-fold.
- La diferencia de CatBoost tuned frente a M1 baseline fue positiva pero pequena: aproximadamente 0.00324 ROC-AUC.
- CatBoost tuned se mantuvo como candidato primario warning-heavy, no como ganador automatico.
- M1 LogisticRegression baseline se conservo como fallback por simplicidad, estabilidad y reproducibilidad con dependencias estandar.

---

## 13. Submission Readiness

En Phase 11 se generaron dos submissions candidatas bajo el run:

```text
phase11_option_c_20260619_0001
```

Ninguna fue subida automaticamente y no se declaro un ganador final dentro del codigo. La decision de upload y orden de submission queda como decision humana, porque la competencia puede usar el ultimo archivo enviado para ranking final.

| Candidato | Rol | Filas | Min prob. | Max prob. | SHA-256 | Estado |
|---|---|---:|---:|---:|---|---|
| `catboost_tuned` | Primario warning-heavy | 696 | 0.0090689208 | 0.9668055592 | `a6f14ef1a79aa883c6455de05fc16132bc9264c2d4ed59407aa86db9ec194cc8` | Pass |
| `m1_logistic_regression_baseline` | Fallback/reference | 696 | 0.0010409330 | 0.9894261702 | `0804613d63c00d353497d20bd8a341721684f645499e2012a99f120557200640` | Pass |

Checks de submission:

- columnas exactamente `Id,Drafted`;
- 696 filas;
- orden de `Id` alineado con `test.csv` y `sample_submission.csv`;
- probabilidades numericas;
- sin valores faltantes;
- sin infinitos;
- valores dentro de `[0, 1]`;
- generacion desde codigo;
- sin edicion manual posterior;
- checksum registrado.

---

## 14. Limitaciones Y Riesgos Documentados

El proyecto no oculta sus riesgos. Los principales son:

- **CatBoost tuned es el mejor global OOF, pero warning-heavy.** Presenta alertas en algunos slices, incluyendo `Age_missing = 1`, ciertos anos y algunas posiciones.
- **La mejora global frente a Logistic Regression es pequena.** El delta frente a M1 baseline es positivo, pero no suficientemente grande como para ignorar estabilidad, simplicidad y riesgo de slices.
- **No se uso `School` como feature.** Puede contener senal real, pero su uso seguro requeriria una estrategia fold-safe mucho mas delicada.
- **El leaderboard publico no se usa como evidencia de seleccion.** Esto puede sacrificar feedback inmediato, pero protege contra overfitting al leaderboard.
- **El baseline oficial historico no se usa como ancla metodologica.** Su preprocessing global lo hace util como referencia historica, no como comparador leakage-safe.

Estas limitaciones no son fallos del proyecto; son parte de la defensa tecnica de una solucion auditable.

---

## 15. Como Ejecutar El Proyecto

### 15.1 Crear entorno local

```powershell
.\.venv\Scripts\Activate.ps1
```

Si el entorno no existe:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 15.2 Instalar dependencias

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Dependencias principales:

- `numpy`;
- `pandas`;
- `scikit-learn`;
- `matplotlib`;
- `jupyter`;
- `ipykernel`;
- `pyyaml`;
- `joblib`;
- utilidades de lectura documental (`pypdf`, `pymupdf`, `pdfplumber`).

CatBoost, XGBoost y LightGBM fueron tratados como dependencias externas condicionales en fases especificas; el stack base del proyecto se mantiene minimalista.

### 15.3 Orden recomendado de notebooks

Para revisar la historia completa:

```text
notebooks/01_baseline_reproduction.ipynb
notebooks/02_eda_and_data_contract.ipynb
notebooks/03_validation_harness_phase6.ipynb
notebooks/04_phase6a_baseline_reconciliation.ipynb
notebooks/07_phase7_missingness_availability_feature_block.ipynb
notebooks/08_phase8_model_family_comparison.ipynb
notebooks/08c_phase8_wave2_external_gbdt_comparison.ipynb
notebooks/09a_auc_ranking_diagnostics.ipynb
notebooks/10_phase10_model_optimization.ipynb
notebooks/11_phase11_submission_readiness.ipynb
```

Para una ejecucion final compacta, el proyecto planifico un notebook integrado bajo `docs/12_final_integrated_notebook/`, destinado a consolidar la historia completa en una entrega portable.

---

## 16. Documentacion Relevante

Documentos clave para auditar el proyecto:

| Documento | Proposito |
|---|---|
| `docs/00_project_contract/challenge_brief.md` | Contrato del reto, archivos oficiales, target, metricas y reglas. |
| `docs/00_project_contract/submission_checklist.md` | Checklist formal antes de generar o subir submissions. |
| `docs/05_methodology/validation_protocol_phase6.md` | Protocolo de validacion congelado. |
| `docs/05_methodology/leakage_checklist_phase6.md` | Checklist de leakage prevention. |
| `docs/01_project_planning/project_execution_plan_v3.md` | Plan maestro de ejecucion por fases. |
| `outputs/reports/phase7_missingness_availability_v1_validation_report.md` | Evidencia de adopcion del feature set F2. |
| `outputs/reports/phase8_model_family_comparison_v1_validation_report.md` | Comparacion sklearn-native. |
| `outputs/reports/phase8_wave2_external_gbdt_v1_validation_report.md` | Comparacion XGBoost / LightGBM / CatBoost. |
| `outputs/reports/phase10_model_optimization_phase10_standard_20260619_0152_validation_report.md` | HPO controlado. |
| `outputs/reports/phase11_submission_readiness_phase11_option_c_20260619_0001_validation_report.md` | Validacion final de submissions candidatas. |

---

## 17. Registro Experimental

El archivo principal de tracking es:

```text
logs/experiment_log.csv
```

El primer experimento registrado reproduce el baseline oficial:

| Experiment ID | Fase | Modelo | CV AUC mean | CV AUC std | Submission |
|---|---|---|---:|---:|---|
| `001_baseline_reproduction` | Phase 2 | RandomForestClassifier | 0.812964 | 0.025740 | `outputs/submissions/submission_001_baseline.csv` |

Fases posteriores escribieron candidate logs y manifests bajo `outputs/reports/`, evitando modificar el log principal sin aprobacion. Esta separacion protege la integridad historica del registro.

---

## 18. Aporte Tecnico Del Proyecto

Este repositorio demuestra una ejecucion avanzada para un proyecto academico de competencia ML por varias razones:

1. **Traduce reglas de competencia en contratos tecnicos.** El proyecto no solo cumple restricciones; las convierte en checks y decisiones de arquitectura experimental.
2. **Distingue entre score historico y score valido.** El baseline oficial se reproduce, pero no se usa ingenuamente como ancla cuando se detecta preprocessing global.
3. **Construye una validacion robusta antes de optimizar.** Los folds congelados y OOF predictions aparecen antes de feature engineering avanzado, modelos externos o HPO.
4. **Trata missingness como senal, no como molestia.** La solucion captura disponibilidad de mediciones de forma row-wise y leakage-safe.
5. **Compara modelos con justicia experimental.** Las familias se evaluan bajo los mismos folds, features y metricas.
6. **No sobrevende el mejor modelo.** CatBoost tuned gana globalmente, pero se reporta con sus warnings y se conserva un fallback mas simple.
7. **Prepara submissions con control de calidad.** Cada CSV final se valida por formato, rangos, orden de IDs y checksum.
8. **Mantiene documentacion auditable.** Planes, checklists, reports y manifests permiten reconstruir por que se tomo cada decision.

En conjunto, el proyecto evidencia capacidad no solo de entrenar modelos, sino de construir un flujo de machine learning responsable, explicable y defendible.

---

## 19. Politica De Git Y Datos

No deben versionarse:

- archivos oficiales CSV si la distribucion no lo permite;
- `.venv/`;
- caches;
- ZIPs;
- outputs generados pesados;
- PDFs/libros de referencia si no corresponde distribuirlos;
- submissions finales si estan gitignored por politica del proyecto.

Los notebooks oficiales en `notebooks/_official/` no se modifican.

---

## 20. Declaracion Sobre Datos Externos

Este proyecto **no usa datos externos**. No incorpora informacion adicional de atletas, universidades, conferencias, rankings, historiales del draft, geografia, resultados deportivos ni datasets similares encontrados en linea.

Toda senal usada para entrenamiento proviene de las columnas disponibles en los archivos oficiales de la competencia. Esta decision protege la comparabilidad del reto y evita violaciones de reglas.

---

## 21. Referencias Y Material Academico

El proyecto se apoyo en materiales de:

- validacion y seleccion de modelos;
- leakage y reproducibilidad;
- feature engineering;
- modelos tabulares;
- gradient boosting;
- hyperparameter optimization;
- disciplina de competencias tipo Kaggle;
- materiales oficiales del curso/reto GCI.

Los detalles bibliograficos y el mapa fuente-decision se encuentran en `JonatanSanchez/references.md` y en los documentos de investigacion bajo `docs/04_research/`.

---

## 22. Estado Final Del Proyecto

Estado documentado:

- baseline oficial reproducido;
- EDA y contrato de datos completados;
- protocolo de validacion congelado;
- folds y OOF como columna vertebral de comparacion;
- feature set F2 adoptado;
- modelos sklearn y GBDT comparados;
- HPO acotado ejecutado;
- dos submissions candidatas generadas y validadas;
- no upload automatico;
- no ganador final declarado por codigo;
- paquete final integrado planificado para entrega academica.

El repositorio representa una solucion completa, seria y revisable para el Reto Tokio GCI, con enfasis en excelencia metodologica, no solamente en performance.
