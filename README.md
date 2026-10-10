# 用 Mini 项目学习复杂架构

一个可复用的 Agent Skill：从真实源码提取一条端到端主流程，构建保留关键架构机制的可运行 mini 项目，让你通过运行、修改和对照源码理解复杂项目。

## 核心原则

缩减业务范围和部署成本，同时保留选定流程的模块职责、调用顺序、接口契约和关键状态变化。原项目涉及队列、重试、幂等或持久化时，明确哪些机制被保留，哪些被简化，以及简化带来的影响。

## 安装

将整个仓库克隆到你的 Agent 宿主配置的技能目录，目录名保留为 `learn-architecture-by-mini`。如果你的 Codex 环境使用 `~/.codex/skills`，可以执行：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/greedy-hat/learn-architecture-by-mini.git ~/.codex/skills/learn-architecture-by-mini
```

按宿主要求重新加载技能或启动新会话。不同宿主的技能搜索路径可能不同；以当前环境配置为准。仅把仓库链接贴进聊天不会自动完成安装，也不会授予访问私有源码的权限。

不支持技能安装的环境，可以直接将 [SKILL.md](SKILL.md) 与 [蓝图](references/blueprint.md) 作为任务指导提供给 Agent。

## 使用

安装后提供要学习的项目路径或仓库链接，最好同时指定版本和学习目标：

```text
使用 $learn-architecture-by-mini 学习 <仓库链接或本地路径>。
版本：<分支或 commit>。
重点理解：任务提交、队列消费、状态更新和结果查询。
保留主流程，构建可本地运行的 mini 项目，并演示正常与失败路径。
```

也可以不指定入口，由 Agent 根据源码选择代表性的流程。没有源码时，技能会先请求来源，不会猜测真实架构。

## 工作流程与交付

1. 确定学习切片，记录原项目版本。
2. 沿真实调用链追踪源码，整理关键不变量。
3. 建立原模块与 mini 模块的映射和简化清单。
4. 在独立目录逐段实现，提供运行命令与可观察日志。
5. 运行正常流程和关键失败场景，验证状态与副作用。
6. 交付代码、架构图、源码证据、运行结果及递进练习。

本仓库提供学习方法和蓝图；具体 mini 项目在使用技能时根据目标源码生成。无法执行原项目时，必须明确区分源码契约检查与实际行为验证。

## 仓库结构

| 路径 | 用途 |
|---|---|
| `SKILL.md` | Agent 执行指令及触发描述 |
| `agents/openai.yaml` | 显示名称、简介和默认提示 |
| `references/blueprint.md` | 架构映射、不变量和验证记录模板 |
| `scripts/validate_skill.py` | 检查元数据、目录、引用和界面配置 |
| `.github/workflows/validate.yml` | 推送和 PR 时自动运行格式校验 |
| `requirements-dev.txt` | 校验工具的开发依赖 |

## 修改与校验

Python 3.10 或更高版本：

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_skill.py
```

修改流程时同步更新蓝图和界面提示。格式校验不能证明教学效果或生成项目的架构保真度；后者需要针对实际源码运行场景验证。提报问题时请附学习目标、原项目版本和实际输出，避免上传凭据。

## 许可证

目前尚未指定开源许可证。仓库公开可见不代表已经授予开源使用、修改或再分发许可。
