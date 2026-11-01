"""Run one bounded, fresh Hermes CLI content review; no new runtime service."""
import json
from pathlib import Path
import subprocess
import sys

lesson_path = Path(sys.argv[1])
lesson = json.loads(lesson_path.read_text(encoding='utf-8'))
prompt = '''你是本次课文的独立内容审查者，不是页面生产者。只审查下面提供的JSON。不要调用工具、读取Skill、文件、记忆或其他上下文，不要写文件，也不要委派。
逐题比较故事实际演出的行动和正确选项的决定。更换人名、物品或说法不代表新决定；引用对应故事原句。至少一道题应留下未被演出的应用决定，并有可信、有好意但缺少关键条件的干扰项。另一题可以回忆。不要只检查名词是否新出现。
同时检查：6-8岁孩子能否比较简短、同一决策点的选项；反馈有无虚构事实或错误赞扬。不因选项更长而认为更完整。不要改动学习目标，不输出总分。
只输出JSON：{"questions":[{"id":"q1","story_action_quote":"...","decision_already_enacted":true,"new_decision":"...","plausible_partial_option":"..."}],"has_valid_application":false,"readability_issues":[],"consistency_issues":[],"required_repairs":[]}
required_repairs必须定位具体题目、证据和需要改变的决定；没有问题就留空。不要要求每道题都迁移，也不要增加无关难度。
课文：
''' + json.dumps(lesson, ensure_ascii=False)
completed = subprocess.run(
    ['hermes', '--profile', 'frontend', 'chat', '--query-file', '-', '--oneshot', '-Q',
     '--ignore-rules', '--max-turns', '2', '--run-budget', '120', '--format', 'text'],
    input=prompt, text=True, capture_output=True, timeout=150, check=True,
)
review = json.loads(completed.stdout.strip())
assert isinstance(review['has_valid_application'], bool)
assert isinstance(review['questions'], list) and isinstance(review['required_repairs'], list)
review_path = lesson_path.with_name('content-review.json')
review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'review_file': str(review_path), 'review': review}, ensure_ascii=False))

