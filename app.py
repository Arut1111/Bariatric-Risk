
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Оценка риска осложнений", page_icon="⚠️", layout="centered")
st.title("⚠️ Прогностическая модель риска послеоперационных осложнений")

st.markdown("""Введите параметры пациента для оценки риска осложнений после бариатрической операции.
Модель учитывает верифицированные клинические признаки и визуализирует расчёт вероятности осложнений.""")

with st.form("risk_form"):
    hb = st.number_input("Гемоглобин (г/л)", min_value=0.0, step=0.1)
    vas = st.slider("Боль по ВАШ (0–10)", 0.0, 10.0, 3.0, step=0.1)
    drain = st.checkbox("Объём дренажа ≥ 70 мл/сут")
    neutro = st.number_input("Палочкоядерные нейтрофилы (%)", min_value=0.0, step=0.1)
    hr = st.number_input("Частота сердечных сокращений (ЧСС)", min_value=0, step=1)
    wbc = st.number_input("Лейкоциты (10⁹/л)", min_value=0.0, step=0.1)
        temp = st.number_input("Температура тела (°C)", min_value=34.0, max_value=42.0, step=0.1)
    crp = st.number_input("С-реактивный белок (СРБ, мг/л)", min_value=0.0, step=0.1)
    submitted = st.form_submit_button("Рассчитать риск")

if submitted:
    r = -2.86
    r += -0.053 * hb
    if vas > 4:
        r += 1.687
    r += 3.146 * int(drain)
    r += 0.167 * neutro
    if hr > 100:
        r += 0.05
    if wbc > 14:
        r += 0.07
    if crp > 129.5:
        r += 0.09
    if temp > 38.0:
        r += 0.06

    st.subheader("📊 Результат")
    st.metric(label="Расчётный индекс риска", value=f"{r:.2f}")

    if r >= 0.08:
        st.error("🔴 Высокий риск осложнений. Рекомендуется экстренное обследование.")
    else:
        st.success("🟢 Низкий риск осложнений.")

    x = np.linspace(-2, 2, 400)
    y = 1 / (1 + np.exp(-x))
    fig, ax = plt.subplots()
    ax.plot(x, y, label="Логистическая кривая")
    ax.axvline(r, color='red', linestyle='--', label=f"r = {r:.2f}")
    ax.set_xlabel("r - логит-функция")
    ax.set_ylabel("P (осложнение)")
    ax.set_title("Логистическая функция вероятности")
    ax.legend()
    st.pyplot(fig)
