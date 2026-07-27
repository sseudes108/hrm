"""Serviços técnicos compartilhados pelo bootstrap e pelas aplicações."""

from .environment import load_environment

__all__ = ["load_environment"]
