import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import neurokit2 as nk
from scipy.signal import firwin, butter, filtfilt, iirnotch, freqz , lfilter
from scipy import signal

# ============================================================
st.set_page_config(page_title="ECG Noise Removal Project")
st.title("ECG Noise Removal using FIR and IIR Digital Filters")
st.write("Digital Signal Processing | Complex Engineering Problem")
st.markdown("---")

# ============================================================
# 1. ECG SIGNAL GENERATION
# ============================================================
st.subheader("1. ECG Signal Generation")

Fs = st.slider("Sampling Frequency (Hz)", 250, 2000, 360)
duration = st.slider("Signal Duration (seconds)", 2, 15, 6)


# Synthetic ECG (PQRST-like)
ecg_clean = nk.ecg_simulate(duration=duration, sampling_rate=Fs)
t = np.arange(len(ecg_clean)) / Fs


fig, ax = plt.subplots()
ax.plot(t, ecg_clean)
ax.set_title("Clean ECG Signal")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.grid(True)
ax.axis("on")
st.pyplot(fig, width="stretch")

# ============================================================
# 2. NOISE MODELING
# ============================================================
st.markdown("---")
st.subheader("2. Noise Analysis & Addition")

pli_amp = st.slider("50 Hz Power Line Interference Strength", 0.0, 1.0, 0.2)
hf_amp = st.slider("High Frequency Noise (>100 Hz)", 0.0, 1.0, 0.05)
baseline_amp = st.slider("Baseline Wander (<1 Hz)", 0.0, 1.0, 0.3)

pli_noise = pli_amp * np.sin(2 * np.pi * 50 * t)
hf_noise = hf_amp * np.random.randn(len(t))
baseline_noise = baseline_amp * np.sin(2 * np.pi * 0.3 * t)

total_noise = pli_noise + hf_noise + baseline_noise
ecg_noisy = ecg_clean + total_noise

fig, ax = plt.subplots()
ax.plot(t, total_noise)
ax.set_title("Noise = PLI + High Freq Noise + Baseline Wander")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.grid(True)
ax.axis("on")
st.pyplot(fig, width="stretch")

fig, ax = plt.subplots()
ax.plot(t, ecg_noisy)
ax.set_title("Noisy ECG Signal")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.grid(True)
ax.axis("on")
st.pyplot(fig, width="stretch")

# ============================================================
# 3. FREQUENCY DOMAIN ANALYSIS
# ============================================================
st.markdown("---")
st.subheader("3. Frequency Analysis (FFT)")

fft_vals = np.fft.fft(ecg_noisy)
freqs = np.fft.fftfreq(len(fft_vals), 1/Fs)

fig, ax = plt.subplots()
ax.plot(freqs[:len(freqs)//2], np.abs(fft_vals[:len(freqs)//2]))
ax.set_title("Frequency Spectrum of Noisy ECG")
ax.set_xlim(0, 150)
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Magnitude")
ax.axis("on")
ax.grid(True)
st.pyplot(fig, width="stretch")

# ============================================================
# 4. FIR FILTER DESIGN
# ============================================================
st.markdown("---")
st.subheader("4. FIR Filter Design")

fir_order = st.slider("FIR Filter Order", 1, 399, 101, step=2)

# FIR filters
hp_fir = firwin(fir_order, 1, fs=Fs, pass_zero=False)
lp_fir = firwin(fir_order, 100, fs=Fs)
notch_fir = firwin(fir_order, [49, 51], fs=Fs, pass_zero=True)

# Apply FIR filtering
ecg_fir = filtfilt(hp_fir, [1], ecg_noisy)
ecg_fir = filtfilt(notch_fir, [1], ecg_fir)
ecg_fir = filtfilt(lp_fir, [1], ecg_fir)

fig, ax = plt.subplots()
ax.plot(t, ecg_fir)
ax.set_title("FIR Filtered ECG Signal")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.grid(True)
ax.axis("on")
st.pyplot(fig, width="stretch")
# ============================================================

# ===============================
# 6. IIR Filter Design
# ===============================

st.subheader("5. IIR Filter Design")

iir_order = st.slider("IIR Filter Order", 1, 10, 4)

b_hp, a_hp = butter(iir_order, 1/(Fs/2), btype='high')
b_lp, a_lp = butter(iir_order, 100/(Fs/2), btype='low')
b_notch, a_notch = iirnotch(50/(Fs/2), 30)

# Apply IIR filtering
ecg_iir = filtfilt(b_hp, a_hp, ecg_noisy)
ecg_iir = filtfilt(b_notch, a_notch, ecg_iir)
ecg_iir = filtfilt(b_lp, a_lp, ecg_iir)
fig, ax = plt.subplots()
ax.plot(t, ecg_iir)
ax.set_title("IIR Filtered ECG Signal")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.grid(True)
ax.axis("on")
st.pyplot(fig, width="stretch")
# ============================================================

st.markdown("---")

# ===============================
# 7. Comparison Plots
# ===============================
st.subheader("6. Comparison of Clean, Noisy, FIR, and IIR Filtered Signals")
fig, ax = plt.subplots(4, 1, figsize=(10, 12), sharex=True)
ax[0].plot(t, ecg_clean, color='g')
ax[0].set_title("Clean ECG Signal")
ax[0].grid(True)
ax[1].plot(t, ecg_noisy, color='r')
ax[1].set_title("Noisy ECG Signal")
ax[1].grid(True)
ax[2].plot(t, ecg_fir, color='b')
ax[2].set_title(f"FIR Filtered ECG Signal (Order={fir_order})")
ax[2].grid(True)
ax[3].plot(t, ecg_iir, color='m')
ax[3].set_title(f"IIR Filtered ECG Signal (Order={iir_order})")
ax[3].set_xlabel("Time (s)")
ax[3].grid(True)
st.pyplot(fig, width="stretch")
# ============================================================

# ===============================
# 8. Frequency Response Plots
# ===============================
st.markdown("---")

st.subheader("7. Frequency Response of FIR and IIR Filters")
fig, ax = plt.subplots(3, 2, figsize=(12, 10))
# FIR Filter Responses
for i, (b, label) in enumerate(zip([hp_fir, notch_fir, lp_fir], ['High-Pass FIR', 'Notch FIR', 'Low-Pass FIR'])):
    w, h = freqz(b, worN=8000)
    ax[i, 0].plot(0.5*Fs*w/np.pi, np.abs(h), 'b')
    ax[i, 0].set_title(f"{label} Frequency Response")
    ax[i, 0].set_xlabel('Frequency (Hz)')
    ax[i, 0].set_ylabel('Gain')
    ax[i, 0].grid(True)
# IIR Filter Responses
for i, (b, a, label) in enumerate(zip([b_hp, b_notch, b_lp], [a_hp, a_notch, a_lp], ['High-Pass IIR', 'Notch IIR', 'Low-Pass IIR'])):
    w, h = freqz(b, a, worN=8000)
    ax[i, 1].plot(0.5*Fs*w/np.pi, np.abs(h), 'r')
    ax[i, 1].set_title(f"{label} Frequency Response")
    ax[i, 1].set_xlabel('Frequency (Hz)')
    ax[i, 1].set_ylabel('Gain')
    ax[i, 1].grid(True)

plt.tight_layout() # Call this BEFORE st.pyplot
st.pyplot(fig, width="stretch")

# ============================================================


# ===============================
# 9. SNR Calculation
# ===============================

st.markdown("---")

st.subheader("8. Signal to Noise Ratio & Mean Squared Error")
def snr_db(signal, noise):
    return 10 * np.log10(np.sum(signal**2) / np.sum(noise**2))

snr_before = snr_db(ecg_clean, ecg_noisy - ecg_clean)
snr_fir = snr_db(ecg_clean, ecg_fir - ecg_clean)
snr_iir = snr_db(ecg_clean, ecg_iir - ecg_clean)

# ===============================
# 10. MSE Calculation
# ===============================
mse_fir = np.mean((ecg_clean - ecg_fir)**2)
mse_iir = np.mean((ecg_clean - ecg_iir)**2)

st.warning(f"""
**Signal-to-Noise Ratio (SNR) Analysis:**
* SNR Before Filtering: {snr_before:.2f} dB
* SNR After FIR Filtering: {snr_fir:.2f} dB
* SNR After IIR Filtering: {snr_iir:.2f} dB

**Mean Squared Error (MSE) Analysis:**
* MSE FIR: {mse_fir:.6f}
* MSE IIR: {mse_iir:.6f}
""")



