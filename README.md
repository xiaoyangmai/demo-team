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
    │   ├── SOUL.md
    │   └── skills/
    └── reviewer/
        ├── distribution.yaml
        ├── SOUL.md
        └── skills/
```

项目注册时提交仓库地址和 `project_id: demo-team`。控制服务负责创建或确认同名 Hermes project、Kanban board 和项目工作区；profile distribution 作为仓库中的角色定义分别维护。
