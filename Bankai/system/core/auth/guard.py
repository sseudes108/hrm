"""Guard visual opcional de autenticação para aplicações Streamlit."""

from typing import Any

import streamlit as st
from streamlit_js_eval import get_cookie, set_cookie

from system.core.managers.database.psql import DatabaseConnectionError, fetch_auth_user, validate_connection
from system.view.components._keys import scoped_key
from system.view.components.cards import card
from .captcha import MathCaptcha, create_captcha
from .config import AuthConfig
from .locks import attempt_lockout
from .passwords import verify_password
from .tokens import issue_token, verify_token


def require_authentication(context: Any, config: AuthConfig) -> bool:
    """Renderiza o login apenas quando necessário e retorna acesso liberado."""
    if not config.enabled:
        return True
    principal_key = _key(context, "principal")
    if principal_key in st.session_state:
        return True

    if st.session_state.get(_key(context, "logout_pending")):
        set_cookie(config.cookie_name, "", -1, component_key=_key(context, "clear_cookie"))
        return _draw_login(context, config)

    restored = _restore_cookie(context, config)
    if restored:
        return True
    return _draw_login(context, config)


def logout(context: Any, config: AuthConfig) -> None:
    st.session_state.pop(_key(context, "principal"), None)
    st.session_state[_key(context, "logout_pending")] = True


def _restore_cookie(context: Any, config: AuthConfig) -> bool:
    # ``st.context.cookies`` chega no request atual; o componente cobre o
    # primeiro ciclo no navegador antes de uma recarga completa.
    token = st.context.cookies.get(config.cookie_name)
    if not token:
        token = get_cookie(config.cookie_name, component_key=_key(context, "read_cookie"))
    payload = verify_token(token, app_id=context.app_name, secret_env=config.cookie_secret_env)
    if payload is None:
        return False
    st.session_state[_key(context, "principal")] = payload["sub"]
    return True


def _draw_login(context: Any, config: AuthConfig) -> bool:
    username_key = _key(context, "username")
    current_identity = str(st.session_state.get(username_key, "")).strip().lower()
    captcha_required = (
        bool(current_identity)
        and attempt_lockout.failure_count(current_identity) >= config.captcha_after_attempts
    )
    captcha = _get_captcha(context) if captcha_required else None

    # Colunas externas preservam uma área deliberadamente reduzida, sem
    # introduzir um grid interno para os campos do formulário.
    left, center, right = st.columns((1.2, 2.2, 1.2))
    with center:
        with st.container(key=scoped_key(context, "co_auth_panel", "main")):
            st.markdown("## 🔐 Acesso protegido")
            st.caption("🛡️ Informe suas credenciais para continuar.")
            with st.form(key=_key(context, "login_form"), clear_on_submit=False):
                username = st.text_input(
                    "👤 Usuário", key=username_key, autocomplete="username"
                )
                password = st.text_input(
                    "🔑 Senha", type="password", autocomplete="current-password"
                )
                answer = ""
                if captcha is not None:
                    st.info("🧮 Confirme a validação matemática para continuar.")
                    answer = st.text_input(
                        f"🧮 {captcha.question}", key=_key(context, "captcha_answer")
                    )
                submitted = card.draw(
                    card.CardConfig(
                        context=context,
                        card_id="auth_submit",
                        model="wrapper",
                        variant="outline",
                        padding="compact",
                        hover=False,
                    ),
                    card.CardRenderConfig(
                        content=lambda: st.form_submit_button("🔓 Entrar", width="stretch")
                    ),
                )

    if not submitted:
        return False
    identity = username.strip().lower()
    remaining = attempt_lockout.is_locked(identity)
    if remaining:
        st.error(f"Acesso temporariamente bloqueado. Tente novamente em {remaining} segundos.")
        return False
    if captcha is not None and not _captcha_matches(answer, captcha):
        # O CAPTCHA não é uma nova falha de senha: mantém o mesmo estágio de
        # proteção e não antecipa o bloqueio por tentativas de credencial.
        st.error("Validação matemática incorreta.")
        return False
    if not _authenticate(identity, password, config):
        _deny(context, config, identity, "Usuário ou senha inválidos.")
        return False

    attempt_lockout.record_success(identity)
    st.session_state[_key(context, "principal")] = identity
    st.session_state.pop(_key(context, "logout_pending"), None)
    token = issue_token(
        username=identity,
        app_id=context.app_name,
        secret_env=config.cookie_secret_env,
        lifetime_days=config.cookie_days,
    )
    set_cookie(config.cookie_name, token, config.cookie_days, component_key=_key(context, "write_cookie"))
    _rotate_captcha(context)
    return True


def _authenticate(username: str, password: str, config: AuthConfig) -> bool:
    """Consulta PostgreSQL quando disponível e mantém fallback local explícito."""
    if validate_connection():
        try:
            user = fetch_auth_user(config.database_table, username)
        except DatabaseConnectionError:
            user = None
        if user is not None:
            return verify_password(password, str(user["password_hash"]))
        if not config.allow_local_auth:
            return False
    if not config.allow_local_auth:
        return False
    stored_hash = config.local_users.get(username)
    return stored_hash is not None and verify_password(password, stored_hash)


def _deny(context: Any, config: AuthConfig, identity: str, message: str) -> None:
    duration = attempt_lockout.record_failure(
        identity,
        max_attempts=config.max_attempts,
        lockout_seconds=config.lockout_seconds,
    )
    if duration:
        st.error(f"Acesso bloqueado por {duration} segundos após tentativas inválidas.")
    else:
        st.error(message)
        if attempt_lockout.failure_count(identity) == config.captcha_after_attempts:
            st.warning("Na próxima tentativa, confirme também a validação matemática.")


def _get_captcha(context: Any) -> MathCaptcha:
    key = _key(context, "captcha")
    captcha = st.session_state.get(key)
    if not isinstance(captcha, MathCaptcha):
        captcha = create_captcha()
        st.session_state[key] = captcha
    return captcha


def _rotate_captcha(context: Any) -> None:
    st.session_state[_key(context, "captcha")] = create_captcha()
    st.session_state.pop(_key(context, "captcha_answer"), None)


def _captcha_matches(answer: str, captcha: MathCaptcha) -> bool:
    try:
        return int(answer.strip()) == captcha.answer
    except (TypeError, ValueError):
        return False


def _key(context: Any, suffix: str) -> str:
    return f"auth_{context.app_name}_{suffix}"
