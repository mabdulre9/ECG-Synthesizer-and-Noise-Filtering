# ECG Synthesizer & Noise Removal Using FIR and IIR Digital Filters
## 🌐 Live Demo: https://ecg-synthesizer-and-noise-filtering.streamlit.app/
## Digital Signal Processing (DSP) Laboratory

**Course:** EE-419K-L
**Semester:** Fall 2025
**Department:** Electrical Engineering
**University:** University of Engineering and Technology (UET), Taxila
**Instructor:** Engr. Zainab Shahid
**Developer:** Muhammad Abdul Rehman (22-EE-040)

---

## Project Overview

This project presents an **interactive Streamlit-based application** for:

* Synthetic **ECG signal generation**
* **Realistic ECG noise modeling**
* **Noise removal using FIR and IIR digital filters**
* **Quantitative performance evaluation** using SNR and MSE
* **Frequency-domain analysis** of signals and filters

The application is designed to support **complex engineering problem analysis** in Digital Signal Processing, focusing on balancing **noise suppression** and **signal preservation**.

---

## Learning Objectives

* Understand ECG signal characteristics in **time and frequency domains**
* Model common ECG noise sources:

  * Power Line Interference (50 Hz)
  * High-frequency EMG noise
  * Low-frequency baseline wander
* Design and implement:

  * **FIR filters** (High-pass, Notch, Low-pass)
  * **IIR filters** (Butterworth and Notch)
* Evaluate filter performance using:

  * Signal-to-Noise Ratio (SNR)
  * Mean Squared Error (MSE)
* Compare FIR vs IIR behavior in both domains

---

## Engineering Problem Context

This project addresses a **Complex Engineering Problem (CEP)** by:

* Applying **DSP theory** to biomedical signals
* Using **filter design trade-offs** (order, cutoff frequencies)
* Performing **quantitative signal quality assessment**
* Implementing a **reconfigurable software framework** for ECG processing

---

## ECG Signal & Noise Modeling

### ECG Generation

* Synthetic ECG generated using **NeuroKit2**
* Adjustable:

  * Sampling frequency (250–2000 Hz)
  * Signal duration (2–15 seconds)

### Noise Sources

| Noise Type              | Frequency Range | Description                    |
| ----------------------- | --------------- | ------------------------------ |
| Baseline Wander         | < 1 Hz          | Respiration & motion artifacts |
| Power Line Interference | 50 Hz           | Electrical mains interference  |
| High-Frequency Noise    | > 100 Hz        | EMG & sensor noise             |

Noise strengths are controlled via interactive sliders.

---

## Filter Design Methodology

### FIR Filtering

* Window-based FIR design using `firwin`
* Components:

  * High-pass filter (baseline removal)
  * Notch filter (50 Hz suppression)
  * Low-pass filter (HF noise removal)
* Zero-phase filtering using `filtfilt`

### IIR Filtering

* Butterworth filters for HPF & LPF
* IIR notch filter for 50 Hz interference
* Efficient low-order design with minimal computational cost

---

## Analysis & Visualization

The application provides:

* Time-domain plots:

  * Clean ECG
  * Noisy ECG
  * FIR-filtered ECG
  * IIR-filtered ECG
* Frequency-domain analysis:

  * FFT of clean and noisy ECG
  * Frequency responses of FIR and IIR filters
* Comparative visualization for performance evaluation

---

## Performance Metrics

### Signal-to-Noise Ratio (SNR)

Evaluates noise suppression effectiveness:

* Before filtering
* After FIR filtering
* After IIR filtering

### Mean Squared Error (MSE)

Measures signal distortion relative to the clean ECG.

---

## Technologies Used

* **Python**
* **Streamlit** – Web interface
* **NumPy** – Numerical operations
* **SciPy** – Filter design and signal processing
* **Matplotlib** – Visualization
* **NeuroKit2** – ECG simulation

---

## How to Run the Project

### 1. Install Dependencies

```bash
pip install streamlit numpy scipy matplotlib neurokit2
```

### 2. Run the Application

```bash
streamlit run app.py
```
## License

This project is intended for **academic and educational use only**.
