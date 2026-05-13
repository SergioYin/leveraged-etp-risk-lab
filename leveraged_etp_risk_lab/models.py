from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ProductTerms:
    name: str
    ticker: str
    underlying: str
    leverage: float
    annual_fee: float
    currency: str = "USD"
    reset_frequency: str = "daily"
    notes: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProductTerms":
        required = ["name", "ticker", "underlying", "leverage", "annual_fee"]
        missing = [key for key in required if key not in data]
        if missing:
            raise ValueError(f"product is missing required field(s): {', '.join(missing)}")
        leverage = float(data["leverage"])
        annual_fee = float(data["annual_fee"])
        if leverage == 0:
            raise ValueError("product leverage must not be zero")
        if annual_fee < 0:
            raise ValueError("annual_fee must be non-negative")
        return cls(
            name=str(data["name"]),
            ticker=str(data["ticker"]),
            underlying=str(data["underlying"]),
            leverage=leverage,
            annual_fee=annual_fee,
            currency=str(data.get("currency", "USD")),
            reset_frequency=str(data.get("reset_frequency", "daily")),
            notes=str(data.get("notes", "")),
        )


@dataclass(frozen=True)
class ScenarioDay:
    day: int
    label: str
    underlying_return: float


@dataclass(frozen=True)
class RiskBand:
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None


@dataclass(frozen=True)
class SimulationConfig:
    product: ProductTerms
    path: List[ScenarioDay]
    initial_nav: float = 100.0
    risk_band: RiskBand = RiskBand()
