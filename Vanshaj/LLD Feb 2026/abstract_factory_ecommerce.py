from __future__ import annotations
from abc import ABC, abstractmethod
import uuid
from typing import Dict, Type


# -------------------------
# Abstract product contracts
# -------------------------
class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount: float, currency: str, **options) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def refund(self, transaction_id: str, amount: float = None) -> Dict:
        raise NotImplementedError

    def validate_amount(self, amount) -> bool:
        return isinstance(amount, (int, float)) and amount > 0

    def validate_currency(self, user_currency: str, nation_currency: str) -> bool:
        return str(user_currency).upper() == str(nation_currency).upper()

    def generate_transaction_id(self, nation_prefix: str) -> str:
        return f"{nation_prefix}_tx_{uuid.uuid4()}"


class ShippingCalculator(ABC):
    @abstractmethod
    def estimate(self, weight_kg: float, distance_km: float, **options) -> float:
        """Return shipping cost (float) in region currency."""
        raise NotImplementedError


# -------------------------
# Concrete Payment Processors
# -------------------------
class USPaymentProcessor(PaymentProcessor):
    _currency = "USD"
    _nation_prefix = "us"

    def charge(self, amount: float, currency: str, **options) -> Dict:
        if not self.validate_amount(amount):
            return {
                "success": False,
                "transaction_id": None,
                "charged_amount": 0.0,
                "currency": currency,
                "message": "invalid amount",
            }
        if not self.validate_currency(currency, self._currency):
            return {
                "success": False,
                "transaction_id": None,
                "charged_amount": 0.0,
                "currency": currency,
                "message": "currency mismatch",
            }
        charged_amount = float(amount)
        tx = self.generate_transaction_id(self._nation_prefix)
        return {
            "success": True,
            "transaction_id": tx,
            "charged_amount": charged_amount,
            "currency": self._currency,
            "message": "charged",
        }

    def refund(self, transaction_id: str, amount: float = None) -> Dict:
        if not isinstance(transaction_id, str) or not transaction_id.startswith(
            f"{self._nation_prefix}_tx_"
        ):
            return {
                "success": False,
                "refund_id": None,
                "refunded_amount": 0.0,
                "transaction_id": transaction_id,
                "message": "invalid transaction id",
            }
        if amount is not None and not self.validate_amount(amount):
            return {
                "success": False,
                "refund_id": None,
                "refunded_amount": 0.0,
                "transaction_id": transaction_id,
                "message": "invalid refund amount",
            }
        refund_id = f"rf_{uuid.uuid4()}"
        refunded_amount = float(amount) if amount is not None else None
        return {
            "success": True,
            "refund_id": refund_id,
            "refunded_amount": refunded_amount,
            "transaction_id": transaction_id,
            "message": "refund processed",
        }


class EUPaymentProcessor(PaymentProcessor):
    _currency = "EUR"
    _nation_prefix = "eu"

    def charge(self, amount: float, currency: str, **options) -> Dict:
        if not self.validate_amount(amount):
            return {
                "success": False,
                "transaction_id": None,
                "charged_amount": 0.0,
                "currency": currency,
                "message": "invalid amount",
            }
        if not self.validate_currency(currency, self._currency):
            return {
                "success": False,
                "transaction_id": None,
                "charged_amount": 0.0,
                "currency": currency,
                "message": "currency mismatch",
            }
        # VAT handling: default apply_tax=True, vat_rate default 0.20
        apply_tax = bool(options.get("apply_tax", True))
        vat_rate = float(options.get("vat_rate", 0.20))
        base = float(amount)
        charged_amount = base * (1 + vat_rate) if apply_tax else base
        tx = self.generate_transaction_id(self._nation_prefix)
        return {
            "success": True,
            "transaction_id": tx,
            "charged_amount": charged_amount,
            "currency": self._currency,
            "message": "charged",
        }

    def refund(self, transaction_id: str, amount: float = None) -> Dict:
        if not isinstance(transaction_id, str) or not transaction_id.startswith(
            f"{self._nation_prefix}_tx_"
        ):
            return {
                "success": False,
                "refund_id": None,
                "refunded_amount": 0.0,
                "transaction_id": transaction_id,
                "message": "invalid transaction id",
            }
        if amount is not None and not self.validate_amount(amount):
            return {
                "success": False,
                "refund_id": None,
                "refunded_amount": 0.0,
                "transaction_id": transaction_id,
                "message": "invalid refund amount",
            }
        refund_id = f"rf_{uuid.uuid4()}"
        refunded_amount = float(amount) if amount is not None else None
        return {
            "success": True,
            "refund_id": refund_id,
            "refunded_amount": refunded_amount,
            "transaction_id": transaction_id,
            "message": "refund processed",
        }


# -------------------------
# Concrete Shipping Calculators
# -------------------------
class USShippingCalculator(ShippingCalculator):
    # deterministic constants for tests
    BASE = 5.0
    PER_KM = 0.1
    PER_KG = 1.0

    def estimate(self, weight_kg: float, distance_km: float, **options) -> float:
        if not isinstance(weight_kg, (int, float)) or not isinstance(
            distance_km, (int, float)
        ):
            raise TypeError("weight_kg and distance_km must be numbers")
        if weight_kg < 0 or distance_km < 0:
            raise ValueError("weight and distance must be non-negative")
        cost = (
            self.BASE
            + self.PER_KM * float(distance_km)
            + self.PER_KG * float(weight_kg)
        )
        if options.get("rush"):
            cost += 10.0
        return float(cost)


class EUShippingCalculator(ShippingCalculator):
    BASE = 7.0
    PER_KM = 0.12
    PER_KG = 1.2
    CROSS_BORDER_SURCHARGE = 3.0

    def estimate(self, weight_kg: float, distance_km: float, **options) -> float:
        if not isinstance(weight_kg, (int, float)) or not isinstance(
            distance_km, (int, float)
        ):
            raise TypeError("weight_kg and distance_km must be numbers")
        if weight_kg < 0 or distance_km < 0:
            raise ValueError("weight and distance must be non-negative")
        cost = (
            self.BASE
            + self.PER_KM * float(distance_km)
            + self.PER_KG * float(weight_kg)
        )
        if options.get("is_international"):
            cost += self.CROSS_BORDER_SURCHARGE
        return float(cost)


# -------------------------
# Abstract factory
# -------------------------
class EcommerceFactory(ABC):
    @abstractmethod
    def create_payment_processor(self) -> PaymentProcessor:
        raise NotImplementedError

    @abstractmethod
    def create_shipping_calculator(self) -> ShippingCalculator:
        raise NotImplementedError


# -------------------------
# Concrete factories
# -------------------------
class USFactory(EcommerceFactory):
    def create_payment_processor(self) -> PaymentProcessor:
        return USPaymentProcessor()

    def create_shipping_calculator(self) -> ShippingCalculator:
        return USShippingCalculator()


class EUFactory(EcommerceFactory):
    def create_payment_processor(self) -> PaymentProcessor:
        return EUPaymentProcessor()

    def create_shipping_calculator(self) -> ShippingCalculator:
        return EUShippingCalculator()


# -------------------------
# FactoryProvider (registry)
# -------------------------
class FactoryProvider:
    _registry: Dict[str, Type[EcommerceFactory]] = {}

    @classmethod
    def register(cls, name: str, factory_cls: Type[EcommerceFactory]) -> None:
        cls._registry[name] = factory_cls

    @classmethod
    def get_factory(cls, name: str, **config) -> EcommerceFactory:
        if name not in cls._registry:
            raise ValueError(f"Factory not registered for: {name!r}")
        factory_cls = cls._registry[name]
        # factories are simple/stateless here; pass config if factory needs it
        return factory_cls(**config) if config else factory_cls()


# -------------------------
# Register default factories
# -------------------------
FactoryProvider.register("us", USFactory)
FactoryProvider.register("eu", EUFactory)


# -------------------------
# Simple demo & tests
# -------------------------
if __name__ == "__main__":
    # US charge + shipping
    us_factory = FactoryProvider.get_factory("us")
    us_pp = us_factory.create_payment_processor()
    us_sc = us_factory.create_shipping_calculator()

    res = us_pp.charge(100.0, currency="USD")
    assert res["success"] is True
    assert res["currency"] == "USD"
    assert res["transaction_id"].startswith("us_tx_")
    print("US charge OK:", res)

    cost = us_sc.estimate(weight_kg=2.0, distance_km=50.0)
    assert isinstance(cost, float) and cost > 0.0
    print("US shipping cost:", cost)

    # EU charge (with VAT)
    eu_factory = FactoryProvider.get_factory("eu")
    eu_pp = eu_factory.create_payment_processor()
    eu_sc = eu_factory.create_shipping_calculator()

    res_eu = eu_pp.charge(100.0, currency="EUR", apply_tax=True, vat_rate=0.20)
    assert res_eu["success"] is True
    assert res_eu["currency"] == "EUR"
    assert abs(res_eu["charged_amount"] - 120.0) < 1e-9
    print("EU charge with VAT OK:", res_eu)

    eu_cost = eu_sc.estimate(weight_kg=1.5, distance_km=30.0, is_international=False)
    assert eu_cost > 0.0
    print("EU shipping cost:", eu_cost)

    # Refund examples (format check)
    r = us_pp.refund(res["transaction_id"], amount=50.0)
    assert r["success"] is True
    print("US refund OK:", r)

    r2 = eu_pp.refund(res_eu["transaction_id"])
    assert r2["success"] is True
    print("EU refund OK:", r2)

    # FactoryProvider errors
    try:
        FactoryProvider.get_factory("unknown")
    except ValueError as exc:
        print("Expected error:", exc)

    print("All basic checks passed.")
