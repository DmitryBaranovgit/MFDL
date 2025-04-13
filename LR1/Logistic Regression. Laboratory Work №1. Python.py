# -*- coding: utf-8 -*-
"""MFDL. Баранов Д.А. ИВТ 2.1. ЛР №1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1s8jTlbeQlTfCxrkPxOuN1ZhQeET2qB9B

Баранов Д.А. ИВТ 2.1

# Лабораторная работа №1

### Предсказание оттока клиентов банка с использованием логистической регресии

## Шаг 1: Импорт необходимых библиотек
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, roc_curve

sns.set(style='whitegrid')

"""## Шаг 2: Загрузка и пердварительный анализ данных"""

df = pd.read_csv("churn.csv")

df.head()
df.info()
df.describe()
df.isnull().sum()

"""## Шаг 3: Предобработка данных"""

# Удаление ненужных колонок
df = df.drop(columns = ["RowNumber", "CustomerId", "Surname"])

# Преобразование категориальных признаков
df = pd.get_dummies(df, columns = ["Geography", "Gender"])

df.head()

"""## Шаг 4: Разделение признаков и целевой переменной"""

X = df.drop(columns = "Exited", axis = 1)
y = df["Exited"]

"""## Шаг 5: Масштабирование признаков"""

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

"""## Шаг 6: Разделение на обучающую и тестовую выборки"""

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size = 0.3, random_state = 42, stratify = y)

"""## Шаг 7: Обучение модели логистической регрессии"""

model = LogisticRegression()
model.fit(X_train, y_train)

"""## Шаг 8: Оценка качества модели"""

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]))

"""## Шаг 9: Визуализация результатов"""

# Матрица ошибок
sns.heatmap(confusion_matrix(y_test, y_pred), annot = True, fmt = 'd', cmap = 'Blues')
plt.title("Матрица ошибок")
plt.xlabel("Предсказание")
plt.ylabel("Факт")
plt.show()

# Roc-кривая
fpr, tpr, thresholds = roc_curve(y_test, model.predict_proba(X_test)[:, 1])
plt.plot(fpr, tpr, label = 'Logistic Regression')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Posotive Rate')
plt.legend()
plt.grid()
plt.show()

"""## Шаг 10: Интерпретация результатов

### Важность признаков по логистической регрессии

После обучения модели логистической регрессии проанализированы коэффициенты признаков:
- Признаки с **положительным коэффицентом** увеличивают вероятность оттока клиента
- Признаки с **отрицательным коэффициентом** уменьшают эту вероятность
*Курсив*
Примеры интерпретации:
- `IsActiveMember` (Актианый клиент) имеет **отрицательный коэффициент**, что логично - активные клиенты чаще остаются.
- `Age` имеет **положительный коэффициент**, то есть с возрастом вероятность оттока увеличивается.
- `NumOfProducts` с отрицательным коэффициентом показывает, что чем больше клиент пользуется продуктами банка, тем он более лоялен.

### Матрица ошибок

На основе матрицы ошибок видно:

- **2318** лояльных клиентов были распознаны правильно.
- **491** ушедших клиентов были ошибочно классифицированы как лояльные (ложные отрицания).
- Модель **чаще ошибается на ушедших клиентах**, т.е. хуже распознает уходящих (что более критично для банка).

### ROC-кривая

ROC-кривая показывает, что модель работает **лучше случайно (чем прямая линия)**, но есть возможности для улучшения. Модель может быть усилена с помощью других методов (например, дерева решений, случайного леса, бустинга).

### Что можно улучшить:

- Использовать более сложные алгоритмы: `RandomForestClassifier`, `XGBoost`, `CatBoost`.
- Провести **балансировку классов** (например, с помощью SMOTE или веса классов), т.к. в выборке отток - редкое событие.
- Провести **гиперпараметрическую оптимизацию**.
- Вести **новые признаки** (например, интерактивные признаки: возраст и активность).
"""