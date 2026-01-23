# Workflow Maintenance Guide

## Overview

This document provides comprehensive guidance for maintaining the CI/CD workflows in the SentinelZero project. Our workflow system is designed to be modular, maintainable, and secure, with built-in rollback mechanisms and automated dependency management.

## Table of Contents

1. [Workflow Architecture](#workflow-architecture)
2. [Workflow Details](#workflow-details)
3. [Trigger Points](#trigger-points)
4. [Environment Setup](#environment-setup)
5. [Dependency Management](#dependency-management)
6. [Rollback Procedures](#rollback-procedures)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

---

## Workflow Architecture

Our CI/CD system consists of three main workflows:

```
┌─────────────────────────────────────────┐
│         CI/CD System                     │
├─────────────────────────────────────────┤
│                                          │
│  1. Continuous Integration (ci.yml)     │
│     - Code validation                   │
│     - Testing (Python/Node.js)          │
│     - Security scanning                 │
│                                          │
│  2. Data Updates (data-update.yml)      │
│     - Scheduled exploit DB updates      │
│     - Automated PR creation             │
│                                          │
│  3. Deployment (deploy.yml)             │
│     - Pre-deployment checks             │
│     - Deployment execution              │
│     - Automatic rollback on failure     │
│                                          │
└─────────────────────────────────────────┘
```

### Design Principles

- **Modularity**: Each workflow has a single, clear responsibility
- **Conditional Execution**: Jobs only run when relevant files exist
- **Security-First**: Built-in security scanning and safe dependency management
- **Fail-Safe**: Automatic rollback mechanisms for failed deployments
- **Minimal Maintenance**: Automated updates via Dependabot

---

## Workflow Details

### 1. Continuous Integration (`ci.yml`)

**Purpose**: Validate code quality, run tests, and perform security scans

**Jobs**:
- `validate`: Basic repository structure and documentation checks
- `test-python`: Python linting and testing (conditional)
- `test-nodejs`: Node.js linting and testing (conditional)
- `security-scan`: Trivy vulnerability scanning

**Key Features**:
- Conditional job execution based on file presence
- Multi-language support (Python, Node.js)
- Integrated security scanning with SARIF upload
- Caching for faster builds

### 2. Automated Data Updates (`data-update.yml`)

**Purpose**: Automatically update the historical exploit database

**Jobs**:
- `update-exploit-database`: Fetch and process exploit data, create PR

**Key Features**:
- Weekly scheduled execution
- Manual trigger option via `workflow_dispatch`
- Automatic PR creation for data updates
- Change detection to avoid empty PRs

### 3. Deployment Pipeline (`deploy.yml`)

**Purpose**: Deploy application with pre-checks and rollback capability

**Jobs**:
- `pre-deployment-checks`: Validate deployment readiness
- `deploy`: Execute deployment to staging or production
- `rollback`: Automatic rollback on failure
- `post-deployment`: Summary and notifications

**Key Features**:
- Environment-based deployment (staging/production)
- Deployment snapshots for rollback
- Health checks after deployment
- Automatic rollback trigger on failure

---

## Trigger Points

### Continuous Integration

| Trigger | Branches | Purpose |
|---------|----------|---------|
| `push` | `main`, `develop` | Validate committed changes |
| `pull_request` | `main`, `develop` | Pre-merge validation |

### Data Updates

| Trigger | Schedule | Purpose |
|---------|----------|---------|
| `schedule` | Weekly (Sunday 00:00 UTC) | Regular exploit DB updates |
| `workflow_dispatch` | Manual | On-demand updates |

### Deployment

| Trigger | Condition | Purpose |
|---------|-----------|---------|
| `push` | `main` branch | Automatic staging deployment |
| `push` | Tags `v*` | Version release deployment |
| `workflow_dispatch` | Manual | Controlled deployments |

---

## Environment Setup

### Required Secrets

Configure these in GitHub Settings → Secrets and Variables → Actions:

| Secret | Purpose | Required For |
|--------|---------|--------------|
| `GITHUB_TOKEN` | Automatic (provided by GitHub) | All workflows |
| `DEPLOY_KEY` (future) | Deployment authentication | `deploy.yml` |
| `NPM_TOKEN` (future) | NPM registry access | `ci.yml` (Node.js) |

### Environment Variables

Set these in workflow files as needed:

```yaml
env:
  PYTHON_VERSION: '3.11'
  NODE_VERSION: '20'
  DEPLOYMENT_ENVIRONMENT: 'staging'
```

### Repository Settings

1. **Branch Protection** (Recommended):
   - Navigate to Settings → Branches
   - Add rule for `main` branch:
     - Require status checks to pass: ✅
     - Require up-to-date branches: ✅
     - Include administrators: ✅

2. **Workflow Permissions**:
   - Settings → Actions → General
   - Workflow permissions: "Read and write permissions"
   - Allow GitHub Actions to create PRs: ✅

---

## Dependency Management

### Dependabot Configuration

Dependabot is configured to automatically manage dependencies across multiple ecosystems:

#### Update Schedule

- **Day**: Monday at 09:00 UTC
- **Frequency**: Weekly
- **Max Open PRs**: 5-10 per ecosystem

#### Supported Ecosystems

1. **GitHub Actions** (`.github/workflows/*.yml`)
   - Updates action versions automatically
   - Critical for security patches

2. **Python** (`requirements.txt`)
   - Security-focused updates
   - Grouped by patch/minor versions

3. **Node.js** (`package.json`)
   - Separate groups for dev/prod dependencies
   - Version strategy: increase

4. **Docker** (`Dockerfile`)
   - Base image updates
   - Tagged version management

#### Reviewing Dependabot PRs

1. **Automated Checks**: Wait for CI to complete
2. **Version Changes**: Review changelog in PR description
3. **Breaking Changes**: Look for major version bumps
4. **Security Updates**: Prioritize and merge quickly
5. **Merge**: Use "Squash and merge" for clean history

---

## Rollback Procedures

### Automatic Rollback (Deployment Workflow)

The deployment workflow includes automatic rollback:

1. **Trigger**: Any job failure in the deploy workflow
2. **Process**:
   - Rollback job activates
   - Downloads deployment snapshot
   - Reverts to previous stable version
   - Sends failure notification

### Manual Rollback

If you need to manually rollback a deployment:

```bash
# 1. Find the last successful deployment commit
git log --grep="deploy-" --oneline -5

# 2. Create a rollback branch
git checkout -b rollback-to-<commit-sha> <commit-sha>

# 3. Push to trigger deployment
git push origin rollback-to-<commit-sha>

# 4. Trigger manual deployment via GitHub Actions UI
# Go to Actions → Deployment Pipeline → Run workflow
# Select the rollback branch
```

### Post-Rollback Actions

1. Investigate failure root cause
2. Create issue documenting the incident
3. Fix the problem in a new branch
4. Test thoroughly before redeploying
5. Update this documentation if needed

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: CI Workflow Fails on Documentation Check

**Symptom**: `validate` job fails with "README.md is required"

**Solution**:
```bash
# Ensure README.md exists and is not empty
echo "# Project Documentation" > README.md
git add README.md
git commit -m "docs: add README"
git push
```

#### Issue: Python Tests Skipped

**Symptom**: `test-python` job shows "Skipped"

**Reason**: No Python files detected (conditional: `hashFiles('**/*.py') != ''`)

**Solution**: This is expected if you haven't added Python code yet. Add `.py` files to trigger:
```bash
# Example: Create a basic Python module
mkdir -p src
touch src/__init__.py
git add src/
git commit -m "feat: initialize Python module"
git push
```

#### Issue: Dependabot PRs Not Appearing

**Symptom**: No dependency update PRs after configuration

**Possible Causes**:
1. **No dependencies exist**: Dependabot only works when dependency files exist
2. **All dependencies up-to-date**: Check manually with `npm outdated` or `pip list --outdated`
3. **Open PR limit reached**: Close some existing Dependabot PRs

**Solution**:
```bash
# Check Dependabot logs
# GitHub → Settings → Security → Dependabot

# Manually trigger a check (if available)
# Or wait for next scheduled run (Monday 09:00 UTC)
```

#### Issue: Deployment Rollback Triggered Unnecessarily

**Symptom**: Rollback occurs on minor issues

**Solution**: Review the health check logic in `deploy.yml`:
```yaml
# Adjust health check tolerance
- name: Health Check
  run: |
    # Add retry logic
    for i in {1..3}; do
      if health_check; then exit 0; fi
      sleep 5
    done
    exit 1
```

#### Issue: Data Update Workflow Creates Empty PRs

**Symptom**: PRs with no file changes

**Solution**: This shouldn't happen due to change detection, but verify:
```bash
# Check the change detection logic in data-update.yml
if [[ -n $(git status -s) ]]; then
  echo "has_changes=true"
fi
```

---

## Best Practices

### Workflow Development

1. **Test Locally**: Use [act](https://github.com/nektos/act) to test workflows locally
   ```bash
   # Install act
   brew install act  # macOS
   # or
   curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
   
   # Run a workflow locally
   act -W .github/workflows/ci.yml
   ```

2. **Use Workflow Dispatch**: Add manual triggers for easier testing
   ```yaml
   on:
     workflow_dispatch:  # Enables manual runs
     push:
       branches: [main]
   ```

3. **Add Debug Steps**: Include debug outputs for troubleshooting
   ```yaml
   - name: Debug Information
     run: |
       echo "Event: ${{ github.event_name }}"
       echo "Branch: ${{ github.ref }}"
       echo "Commit: ${{ github.sha }}"
   ```

### Security Practices

1. **Never Commit Secrets**: Use GitHub Secrets for sensitive data
2. **Pin Action Versions**: Use SHA hashes for critical actions
   ```yaml
   # Good
   uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4
   
   # Avoid
   uses: actions/checkout@v4
   ```

3. **Review Third-Party Actions**: Audit any action from unknown sources
4. **Limit Permissions**: Use minimal required permissions
   ```yaml
   permissions:
     contents: read
     pull-requests: write
   ```

### Maintenance Schedule

| Task | Frequency | Responsibility |
|------|-----------|----------------|
| Review Dependabot PRs | Weekly | Maintainer |
| Update workflow documentation | As needed | Developer |
| Security audit of workflows | Monthly | Security Lead |
| Test rollback procedures | Quarterly | DevOps Team |
| Review workflow efficiency | Quarterly | Team Lead |

### Monitoring and Alerts

1. **GitHub Actions Dashboard**: Monitor workflow runs
   - Repository → Actions
   - Check for failures and bottlenecks

2. **Workflow Run Time**: Track execution duration
   - Optimize slow workflows
   - Use caching effectively

3. **Failure Rate**: Monitor success/failure ratio
   - Investigate patterns
   - Improve flaky tests

---

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Dependabot Configuration](https://docs.github.com/en/code-security/dependabot)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)

---

## Support and Contact

For questions or issues with workflows:

1. **Check this documentation first**
2. **Search existing GitHub Issues**
3. **Create a new issue** with:
   - Workflow name
   - Run ID (from Actions page)
   - Error logs
   - Expected vs actual behavior

---

**Last Updated**: January 2026  
**Maintained By**: SentinelZero Development Team  
**Version**: 1.0.0
