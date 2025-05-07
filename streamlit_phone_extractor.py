import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd
import re

st.title("📞 Extract Phone Numbers from Images")
st.write("Upload images with phone numbers, and I'll extract them for you!")

uploaded_files = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    phone_numbers = []

    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        text = pytesseract.image_to_string(image)

        # Extracting phone numbers using regex
        phones = re.findall(r"\+7\s?\d{3}\s?\d{3}-\d{2}-\d{2}", text)
        phone_numbers.extend(phones)

    # Removing duplicates
    unique_numbers = list(set(phone_numbers))

    # Displaying extracted phone numbers
    st.subheader("Extracted Phone Numbers")
    df_phones = pd.DataFrame({'Phone Numbers': unique_numbers})
    st.dataframe(df_phones)

    # Download options
    csv = df_phones.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download as CSV", data=csv, file_name='extracted_phone_numbers.csv', mime='text/csv')
