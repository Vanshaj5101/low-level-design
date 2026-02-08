from abc import ABC, abstractmethod

class ShippingStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, order):
        pass


class FlatRateShipping(ShippingStrategy):
    def __init__(self, rate):
        self.rate = rate

    def calculate_cost(self, order):
        print(f"Calculating with Flat Rate strategy (${self.rate})")
        return self.rate


class WeightBasedShipping(ShippingStrategy):
    def __init__(self, rate_per_kg):
        self.rate_per_kg = rate_per_kg

    def calculate_cost(self, order):
        print(f"Calculating with Weight-Based strategy (${self.rate_per_kg}/kg)")
        return order["total_weight"] * self.rate_per_kg


class ThirdPartyApiShipping(ShippingStrategy):
    def __init__(self, base_fee, percentage_fee):
        self.base_fee = base_fee
        self.percentage_fee = percentage_fee

    def calculate_cost(self, order):
        print("Calculating with Third-Party API strategy.")
        # Simulate API call
        return self.base_fee + (order["order_value"] * self.percentage_fee)


class ShippingCostService:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        print(f"ShippingCostService: Strategy changed to {strategy.__class__.__name__}")
        self.strategy = strategy

    def calculate_shipping_cost(self, order):
        if self.strategy is None:
            raise ValueError("Shipping strategy not set.")

        cost = self.strategy.calculate_cost(order)
        print(
            f"ShippingCostService: Final Calculated Shipping Cost: ${cost} "
            f"(using {self.strategy.__class__.__name__})"
        )
        return cost


def ecommerce_app_v2():
    order1 = {
        "total_weight" : 10,
        "order_value" : 250
    }

    # Create different strategy instances
    flat_rate = FlatRateShipping(10.0)
    weight_based = WeightBasedShipping(2.5)
    third_party = ThirdPartyApiShipping(7.5, 0.02)

    # Create context with an initial strategy
    shipping_service = ShippingCostService(flat_rate)

    print("--- Order 1: Using Flat Rate (initial) ---")
    shipping_service.calculate_shipping_cost(order1)

    print("\n--- Order 1: Changing to Weight-Based ---")
    shipping_service.set_strategy(weight_based)
    shipping_service.calculate_shipping_cost(order1)

    print("\n--- Order 1: Changing to Third-Party API ---")
    shipping_service.set_strategy(third_party)
    shipping_service.calculate_shipping_cost(order1)

    # Adding a NEW strategy is easy:
    # 1. Create a new class implementing ShippingStrategy (e.g., FreeShippingStrategy)
    # 2. Client can then instantiate and use it:
    #    free_shipping = FreeShippingStrategy()
    #    shipping_service.set_strategy(free_shipping)
    #    shipping_service.calculate_shipping_cost(prime_member_order)
    # No modification to ShippingCostService is needed!


# Example usage
if __name__ == "__main__":
    ecommerce_app_v2()
