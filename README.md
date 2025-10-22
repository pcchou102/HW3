# 📬 SMS Spam Classification (Baseline SVM + TF‑IDF)

> **專案目標**：建立可重現的 SMS 垃圾簡訊分類模型基線，並提供互動式 Streamlit Web 介面展示分類結果與指標。

**🚀 立即體驗 → [Streamlit Demo](https://hzx82zfwwyazqv45fvqxqs.streamlit.app/)**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📖 專案簡介

本專案使用 **Linear SVM (LinearSVC)** 與 **TF‑IDF 向量化**技術,訓練 SMS 簡訊垃圾分類模型。資料來自 [PacktPublishing 公開資料集](https://github.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity/blob/master/Chapter03/datasets/sms_spam_no_header.csv)，完整實作包含：

- **資料下載與前處理**：自動下載 CSV、清理資料、分層拆分訓練/測試集
- **特徵工程**：TF‑IDF (unigrams + bigrams)
- **模型訓練**：LinearSVC 基線模型
- **評估與輸出**：準確率 **≈ 98.4%**，並產生混淆矩陣、metrics.json
- **互動式可視化**：Streamlit Web App，即時預測與展示歷史指標

### 🎯 專案特色

- 完全可重現：固定 random seed + 版本鎖定
- CLI 友善：支援參數化訓練 (`--data`, `--out`, `--seed`, `--balanced`)
- 端到端流程：從資料取得、訓練、到 Web 介面一站完成
- OpenSpec 規範：使用 [OpenSpec](https://github.com/Fission-AI/OpenSpec) 進行變更管理與規格追蹤

---

## 🛠 技術棧

| 類別 | 工具/框架 |
|------|-----------|
| **語言** | Python 3.13+ |
| **ML / 資料** | scikit-learn, pandas, numpy, scipy |
| **視覺化** | matplotlib, seaborn, Streamlit |
| **開發管理** | OpenSpec (spec-driven development), Git |

---

## 📦 安裝與環境設定

### 前置需求

- Python >= 3.10
- pip / venv
- (可選) Git for Windows

### 快速開始 (Windows PowerShell)

```powershell
# 1. 複製專案
git clone https://github.com/pcchou102/HW3.git
cd HW3

# 2. 建立並啟用虛擬環境
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. 安裝依賴
pip install --upgrade pip
pip install -r requirements.txt

# 4. 下載資料集 (自動化)
New-Item -ItemType Directory -Path dataset -Force | Out-Null
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity/master/Chapter03/datasets/sms_spam_no_header.csv" -OutFile "dataset/sms_spam_no_header.csv"

# 5. 訓練模型
python train.py --data dataset/sms_spam_no_header.csv --out artifacts --seed 42

# 6. (可選) 快速驗證
python test_smoke.py --artifacts artifacts
```

---

## 🚀 使用方式

### 訓練模型 (`train.py`)

```bash
python train.py --data <CSV路徑> --out <輸出目錄> --seed <隨機種子> [--balanced]
```

**參數說明**：
- `--data`：CSV 資料集路徑（預設：`dataset/sms_spam_no_header.csv`）
- `--out`：Artifact 輸出目錄（預設：`artifacts`）
- `--seed`：隨機種子（預設：42）
- `--test-size`：測試集比例（預設：0.2）
- `--balanced`：是否使用類別權重平衡

**輸出檔案**：
- `artifacts/model.joblib` — 訓練完成的 LinearSVC 模型
- `artifacts/vectorizer.joblib` — TF‑IDF 向量器
- `artifacts/metrics.json` — 評估指標 (accuracy, precision, recall, F1)
- `artifacts/confusion_matrix.png` — 混淆矩陣視覺化

### 啟動 Streamlit Web App

```bash
streamlit run streamlit_app.py
```

本機開啟 `http://localhost:8501`，可以：
- 輸入任意 SMS 文字進行即時分類
- 查看訓練指標（準確率、混淆矩陣）
- 瞭解模型決策邊界（SVM decision margin）

---

## 📊 實驗結果

| 指標 | 數值 |
|------|------|
| **Accuracy** | **0.9839** |
| **Weighted Precision** | 0.9838 |
| **Weighted Recall** | 0.9839 |
| **Weighted F1** | 0.9836 |

> 測試於 5574 筆資料（80/20 分割），使用 LinearSVC + TF‑IDF (unigrams + bigrams)。

---

## 🌐 Streamlit Cloud 部署

本專案已準備好在 [Streamlit Community Cloud](https://share.streamlit.io) 上公開展示：

1. 前往 [share.streamlit.io](https://share.streamlit.io)
2. 登入並授權 GitHub
3. 選擇此倉庫 `pcchou102/HW3`
4. 主檔案路徑：`streamlit_app.py`
5. 點擊 **Deploy!** 即可在雲端執行

> **注意**：由於 Streamlit Cloud 無法保存本地 artifacts，首次部署時需在 `streamlit_app.py` 中加入自動訓練邏輯，或使用預訓練模型（可上傳至 GitHub LFS 或雲端儲存）。

---

## 📁 專案結構

```
HW3/
├── train.py                    # 訓練腳本 (CLI)
├── test_smoke.py              # 快速驗證模型載入與推論
├── streamlit_app.py           # Streamlit Web UI
├── requirements.txt           # Python 依賴清單
├── README.md                  # 本文件
├── .gitignore                 # Git 忽略規則
├── dataset/                   # 資料集目錄 (不納入版本控制)
│   └── sms_spam_no_header.csv
├── artifacts/                 # 訓練產物 (不納入版本控制)
│   ├── model.joblib
│   ├── vectorizer.joblib
│   ├── metrics.json
│   └── confusion_matrix.png
├── openspec/                  # OpenSpec 變更管理
│   ├── AGENTS.md
│   ├── project.md
│   ├── changes/
│   │   └── spam-email-classification/
│   └── specs/
└── .github/
    └── prompts/               # GitHub Copilot 整合
```

---

## 🔧 開發與貢獻

### OpenSpec 工作流程

本專案採用 [OpenSpec](https://github.com/Fission-AI/OpenSpec) 進行需求管理與變更追蹤：

```bash
# 查看目前變更
openspec list

# 顯示變更細節
openspec show spam-email-classification

# 驗證規格格式
openspec validate spam-email-classification
```

### 未來規劃 (Phase 2+)

- [ ] Logistic Regression 實作與對比
- [ ] 超參數調校 (GridSearchCV / RandomizedSearchCV)
- [ ] 特徵工程強化 (char n-grams, word embeddings)
- [ ] REST API 包裝與容器化 (Docker)
- [ ] A/B 測試框架

---

## 📜 授權與免責聲明

- **授權**：MIT License
- **資料來源**：[PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity](https://github.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity)（教育用途）
- **免責**：本專案僅供學術研究與教學用途，不保證生產環境穩定性。

---

## 👤 作者

**專案維護者**：[pcchou102](https://github.com/pcchou102)

有任何問題或建議，歡迎開 [Issue](https://github.com/pcchou102/HW3/issues) 或 Pull Request！

---

## 🙏 致謝

- [Fission AI](https://github.com/Fission-AI) 的 OpenSpec 框架
- [PacktPublishing](https://github.com/PacktPublishing) 提供公開資料集
- Streamlit 社群提供優質的 Web 框架
