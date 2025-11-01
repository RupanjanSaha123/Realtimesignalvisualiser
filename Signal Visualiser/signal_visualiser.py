"""
Real-time Signal Processing Visualizer
======================================
A comprehensive Tkinter-based application for visualizing signal processing operations.
Includes signal generation, filtering, and frequency domain analysis with real-time updates.

Author: Expert Python Developer
Date: October 31, 2025
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
from scipy.signal import butter, filtfilt, get_window
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class SignalProcessingVisualizer:
    """
    Main application class for real-time signal processing visualization.
    Handles GUI setup, signal generation, filtering, and plot updates.
    """
    
    def __init__(self, root):
        """
        Initialize the application and set up the GUI.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.title("Real-Time Signal Processing Visualizer")
        self.root.geometry("1400x700")
        self.root.configure(bg='#f0f0f0')
        
        # Signal generation parameters
        self.sampling_rate = 1000  # Hz
        self.duration = 2  # seconds
        
        # Create GUI layout
        self._setup_gui()
        
        # Perform initial plot
        self._update_plots()
    
    def _setup_gui(self):
        """
        Set up the main GUI layout with control panel and visualization area.
        """
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # ===== LEFT PANEL: CONTROL PANEL =====
        self._create_control_panel(main_frame)
        
        # ===== RIGHT PANEL: VISUALIZATION =====
        self._create_visualization_panel(main_frame)
    
    def _create_control_panel(self, parent):
        """
        Create the left-side control panel with all user input controls.
        
        Args:
            parent: Parent frame to place the control panel in
        """
        control_frame = ttk.LabelFrame(parent, text="Control Panel", padding="15")
        control_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W), padx=(0, 10), pady=0)
        
        # Configure grid for proper spacing
        control_frame.columnconfigure(0, weight=1)
        
        current_row = 0
        
        # ===== SIGNAL TYPE DROPDOWN =====
        ttk.Label(control_frame, text="Signal Type:").grid(row=current_row, column=0, sticky=tk.W, pady=(0, 5))
        current_row += 1
        
        self.signal_type_var = tk.StringVar(value="Sine")
        signal_dropdown = ttk.Combobox(
            control_frame, 
            textvariable=self.signal_type_var, 
            values=["Sine", "Square", "Sawtooth"],
            state="readonly",
            width=20
        )
        signal_dropdown.grid(row=current_row, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        signal_dropdown.bind("<<ComboboxSelected>>", lambda e: self._update_plots())
        current_row += 1
        
        # ===== FREQUENCY SLIDER =====
        ttk.Label(control_frame, text="Frequency (Hz):").grid(row=current_row, column=0, sticky=tk.W, pady=(0, 5))
        current_row += 1
        
        self.frequency_var = tk.DoubleVar(value=5)
        frequency_slider = ttk.Scale(
            control_frame,
            from_=1,
            to=20,
            orient=tk.HORIZONTAL,
            variable=self.frequency_var,
            command=lambda v: self._update_frequency_label()
        )
        frequency_slider.grid(row=current_row, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        frequency_slider.bind("<ButtonRelease-1>", lambda e: self._update_plots())
        current_row += 1
        
        self.frequency_label = ttk.Label(control_frame, text="5.0 Hz")
        self.frequency_label.grid(row=current_row, column=0, sticky=tk.W, pady=(0, 15))
        current_row += 1
        
        # ===== AMPLITUDE SLIDER =====
        ttk.Label(control_frame, text="Amplitude:").grid(row=current_row, column=0, sticky=tk.W, pady=(0, 5))
        current_row += 1
        
        self.amplitude_var = tk.DoubleVar(value=1.0)
        amplitude_slider = ttk.Scale(
            control_frame,
            from_=0.1,
            to=2.0,
            orient=tk.HORIZONTAL,
            variable=self.amplitude_var,
            command=lambda v: self._update_amplitude_label()
        )
        amplitude_slider.grid(row=current_row, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        amplitude_slider.bind("<ButtonRelease-1>", lambda e: self._update_plots())
        current_row += 1
        
        self.amplitude_label = ttk.Label(control_frame, text="1.0")
        self.amplitude_label.grid(row=current_row, column=0, sticky=tk.W, pady=(0, 15))
        current_row += 1
        
        # ===== NOISE SLIDER =====
        ttk.Label(control_frame, text="Noise Level:").grid(row=current_row, column=0, sticky=tk.W, pady=(0, 5))
        current_row += 1
        
        self.noise_var = tk.DoubleVar(value=0.1)
        noise_slider = ttk.Scale(
            control_frame,
            from_=0.0,
            to=1.0,
            orient=tk.HORIZONTAL,
            variable=self.noise_var,
            command=lambda v: self._update_noise_label()
        )
        noise_slider.grid(row=current_row, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        noise_slider.bind("<ButtonRelease-1>", lambda e: self._update_plots())
        current_row += 1
        
        self.noise_label = ttk.Label(control_frame, text="0.1")
        self.noise_label.grid(row=current_row, column=0, sticky=tk.W, pady=(0, 15))
        current_row += 1
        
        # ===== FILTER TYPE DROPDOWN =====
        ttk.Label(control_frame, text="Filter Type:").grid(row=current_row, column=0, sticky=tk.W, pady=(0, 5))
        current_row += 1
        
        self.filter_type_var = tk.StringVar(value="Low-Pass")
        filter_dropdown = ttk.Combobox(
            control_frame,
            textvariable=self.filter_type_var,
            values=["Low-Pass", "High-Pass"],
            state="readonly",
            width=20
        )
        filter_dropdown.grid(row=current_row, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        filter_dropdown.bind("<<ComboboxSelected>>", lambda e: self._update_plots())
        current_row += 1
        
        # ===== FILTER CUTOFF SLIDER =====
        ttk.Label(control_frame, text="Filter Cutoff (Hz):").grid(row=current_row, column=0, sticky=tk.W, pady=(0, 5))
        current_row += 1
        
        self.cutoff_var = tk.DoubleVar(value=10)
        cutoff_slider = ttk.Scale(
            control_frame,
            from_=1,
            to=50,
            orient=tk.HORIZONTAL,
            variable=self.cutoff_var,
            command=lambda v: self._update_cutoff_label()
        )
        cutoff_slider.grid(row=current_row, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        cutoff_slider.bind("<ButtonRelease-1>", lambda e: self._update_plots())
        current_row += 1
        
        self.cutoff_label = ttk.Label(control_frame, text="10.0 Hz")
        self.cutoff_label.grid(row=current_row, column=0, sticky=tk.W, pady=(0, 15))
        current_row += 1
        
        # ===== RESET BUTTON =====
        reset_button = ttk.Button(control_frame, text="Reset to Defaults", command=self._reset_defaults)
        reset_button.grid(row=current_row, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def _create_visualization_panel(self, parent):
        """
        Create the right-side visualization panel with matplotlib plots.
        
        Args:
            parent: Parent frame to place the visualization panel in
        """
        viz_frame = ttk.LabelFrame(parent, text="Signal Visualization", padding="10")
        viz_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W), padx=0, pady=0)
        
        # Configure grid weights
        viz_frame.columnconfigure(0, weight=1)
        viz_frame.rowconfigure(0, weight=1)
        
        # Create matplotlib figure with two subplots
        self.fig = Figure(figsize=(10, 8), dpi=100)
        self.fig.patch.set_facecolor('#f0f0f0')
        
        # Top plot (Time Domain)
        self.ax_time = self.fig.add_subplot(2, 1, 1)
        self.ax_time.set_xlabel("Time (s)")
        self.ax_time.set_ylabel("Amplitude")
        self.ax_time.set_title("Time Domain - Original (blue) vs Filtered (orange)")
        self.ax_time.grid(True, alpha=0.3)
        
        # Bottom plot (Frequency Domain)
        self.ax_freq = self.fig.add_subplot(2, 1, 2)
        self.ax_freq.set_xlabel("Frequency (Hz)")
        self.ax_freq.set_ylabel("Magnitude")
        self.ax_freq.set_title("Frequency Domain (FFT) - Original (blue) vs Filtered (orange)")
        self.ax_freq.grid(True, alpha=0.3)
        
        # Adjust layout
        self.fig.tight_layout()
        
        # Embed matplotlib figure in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    
    def _generate_signal(self):
        """
        Generate the base signal based on user parameters.
        
        Returns:
            tuple: (time_array, signal_array)
        """
        # Create time array
        t = np.linspace(0, self.duration, self.sampling_rate * self.duration, endpoint=False)
        
        # Get user parameters
        frequency = self.frequency_var.get()
        amplitude = self.amplitude_var.get()
        noise_level = self.noise_var.get()
        signal_type = self.signal_type_var.get()
        
        # Generate base signal
        if signal_type == "Sine":
            signal = amplitude * np.sin(2 * np.pi * frequency * t)
        elif signal_type == "Square":
            signal = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
        elif signal_type == "Sawtooth":
            signal = amplitude * (2 * (t * frequency - np.floor(t * frequency + 0.5)))
        else:
            signal = amplitude * np.sin(2 * np.pi * frequency * t)
        
        # Add noise
        if noise_level > 0:
            noise = np.random.normal(0, noise_level, len(signal))
            signal = signal + noise
        
        return t, signal
    
    def _apply_filter(self, signal):
        """
        Apply the selected filter to the signal.
        
        Args:
            signal: Input signal array
            
        Returns:
            filtered_signal: The filtered signal
        """
        # Get filter parameters
        filter_type = self.filter_type_var.get()
        cutoff_frequency = self.cutoff_var.get()
        
        # Normalize cutoff frequency (must be less than Nyquist frequency)
        nyquist_frequency = self.sampling_rate / 2
        normalized_cutoff = cutoff_frequency / nyquist_frequency
        
        # Ensure normalized cutoff is valid
        normalized_cutoff = max(0.001, min(normalized_cutoff, 0.999))
        
        try:
            # Design Butterworth filter (order 4)
            if filter_type == "Low-Pass":
                b, a = butter(4, normalized_cutoff, btype='low')
            else:  # High-Pass
                b, a = butter(4, normalized_cutoff, btype='high')
            
            # Apply filter (forward-backward to maintain phase)
            filtered_signal = filtfilt(b, a, signal)
            return filtered_signal
        except Exception as e:
            print(f"Filter error: {e}")
            return signal
    
    def _compute_fft(self, signal):
        """
        Compute the Fast Fourier Transform of the signal.
        
        Args:
            signal: Input signal array
            
        Returns:
            tuple: (frequencies, magnitude_spectrum)
        """
        # Compute FFT
        fft_values = fft(signal)
        
        # Compute frequency array
        frequencies = fftfreq(len(signal), 1 / self.sampling_rate)
        
        # Only use positive frequencies
        positive_freq_idx = frequencies > 0
        frequencies = frequencies[positive_freq_idx]
        magnitude = np.abs(fft_values[positive_freq_idx])
        
        return frequencies, magnitude
    
    def _update_plots(self):
        """
        Update both time-domain and frequency-domain plots with current parameters.
        This is the main plot update function that handles real-time interactivity.
        """
        # Generate signal
        t, original_signal = self._generate_signal()
        
        # Apply filter
        filtered_signal = self._apply_filter(original_signal)
        
        # Compute FFTs
        freq_original, mag_original = self._compute_fft(original_signal)
        freq_filtered, mag_filtered = self._compute_fft(filtered_signal)
        
        # Clear previous plots
        self.ax_time.clear()
        self.ax_freq.clear()
        
        # ===== TIME DOMAIN PLOT =====
        self.ax_time.plot(t, original_signal, label="Original Signal", linewidth=1.5, alpha=0.7, color='#1f77b4')
        self.ax_time.plot(t, filtered_signal, label="Filtered Signal", linewidth=1.5, alpha=0.7, color='#ff7f0e')
        self.ax_time.set_xlabel("Time (s)", fontsize=10)
        self.ax_time.set_ylabel("Amplitude", fontsize=10)
        self.ax_time.set_title("Time Domain - Original (blue) vs Filtered (orange)", fontsize=11, fontweight='bold')
        self.ax_time.legend(loc='upper right', fontsize=9)
        self.ax_time.grid(True, alpha=0.3)
        self.ax_time.set_xlim(0, self.duration)
        
        # ===== FREQUENCY DOMAIN PLOT =====
        self.ax_freq.plot(freq_original, mag_original, label="Original Signal FFT", linewidth=1.5, alpha=0.7, color='#1f77b4')
        self.ax_freq.plot(freq_filtered, mag_filtered, label="Filtered Signal FFT", linewidth=1.5, alpha=0.7, color='#ff7f0e')
        self.ax_freq.set_xlabel("Frequency (Hz)", fontsize=10)
        self.ax_freq.set_ylabel("Magnitude", fontsize=10)
        self.ax_freq.set_title("Frequency Domain (FFT) - Original (blue) vs Filtered (orange)", fontsize=11, fontweight='bold')
        self.ax_freq.legend(loc='upper right', fontsize=9)
        self.ax_freq.grid(True, alpha=0.3)
        self.ax_freq.set_xlim(0, 50)
        
        # Adjust layout and redraw
        self.fig.tight_layout()
        self.canvas.draw()
    
    def _update_frequency_label(self):
        """Update the frequency label with current slider value."""
        value = self.frequency_var.get()
        self.frequency_label.config(text=f"{value:.1f} Hz")
    
    def _update_amplitude_label(self):
        """Update the amplitude label with current slider value."""
        value = self.amplitude_var.get()
        self.amplitude_label.config(text=f"{value:.2f}")
    
    def _update_noise_label(self):
        """Update the noise label with current slider value."""
        value = self.noise_var.get()
        self.noise_label.config(text=f"{value:.2f}")
    
    def _update_cutoff_label(self):
        """Update the cutoff frequency label with current slider value."""
        value = self.cutoff_var.get()
        self.cutoff_label.config(text=f"{value:.1f} Hz")
    
    def _reset_defaults(self):
        """Reset all parameters to default values."""
        self.signal_type_var.set("Sine")
        self.frequency_var.set(5)
        self.amplitude_var.set(1.0)
        self.noise_var.set(0.1)
        self.filter_type_var.set("Low-Pass")
        self.cutoff_var.set(10)
        
        # Update labels
        self._update_frequency_label()
        self._update_amplitude_label()
        self._update_noise_label()
        self._update_cutoff_label()
        
        # Update plots
        self._update_plots()


def main():
    """
    Main entry point for the application.
    """
    root = tk.Tk()
    app = SignalProcessingVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
    