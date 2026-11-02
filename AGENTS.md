# demo-team agent rules

- Kanban 是任务、依赖和状态的来源。
- Git 是代码、提交和评审的来源。
- Architect、backend、frontend、reviewer 是不同的 Hermes profile。
- Profile 更新、Kanban 更新、Git 项目更新和 Gateway 重启是不同操作。
- 不在仓库中保存 API key、Token 或其他凭据。
- 普通开发任务完成前留下可检查的提交、测试结果和任务状态。评估运行只写指定的结果目录，不提交代码、不修改 profile 或 Skill。
- DSPy 实验由 Self-Evolution 驱动；`harness/dspy_project.py` 是本项目任务和自动验收规则的唯一来源。不要在 control-plane 再实现评分、候选生成或采纳逻辑。
- 优化期间只允许改变选定 Skill 正文。修改模型、工具、其他 profile 或评分标准必须结束当前实验并建立新基线。
