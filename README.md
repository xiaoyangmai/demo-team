# demo-team

这是一个使用 Hermes 执行、DSPy + GEPA 优化真实 Skill 的多 profile 项目。

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

## 所有权

- `profiles/` 是 Hermes 原生角色、distribution、Skill 的发布源。当前优化目标是 frontend 的 `illustrated-comic-delivery/SKILL.md` 正文；其自带的页面模板和打包脚本在搜索期间冻结。
- `harness/dspy_project.py` 定义任务协议、远端取证要求、浏览器检查、独立模型评分和采纳规则。它不生成候选，不实现搜索算法。
- [Self-Evolution fork](https://github.com/xiaoyangmai/hermes-agent-self-evolution) 的 `hermes-evolve` 使用 DSPy GEPA 生成候选，并把优化后的 `Predict.signature.instructions` 原样写入实际 Skill，提交、推送、发布、运行和收集证据。
- LLMHub control-plane 只做 Git 接入/同步、环境准备、profile 发布、运行结果与产物登记下载。任务执行属于 Hermes Gateway；评分和采纳属于 Self-Evolution 与本项目的评估协议。

## 环境和运行

本地安装本项目 `pyproject.toml` 声明的依赖（含 Pillow），使用 Python 3.11+、Git 和 Edge。`harness/dspy_project.py` 使用真实浏览器测试离线页面，不在生产 Hermes 容器里安装浏览器。远端使用已配置的 `image_generate` 和 `vision_analyze`。凭据通过环境变量提供，见引擎 README。

远端 `ops/check-environment` 返回实际 Git revision、frontend 已安装文件的 SHA-256 和配置检查。`ops/install-environment` 通过原生 Hermes CLI 关闭后台 Skill review、默认开启的 curator，以及无人值守环境不支持的 `code_execution`；两个脚本使用受控运行环境提供的 `HERMES_HOME`。普通 distribution update 保留 config.yaml，因此这些设置由受控 prepare 明确应用，检查会在 curator 未明确关闭时拒绝就绪。实验使用独立 Hermes home、checkout 与 Gateway；生产任务总并发不超过四个，运行期间不切换所在实例的候选。

在仓库外创建私有 cases.json，包含非空 `train`、`validation`、`test` 列表，每项为 `{ "id": "唯一标识", "topic": "教学目标与场景" }`。重复测量用不同 id。训练/验证供 GEPA 搜索，test 只用于最后一次采纳比较；不要把私有验收案例提交到生产仓库。

```powershell
hermes-evolve --repo D:\demo-team --dataset D:\experiments\cases.json --output D:\experiments\run-001
```

先提交项目修改。引擎将候选提交推送到实验分支，并通过 control-plane 按 SHA 发布到实验实例；通过最终验收的候选才进入生产发布流程。一个优化进程独占实验实例：进程内控制并发，不提供跨客户端租约。复用同一个 output 可恢复同一冻结实验；改案例、评估器、模型或预算要使用新目录。

## 评估与结束

产物是四页真实插画漫画、两道互动题和具体行动小结，含离线 HTML、lesson.json 与四张图片。固定模板提供翻页、答题、重试、完成页和重置；Hermes 负责内容和插画。自动检查图片解码/不重复、两种宽度的完整阅读与答题流程，以及文本一致性、阅读预算和明显的选项长度线索。

两个独立评估上下文各自观察实际插画和可见字幕，再检查教学、可读性、视觉叙事、一致性、题目和结尾；不会共享第三方预先生成的读图结论。实际插画与移动端截图都会传给评估器，不只传 JSON。校准包括文本正反例、重复例，以及 `evals/calibration/bridge.jpg` 的真实图像正反例、合理省略和形变；这些公开校准材料不是隐藏验收题。评分不接收候选指令或生产者自评。阅读字数是本项目约定，不是已验证的儿童学习规律。

质量分为 60% 最弱维度加 40% 各维平均（归一化到0–1）。实际轨迹超过5次生图尝试时保留搜索质量分和明确的预算失败反馈，但最终验收失败；预算合规本身不能作为质量提升。这是事后验收门槛，提示词中的次数约定不是计费层硬限制。两次评审使用独立上下文并发调用，不增加评审数量或选择性重试。

采纳要求所有留出用例各维度达到3/4且未超预算、每对用例各维度均不退步、平均搜索分数和纯质量分均至少提升0.03。未达到则恢复基线并验证实际生效。同模型的独立上下文仍有相关偏差，分数不能证明真实儿童学习或付费意愿。旧学习页实验与当前漫画协议不同，不直接比较分数。

每次实验保留编译后的 `program.json`、候选 Skill、GEPA 搜索状态、Git/部署回执、Skill 加载轨迹、下载文件及校验值、浏览器截图、独立评分、采纳决定和最终发布回执。实验产物与私有用例放仓库外。以前人工规定轮次的配置已由此流程替代。
