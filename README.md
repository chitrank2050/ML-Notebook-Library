# ML-Notebook-Library
Learning AI with microprojects in the form of notebooks

### Project Structure
```text
datasets/                            (Store datasets here)
explanation/                         (Store explanations here)
|
├── gradient_descent.py              (Gradient Descent detailed explanation)
|
notebooks/
│
├── math-refresh/
│   ├── linear_algebra.ipynb          (SVD, PCA manual)
│   ├── calculus.ipynb
│   ├── probability.ipynb
│   └── statistics.ipynb              (replaces discrete_math — std, variance,
│                                      hypothesis testing, p-value, CLT)
│
├── python-refresh/
│   ├── python_basics.ipynb           (syntax, list comp, dicts — quick pass)
│   ├── oop.ipynb                     (classes, inheritance, dunder methods)
│   └── python_for_ml.ipynb           (numpy idioms, list vs array, vectorization)
│                                      skip async/decorators — not used in ML
│
├── data-science/
│   ├── numpy_pandas.ipynb
│   ├── data_cleaning.ipynb
│   ├── eda_visualization.ipynb       (matplotlib, seaborn, plotly)
│   └── feature_engineering.ipynb    (encoding, scaling, missing values)
│
├── ml-algorithms/
│   │
│   ├── regression/
│   │   ├── linear_regression.ipynb   (OLS, assumptions, R², MSE)
│   │   ├── regularization.ipynb      (Ridge, Lasso, ElasticNet — why each)
│   │   ├── polynomial_regression.ipynb
│   │   └── regression_kaggle.ipynb   (real Kaggle dataset end-to-end)
│   │
│   ├── classification/
│   │   ├── logistic_regression.ipynb
│   │   ├── svm.ipynb
│   │   ├── knn.ipynb
│   │   └── naive_bayes.ipynb
│   │
│   ├── trees/
│   │   ├── decision_trees.ipynb
│   │   ├── random_forest.ipynb
│   │   └── gradient_boosting.ipynb   (XGBoost, LightGBM — used heavily on Kaggle)
│   │
│   ├── clustering/
│   │   ├── kmeans.ipynb
│   │   └── dbscan.ipynb
│   │
│   ├── dimensionality_reduction/
│   │   ├── pca.ipynb
│   │   ├── tsne.ipynb
│   │   └── umap.ipynb
│   │
│   └── model_evaluation/             (easy to skip, costly to miss)
│       ├── metrics.ipynb             (accuracy, F1, AUC-ROC, RMSE)
│       ├── cross_validation.ipynb
│       └── bias_variance_tradeoff.ipynb
│
├── dl-models/
│   ├── fnn.ipynb                     (fully connected, from scratch then PyTorch)
│   ├── cnn.ipynb                     (image classification)
│   ├── rnn_lstm_gru.ipynb            (sequences, time series)
│   ├── gan.ipynb
│   └── transformers_basics.ipynb
│
├── transformers-deep/
│   ├── attention_mechanisms.ipynb
│   ├── bert_architecture.ipynb
│   ├── gpt_architecture.ipynb
│   └── fine_tuning.ipynb             (HuggingFace)
│
├── embeddings/
│   ├── word2vec_glove.ipynb
│   ├── sentence_embeddings.ipynb
│   └── vector_search_faiss.ipynb
│
└── generative-ai/
    ├── vae.ipynb
    ├── diffusion_models.ipynb
    └── llm_prompting_rag.ipynb
```