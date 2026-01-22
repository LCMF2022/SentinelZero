# SentinelZero — Risk Model Specification

## 1. Purpose

SentinelZero is a pre-listing risk analysis framework designed to assist exchanges,
launchpads, and investors in evaluating DeFi protocols prior to token listing.

This model focuses on **structural risk**, not market speculation.

---

## 2. Risk Categories

SentinelZero currently evaluates the following immutable risk categories:

### 2.1 Governance Risk
Risks related to control, upgradeability, and administrative power.

Examples:
- Upgradeable contracts
- Emergency admin or pause functions
- Small multisig or EOA-controlled governance

---

### 2.2 Oracle Risk
Risks related to price feeds and external data dependencies.

Examples:
- Single oracle dependency
- Low-liquidity oracle sources
- Non-redundant or manipulable feeds

---

### 2.3 Liquidity Risk
Risks related to capital concentration and liquidity stability.

Examples:
- High TVL concentration
- Shallow liquidity pools
- Sudden TVL drawdowns

---

## 3. Severity Levels

Each detected risk signal is assigned a severity:

| Severity  | Description |
|---------|------------|
| LOW     | Minor or informational risk |
| MEDIUM  | Meaningful but non-critical risk |
| HIGH    | Critical structural risk |

Severity weights are defined in code and are globally consistent.

---

## 4. Scoring Methodology

1. Each risk signal generates a score based on severity weight.
2. Scores are aggregated **per risk category**.
3. Each category has a maximum score cap.
4. Category scores are summed.
5. Final score is capped at 100.

This prevents a single category from dominating the overall risk score.

---

## 5. Interpretation of Score

| Score Range | Interpretation |
|-----------|---------------|
| 0–20      | Low structural risk |
| 21–40     | Moderate risk |
| 41–60     | Elevated risk |
| 61–80     | High risk |
| 81–100    | Critical risk |

---

## 6. Non-Goals

SentinelZero does NOT:
- Predict price action
- Provide investment advice
- Replace full smart contract audits

It is designed as a **screening and risk signaling tool**.

---

## 7. Model Stability

Risk categories, severity definitions, and scoring caps are considered
**stable interfaces** and should only change via major version updates.
