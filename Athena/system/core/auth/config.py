from dataclasses import dataclass, field


@dataclass(frozen=True)
class AuthConfig:
    """Configuração opcional de autenticação por aplicação."""

    enabled: bool = False
    cookie_name: str = "zanpakutou_session"
    cookie_days: int = 1
    captcha_after_attempts: int = 2
    max_attempts: int = 5
    lockout_seconds: int = 600
    allow_local_auth: bool = False
    local_users: dict[str, str] = field(default_factory=dict)
    database_table: str = "app_users"
    cookie_secret_env: str = "AUTH_COOKIE_SECRET"

    def __post_init__(self) -> None:
        if self.cookie_days < 1:
            raise ValueError("cookie_days deve ser maior que zero.")
        if self.captcha_after_attempts < 0:
            raise ValueError("captcha_after_attempts não pode ser negativo.")
        if self.max_attempts < 1 or self.lockout_seconds < 1:
            raise ValueError("max_attempts e lockout_seconds devem ser positivos.")
        if self.captcha_after_attempts >= self.max_attempts:
            raise ValueError("captcha_after_attempts deve ser menor que max_attempts.")
