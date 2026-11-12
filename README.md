# agent-residue

**清理 AI coding agent 留下的垃圾。** 一个命令，看清 Claude Code、Codex、Cursor、Qoder、WorkBuddy 这些工具在你机器上占了多少、哪些能安全删。

- 支持 **22 种** AI coding agent，Windows / macOS / Linux 通用
- **默认只读**，`clean` 也默认只隔离不删除，一行命令可回滚
- 每一类路径都标了 **Tier 0–3**：凭据和会话永远不动，缓存随便清
- 单一 Python 文件 + 一份 JSON 路径表，**零第三方依赖**

```console
$ agent-residue scan

agent-residue 0.2.0   home=~   selected tiers: 1   reclaimable: 4.8 GB

AGENT                TIER        SIZE   FILES  LAST       PATH
----------------------------------------------------------------
Codex CLI               1     2.1 GB   41203  2026-10-09 ~/.codex/.tmp
Trae                    1   712.4 MB    2999  2026-09-13 ~/Library/Application Support/Trae/logs
Claude Code             1    40.3 MB       2  2026-08-06 ~/.claude/downloads
...
```

## 为什么需要它

每个 agent 都会在 home 目录堆东西：日志、缓存、下载的二进制、会话数据库。它们没有统一的清理入口，卸载之后目录照样留着。手动删又怕删掉聊天记录或登录态。

`agent-residue` 把这件事变成一张带分级的表：**看得到、删得掉、撤得回**。

## 支持的 agent

| Agent | 厂商 | 路径来源 |
|---|---|---|
| Claude Code | Anthropic | 实测 |
| Codex CLI | OpenAI | 实测 |
| Qoder | Alibaba | 实测 |
| WorkBuddy | Tencent | 实测 |
| CodeBuddy | Tencent | 实测 |
| Trae | ByteDance | 实测 |
| Kimi Work | Moonshot | 实测 |
| Cursor | Anysphere | 文档 |
| Windsurf | Codeium | 文档 |
| Gemini CLI | Google | 文档 |
| GitHub Copilot CLI | GitHub | 文档 |
| Cline | Cline Bot | 文档 |
| Roo Code | Roo Veterinary | 文档 |
| Aider | Aider | 文档 |
| Continue | Continue | 文档 |
| OpenCode | SST | 文档 |
| Zed | Zed Industries | 文档 |
| Amp | Sourcegraph | 文档 |
| Factory Droid | Factory | 文档 |
| Crush | Charm | 文档 |
| Goose | Block | 文档 |
| Qwen Code | Alibaba | 文档 |

「实测」= 在真实安装上确认过目录结构，默认参与扫描。
「文档」= 路径来自官方文档或社区，默认**不**参与扫描，需要 `--include-unverified` 才生效——避免猜错路径误删。

每个 agent 的完整路径和层级见 [docs/agents.md](docs/agents.md)，或运行 `agent-residue list`。

## 安装

```bash
pipx install git+https://github.com/0721gaoshoua/agent-residue
# 或者
git clone https://github.com/0721gaoshoua/agent-residue
cd agent-residue && pip install -e .
```

不想安装也可以直接跑：

```bash
python -m agent_residue scan
```

## 用法

```bash
# 看所有 agent 的路径表
agent-residue list

# 扫描（只读，什么都不改）
agent-residue scan
agent-residue scan -a claude-code,codex --tier 1,2
agent-residue scan --include-unverified

# 清理：默认移入 ./.agent-trash/<时间戳>/，写 manifest
agent-residue clean
agent-residue clean --tier 1,2
agent-residue clean -a qoder --exclude file-history

# 永久删除（不可逆，必须显式 --yes）
agent-residue clean --tier 1 --purge --yes

# 撤销上一批
agent-residue restore .agent-trash/20260101-120000/manifest.json
```

常用参数：

| 参数 | 作用 |
|---|---|
| `-a, --agents` | 逗号分隔的 agent id，`all` 表示全部 |
| `--tier` | `0,1,2,3` 的组合，默认 `1` |
| `--include-unverified` | 纳入「文档」来源的 agent |
| `--exclude` | 按标签排除，可重复，支持 `*` |
| `--older-than DAYS` | 只处理 N 天前的目标 |
| `--home DIR` | 指向别的家目录（测试用） |
| `--json` | 机器可读输出 |
| `--purge --yes` | 真删 |

退出码：`0` 成功，`1` 有单项失败，`2` 缺少 `--yes`，`3` 有 agent 进程在跑。

## 分层

| Tier | 内容 | 删了会怎样 |
|---|---|---|
| 0 | 凭据、`settings.json`、会话数据库、正在使用的组件 | **永不删除**，只出现在报表里 |
| 1 | 日志、缓存、崩溃转储、更新包、shell 快照 | 无感，自动重建 |
| 2 | 二进制、插件、扩展、内嵌 app 包 | 下次启动重新下载 |
| 3 | 会话、项目、记忆、历史 | 等于删聊天记录 |

默认只清 Tier 1。Tier 3 必须手动指定。

## 安全设计

- **默认 dry-run**：只有 `clean` 会写盘，且默认隔离。
- **路径守卫**：只允许操作家目录下、深度 ≥ 4 的路径；拒绝根目录、家目录本身；跳过符号链接。
- **进程检测**：目标 agent 正在运行就整体跳过（`--force` 覆盖）。
- **单项失败不中断**：被占用的目录记录后继续，不影响其余目标。
- **回滚**：隔离区带 `manifest.json`，`restore` 原样搬回。

## 扩展

`agent_residue/targets.json` 是唯一事实来源：

```json
{
  "id": "my-agent",
  "name": "My Agent",
  "vendor": "Someone",
  "processes": ["myagent"],
  "verified": false,
  "paths": [
    ["~/.myagent/logs", 1, "logs"],
    ["~/.myagent/sessions", 3, "sessions"]
  ]
}
```

路径支持 `~`、`%APPDATA%`、`$HOME` 等变量；变量不存在时整条路径被跳过，所以同一份表在三个平台上都能用。

## English

**agent-residue** finds and cleans leftovers (caches, logs, temp dirs, rebuildable components) left behind by 22 AI coding agents. Read-only by default, quarantine instead of delete, one-command rollback. Tier 0 (credentials, settings, session databases) is never touched.

```bash
pipx install git+https://github.com/0721gaoshoua/agent-residue
agent-residue scan                 # report only
agent-residue clean --tier 1       # quarantine, reversible
agent-residue restore <manifest>   # undo
```

## 免责声明

路径基于各工具的真实安装结构整理，但版本迭代可能改变目录布局。所有清理默认隔离、可回滚；请先 `scan` 确认再执行。因路径变更导致的误删不在保证范围内。

## License

MIT
