from sentinelzero.signals import liquidity, governance, oracle
from sentinelzero.scoring.calculator import calculate_risk as calculate

class RiskEngine:

    def run(self, snapshot):
        signals = []

        signals.extend(liquidity.detect(snapshot))
        signals.extend(governance.detect(snapshot))
        signals.extend(oracle.detect(snapshot))

        score = calculate(signals)
        return score, signals
