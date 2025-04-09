import time
import matplotlib.pyplot as plot
from data.primes2 import primes
from src.trial_division import trial_division
from src.miller_rabin import miller_rabin
from src.aks import aks

def main():
    miller_rabin_times = []
    aks_times = []
    trial_division_times = []

    for prime in primes:
        miller_rabin_times.append(get_execution_time(miller_rabin, prime))
        aks_times.append(get_execution_time(aks, prime))

        if len(str(prime)) <= 18:
            trial_division_times.append(get_execution_time(trial_division, prime))
        else:
            trial_division_times.append(None)

    print_and_plot_results(primes, miller_rabin_times, aks_times, trial_division_times)

def get_execution_time(function, input):
    start_time = time.perf_counter()
    function(input)
    end_time = time.perf_counter()
    return end_time - start_time

def print_and_plot_results(primes, time_rabin_miller, time_aks, time_trial_division):
    digit_lengths = [len(str(p)) for p in primes]

    print('{:<10s} {:<12s} {:<10s} {:<15s}'.format(
        'Digits',
        'Miller-Rabin',
        'AKS',
        'Trial Division'
    ))

    for index, _ in enumerate(primes):
        print('{:<10d} {:<12.12f} {:<10.12f} {:<15.12f}'.format(
            digit_lengths[index],
            time_rabin_miller[index],
            time_aks[index],
            time_trial_division[index] if time_trial_division[index]
            else float('inf')
        ))

    plot.figure(figsize=(10, 6))
    plot.plot(digit_lengths, time_rabin_miller, label='Rabin-Miller')
    plot.plot(digit_lengths, time_aks, label='AKS')
    plot.plot(digit_lengths, time_trial_division, label='Trial Division')
    plot.xlabel('Digits')
    plot.ylabel('Logarithmic Execution Time (s)')
    plot.yscale('log')
    plot.title('Primality Testing Performance')
    plot.legend()
    plot.figtext(
        0.5,
        0.01,
        'Figure: Execution time comparison for Miller-Rabin, AKS, and Trial Division primality ' +
        'tests across different number sizes (in digits). Logarithmic scale used on the y-axis for clearer ' +
        'visualization of time differences due to large disparity in execution times. Miller-Rabin, ' +
        'and AKS tests show moderate time increases with number size, while Trial Division shows a more ' +
        'dramatic time increase, becoming unfeasible after 18 digits.',
        fontsize=10,
        ha='center',
        va='bottom',
        wrap=True,
        bbox={"facecolor": "lightgrey", "alpha": 0.7, "pad": 5}
    )
    plot.subplots_adjust(bottom=0.2)
    plot.savefig('primality_testing_performance.png', dpi=300)
    plot.show()


main()