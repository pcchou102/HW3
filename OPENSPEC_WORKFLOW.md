# OpenSpec 工作流程說明

## 📖 什麼是 OpenSpec？

OpenSpec 是一個**規格驅動開發（Spec-Driven Development）**的框架，幫助人類與 AI 助手在開發前**先對齊需求與設計**，避免浪費時間在錯誤的實作上。

---

## 🔄 三階段工作流程

### Stage 1: 建立變更提案（Creating Changes）

**何時需要建立提案？**
- ✅ 新增功能或能力
- ✅ 進行破壞性變更（API、資料結構）
- ✅ 改變架構或模式
- ✅ 效能優化（會改變行為）
- ✅ 更新安全模式

**何時不需要提案？**
- ❌ 錯誤修正（恢復原有行為）
- ❌ 拼字、格式、註解
- ❌ 依賴版本更新（非破壞性）
- ❌ 設定檔調整
- ❌ 測試既有行為

**步驟**：
```bash
# 1. 查看目前狀態
openspec list                  # 列出活躍的變更
openspec list --specs          # 列出現有規格

# 2. 選擇唯一的 change-id（kebab-case，動詞開頭）
# 例：add-spam-email-classification, update-ui-confidence-display

# 3. 建立變更資料夾結構
openspec/changes/<change-id>/
├── proposal.md       # 變更提案（目標、範圍、驗收標準）
├── tasks.md          # 實作任務清單
├── design.md         # 技術設計（可選）
└── specs/            # 規格變更（deltas）
    └── <capability>/
        └── spec.md   # 使用 ADDED/MODIFIED/REMOVED Requirements

# 4. 撰寫 spec deltas
## ADDED Requirements       # 新增的需求
## MODIFIED Requirements    # 修改的需求
## REMOVED Requirements     # 移除的需求

# 每個 Requirement 必須包含至少一個 Scenario
#### Scenario: 情境名稱
- GIVEN 前提條件
- WHEN 觸發動作
- THEN 預期結果

# 5. 驗證
openspec validate <change-id> --strict

# 6. 等待核准（不要在核准前開始實作）
```

---

### Stage 2: 實作變更（Implementing Changes）

**步驟**（按順序完成）：
```bash
# 1. 閱讀 proposal.md
# 理解要建立什麼、為什麼、範圍與驗收標準

# 2. 閱讀 design.md（如果有）
# 了解技術決策、架構選擇、權衡

# 3. 閱讀 tasks.md
# 取得實作檢查清單

# 4. 循序實作每個任務
# 按照 tasks.md 的順序完成

# 5. 確認完成度
# 確保 tasks.md 中每個項目都完成

# 6. 更新檢查清單
# 將完成的任務標記為 [x]
- [x] 1.1 Create Python virtual environment
- [x] 1.2 Add requirements.txt
...

# 7. 核准關卡
# 在提案審核通過前，不要開始實作
```

**本專案實作範例**：
```markdown
## 1. Environment Setup
- [x] 1.1 Create a Python 3.10+ virtual environment
- [x] 1.2 Add requirements.txt with dependencies
- [x] 1.3 Verify installation on Windows PowerShell

## 2. Data Acquisition & Preparation
- [x] 2.1 Download dataset to dataset/sms_spam_no_header.csv
- [x] 2.2 Validate schema (label,text) and handle headerless format
...
```

---

### Stage 3: 歸檔變更（Archiving Changes）

**部署後執行**：
```bash
# 1. 歸檔變更（移動到 archive/ 並更新 specs/）
openspec archive <change-id> --yes

# 實際操作：
# - 移動 changes/<name>/ → changes/archive/YYYY-MM-DD-<name>/
# - 合併 spec deltas 到 specs/ 目錄
# - 保留歷史記錄

# 2. 僅工具變更（不涉及功能規格）
openspec archive <change-id> --skip-specs --yes

# 3. 驗證歸檔結果
openspec validate --strict
```

---

## 🛠 常用指令

```bash
# 列出
openspec list                  # 活躍的變更
openspec list --specs          # 現有規格
openspec spec list --long      # 詳細規格列表

# 檢視
openspec show <change-id>      # 顯示變更詳情
openspec show <spec-id> --type spec   # 顯示規格

# 差異
openspec diff <change-id>      # 顯示規格差異

# 驗證
openspec validate <change-id>  # 驗證單一變更
openspec validate --strict     # 驗證所有規格

# 歸檔
openspec archive <change-id> --yes    # 非互動式歸檔
```

---

## 📝 本專案實例：SMS Spam Classifier

### 1. **已完成的變更**
```
openspec/changes/spam-email-classification/
├── proposal.md       # 目標：建立 SVM 基線模型
├── tasks.md          # 18/21 tasks（基線完成，Phase 2+ 保留）
└── specs/ml/spam-classifier/spec.md   # Delta：ADDED Requirements
```

### 2. **當前狀態**
```bash
$ openspec list
Changes:
  spam-email-classification     18/21 tasks
```

### 3. **未來變更範例**
若要新增 Logistic Regression 對比：
```bash
# 1. 建立新變更
mkdir -p openspec/changes/add-logistic-regression-comparison

# 2. 撰寫 proposal.md
# - 目標：實作 Logistic Regression 並與 SVM 對比
# - 範圍：新增 train_logreg.py、比較報告、Streamlit 模型切換

# 3. 撰寫 tasks.md
## 1. Model Implementation
- [ ] 1.1 Create train_logreg.py with similar interface
- [ ] 1.2 Train on same dataset with stratified split
...

# 4. 撰寫 spec delta
## ADDED Requirements
### Requirement: Logistic Regression Baseline
...

# 5. 驗證
openspec validate add-logistic-regression-comparison --strict

# 6. 實作 → 完成 → 歸檔
```

---

## 💡 與 AI 助手協作的最佳實踐

### 啟動新功能
```
您：「我想新增批量分類功能，可以上傳 CSV 檔案並批次預測。請建立 OpenSpec 變更提案。」

AI：
1. 查看 openspec/project.md 與 openspec list
2. 選擇 change-id: add-batch-classification
3. 建立 proposal.md、tasks.md、spec deltas
4. 執行 openspec validate add-batch-classification --strict
5. 回報結果並等待核准
```

### 實作功能
```
您：「請實作 add-batch-classification 的任務。」

AI：
1. 讀取 proposal.md 了解目標
2. 讀取 tasks.md 取得清單
3. 循序完成每個任務
4. 更新 tasks.md 標記進度
5. 完成後回報
```

### 歸檔變更
```
您：「批量分類功能已部署，請歸檔變更。」

AI：
執行 openspec archive add-batch-classification --yes
確認 specs/ 已更新
```

---

## 🎯 關鍵原則

1. **先規格，後實作**：不要在提案核准前寫程式
2. **小步前進**：每個變更聚焦單一能力
3. **可追溯**：所有決策都記錄在 proposal.md
4. **可驗證**：用 Scenarios 描述預期行為
5. **可歸檔**：完成後合併回 specs/ 成為真相來源

---

## 📚 延伸閱讀

- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec)
- [AGENTS.md 規範](https://agents.md/)
- 本專案：`openspec/AGENTS.md`（完整指令參考）
