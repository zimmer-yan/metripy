class FailureConfig:
    def __init__(self, value: str, severity: str, amount: int):
        self.value = value
        self.severity = severity
        self.amount = amount

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "severity": self.severity,
            "amount": self.amount,
        }