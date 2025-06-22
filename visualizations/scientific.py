"""
Scientific Plotting Module for E.L.E.S.

This module provides advanced scientific visualization tools for
extinction event simulations, including:
- Phase space plots
- Spectral analysis plots
- Statistical distribution plots
- Monte Carlo simulation plots
- Uncertainty quantification plots
- Multi-dimensional parameter sweeps
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.figure import Figure
from matplotlib.colors import ListedColormap
import seaborn as sns
from typing import Dict, Any, List, Optional, Tuple, Union
from scipy import stats
from scipy.signal import spectrogram
from scipy.optimize import curve_fit


def plot_phase_space(data: Dict[str, np.ndarray],
                    x_var: str, y_var: str,
                    trajectory_color: str = 'blue',
                    figsize: Tuple[int, int] = (10, 8)) -> Figure:
    """Create phase space plot showing system dynamics evolution."""

    fig, ax = plt.subplots(figsize=figsize)

    x_data = data.get(x_var, np.array([]))
    y_data = data.get(y_var, np.array([]))

    if len(x_data) == 0 or len(y_data) == 0:
        # Generate sample data
        t = np.linspace(0, 10*np.pi, 1000)
        x_data = np.exp(-0.1*t) * np.cos(t)
        y_data = np.exp(-0.1*t) * np.sin(t)

    # Plot trajectory
    ax.plot(x_data, y_data, color=trajectory_color, linewidth=2, alpha=0.7)

    # Add direction arrows
    n_arrows = 10
    skip = len(x_data) // n_arrows if len(x_data) > n_arrows else 1
    for i in range(0, len(x_data)-1, skip):
        if i + 1 < len(x_data):
            dx = x_data[i+1] - x_data[i]
            dy = y_data[i+1] - y_data[i]
            ax.arrow(x_data[i], y_data[i], dx*0.5, dy*0.5,
                    head_width=0.1, head_length=0.1,
                    fc=trajectory_color, ec=trajectory_color, alpha=0.6)

    # Mark start and end points
    ax.scatter(x_data[0], y_data[0], color='green', s=100,
              marker='o', label='Start', zorder=5)
    ax.scatter(x_data[-1], y_data[-1], color='red', s=100,
              marker='s', label='End', zorder=5)

    ax.set_xlabel(x_var, fontsize=14)
    ax.set_ylabel(y_var, fontsize=14)
    ax.set_title(f'Phase Space: {y_var} vs {x_var}', fontsize=16)
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()
    return fig


def plot_spectral_analysis(time_series: np.ndarray,
                         sampling_rate: float = 1.0,
                         window_type: str = 'hann',
                         figsize: Tuple[int, int] = (12, 8)) -> Figure:
    """Create spectral analysis plots (FFT and spectrogram)."""

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=figsize)

    # Generate sample data if none provided
    if len(time_series) == 0:
        t = np.linspace(0, 10, 1000)
        time_series = (np.sin(2*np.pi*2*t) + 0.5*np.sin(2*np.pi*5*t) +
                      0.3*np.random.randn(len(t)))
        sampling_rate = 100.0

    time = np.arange(len(time_series)) / sampling_rate

    # Plot 1: Time series
    ax1.plot(time, time_series, 'b-', linewidth=1)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Time Series')
    ax1.grid(True, alpha=0.3)

    # Plot 2: Power spectral density
    freqs = np.fft.fftfreq(len(time_series), 1/sampling_rate)
    fft_values = np.fft.fft(time_series)
    power_spectrum = np.abs(fft_values)**2

    # Only plot positive frequencies
    positive_freq_idx = freqs > 0
    ax2.loglog(freqs[positive_freq_idx], power_spectrum[positive_freq_idx])
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Power Spectral Density')
    ax2.set_title('Power Spectrum')
    ax2.grid(True, alpha=0.3)

    # Plot 3: Spectrogram
    f, t_spec, Sxx = spectrogram(time_series, sampling_rate, window=window_type)
    im = ax3.pcolormesh(t_spec, f, 10*np.log10(Sxx), shading='gouraud')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Frequency (Hz)')
    ax3.set_title('Spectrogram')
    plt.colorbar(im, ax=ax3, label='Power (dB)')

    # Plot 4: Autocorrelation
    autocorr = np.correlate(time_series, time_series, mode='full')
    autocorr = autocorr / np.max(autocorr)
    lags = np.arange(-len(time_series)+1, len(time_series))
    ax4.plot(lags, autocorr)
    ax4.set_xlabel('Lag')
    ax4.set_ylabel('Autocorrelation')
    ax4.set_title('Autocorrelation Function')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_distribution_analysis(data: np.ndarray,
                             distribution_types: List[str] = None,
                             figsize: Tuple[int, int] = (12, 10)) -> Figure:
    """Analyze and plot statistical distributions of extinction event data."""

    if distribution_types is None:
        distribution_types = ['normal', 'lognormal', 'exponential', 'gamma']

    fig, axes = plt.subplots(2, 2, figsize=figsize)
    axes = axes.flatten()

    # Generate sample data if none provided
    if len(data) == 0:
        data = np.random.lognormal(0, 1, 1000)

    # Plot 1: Histogram with fitted distributions
    ax = axes[0]
    n_bins = min(50, int(np.sqrt(len(data))))
    counts, bins, _ = ax.hist(data, bins=n_bins, density=True, alpha=0.7,
                             color='skyblue', edgecolor='black')

    # Fit distributions
    x_fit = np.linspace(np.min(data), np.max(data), 100)
    colors = ['red', 'green', 'orange', 'purple']

    for i, dist_name in enumerate(distribution_types):
        try:
            if dist_name == 'normal':
                mu, sigma = stats.norm.fit(data)
                y_fit = stats.norm.pdf(x_fit, mu, sigma)
                label = f'Normal (μ={mu:.2f}, σ={sigma:.2f})'
            elif dist_name == 'lognormal':
                sigma, loc, scale = stats.lognorm.fit(data, floc=0)
                y_fit = stats.lognorm.pdf(x_fit, sigma, loc, scale)
                label = f'Lognormal (σ={sigma:.2f})'
            elif dist_name == 'exponential':
                loc, scale = stats.expon.fit(data)
                y_fit = stats.expon.pdf(x_fit, loc, scale)
                label = f'Exponential (λ={1/scale:.2f})'
            elif dist_name == 'gamma':
                a, loc, scale = stats.gamma.fit(data)
                y_fit = stats.gamma.pdf(x_fit, a, loc, scale)
                label = f'Gamma (α={a:.2f})'
            else:
                continue

            ax.plot(x_fit, y_fit, color=colors[i % len(colors)],
                   linewidth=2, label=label)
        except:
            continue

    ax.set_xlabel('Value')
    ax.set_ylabel('Density')
    ax.set_title('Distribution Fitting')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 2: Q-Q plot
    ax = axes[1]
    stats.probplot(data, dist="norm", plot=ax)
    ax.set_title('Q-Q Plot (Normal Distribution)')
    ax.grid(True, alpha=0.3)

    # Plot 3: Cumulative distribution
    ax = axes[2]
    sorted_data = np.sort(data)
    cumulative = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    ax.plot(sorted_data, cumulative, 'b-', linewidth=2, label='Empirical CDF')

    # Add theoretical CDFs
    for i, dist_name in enumerate(distribution_types[:2]):  # Limit to 2 for clarity
        try:
            if dist_name == 'normal':
                mu, sigma = stats.norm.fit(data)
                theoretical_cdf = stats.norm.cdf(sorted_data, mu, sigma)
            elif dist_name == 'lognormal':
                sigma, loc, scale = stats.lognorm.fit(data, floc=0)
                theoretical_cdf = stats.lognorm.cdf(sorted_data, sigma, loc, scale)
            else:
                continue

            ax.plot(sorted_data, theoretical_cdf, '--',
                   color=colors[i], linewidth=2, label=f'{dist_name.title()} CDF')
        except:
            continue

    ax.set_xlabel('Value')
    ax.set_ylabel('Cumulative Probability')
    ax.set_title('Cumulative Distribution Functions')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 4: Box plot and statistics
    ax = axes[3]
    bp = ax.boxplot(data, patch_artist=True)
    bp['boxes'][0].set_facecolor('lightblue')

    # Add statistics text
    stats_text = f"""Statistics:
    Mean: {np.mean(data):.3f}
    Median: {np.median(data):.3f}
    Std: {np.std(data):.3f}
    Skewness: {stats.skew(data):.3f}
    Kurtosis: {stats.kurtosis(data):.3f}
    Min: {np.min(data):.3f}
    Max: {np.max(data):.3f}"""

    ax.text(1.1, 0.5, stats_text, transform=ax.transAxes,
           verticalalignment='center', fontsize=10,
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    ax.set_title('Box Plot & Statistics')
    ax.set_ylabel('Value')

    plt.tight_layout()
    return fig


def plot_monte_carlo_analysis(simulation_results: Dict[str, List[float]],
                            confidence_levels: List[float] = [0.68, 0.95, 0.99],
                            figsize: Tuple[int, int] = (14, 10)) -> Figure:
    """Visualize Monte Carlo simulation results with uncertainty quantification."""

    fig, axes = plt.subplots(2, 2, figsize=figsize)

    # Generate sample data if none provided
    if not simulation_results:
        n_sims = 1000
        simulation_results = {
            'casualties': np.random.lognormal(12, 2, n_sims).tolist(),
            'economic_damage': np.random.lognormal(15, 1.5, n_sims).tolist(),
            'recovery_time': np.random.gamma(2, 5, n_sims).tolist(),
            # Generate severity score samples and scale by 10
            'severity_score': (np.random.beta(2, 5, n_sims) * 10).tolist()
        }

    variables = list(simulation_results.keys())

    # Plot 1: Convergence analysis
    ax = axes[0, 0]
    for var in variables[:2]:  # Limit to 2 variables for clarity
        data = simulation_results[var]
        running_mean = np.cumsum(data) / np.arange(1, len(data) + 1)
        ax.plot(running_mean, label=var)

    ax.set_xlabel('Simulation Number')
    ax.set_ylabel('Running Mean')
    ax.set_title('Monte Carlo Convergence')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 2: Correlation matrix
    ax = axes[0, 1]
    df = pd.DataFrame(simulation_results)
    correlation_matrix = df.corr()

    im = ax.imshow(correlation_matrix, cmap='RdBu_r', vmin=-1, vmax=1)
    ax.set_xticks(range(len(variables)))
    ax.set_yticks(range(len(variables)))
    ax.set_xticklabels(variables, rotation=45, ha='right')
    ax.set_yticklabels(variables)

    # Add correlation values
    for i in range(len(variables)):
        for j in range(len(variables)):
            text = ax.text(j, i, f'{correlation_matrix.iloc[i, j]:.2f}',
                         ha="center", va="center", color="black")

    ax.set_title('Variable Correlations')
    plt.colorbar(im, ax=ax)

    # Plot 3: Uncertainty quantification
    ax = axes[1, 0]
    primary_var = variables[0] if variables else 'casualties'
    data = simulation_results.get(primary_var, [])

    if data:
        # Calculate percentiles for confidence intervals
        percentiles = []
        for conf in confidence_levels:
            lower = (1 - conf) / 2 * 100
            upper = (1 + conf) / 2 * 100
            p_lower = np.percentile(data, lower)
            p_upper = np.percentile(data, upper)
            percentiles.append((conf, p_lower, p_upper))

        # Plot histogram
        ax.hist(data, bins=50, density=True, alpha=0.7, color='lightblue')

        # Add confidence interval lines
        colors = ['red', 'orange', 'green']
        for i, (conf, p_lower, p_upper) in enumerate(percentiles):
            ax.axvline(p_lower, color=colors[i], linestyle='--',
                      label=f'{conf*100:.0f}% CI Lower')
            ax.axvline(p_upper, color=colors[i], linestyle='--',
                      label=f'{conf*100:.0f}% CI Upper')

        ax.axvline(np.mean(data), color='black', linestyle='-',
                  linewidth=2, label='Mean')
        ax.axvline(np.median(data), color='purple', linestyle='-',
                  linewidth=2, label='Median')

    ax.set_xlabel(primary_var)
    ax.set_ylabel('Density')
    ax.set_title(f'Uncertainty Distribution: {primary_var}')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 4: Sensitivity analysis (scatter plot matrix style)
    ax = axes[1, 1]
    if len(variables) >= 2:
        var1, var2 = variables[0], variables[1]
        data1 = simulation_results[var1]
        data2 = simulation_results[var2]

        # Create scatter plot with density coloring
        ax.scatter(data1, data2, alpha=0.5, s=10)

        # Add trend line
        try:
            z = np.polyfit(data1, data2, 1)
            p = np.poly1d(z)
            x_trend = np.linspace(min(data1), max(data1), 100)
            ax.plot(x_trend, p(x_trend), "r--", alpha=0.8, linewidth=2)

            # Calculate R²
            y_pred = p(data1)
            ss_res = np.sum((data2 - y_pred) ** 2)
            ss_tot = np.sum((data2 - np.mean(data2)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)
            ax.text(0.05, 0.95, f'R² = {r_squared:.3f}',
                   transform=ax.transAxes, bbox=dict(boxstyle='round',
                   facecolor='white', alpha=0.8))
        except:
            pass

        ax.set_xlabel(var1)
        ax.set_ylabel(var2)
        ax.set_title(f'Relationship: {var2} vs {var1}')

    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_parameter_sweep_3d(parameter_data: Dict[str, Any],
                           x_param: str, y_param: str, z_param: str,
                           figsize: Tuple[int, int] = (12, 9)) -> Figure:
    """Create 3D parameter sweep visualization."""

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')

    # Generate sample data if none provided
    if not parameter_data:
        x_vals = np.linspace(0, 10, 20)
        y_vals = np.linspace(0, 5, 15)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = np.sin(X) * np.cos(Y) + 0.1 * np.random.randn(*X.shape)

        x_data = X.flatten()
        y_data = Y.flatten()
        z_data = Z.flatten()
    else:
        x_data = parameter_data.get(x_param, [])
        y_data = parameter_data.get(y_param, [])
        z_data = parameter_data.get(z_param, [])

    # Create 3D scatter plot
    scatter = ax.scatter(x_data, y_data, z_data, c=z_data,
                        cmap='viridis', s=50, alpha=0.7)

    # Add surface if data is gridded
    try:
        if len(set(x_data)) * len(set(y_data)) == len(x_data):
            # Data appears to be on a grid
            unique_x = sorted(set(x_data))
            unique_y = sorted(set(y_data))

            Z_grid = np.array(z_data).reshape(len(unique_y), len(unique_x))
            X_grid, Y_grid = np.meshgrid(unique_x, unique_y)

            ax.plot_surface(X_grid, Y_grid, Z_grid, alpha=0.3, cmap='viridis')
    except:
        pass

    ax.set_xlabel(x_param)
    ax.set_ylabel(y_param)
    ax.set_zlabel(z_param)
    ax.set_title(f'3D Parameter Sweep: {z_param} vs {x_param} & {y_param}')

    # Add colorbar
    plt.colorbar(scatter, ax=ax, shrink=0.5, aspect=20)

    return fig


def plot_uncertainty_bands(time_data: np.ndarray,
                         ensemble_data: np.ndarray,
                         percentiles: List[float] = [10, 25, 75, 90],
                         figsize: Tuple[int, int] = (12, 8)) -> Figure:
    """Plot ensemble data with uncertainty bands."""

    fig, ax = plt.subplots(figsize=figsize)

    # Generate sample data if none provided
    if len(time_data) == 0 or ensemble_data.size == 0:
        time_data = np.linspace(0, 10, 100)
        n_ensemble = 50
        ensemble_data = np.zeros((n_ensemble, len(time_data)))

        for i in range(n_ensemble):
            noise = np.random.normal(0, 0.5, len(time_data))
            trend = np.exp(-time_data/5) * np.sin(time_data)
            ensemble_data[i] = trend + noise

    # Calculate percentiles
    percentile_data = {}
    for p in percentiles:
        percentile_data[p] = np.percentile(ensemble_data, p, axis=0)

    # Calculate mean and median
    mean_data = np.mean(ensemble_data, axis=0)
    median_data = np.median(ensemble_data, axis=0)

    # Plot uncertainty bands
    colors = ['lightgray', 'silver', 'darkgray']
    alphas = [0.3, 0.5, 0.7]

    # Fill between percentiles
    if len(percentiles) >= 4:
        ax.fill_between(time_data, percentile_data[percentiles[0]],
                       percentile_data[percentiles[-1]],
                       alpha=alphas[0], color=colors[0],
                       label=f'{percentiles[0]}-{percentiles[-1]}%')

        ax.fill_between(time_data, percentile_data[percentiles[1]],
                       percentile_data[percentiles[-2]],
                       alpha=alphas[1], color=colors[1],
                       label=f'{percentiles[1]}-{percentiles[-2]}%')

    # Plot central tendencies
    ax.plot(time_data, mean_data, 'b-', linewidth=2, label='Mean')
    ax.plot(time_data, median_data, 'r-', linewidth=2, label='Median')

    # Plot some individual ensemble members
    n_show = min(5, ensemble_data.shape[0])
    for i in range(n_show):
        ax.plot(time_data, ensemble_data[i], 'k-', alpha=0.1, linewidth=0.5)

    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.set_title('Ensemble Forecast with Uncertainty Bands')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


# Demo function
def demo_scientific_plots():
    """Demonstrate scientific plotting capabilities."""

    print("🔬 Demonstrating Scientific Plotting Capabilities")
    print("=" * 50)    # Demo 1: Phase space plot
    print("1. Creating phase space plot...")
    try:
        data = {}  # Will use default sample data
        fig1 = plot_phase_space(data, "x", "y")
        print("   ✅ Phase space plot created")
        plt.close(fig1)
    except Exception as e:
        print(f"   ❌ Error creating phase space plot: {e}")

    # Demo 2: Spectral analysis
    print("2. Creating spectral analysis...")
    try:
        time_series = np.array([])  # Will use default sample data
        fig2 = plot_spectral_analysis(time_series)
        print("   ✅ Spectral analysis created")
        plt.close(fig2)
    except Exception as e:
        print(f"   ❌ Error creating spectral analysis: {e}")

    # Demo 3: Distribution analysis
    print("3. Creating distribution analysis...")
    try:
        data = np.array([])  # Will use default sample data
        fig3 = plot_distribution_analysis(data)
        print("   ✅ Distribution analysis created")
        plt.close(fig3)
    except Exception as e:
        print(f"   ❌ Error creating distribution analysis: {e}")

    # Demo 4: Monte Carlo analysis
    print("4. Creating Monte Carlo analysis...")
    try:
        results = {}  # Will use default sample data
        fig4 = plot_monte_carlo_analysis(results)
        print("   ✅ Monte Carlo analysis created")
        plt.close(fig4)
    except Exception as e:
        print(f"   ❌ Error creating Monte Carlo analysis: {e}")

    print("\n✅ Scientific plotting demonstrations completed!")


if __name__ == "__main__":
    demo_scientific_plots()
