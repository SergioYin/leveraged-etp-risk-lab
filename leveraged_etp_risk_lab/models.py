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


@dataclass(frozen=True)
class PortfolioPosition:
    identifier: str
    product_fixture: str
    path_fixture: str
    notional: float
    risk_band: RiskBand = RiskBand()

    @classmethod
    def from_dict(cls, data: Dict[str, Any], index: int) -> "PortfolioPosition":
        product_fixture = data.get("product_fixture", data.get("product"))
        path_fixture = data.get("path_fixture", data.get("path"))
        if not product_fixture:
            raise ValueError(f"position {index} is missing product_fixture")
        if not path_fixture:
            raise ValueError(f"position {index} is missing path_fixture")
        if "notional" not in data:
            raise ValueError(f"position {index} is missing notional")
        notional = float(data["notional"])
        if notional <= 0:
            raise ValueError(f"position {index} notional must be positive")
        identifier = str(data.get("id") or data.get("name") or f"position_{index}")
        return cls(
            identifier=identifier,
            product_fixture=str(product_fixture),
            path_fixture=str(path_fixture),
            notional=notional,
            risk_band=RiskBand(
                stop_loss=_optional_float(data.get("stop_loss")),
                take_profit=_optional_float(data.get("take_profit")),
            ),
        )


@dataclass(frozen=True)
class PortfolioManifest:
    name: str
    base_currency: str
    positions: List[PortfolioPosition]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PortfolioManifest":
        raw_positions = data.get("positions")
        if not isinstance(raw_positions, list) or not raw_positions:
            raise ValueError("portfolio manifest must contain at least one position")
        return cls(
            name=str(data.get("name", "Portfolio")),
            base_currency=str(data.get("base_currency", "USD")),
            positions=[PortfolioPosition.from_dict(item, index + 1) for index, item in enumerate(raw_positions)],
        )


def _optional_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    return float(value)
