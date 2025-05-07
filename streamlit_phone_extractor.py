import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd
import re

st.title("📞 Извлекает номера из Скриншотов telegram каналов")
st.write("Загружайте изображения с номерами телефонов, и я извлеку их для вас!")

uploaded_files = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    st.subheader("Загруженные файлы")
    for uploaded_file in uploaded_files:
        st.write(f"- {uploaded_file.name}")

    phone_numbers = []

    status_text = st.empty()
    progress_bar = st.progress(0)
    total_files = len(uploaded_files)

    for i, uploaded_file in enumerate(uploaded_files):
        try:
            image = Image.open(uploaded_file)
            text = pytesseract.image_to_string(image)

            # Обновление текста статуса
            status_text.text(f"Обрабатывается: {uploaded_file.name} ({i + 1}/{total_files})")

            # Извлечение номеров телефонов
            phones = re.findall(r"\+7\s?\d{3}\s?\d{3}-\d{2}-\d{2}", text)
            phone_numbers.extend(phones)

        except Exception as e:
            st.error(f"Ошибка при обработке {uploaded_file.name}: {str(e)}")

        # Обновление прогресс-бара
        progress_bar.progress((i + 1) / total_files)

    # Удаление дубликатов
    unique_numbers = list(set(phone_numbers))

    # Отображение извлеченных номеров телефонов
    st.subheader("Выгруженные номера")
    df_phones = pd.DataFrame({'Phone Numbers': unique_numbers})
    st.dataframe(df_phones)

    # Сохранение данных в CSV
    csv = df_phones.to_csv(index=False).encode('utf-8')
    st.download_button(label="Сохранить в CSV", data=csv, file_name='extracted_phone_numbers.csv', mime='text/csv')
