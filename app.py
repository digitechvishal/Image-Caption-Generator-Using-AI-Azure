import streamlit as st
import requests
from PIL import Image
import io

# Replace with your own endpoint and key
AZURE_ENDPOINT = "https://<your-region>.api.cognitive.microsoft.com/"
AZURE_KEY = "your_key_here"


# Vision API setup
vision_api_url = AZURE_ENDPOINT + "vision/v3.2/analyze"
params = {
    "visualFeatures": "Description",
    "language": "en"
}
headers = {
    "Ocp-Apim-Subscription-Key": AZURE_KEY,
    "Content-Type": "application/octet-stream"
}

st.set_page_config(page_title="Image Caption Generator", layout="wide")
st.title("🖼️ Image Caption Generator using Azure")
st.write("Upload an image and get an automatic caption using Azure Computer Vision!")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    col1, col2 = st.columns([1, 1])  # Split layout: left (output), right (image)

    with col2:
        st.image(image, caption="Uploaded Image", use_container_width=True)

    with col1:
        if st.button("Generate Caption"):
            with st.spinner("Analyzing image..."):
                # Convert image to bytes
                image_bytes = io.BytesIO()
                image.save(image_bytes, format='JPEG')
                image_data = image_bytes.getvalue()

                # Call Azure Vision API
                response = requests.post(
                    vision_api_url,
                    headers=headers,
                    params=params,
                    data=image_data
                )

                if response.status_code == 200:
                    result = response.json()
                    caption = result["description"]["captions"][0]["text"]
                    confidence = result["description"]["captions"][0]["confidence"]
                    st.success(f"**Caption:** {caption}")
                    st.info(f"**Confidence:** {confidence:.2f}")
                else:
                    st.error("❌ Error calling API: " + response.text)
