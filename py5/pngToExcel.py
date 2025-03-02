import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import os
from io import BytesIO

# Set Streamlit page config
st.set_page_config(page_title="Data Sweeper", layout="wide")

# Display app title
st.title("🖼️ Image to Excel Converter & File Sweeper")
st.write("Upload PNG/JPG images to extract text and convert it to Excel/CSV. You can also upload CSV/Excel files for conversion.")

# File uploader (supports CSV, Excel, PNG, and JPG)
uploaded_files = st.file_uploader(
    "Upload your files (CSV, Excel, PNG, JPG):",
    type=["csv", "xlsx", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()
        
        if file_extension in [".csv", ".xlsx"]:
            # Read CSV/Excel files into a DataFrame
            if file_extension == ".csv":
                df = pd.read_csv(file)
            elif file_extension == ".xlsx":
                df = pd.read_excel(file)
            
            # Display file info
            st.write(f"📄 **File Name:** {file.name}")
            st.write(f"📏 **File Size:** {file.size / 1024:.2f} KB")
            st.dataframe(df.head())  # Show first 5 rows

            # Conversion options (CSV or Excel)
            conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
            if st.button(f"Convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    mime_type = "text/csv"
                    new_file_name = file.name.replace(file_extension, ".csv")
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False, engine="openpyxl")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    new_file_name = file.name.replace(file_extension, ".xlsx")
                
                buffer.seek(0)
                st.download_button(label=f"⬇️ Download {new_file_name}", data=buffer, file_name=new_file_name, mime=mime_type)

        elif file_extension in [".png", ".jpg", ".jpeg"]:
            # Process image files
            image = Image.open(file)
            st.image(image, caption=f"🖼️ Uploaded: {file.name}", use_column_width=True)

            # Extract text using Tesseract
            extracted_text = pytesseract.image_to_string(image)

            # Display extracted text
            st.subheader("📝 Extracted Text")
            st.text_area("Text from Image:", extracted_text, height=200)

            # Convert extracted text to DataFrame
            df_text = pd.DataFrame({"Extracted Text": [extracted_text]})

            # Allow user to download as Excel or CSV
            conversion_type = st.radio(f"Convert Extracted Text to:", ["CSV", "Excel"], key=f"ocr_{file.name}")
            if st.button(f"Convert Extracted Text from {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df_text.to_csv(buffer, index=False)
                    mime_type = "text/csv"
                    new_file_name = file.name.replace(file_extension, ".csv")
                elif conversion_type == "Excel":
                    df_text.to_excel(buffer, index=False, engine="openpyxl")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    new_file_name = file.name.replace(file_extension, ".xlsx")

                buffer.seek(0)
                st.download_button(label=f"⬇️ Download {new_file_name}", data=buffer, file_name=new_file_name, mime=mime_type)

st.success("🎉 All files processed successfully!")
