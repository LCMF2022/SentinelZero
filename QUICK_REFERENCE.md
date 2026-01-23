# CI/CD Quick Reference

Quick reference guide for developers working with SentinelZero CI/CD workflows.

## Workflow Files

| File | Purpose | Triggers |
|------|---------|----------|
| `.github/workflows/ci.yml` | Continuous Integration | Push to main/develop, PRs |
| `.github/workflows/data-update.yml` | Exploit DB Updates | Weekly schedule, manual |
| `.github/workflows/deploy.yml` | Deployment Pipeline | Push to main, tags, manual |
| `.github/dependabot.yml` | Dependency Management | Weekly schedule |

## Common Commands

### Manually Trigger Workflows

```bash
# Via GitHub UI:
# 1. Go to Actions tab
# 2. Select workflow
# 3. Click "Run workflow"
# 4. Choose branch and options
```

### Check Workflow Status

```bash
# View recent runs
gh run list --workflow=ci.yml

# View specific run details
gh run view <run-id>

# Download logs
gh run download <run-id>
```

## Workflow Conditional Execution

Workflows intelligently skip jobs when not applicable:

- **Python tests**: Only run when `.py` files exist
- **Node.js tests**: Only run when `package.json` exists
- **Deployment**: Only runs on specific branches/tags

## Deployment Environments

| Environment | Trigger | Purpose |
|-------------|---------|---------|
| Staging | Push to `main` | Testing in prod-like environment |
| Production | Tags `v*` or manual | Live deployment |

## Emergency Procedures

### Stop a Running Workflow

```bash
# Via CLI
gh run cancel <run-id>

# Via UI: Actions → Click run → Cancel workflow
```

### Manual Rollback

```bash
# Find last good commit
git log --grep="deploy-" --oneline

# Deploy that commit
git checkout -b hotfix-rollback <commit-sha>
git push origin hotfix-rollback
# Then trigger deployment workflow manually
```

## Getting Help

- 📖 Full documentation: [`docs/WORKFLOW_MAINTENANCE.md`](./WORKFLOW_MAINTENANCE.md)
- 🐛 Report issues: [GitHub Issues](https://github.com/myrosepetalbroker-maker/SentinelZero/issues)
- 💬 Ask questions: Create a discussion in the repository

## Monitoring

- **GitHub Actions Dashboard**: Repository → Actions
- **Dependabot**: Security → Dependabot
- **Security Alerts**: Security → Code scanning alerts

## Best Practices

✅ **DO**:
- Review Dependabot PRs weekly
- Test changes locally when possible
- Use descriptive commit messages
- Monitor workflow run times

❌ **DON'T**:
- Skip tests in production deployments
- Ignore security scanning results
- Commit secrets or credentials
- Override branch protection rules

---

For detailed information, see [`docs/WORKFLOW_MAINTENANCE.md`](./WORKFLOW_MAINTENANCE.md)
