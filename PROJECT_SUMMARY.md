# 專案開發紀錄 - 問題與解決方案

**專案**: SMS 垃圾訊息分類系統  
**日期**: 2025年10月22日  
**目的**: 記錄開發過程中遇到的問題、使用者指令、以及 AI 助手的調整方案

---

## 階段 1: OpenSpec 安裝與環境準備

### 使用者指令
```
"please install https://github.com/Fission-AI/OpenSpec.git"
```

### 遇到的問題
- 需要判斷是 git clone 還是 npm 套件

### AI 的調整
1. 檢查 GitHub 文件，確認為 npm 套件
2. 執行全域安裝：`npm install -g @fission-ai/openspec@latest`
3. 驗證安裝：`openspec --version` → 顯示 0.12.0
4. 初始化專案：`openspec init`

---

## 階段 2: 建立變更提案

### 使用者指令
```
"write the proposal, my goal is to spam email classification"
```

### 遇到的問題
- 使用者提到 Logistic Regression，但需要評估最佳方案

### AI 的調整
1. 執行 `openspec create spam-email-classification`
2. 決定使用 **Linear SVM** 作為基線（而非 LR）
   - 理由: SVM 在文本分類上通常表現更好
   - 策略: 先建立高準確率基線，Phase 2 再加入 LR 對比
3. 建立 proposal.md，規劃 TF-IDF + LinearSVC 架構
4. 建立 tasks.md，拆解為 21 個子任務

---

## 階段 3: Python 訓練管道實作

### 使用者指令
```
"i will used python to implement，你可以開始實作"
```

### 遇到的問題
- 需要下載資料集、建立虛擬環境、實作訓練腳本

### AI 的調整
1. 建立 Python 虛擬環境：`python -m venv .venv`
2. 建立 `requirements.txt` 列出依賴套件
3. 下載 SMS Spam Collection 資料集（5,574 筆）
4. 實作 `train.py` 訓練腳本：
   - 支援 CLI 參數（`--data`, `--out`, `--seed`, `--test-size`）
   - TF-IDF 特徵提取（ngram_range=(1,2), max_features=50000）
   - LinearSVC 訓練
   - 輸出模型、向量器、評估指標、混淆矩陣
5. 實作 `test_smoke.py` 快速驗證
6. 訓練結果：準確率 **98.39%**

---

## 階段 4: Git 版本控制

### 使用者指令
```
"help me to upload this project to github"
```

### 遇到的問題
- Windows 系統未安裝 Git
- 安裝後 PATH 未立即更新

### AI 的調整
1. 使用 winget 安裝 Git：`winget install --id Git.Git -e --source winget`
2. 發現 `git` 指令無法使用（PATH 問題）
3. **解決方案**: 使用完整路徑
   ```powershell
   & "C:\Program Files\Git\cmd\git.exe" init
   & "C:\Program Files\Git\cmd\git.exe" add .
   & "C:\Program Files\Git\cmd\git.exe" commit -m "Initial commit"
   ```
4. 建立 `.gitignore` 排除 `.venv/`, `artifacts/`, `dataset/`
5. 連結 GitHub 遠端倉庫並推送：
   ```powershell
   & "C:\Program Files\Git\cmd\git.exe" remote add origin https://github.com/pcchou102/HW3.git
   & "C:\Program Files\Git\cmd\git.exe" push -u origin main
   ```

---

## 階段 5: Streamlit 視覺化

### 使用者指令
```
"used streamlit to 可視化"
```

### 遇到的問題
- 需要建立網頁介面讓使用者輸入訊息並查看預測結果

### AI 的調整
1. 建立 `streamlit_app.py`
2. 實作功能：
   - 載入模型和向量器
   - 提供 `text_area` 輸入介面
   - 點擊按鈕後顯示預測結果（Ham/Spam）
3. 更新 `requirements.txt` 加入 `streamlit>=1.38.0`
4. 本地測試：`streamlit run streamlit_app.py` → 成功運行

---

## 階段 6: Streamlit Cloud 部署 - subprocess 問題

### 使用者指令
```
"幫我將成果利用 https://share.streamlit.io 進行展示"
```

### 遇到的問題
- Streamlit Cloud 環境沒有本地 `artifacts/` 資料
- 使用 subprocess 呼叫 `train.py` 訓練失敗

### 第一次嘗試（失敗）
```python
# streamlit_app.py
if not os.path.exists('artifacts/model.joblib'):
    subprocess.run(['python', 'train.py'], check=True)
```
**錯誤訊息**: `subprocess.CalledProcessError: Command failed`

### AI 的調整
1. 分析問題：Streamlit Cloud 的 subprocess 權限受限
2. **解決方案**: 將訓練邏輯內嵌到 `streamlit_app.py`
3. 建立 `ensure_artifacts()` 函數：
   ```python
   def ensure_artifacts():
       if os.path.exists('artifacts/model.joblib'):
           return
       
       st.info("🔄 首次啟動，正在訓練模型...")
       
       # 直接在此執行訓練（不用 subprocess）
       import pandas as pd
       from sklearn.feature_extraction.text import TfidfVectorizer
       from sklearn.svm import LinearSVC
       # ... 完整訓練邏輯 ...
       
       st.success("✅ 模型訓練完成！")
   ```
4. 建立 `.streamlit/config.toml` 配置檔
5. 提交更新：
   ```powershell
   & "C:\Program Files\Git\cmd\git.exe" add streamlit_app.py .streamlit/
   & "C:\Program Files\Git\cmd\git.exe" commit -m "fix: replace subprocess training with inline logic"
   & "C:\Program Files\Git\cmd\git.exe" push origin main
   ```

---

## 階段 7: UI 優化 - 範例按鈕

### 使用者指令
```
"產生範例的按鈕會有3個，一個產生ham，一個spam，另一個隨機生成"
```

### 遇到的問題
- 需要加入範例按鈕讓使用者快速測試

### AI 的調整
1. 準備範例資料池：
   ```python
   HAM_EXAMPLES = [
       "Hey, are we still meeting at 5pm?",
       "Thanks for the dinner last night",
       # ... 共 6 個範例
   ]
   
   SPAM_EXAMPLES = [
       "WINNER! You've won a $1000 gift card",
       "URGENT: Your account will expire",
       # ... 共 6 個範例
   ]
   ```
2. 新增三個按鈕：
   ```python
   col1, col2, col3 = st.columns(3)
   with col1:
       st.button("📧 Ham Example")
   with col2:
       st.button("🚨 Spam Example")
   with col3:
       st.button("🎲 Random Example")
   ```

---

## 階段 8: 按鈕狀態管理問題 ⚠️

### 使用者指令
```
"你做的按鈕並不會把文字放進 Enter an SMS message: 的格子裡"
```

### 遇到的問題
- 點擊按鈕後，`text_area` 的內容沒有更新

### 第一次嘗試（失敗）
```python
user_input = ""
if st.button("Ham Example"):
    user_input = random.choice(HAM_EXAMPLES)
    
user_input = st.text_area("Enter message:", value=user_input)
```
**問題**: Streamlit 每次互動都會重新執行整個腳本，變數會被重置

### 第二次嘗試（失敗）
```python
if st.button("Ham Example"):
    example = random.choice(HAM_EXAMPLES)
    st.text_area("Enter message:", value=example)
```
**問題**: widget 的渲染順序問題，按鈕點擊時 text_area 已渲染完成

### AI 的調整 ✅
使用 **session_state** 解決：
```python
# 初始化狀態
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

# 按鈕更新狀態並重新渲染
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📧 Ham Example"):
        st.session_state.input_text = random.choice(HAM_EXAMPLES)
        st.rerun()  # 關鍵！強制重新執行
        
with col2:
    if st.button("🚨 Spam Example"):
        st.session_state.input_text = random.choice(SPAM_EXAMPLES)
        st.rerun()
        
with col3:
    if st.button("🎲 Random Example"):
        all_examples = HAM_EXAMPLES + SPAM_EXAMPLES
        st.session_state.input_text = random.choice(all_examples)
        st.rerun()

# text_area 綁定 session_state
user_input = st.text_area(
    "Enter an SMS message:",
    value=st.session_state.input_text,
    key="input_text"  # 雙向綁定
)
```

**關鍵技術點**:
1. `session_state` 在重新執行間保持資料
2. `st.rerun()` 強制立即重新執行腳本
3. `key="input_text"` 讓 widget 直接綁定狀態

---

## 階段 9: 美化結果顯示

### 使用者指令
```
"可以了，不過我想做一些優化"
```

### 遇到的問題
- 預測結果太單調，希望更美觀

### AI 的調整
1. 加入信心度計算：
   ```python
   # 使用 decision_function 計算距離
   confidence_score = model.decision_function(X_input)[0]
   
   # 轉換為百分比（sigmoid 近似）
   confidence_pct = 1 / (1 + np.exp(-abs(confidence_score)))
   confidence_pct = round(confidence_pct * 100, 2)
   ```

2. 彩色結果顯示 + 進度條：
   ```python
   if prediction == 1:  # Spam
       st.error(f"🚨 **Spam** (Confidence: {confidence_pct}%)")
       st.progress(confidence_pct / 100)
   else:  # Ham
       st.success(f"✅ **Ham** (Confidence: {confidence_pct}%)")
       st.progress(confidence_pct / 100)
   ```

---

## 階段 10: 側邊欄優化

### 使用者指令
```
"將左側的Run Status & Metrics做優化嗎"
```

### 遇到的問題
- 側邊欄內容過多，佔用空間

### AI 的調整
使用可折疊區塊（`st.expander`）：
```python
with st.sidebar:
    with st.expander("📊 Model Performance", expanded=True):
        col1, col2 = st.columns(2)
        col1.metric("Accuracy", "98.39%")
        col2.metric("Precision", "96.56%")
        # ...
    
    with st.expander("📈 Confusion Matrix", expanded=False):
        if os.path.exists("artifacts/confusion_matrix.png"):
            st.image("artifacts/confusion_matrix.png")
    
    with st.expander("📦 Dataset Info", expanded=False):
        st.write("**Total Messages**: 5,574")
        st.write("**Ham**: 4,827 (86.6%)")
        st.write("**Spam**: 747 (13.4%)")
```

**優點**: 預設展開重要資訊，其他資訊可折疊節省空間

---

## 階段 11: 加入清除按鈕

### 使用者指令
（隱含需求：需要清空輸入框）

### AI 的調整
```python
if st.button("🗑️ Clear", use_container_width=True):
    st.session_state.input_text = ""
    st.rerun()  # 立即清空顯示
```

---

## 階段 12: OpenSpec 工作流程檢查

### 使用者指令
```
"我們整份專案有依照 OpenSpec workflow 的流程嗎，如果沒有，幫我做更新"
```

### 遇到的問題
- 檢查 `openspec/project.md` 發現大量 TBD（待填寫）
- 缺少中文工作流程指引文件

### AI 的調整

#### 1. 填寫 project.md
原本：
```markdown
## Purpose
TBD: Brief description...

## Tech Stack
- **Primary languages/frameworks**: TBD
```

修改為：
```markdown
## Purpose
本專案建立一個端到端的 **SMS 垃圾訊息分類系統**，使用機器學習
（Linear SVM + TF-IDF）達成高準確率（≈98.4%）...

## Tech Stack
- **Primary languages/frameworks**: 
  - **Python**: scikit-learn 1.7+, pandas 2.2+, numpy, scipy
  - **ML Pipeline**: TF-IDF vectorization + LinearSVC
  - **Web Framework**: Streamlit 1.50+
  - **Deployment**: Streamlit Community Cloud

## Development Conventions
- **Code Style**: PEP 8
- **Naming**: snake_case for functions/variables
- **Docstrings**: Google style

## Domain Context
### Spam vs Ham
- **Ham**: 正常訊息（非垃圾訊息）
- **Spam**: 垃圾訊息（詐騙、廣告、釣魚等）

### TF-IDF
將文字轉換為數值向量的技術...

## Known Constraints
- **Python Version**: ≥3.10
- **Memory**: 訓練需約 500MB RAM
- **Deployment**: Streamlit Cloud 限制 1GB 記憶體
```

#### 2. 建立 OPENSPEC_WORKFLOW.md
新增完整的中文工作流程指引，包含：
- OpenSpec 的三大階段說明
- 何時建立變更提案
- 如何實作與追蹤任務
- 如何歸檔完成的變更
- 本專案的實踐範例

#### 3. 提交更新
```powershell
& "C:\Program Files\Git\cmd\git.exe" add openspec/project.md OPENSPEC_WORKFLOW.md
& "C:\Program Files\Git\cmd\git.exe" commit -m "docs: complete OpenSpec workflow integration"
& "C:\Program Files\Git\cmd\git.exe" push origin main
```

---

## 總結

### 主要技術挑戰與解決

| 問題 | 使用者遇到的現象 | AI 的解決方案 |
|------|------------------|---------------|
| Git 未安裝 | `git` 指令無法識別 | 用 winget 安裝，使用完整路徑操作 |
| Streamlit Cloud subprocess | 訓練腳本執行失敗 | 改用內嵌訓練邏輯（inline） |
| 按鈕不更新輸入框 | 點擊範例按鈕無反應 | 使用 `session_state` + `st.rerun()` |
| 結果顯示單調 | 只有文字結果 | 加入信心度計算、彩色標籤、進度條 |
| 側邊欄過於擁擠 | 資訊過多難閱讀 | 使用 `st.expander` 可折疊區塊 |
| OpenSpec 文件不完整 | project.md 有 TBD 佔位符 | 填寫完整專案脈絡、建立中文指引 |

### Git 提交歷史

```bash
# 主要提交記錄
1. Initial commit: SMS spam classifier with SVM
2. Add Streamlit visualization app
3. fix: replace subprocess training with inline logic for Streamlit Cloud compatibility
4. feat: add example buttons and beautify results with confidence visualization
5. feat: optimize sidebar with collapsible sections and metrics
6. fix: update button state management with session_state and rerun
7. docs: complete OpenSpec workflow integration with filled project.md and workflow guide
```

### 最終成果

- ✅ 準確率 98.39% 的 SVM 分類器
- ✅ 具備範例按鈕、信心度顯示的 Streamlit 網頁應用
- ✅ Streamlit Cloud 可直接部署（自動訓練）
- ✅ 完整的 OpenSpec 變更提案與任務追蹤
- ✅ GitHub 倉庫: https://github.com/pcchou102/HW3.git

---

**文件版本**: 2.0  
**最後更新**: 2025-10-22  
**記錄重點**: 問題分析、使用者指令、AI 調整方案
