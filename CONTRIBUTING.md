# Contributing to SentinelZero

First of all, thank you for considering contributing 🚀

## Philosophy
SentinelZero focuses on **post-audit DeFi risk intelligence**.
Contributions must prioritize:
- Deterministic logic
- Explainable scoring
- Reproducibility
- Security-first design

## How to Contribute
1. Fork the repository
2. Create a feature branch (`feature/my-feature`)
3. Write **tests first**
4. Ensure all tests pass (`pytest`)
5. Submit a Pull Request

## Code Standards
- Python ≥ 3.9
- Follow PEP8
- Prefer explicit logic over clever tricks
- No network calls in unit tests

## Testing
Run locally:
```bash
pytest tests -v
