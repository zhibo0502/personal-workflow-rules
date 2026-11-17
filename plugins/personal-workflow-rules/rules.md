# 我的通用规则（来自 personal-workflow-rules 插件，每个会话都适用）

## 验证规则
- 同一项检查（测试、类型检查、lint、verify skill）连续三轮修不好，就停下来报告：失败的是哪项检查、试过哪些办法、你认为根因是什么。不要继续硬修。
- 测试时过时不过（flaky）时：不许跳过，不许加 sleep 或调大超时来掩盖，不许重跑到通过。先找根因并修好；找不到根因就删掉这个测试，并在提交说明里写明原因。
- 不要为了让改动通过检查，去修改评判它的检查：测试断言、verify skill、REVIEW.md、CI 门禁配置、这份规则。确实需要改的，单独提出来，说明理由，等用户确认。
- 提交之前先运行项目的 verify skill（`.claude/skills/verify*`），把怎么验证的写进提交说明。没有验证就写 `Verified: none`。

## pstack 角色分工（等同 ~/.claude/rules/pstack-models.md；本地也有这个文件时，以本地文件为准）
# pstack model configuration. One line per role.
# defaults: 3
# budget: small (medium)
feature, refactoring: opus medium
bug-fix: opus medium
perf-issue: opus medium
hillclimb: sonnet high
judgment and prose: opus medium
arena runners: opus medium, sonnet high, haiku high
arena cross-judge pool: sonnet high
swarm workers: haiku high
interrogate reviewers: opus medium, sonnet high, haiku high
