# Project Context

> Note: This file captures context your AI assistants will rely on. Fill in the TBD items so we align on the same constraints and conventions.

## Purpose
本專案建立一個端到端的 **SMS 垃圾訊息分類系統**，使用機器學習（Linear SVM + TF-IDF）達成高準確率（≈98.4%）的二元分類。核心使用者為研究人員、學生與開發者，用於學習與展示 ML 基線模型的完整流程。成功指標包括：可重現性（固定 seed）、準確率 ≥95%、Streamlit 互動介面可部署至雲端。

## Tech Stack
- **OS/Env**: Windows (PowerShell 5.1+), Python 3.13+
- **Runtime/Tooling**: Node.js v22.21.0, npm 10.9.4, OpenSpec CLI 0.12.0, Git for Windows
- **Editor/AI**: VS Code + GitHub Copilot（本專案啟用 OpenSpec 工作流程）
- **Primary languages/frameworks**: 
  - **Python**: scikit-learn 1.7+, pandas 2.2+, numpy, scipy
  - **ML Pipeline**: TF-IDF vectorization + LinearSVC (baseline), future: Logistic Regression
  - **Web UI**: Streamlit 1.50+ (互動式分類介面)
  - **Dev Tools**: matplotlib, seaborn (視覺化), joblib (模型序列化)

## Project Conventions

### Code Style
- **Python**: PEP 8 規範，4 空格縮排，行長 ≤100 字元
- **Type hints**: 建議在函式簽章使用（例：`def train(data: pd.DataFrame) -> LinearSVC`）
- **Docstrings**: 公開函式使用 Google style docstrings
- **命名**: 
  - 檔案/目錄：`snake_case`（`train.py`, `test_smoke.py`）
  - 函式/變數：`snake_case`
  - 常數：`UPPER_CASE`（`HAM_EXAMPLES`, `SPAM_EXAMPLES`）
  - 類別：`PascalCase`（未來擴展時適用）

### Architecture Patterns
- **模組化設計**：
  - `train.py` — 訓練邏輯（CLI 友善）
  - `streamlit_app.py` — Web UI（自動訓練 + 互動分類）
  - `test_smoke.py` — 快速驗證（載入模型 + 推論）
- **資料流**：
  - 下載 CSV → 清理 → 分割（80/20）→ TF-IDF 向量化 → SVM 訓練 → 評估 → 序列化模型
- **Artifacts 管理**：所有訓練產物集中於 `artifacts/`（不納入版本控制）

### Testing Strategy
- **測試層級**：
  - **Smoke Test**（`test_smoke.py`）：驗證模型載入與推論基本功能
  - **未來擴展**：單元測試（pytest）、整合測試（資料管線）
- **覆蓋率目標**：基線階段無強制覆蓋率，Phase 2+ 目標 ≥70%
- **工具**：pytest（未來）、手動驗證（目前）

### Git Workflow
- **分支策略**：`main` 穩定分支；功能開發建議使用 `feature/<change-id>` 分支（目前直接提交至 main）
- **提交訊息**：Conventional Commits
  - `feat:` 新功能（例：`feat: add Streamlit UI with confidence visualization`）
  - `fix:` 錯誤修正（例：`fix: properly bind text_area to session_state`）
  - `docs:` 文件更新（例：`docs: enhance README with deployment guide`）
  - `refactor:` 重構（例：`refactor: optimize sidebar with collapsible sections`）
- **PR 規範**：需連結對應的 OpenSpec change（`openspec/changes/<id>`），描述影響範圍與測試結果

## Domain Context
- **領域**：自然語言處理（NLP）、垃圾訊息過濾、二元文本分類
- **關鍵概念**：
  - **Ham**：正常訊息（legitimate message）
  - **Spam**：垃圾/詐騙訊息（unsolicited bulk message）
  - **TF-IDF**：詞頻-逆文檔頻率（Term Frequency-Inverse Document Frequency），用於文本向量化
  - **Decision Margin**：SVM 決策邊界距離，絕對值越大表示信心度越高
- **資料模型**：
  - 輸入：CSV 兩欄（`label`, `text`），無表頭
  - 輸出：二元標籤（0=ham, 1=spam）+ decision margin
- **使用情境**：
  - 教學演示：展示 ML 基線模型的完整流程
  - 互動測試：使用者輸入任意文字，即時查看分類結果
  - 研究基線：作為後續模型（Logistic Regression, Deep Learning）的對比基準

## Important Constraints
- **環境需求**：
  - Python >= 3.10（已滿足 3.13）
  - Node.js >= 20.19.0（已滿足 22.21.0，用於 OpenSpec CLI）
- **安全/法規**：
  - 資料來源為公開教育資料集（PacktPublishing），無 PII 敏感資訊
  - 僅供學術研究與教學用途，不保證生產環境穩定性
- **效能 SLA**：
  - 訓練時間：≤ 2 分鐘（5,574 筆資料）
  - 推論延遲：< 100ms（單筆訊息）
  - Streamlit Cloud 記憶體限制：≤ 1GB（免費版）

## External Dependencies
- **資料集**：
  - 來源：https://github.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity
  - 檔案：`Chapter03/datasets/sms_spam_no_header.csv`
  - 授權：教育用途公開資料
  - 取得方式：`urllib.request.urlretrieve()` 自動下載
- **第三方服務**：
  - **Streamlit Community Cloud**：免費 Web 託管（https://share.streamlit.io）
  - **GitHub**：版本控制與 CI/CD 觸發
- **資料庫/快取**：無（所有資料與模型存於本地或記憶體）

## OpenSpec Workflow Integration
本專案採用 OpenSpec 進行變更管理：
- 所有功能變更需先建立 change proposal（`openspec/changes/<id>/`）
- 包含 `proposal.md`（目標與範圍）、`tasks.md`（實作清單）、spec deltas（需求變更）
- 完成後執行 `openspec archive <id>` 歸檔並更新 `openspec/specs/`

