# Project Context

> Note: This file captures context your AI assistants will rely on. Fill in the TBD items so we align on the same constraints and conventions.

## Purpose
TBD – 請用 2–3 句描述專案目標、核心使用者與成功指標。

## Tech Stack
- OS/Env: Windows (PowerShell 5.1)
- Runtime/Tooling: Node.js v22.21.0, npm 10.9.4, OpenSpec CLI 0.12.0
- Editor/AI: VS Code + GitHub Copilot（本專案啟用 OpenSpec 工作流程）
- Primary languages/frameworks: TBD（請填：例如 TypeScript + React + Express）

## Project Conventions

### Code Style
- Formatter/Lint: 建議使用 Prettier + ESLint（若為 TS/JS）。
- 基本格式：2 空白縮排；保留分號（;）；單引號或專案既定規則（TBD）。
- 命名：kebab-case（檔案/資料夾）、camelCase（變數/函式）、PascalCase（型別/元件/類別）。

### Architecture Patterns
- 模組化、單一職責原則（SRP）。
- 清楚分層（例如：api/controllers/services/repositories 或前後端分離）。
- 具體落點與資料流約定：TBD（請簡述系統主路徑/邊界）。

### Testing Strategy
- 測試層級：單元（必備）、整合（視需要）、端到端（關鍵流程）。
- 覆蓋率目標：TBD（範例：語句/分支 ≥ 80%）。
- 工具：TBD（範例：Vitest/Jest、Playwright）。

### Git Workflow
- 分支策略：`main` 穩定分支；功能以 `feature/<short-kebab>` 建分支；熱修以 `hotfix/<short-kebab>`。
- 提交訊息：Conventional Commits（例如：`feat(ui): add search filter`）。
- PR 規範：需連結對應的 OpenSpec change（`openspec/changes/<id>`），描述影響範圍與風險。

## Domain Context
TBD – 請填寫與領域相關的關鍵概念、名詞定義、資料模型大致輪廓、常見使用情境。

## Important Constraints
- Node.js >= 20.19.0（已滿足）。
- 安全/法規/相容性限制：TBD（例如：GDPR、PII 資料處理、內網僅限存取）。
- 效能 SLA：TBD（例：P95 API < 300ms；峰值併發 X）。

## External Dependencies
- 第三方 API／系統：TBD（名稱、用途、授權/金鑰管理方式）。
- 資料庫／快取：TBD（例如：PostgreSQL、Redis；連線與遷移策略）。

