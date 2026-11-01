# demo-team

这是一个 Hermes 多 profile 团队项目模板。

```text
Git 项目:    demo-team
Hermes 项目: demo-team
Kanban:      demo-team
Profiles:    architect, backend, frontend, reviewer
```

目录关系：

```text
demo-team/
├── AGENTS.md
├── .gitignore
└── profiles/
    ├── architect/
    │   ├── distribution.yaml
    │   ├── SOUL.md
    │   └── skills/
    ├── backend/
    │   ├── distribution.yaml
    │   ├── SOUL.md
    │   └── skills/
    ├── frontend/
    │   ├── distribution.yaml
    │   ├── config.yaml
    │   ├── SOUL.md
    │   └── skills/
    └── reviewer/
        ├── distribution.yaml
        ├── SOUL.md
        └── skills/
```

项目注册时提交仓库地址和 `project_id: demo-team`。控制服务负责创建或确认同名 Hermes project、Kanban board 和项目工作区；profile distribution 作为仓库中的角色定义分别维护。

frontend 的 `config.yaml` 禁用 `code_execution` 工具集，保留普通文件和终端工具。当前部署在无人值守模式下会拒绝 `execute_code`，因此不向模型暴露这个不可用入口。

已有 profile 的 `config.yaml` 会被原生 distribution update 保留，普通 `gateway/refresh` 不会覆盖它。发布这个设置时，先提交并同步 Git，再在已授权的部署管理步骤中执行一次 `hermes --profile frontend config set agent.disabled_toolsets '["code_execution"]'`，随后执行现有 `gateway/refresh`。验收 `/p/frontend/v1/toolsets` 中 `code_execution.enabled=false`、其他工具集未变，以及新会话的实际交付。不要用关闭审批或整体覆盖配置来代替这项迁移。
