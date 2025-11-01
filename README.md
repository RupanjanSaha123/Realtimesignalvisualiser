# 🎵 Real-Time Signal Processing Visualizer

An **interactive desktop application** built using **Python and Tkinter** to visualize and analyze signals in **real time**.  
It provides an educational and intuitive way to explore the effects of **frequency, amplitude, noise**, and **digital filtering** on signals — right from your desktop.

---

## 🌟 Features

✅ **User-friendly GUI** – Intuitive control panel with smooth, real-time visual updates.  
✅ **Signal Types Supported:**
- Sine Wave  
- Square Wave  
- Sawtooth Wave  

✅ **Customizable Parameters:**
- Frequency: `1 – 20 Hz`  
- Amplitude: `0.1 – 2.0`  
- Noise Level: `0.0 – 1.0`  

✅ **Digital Filtering Options:**
- **Low-Pass** and **High-Pass** Butterworth filters  
- Adjustable cutoff frequency: `1 – 50 Hz`

✅ **Real-Time Visualization:**
- Time-domain plot (original vs filtered signal)  
- Frequency-domain plot (FFT spectra)  

✅ **Instant Feedback:**
- Every parameter change updates the visualization immediately  
- Simple reset option to return to defaults

---

## 🧠 Motivation

Signal processing is a core topic in **Electronics and Communication Engineering** and **Data Science**, but often difficult to grasp through equations alone.  
This project bridges that gap by offering a **visual, interactive experience** — helping students and enthusiasts **see** how filters, noise, and frequency affect real signals.

---

## ⚙️ Getting Started

### 🧩 Dependencies

Ensure you have **Python 3.6+** installed.  
Then install the required Python libraries:

```bash
pip install numpy scipy matplotlib

```
## Note: Tkinter is bundled with standard Python installations (no extra install needed).

▶️ How to Run

Save the script as signal_visualizer.py in your project folder.
Open your terminal or command prompt in that folder.
Run the application:
```bash
python signal_visualizer.py
```
The GUI window will launch with sliders and dropdowns for real-time control.

## 🕹️ Controls Overview

| Control              | Description                                  |
| -------------------- | -------------------------------------------- |
| **Signal Type**      | Select waveform (Sine, Square, or Sawtooth)  |
| **Frequency Slider** | Adjusts signal frequency (1–20 Hz)           |
| **Amplitude Slider** | Controls waveform amplitude                  |
| **Noise Level**      | Adds white noise to the signal               |
| **Filter Type**      | Select Low-Pass or High-Pass filter          |
| **Cutoff Frequency** | Sets cutoff for filtering (1–50 Hz)          |
| **Reset Button**     | Restores all controls to their default state |

## 📊 Screenshots
<img width="1905" height="1012" alt="image" src="https://github.com/user-attachments/assets/eebdfd02-7d95-4e37-aad0-d57a8bb65ef2" />
<img width="1904" height="1008" alt="image" src="https://github.com/user-attachments/assets/7b7dee4d-6eb0-46cc-a3f6-fdae499212ef" />
<img width="1904" height="1012" alt="image" src="https://github.com/user-attachments/assets/72215321-cdd5-4f30-b760-1ba15a108f07" />




Example layout:
Left side: Control panel;
Right side: Two Matplotlib plots;
Top: Time-domain waveform;
Bottom: Frequency-domain FFT;

## 🧪 Example Workflow

Choose Sine Wave with frequency = 10 Hz, amplitude = 1.5.
Add noise level = 0.5.
Apply a Low-Pass filter with cutoff = 8 Hz.
Watch the difference between original and filtered signals in real-time!

## 🤝 Contributing

Contributions are welcome!
If you’d like to improve the visualizer or add new features:

Fork the repository.
Create a new feature branch.
Commit your changes.
Submit a pull request with clear details.

## 👨‍💻 Author

Developed by: An Expert Python Developer(Comet)😂 
Special Thanks: Rupanjan Saha for creating this in a single prompt ❤️

**🧭 "See the invisible world of signals come alive — interactively and intuitively!"**
