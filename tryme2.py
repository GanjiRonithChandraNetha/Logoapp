import streamlit as st
import requests
import base64

# Function to generate logo using Stability AI API
def generate_image_with_stability(api_key, text_prompt):
    # API endpoint
    url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"

    # Headers with the API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Data payload with the text prompt
    data = {
        "text_prompts": [{"text": text_prompt}],
        "cfg_scale": 7,  # Controls how closely the image follows the prompt
        "height": 512,   # Image height
        "width": 512,    # Image width
        "samples": 1,    # Number of images to generate
        "steps": 30      # Number of diffusion steps
    }

    # Make the API request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        result = response.json()
        
        # Extract the base64-encoded image
        image_base64 = result["artifacts"][0]["base64"]
        
        # Decode the base64 image
        image_data = base64.b64decode(image_base64)
        
        return image_data
    else:
        st.error(f"Failed to generate logo. Status code: {response.status_code}")
        st.error(response.text)
        return None

# Streamlit app
def main():
    st.title("🚀 Company Logo Generator")
    st.write("Generate a professional logo for your company using AI!")

    # Input fields for company details
    company_name = st.text_input("Enter the name of your company:")
    industry = st.text_input("Enter the industry of your company (e.g., tech, fashion, food):")
    style = st.text_input("Enter the style of the logo (e.g., modern, minimalist, vintage):")
    colors = st.text_input("Enter preferred colors (e.g., blue and white, red and black):")

    # Hardcoded Stability AI API key
    api_key = "sk-aqZFjQwIvyaidHnXyGYXHcQSWKjbVkrwU1CoKj4oiwzoZw5d"  # Replace with your actual API key

    # Generate logo button
    if st.button("Generate Logo"):
        if not company_name or not industry or not style or not colors:
            st.error("Please fill in all the fields.")
        else:
            # Create the text prompt
            text_prompt = (
                f"A realistic and professional logo for a company named {company_name}, "
                f"which operates in the {industry} industry. The logo should be {style} style, "
                f"using colors {colors}. The logo should be clean, scalable, and suitable for "
                f"business use."
            )

            # Generate the logo
            with st.spinner("Generating your logo..."):
                image_data = generate_image_with_stability(api_key, text_prompt)

            # Display the generated logo
            if image_data:
                st.success("Logo generated successfully!")
                st.image(image_data, caption="Your Generated Logo", use_container_width=True)

                # Download button for the logo
                st.download_button(
                    label="Download Logo",
                    data=image_data,
                    file_name="generated_logo.png",
                    mime="image/png"
                )

# Run the Streamlit app
if __name__ == "__main__":
    main()