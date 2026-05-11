import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image #to handle image in QR

#page settings
st.set_page_config(page_title="myQR", page_icon = "myQR.png", layout = "centered")

#hide hamburger menu
st.markdown("""
    <style>
    /* Hides the Streamlit header (Hamburger menu and Deploy button) */
    header {visibility: hidden;}
    
    /* Hides the 'Made with Streamlit' footer at the bottom */
    footer {visibility: hidden;}
    
    /* Removes the excess white space at the top of the page */
    .block-container {
        padding-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

#title
st.title("🔗Custom QR Code")
st.write("Create your own QR codes instantly from a text or link!")

#user i/p
data = st.text_input("📝 Enter the content for your QR code:")

#customization
st.subheader("🎨 Customization")
col1, col2 = st.columns(2)
with col1:
    fill_color = st.color_picker("🖌️ QR color", "#000000")
with col2:
    back_color = st.color_picker("🖌️ Background color", "#FFFFFF")

logo_file = st.file_uploader("🖼️ Custom Image (optional)", type=["png", "jpg", "jpeg"])

#the slider only appears if an image is uploaded
if logo_file:
    logo_size = st.slider("Logo Size %", min_value=11, max_value=30, value=25)
else:
    #set a default value so the code doesn't crash 
    #when the button is clicked without a logo
    logo_size = 25

#generate button
if st.button("Generate QR code"):
    if data.strip()=="":
        st.warning("⚠️ Please enter valid content")
    else:
        #create QR
        qr = qrcode.QRCode(
            version = 1, #basic size of QR
            error_correction=qrcode.constants.ERROR_CORRECT_H, #level H (high) allows the code to sustain up to 30% damage/coverage and still function
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True) #calc the smallest possible grid that can fit text

        #generate image
        img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

        if logo_file:
            logo = Image.open(logo_file).convert("RGBA")
            
            #calculate size (logo should be 1/5th of the QR size)
            qr_w, qr_h = img.size
            size = int(qr_w * (logo_size / 100))
            logo = logo.resize((size, size), Image.LANCZOS) #LANCZOS is a high quality sharpening filter

            padding = 10
            logo_bg = Image.new("RGBA", (size + padding, size + padding), back_color)
            logo_bg.paste(logo, (padding // 2, padding // 2), logo if logo.mode == 'RGBA' else None)

            #calculate position (center)
            pos = ((qr_w - (size + padding)) // 2, (qr_h - (size + padding)) // 2)

            #paste the logo
            img.paste(logo_bg, pos)

        #show image
        st.image(img, caption = "Your QR code", use_container_width=False)

        #download 
        buf = BytesIO()
        img.save(buf, format="PNG")
        bytes_im = buf.getvalue()

        st.download_button(
            label="Download QR code",
            data = bytes_im,
            file_name = "myQR.png",
            mime = "image/png"
        )
        st.info("💡 **Tip:** You can also right-click the image above and select **'Copy Image'** to paste it anywhere instantly!")

#footer
st.markdown("---")
st.markdown(
    """
    <div align="center">
        <img src="https://cdn-icons-png.flaticon.com/16/25/25231.png" width="16"> 
        Developed by <a href="https://github.com/neharoy3" target="_blank">Neha Roy</a>
    </div>
    """, 
    unsafe_allow_html=True
)
