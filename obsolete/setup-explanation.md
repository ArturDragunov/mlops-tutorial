### 🧩 Why `setup.py` and `-e .` Are Used

**Purpose:**
`setup.py` defines your project as a **Python package**, making it installable (locally or remotely). It tells Python how to build, install, and manage dependencies for your code.

**Key points:**

* `-e .` (editable install) means “install this project in editable mode.”
  → Your local code is linked directly, so changes take effect immediately without reinstalling.
* When you run `pip install -r requirements.txt` (or `uv pip install`), and the file includes `-e .`,
  → It **automatically runs** `setup.py` to install your local package.

**Why it’s useful:**

* Enables **clean imports** like `from mlproject.module import something` instead of relative paths.
* Common in **production**, **ML pipelines**, and **larger modular codebases**.
* Still relevant with **`uv`**, though modern projects often prefer `pyproject.toml` (PEP 621) instead of `setup.py`.

**TL;DR:**
`setup.py` + `-e .` = treat your project as an installable local package → cleaner structure, better dependency management, and easier collaboration.



### ⚙️ Using `pyproject.toml` Instead of `setup.py`

Modern Python projects use **`pyproject.toml`** (PEP 621) to define metadata and dependencies — replacing `setup.py`.

**Example:**

```toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mlproject"
version = "0.0.1"
description = "My ML project"
authors = [{ name = "Artur", email = "dragunovartur61@gmail.com" }]
dependencies = [
    "pandas",
    "numpy",
    "seaborn",
    "matplotlib",
    "scikit-learn",
    "catboost",
    "xgboost",
    "Flask",
]

[tool.setuptools.packages.find]
where = ["."]
```

**Install in editable mode (same as `-e .`):**

```bash
uv pip install -e .
```

✅ This automatically links your local code just like `setup.py`,
but uses the **modern, standardized** packaging format.
