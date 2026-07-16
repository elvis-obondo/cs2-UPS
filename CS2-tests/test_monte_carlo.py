import numpy as np

from monte_carlo import run_batch_simulation


def test_batch_simulation_shape_and_start_column():
    history = run_batch_simulation(
        n_trials=50, starting_bankroll=300, cost_per_try=7.5,
        win_payout=85, win_chance=0.10, total_attempts=30, seed=1,
    )
    assert history.shape == (50, 31)
    assert np.all(history[:, 0] == 300)


def test_batch_simulation_matches_expected_value():
    n_trials = 20000
    starting_bankroll = 300
    cost_per_try = 7.5
    win_payout = 85
    win_chance = 0.10
    total_attempts = 30

    history = run_batch_simulation(
        n_trials=n_trials, starting_bankroll=starting_bankroll, cost_per_try=cost_per_try,
        win_payout=win_payout, win_chance=win_chance, total_attempts=total_attempts, seed=7,
    )
    expected_final = starting_bankroll + total_attempts * (win_chance * win_payout - cost_per_try)
    assert abs(history[:, -1].mean() - expected_final) < 5
