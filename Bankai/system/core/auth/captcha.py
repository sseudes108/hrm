from dataclasses import dataclass
import secrets


@dataclass(frozen=True)
class MathCaptcha:
    left: int
    right: int
    operator: str

    @property
    def question(self) -> str:
        return f"Quanto é {self.left} {self.operator} {self.right}?"

    @property
    def answer(self) -> int:
        return self.left + self.right if self.operator == "+" else self.left - self.right


def create_captcha() -> MathCaptcha:
    left = secrets.randbelow(8) + 3
    right = secrets.randbelow(8) + 1
    operator = "+" if secrets.randbelow(2) else "-"
    if operator == "-" and right > left:
        left, right = right, left
    return MathCaptcha(left, right, operator)
