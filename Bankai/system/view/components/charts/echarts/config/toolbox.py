from dataclasses import dataclass
from typing import Literal, Optional
import streamlit as st

ToolboxOrient = Literal["horizontal", "vertical"]

VALID_ORIENT = {"horizontal", "vertical"}

@dataclass
class ToolboxConfig:
    # Features
    save:    bool           = True
    restore: bool           = True
    view:    bool           = False
    zoom:    bool           = False
    magic:   Optional[list] = None # None = desativado, ["line", "bar"] = ativado

    # Layout
    orient: ToolboxOrient  = "horizontal"
    top:    Optional[str]  = "0%"
    right:  Optional[str]  = "0%"
    bottom: Optional[str]  = None
    left:   Optional[str]  = None

    def __post_init__(self):
        if self.orient not in VALID_ORIENT:
            st.error(f"ToolboxConfig — orient inválido: '{self.orient}'. Use: {VALID_ORIENT}")
            raise ValueError(f"orient inválido: '{self.orient}'")
