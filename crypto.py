import numpy as np

class CryptoCurrency():
    def __init__(self, startprice, drift, volatility, N , jump_chance, jump_magnitude) -> None:
        self.startprice = startprice
        self.drift = drift
        self.volatility = volatility
        self.simulation_no = N
        self.jump_chance = jump_chance
        self.jump_magnitude = jump_magnitude

    def simulation_engine(self):
        prices = [self.startprice]
        volatility = self.volatility

        for _ in range(1, self.simulation_no):
            # Random walk
            dt = 1  # Assuming each step is one time unit
            random_change = np.random.normal(self.drift * dt, volatility * np.sqrt(dt))
            
            # Volatility clustering
            recent_change = np.log(prices[-1] / prices[-2]) if len(prices) > 1 else 0
            volatility = volatility * 0.9 + 0.1 * abs(recent_change)  # Example of EWMA

            # Jump logic
            if np.random.rand() < self.jump_chance:
                jump = np.random.normal(0, self.jump_magnitude)
            else:
                jump = 0

            new_price = prices[-1] * np.exp(random_change + jump)
            prices.append(new_price)

        return prices

        
