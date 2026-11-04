# drill-pricing

一次性靶场仓库，用于演练「Agent 交付 + 人工证据审查」。无业务价值，随时可删。

金额一律用整数「分」表示，规格与已知问题见 README.md。

## 工作方式

- 交付形式：在独立 worktree 分支上改动，push 后开 PR，**等人审查**。
- PR 正文规范与禁止事项见 `.qoder/rules/pr-evidence.md`（always_on 规则，已由
  `.qoder/hooks/pr_evidence.py` 门禁强制）。
- `gh pr merge` / `gh pr review` / `git push --force` / `git reset --hard` 已被
  `.qoder/settings.json` 的 `permissions.deny` 拒绝，不要尝试绕过。

## 跑测试

```
python -m unittest discover -s tests
```
