# personal-workflow-rules
个人通用规则。改规则：编辑 rules.md（pstack 分工同时改 pstack-models.md），提交后在各处更新插件。
- SessionStart hook：把 rules.md 注入每个会话；~/.claude/rules/pstack-models.md 不存在时自动装上（已存在的本地文件不覆盖）。
- PreToolUse hook：提交门禁，默认 observe（只往 ~/.claude/verify-gate.log 记日志）；设置环境变量 VERIFY_GATE_MODE=enforce 后真正拦截，拦两次后放行。

安装：

```
/plugin install personal-workflow-rules --marketplace zhibo0502/personal-workflow-rules
```
