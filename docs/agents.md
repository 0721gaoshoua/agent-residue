# 支持的 agent 与路径表

本文件由 `agent_residue/targets.json` 生成，改动请直接改 JSON。

**verified** = 在本机实测过该目录结构；**unverified** = 路径来自官方文档/社区，需 `--include-unverified` 才会被扫描。

## claude-code — Claude Code（Anthropic） · verified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `~/.claude/downloads` | downloads |
| 1 | `~/.claude/cache` | cache |
| 1 | `~/.claude/logs` | logs |
| 1 | `~/.claude/debug` | debug logs |
| 1 | `~/.claude/shell-snapshots` | shell snapshots |
| 1 | `~/.claude/statsig` | statsig cache |
| 1 | `~/.claude/session-env` | session env |
| 1 | `~/.claude/ide` | ide lockfiles |
| 2 | `~/.claude/plugins` | plugins |
| 3 | `~/.claude/backups` | backups |
| 3 | `~/.claude/projects` | conversations (jsonl) |
| 3 | `~/.claude/todos` | todos |
| 3 | `~/.claude/file-history` | edit history |
| 3 | `~/.claude/history.jsonl` | prompt history |
| 3 | `~/.claude.json` | app state |
| 0 | `~/.claude/settings.json` | settings |
| 0 | `~/.claude/.credentials.json` | credentials |
| 1 | `%APPDATA%/Claude/Cache` | desktop cache |
| 1 | `%APPDATA%/Claude/Code Cache` | desktop code cache |
| 1 | `%APPDATA%/Claude/GPUCache` | desktop gpu cache |
| 1 | `~/Library/Application Support/Claude/Cache` | desktop cache |
| 1 | `~/Library/Application Support/Claude/Code Cache` | desktop code cache |

## codex — Codex CLI（OpenAI） · verified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `~/.codex/.tmp` | temp workspace |
| 1 | `~/.codex/tmp` | temp |
| 1 | `~/.codex/cache` | cache |
| 1 | `~/.codex/log` | logs |
| 2 | `~/.codex/plugins` | plugins |
| 3 | `~/.codex/sessions` | sessions |
| 3 | `~/.codex/archived_sessions` | archived sessions |
| 3 | `~/.codex/history.jsonl` | history |
| 0 | `~/.codex/auth.json` | credentials |
| 0 | `~/.codex/config.toml` | config |

## qoder — Qoder（Alibaba） · verified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `~/.qoder/logs` | logs |
| 1 | `~/.qoder/tmp` | temp |
| 1 | `~/.qoder/.cache` | cache |
| 1 | `~/.qoder/shell-snapshots` | shell snapshots |
| 1 | `~/.qoder/ipc` | stale ipc endpoints |
| 2 | `~/.qoder/plugins` | plugins |
| 2 | `~/.qoder/skills` | bundled skills |
| 3 | `~/.qoder/file-history` | edit history |
| 3 | `~/.qoder/projects` | per-project sessions |
| 3 | `~/.qoder/memory` | memory |
| 0 | `~/.qoder/.auth` | credentials |
| 0 | `~/.qoder/settings.json` | settings |
| 0 | `~/.qoder/browser-connector` | chrome native host (live) |
| 0 | `~/.qoder/state.json` | state |
| 1 | `%APPDATA%/com.qoder.app.stable/Cache` | electron cache |
| 1 | `%APPDATA%/com.qoder.app.stable/Code Cache` | electron code cache |
| 1 | `%APPDATA%/com.qoder.app.stable/GPUCache` | electron gpu cache |
| 1 | `%APPDATA%/com.qoder.app.stable/Crashpad` | crash dumps |
| 1 | `%APPDATA%/com.qoder.app.stable/logs` | electron logs |
| 3 | `%APPDATA%/com.qoder.app.stable/main.sqlite` | session database |
| 0 | `%APPDATA%/com.qoder.app.stable/auth.v1.dat` | credentials |
| 1 | `%LOCALAPPDATA%/qoder-updater` | update packages |

## workbuddy — WorkBuddy（Tencent） · verified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `~/.workbuddy/logs` | legacy cli logs |
| 1 | `~/.workbuddy-ai/logs` | logs |
| 1 | `~/.workbuddy-ai/cache` | cache |
| 1 | `~/.workbuddy-ai/traces` | agent traces |
| 1 | `~/.workbuddy-ai/audit-log` | audit log |
| 1 | `~/.workbuddy-ai/clipboard-images` | clipboard images |
| 1 | `~/.workbuddy-ai/shell-snapshots` | shell snapshots |
| 1 | `~/.workbuddy-ai/pending-telemetry` | pending telemetry |
| 2 | `~/.workbuddy-ai/blobs` | blob cache |
| 2 | `~/.workbuddy-ai/changes-detail` | diff cache |
| 2 | `~/.workbuddy-ai/changes-index` | diff index |
| 2 | `~/.workbuddy-ai/binaries` | toolchain binaries |
| 2 | `~/.workbuddy-ai/plugins` | plugins |
| 2 | `~/.workbuddy-ai/app` | embedded app |
| 2 | `~/.workbuddy-ai/external-packages` | external packages |
| 2 | `~/.workbuddy-ai/connectors-marketplace` | marketplace cache |
| 3 | `~/.workbuddy-ai/file-history` | edit history |
| 3 | `~/.workbuddy-ai/projects` | project sessions |
| 3 | `~/.workbuddy-ai/workspace` | workspace snapshots |
| 3 | `~/.workbuddy-ai/sessions` | sessions |
| 3 | `~/.workbuddy-ai/memory` | memory |
| 3 | `~/.workbuddy-ai/storage` | conversation metadata |
| 3 | `~/.workbuddy-ai/workbuddy.db` | main database |
| 3 | `~/WorkBuddy AI` | task outputs |
| 0 | `~/.workbuddy-ai/security` | threat database |
| 0 | `~/.workbuddy-ai/settings.json` | settings |
| 1 | `%LOCALAPPDATA%/@genieworkbuddy-desktop-updater` | update packages |

## codebuddy — CodeBuddy（Tencent） · verified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `~/.codebuddy/logs` | logs |
| 1 | `~/.codebuddy/diagnostics` | diagnostics |
| 2 | `%LOCALAPPDATA%/CodeBuddyExtension` | vscode extension |

## trae — Trae（ByteDance） · verified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `~/.trae/trae-browser-screenshots` | browser screenshots |
| 1 | `%APPDATA%/Trae/logs` | electron logs |
| 1 | `%APPDATA%/Trae/Cache` | electron cache |
| 1 | `%APPDATA%/Trae/Code Cache` | electron code cache |
| 1 | `%APPDATA%/Trae/GPUCache` | electron gpu cache |
| 1 | `~/Library/Application Support/Trae/logs` | electron logs |
| 1 | `~/.config/Trae/logs` | electron logs |
| 2 | `~/.trae/extensions` | installed extensions (reinstall needed) |
| 3 | `~/.trae/memory` | memory |

## kimi-work — Kimi Work（Moonshot） · verified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `~/.kimi-work/logs` | logs |
| 2 | `~/.kimi-work/bin` | toolchain binaries |

## cursor — Cursor（Anysphere） · unverified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `%APPDATA%/Cursor/Cache` | electron cache |
| 1 | `%APPDATA%/Cursor/Code Cache` | electron code cache |
| 1 | `%APPDATA%/Cursor/GPUCache` | electron gpu cache |
| 1 | `%APPDATA%/Cursor/CachedData` | cached data |
| 1 | `%APPDATA%/Cursor/Crashpad` | crash dumps |
| 1 | `%APPDATA%/Cursor/logs` | logs |
| 1 | `~/Library/Application Support/Cursor/Cache` | electron cache |
| 1 | `~/Library/Application Support/Cursor/Code Cache` | electron code cache |
| 1 | `~/Library/Application Support/Cursor/logs` | logs |
| 1 | `~/.config/Cursor/Cache` | electron cache |
| 1 | `~/.config/Cursor/logs` | logs |
| 2 | `~/.cursor/extensions` | installed extensions |
| 3 | `%APPDATA%/Cursor/User/globalStorage` | global storage |
| 3 | `%APPDATA%/Cursor/User/workspaceStorage` | workspace storage |
| 0 | `%APPDATA%/Cursor/User/settings.json` | settings |

## windsurf — Windsurf（Codeium） · unverified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `%APPDATA%/Windsurf/Cache` | electron cache |
| 1 | `%APPDATA%/Windsurf/Code Cache` | electron code cache |
| 1 | `%APPDATA%/Windsurf/GPUCache` | electron gpu cache |
| 1 | `%APPDATA%/Windsurf/logs` | logs |
| 1 | `~/Library/Application Support/Windsurf/Cache` | electron cache |
| 1 | `~/Library/Application Support/Windsurf/logs` | logs |
| 1 | `~/.config/Windsurf/Cache` | electron cache |
| 3 | `~/.codeium/windsurf/memories` | memories |

## gemini-cli — Gemini CLI（Google） · unverified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `~/.gemini/tmp` | temp |
| 1 | `~/.gemini/logs` | logs |
| 3 | `~/.gemini/history` | history |
| 0 | `~/.gemini/settings.json` | settings |
| 0 | `~/.gemini/oauth_creds.json` | credentials |

## copilot-cli — GitHub Copilot CLI（GitHub） · unverified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `~/.copilot/logs` | logs |
| 3 | `~/.copilot/history` | history |
| 0 | `~/.copilot/config.json` | config |

## cline — Cline（Cline Bot） · unverified

| Tier | 路径 | 说明 |
|---|---|---|
| 3 | `%APPDATA%/Code/User/globalStorage/saoudrizwan.claude-dev` | tasks and conversations |
| 3 | `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev` | tasks and conversations |
| 3 | `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev` | tasks and conversations |

## roo-code — Roo Code（Roo Veterinary） · unverified

| Tier | 路径 | 说明 |
|---|---|---|
| 3 | `%APPDATA%/Code/User/globalStorage/rooveterinaryinc.roo-cline` | tasks and conversations |
| 3 | `~/Library/Application Support/Code/User/globalStorage/rooveterinaryinc.roo-cline` | tasks and conversations |
| 3 | `~/.config/Code/User/globalStorage/rooveterinaryinc.roo-cline` | tasks and conversations |

## aider — Aider（Aider） · unverified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `~/.aider/caches` | caches |
| 1 | `~/.aider/analytics` | analytics |
| 0 | `~/.aider.conf.yml` | config |

## continue — Continue（Continue） · unverified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `~/.continue/index` | codebase index |
| 1 | `~/.continue/logs` | logs |
| 3 | `~/.continue/sessions` | sessions |
| 0 | `~/.continue/config.json` | config |

## opencode — OpenCode（SST） · unverified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `~/.local/share/opencode/log` | logs |
| 1 | `%LOCALAPPDATA%/opencode/log` | logs |
| 3 | `~/.local/share/opencode/storage` | session storage |
| 0 | `~/.config/opencode` | config |

## zed — Zed（Zed Industries） · unverified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `%APPDATA%/Zed/logs` | logs |
| 1 | `%APPDATA%/Zed/Cache` | cache |
| 1 | `~/Library/Application Support/Zed/logs` | logs |
| 1 | `~/.local/share/zed/logs` | logs |

## amp — Amp（Sourcegraph） · unverified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `~/.amp/logs` | logs |
| 1 | `~/.amp/cache` | cache |
| 3 | `~/.amp/sessions` | sessions |

## droid — Factory Droid（Factory） · unverified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `~/.factory/logs` | logs |
| 1 | `~/.factory/cache` | cache |
| 3 | `~/.factory/sessions` | sessions |

## crush — Crush（Charm） · unverified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `~/.local/share/crush/logs` | logs |
| 1 | `~/.local/share/crush/cache` | cache |
| 0 | `~/.config/crush` | config |

## goose — Goose（Block） · unverified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `~/.local/share/goose/logs` | logs |
| 0 | `~/.config/goose` | config |

## qwen-code — Qwen Code（Alibaba） · unverified

| Tier | 路径 | 说明 |
|---|---|---|
| 1 | `~/.qwen/tmp` | temp |
| 1 | `~/.qwen/logs` | logs |
| 3 | `~/.qwen/history` | history |
| 0 | `~/.qwen/settings.json` | settings |

