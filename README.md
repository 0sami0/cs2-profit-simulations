# CS2 Profitability Simulations

This repository contains the Python and Manim scripts used to create the data-driven simulations for my YouTube video, "I Simulated Every Way to Make Money in CS2."

► **Watch the full video here:** [LINK TO YOUR YOUTUBE VIDEO ONCE IT'S LIVE]

---

## About This Project

This project was created to provide a realistic, data-driven look at the most popular methods for making money in Counter-Strike 2. Each script generates a different animation that visualizes the long-term profitability (or lack thereof) for each strategy.

## Scripts Included

- **`cs2_simulation_video.py`**: Simulates opening the Fever Case over one year.
- **`tradeup_video_with_fees.py`**: Simulates a high-stakes trade-up, first without fees, and then with the 15% Steam fee to show the impact.
- **`flipper_video.py`**: Simulates a "biased random walk" to model the volatility of skin flipping over 90 days.
- **`investor_video.py`**: Simulates the "Smart Investor" strategy of compounding weekly CS2 drops into a crypto LP over three years.
- **`finale_video.py`**: The Grand Finale! Pits all four strategies against each other in a 3-year race.

## How to Use

To run these animations yourself, you will need Python and Manim (Community Edition) installed.

1.  Install Manim: `pip install manim`
2.  Run any script from your terminal, for example:
    `manim render -pqh finale_video.py GrandFinale`
