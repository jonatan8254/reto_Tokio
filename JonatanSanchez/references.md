# Bibliographic References — Reto Tokio / GCI World NFL Draft Prediction

This bibliography lists the sources consulted during the project. Every entry corresponds to
a source held in the project's reference library. Where a specific bibliographic detail
(edition year, publisher, or DOI) could not be confirmed from the source itself, the entry is
marked **(details to verify against the source)** rather than stated with false precision.

The references are grouped by the methodological role they played. A compact
reference-to-decision map follows in the final subsection.

---

## Validation and model selection

- Cawley, G. C., & Talbot, N. L. C. (2010). *On over-fitting in model selection and subsequent
  selection bias in performance evaluation.* Journal of Machine Learning Research, 11, 2079–2107.
- James, G., Witten, D., Hastie, T., Tibshirani, R., & Taylor, J. (2023). *An Introduction to
  Statistical Learning with Applications in Python.* Springer.
- Banachewicz, K., & Massaron, L. (2025). *The Kaggle Book* (2nd ed.). Packt Publishing.
- *The Kaggle Workbook* (2023). Packt Publishing. **(author details to verify against the source)**
- *A meta-analysis of overfitting in machine learning / Kaggle competitions.* **(authors, venue, and year to verify against the source)**

## Leakage and reproducibility

- Kapoor, S., & Narayanan, A. (2023). *Leakage and the reproducibility crisis in machine-learning-based
  science.* Patterns. **(volume/issue to verify against the source)**
- *On leakage in machine-learning pipelines.* **(authors, venue, and year to verify against the source)**
- McKinney, W. (2022). *Python for Data Analysis* (3rd ed.). O'Reilly Media.

## Feature engineering and selection

- Kuhn, M., & Johnson, K. *Feature Engineering and Selection: A Practical Approach for Predictive
  Models.* CRC Press. **(edition year to verify against the source)**
- *Feature Engineering for Modern Machine Learning* (2024). **(authors and publisher to verify against the source)**
- *A survey of feature selection methods* (2024). **(authors and venue to verify against the source)**
- *Causal feature selection for responsible machine learning.* **(authors, venue, and year to verify against the source)**
- Course reading: *Feature Engineering* (lecture reading, GCI World course materials).

## Tabular models and gradient boosting

- Chen, T., & Guestrin, C. (2016). *XGBoost: A scalable tree boosting system.* Proceedings of the
  22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 785–794.
- Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T.-Y. (2017).
  *LightGBM: A highly efficient gradient boosting decision tree.* Advances in Neural Information
  Processing Systems, 30.
- Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V., & Gulin, A. (2018). *CatBoost:
  Unbiased boosting with categorical features.* Advances in Neural Information Processing Systems, 31.
- *A closer look at deep learning on tabular datasets.* **(authors, venue, and year to verify against the source)**
- Géron, A. *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow / PyTorch.*
  O'Reilly Media. **(edition year to verify against the source)**
- *Machine Learning with LightGBM and Python* (2023). Packt Publishing. **(author to verify against the source)**
- *Python Machine Learning by Example* (4th ed., 2024). Packt Publishing. **(author to verify against the source)**

## Hyperparameter optimization

- Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M. (2019). *Optuna: A next-generation
  hyperparameter optimization framework.* Proceedings of the 25th ACM SIGKDD International
  Conference on Knowledge Discovery and Data Mining, 2623–2631.

## Data engineering background

- Reis, J., & Housley, M. (2022). *Fundamentals of Data Engineering.* O'Reilly Media.

## Competition and course materials (GCI World)

- GCI World NFL Draft Prediction — competition tutorial, final assignment tutorial, Q&A, session
  notes, and lecture slides (course materials). These define the official task, the `Id,Drafted`
  submission format, the 696-row requirement, the ROC-AUC metric, and the prohibition on external
  data.

## Python tooling documentation

- The pandas, NumPy, and scikit-learn project documentation were used for API reference during
  implementation.

---

## Reference-to-decision map

| Source | Project decision it supported |
|---|---|
| Cawley & Talbot (2010) | Guarding against model-selection overfitting and selection bias; out-of-fold evaluation; the pre-registered promotion bar and no-leaderboard-for-selection rule. |
| Kapoor & Narayanan (2023); *On leakage in ML pipelines* | The fit-scope leakage rule — every learned transform fitted inside training folds (or on full train at refit), never on test. |
| Kuhn & Johnson (Feature Engineering and Selection) | The missingness/availability feature block (F2) and slice-aware feature evaluation. |
| An Introduction to Statistical Learning (Python) | Validation design, ROC-AUC reasoning under class imbalance, and stability considerations. |
| Chen & Guestrin (2016); Ke et al. (2017); Prokhorenkova et al. (2018) | The external gradient-boosting comparison (XGBoost, LightGBM, CatBoost) in Phase 8 Wave 2. |
| Akiba et al. (2019) | The bounded, pre-registered hyperparameter-optimization governance in Phase 10. |
| The Kaggle Book / Workbook | Competition discipline: leaderboard as sanity check only, reproducibility, and ensemble-diversity reasoning (kept future-locked). |
| Meta-analysis of overfitting; survey of feature selection | Caution on over-reading small slices and on uncontrolled feature search. |

---

## Generative AI assistance disclosure

This project benefited from generative AI assistance (ChatGPT) in an auxiliary capacity:
conceptual consultation on validation, leakage, and feature-engineering frameworks; coding
recommendations and debugging guidance during notebook development; and review of notebook
organisation and documentation structure. It did **not** train, tune, or select models; did
**not** execute hyperparameter optimisation; did **not** make submission decisions; and did
**not** determine the methodological trajectory beyond advisory consultation. All methodological
decisions, validation criteria, modelling choices, submission handling, and final interpretation
were made and documented by the author as part of the project workflow.

Approximate citation:

> OpenAI. (2026). *ChatGPT* [Large language model]. Used as an auxiliary support tool for
> conceptual consultation, coding recommendations, debugging guidance, and review of notebook
> organisation.
