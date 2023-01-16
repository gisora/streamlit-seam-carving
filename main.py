import streamlit as st
from io import BytesIO
from PIL import Image
from skimage.io import imsave
from app.seamcarver import SeamCarver

# Nuotraukos konvertavimas atsisiutimui (pixeliu reiksmes konvertuojamos is float64 i uint8)
def convert_image_for_download(image):
    img = Image.open(image)
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im


st.set_page_config(layout="wide", page_title="Seam Carving")
st.header("Seam Carving for Content-Aware Image Resizing")
st.write("**(Nuotraukos sutraukimas panaikinant mažiausios svarbos siūles)**")
st.write("***")

# Sidebar
st.sidebar.write("# Nustatymai")
scale_ratio = st.sidebar.slider("Nuotraukos dydis procentais: ", 25, 100, 50)
quality = st.sidebar.selectbox("Rezultato kokybė:", ("Geriausia", "Vidutinė", "Prasčiausia"))
draw_mode_radio = st.sidebar.radio("Papildoma informaciją originalioje nuotraukoje:", ["Jokia", "Siūlė", "Stulpelis"])        
auto_shrink_image = st.sidebar.checkbox("Sutraukti automatiškai")

st.sidebar.write("***")
st.sidebar.write("# Failai")
image_file = st.sidebar.file_uploader("Įkelkite nuotrauką: ", type=["png", "jpg", "jpeg"])

# Jei nuotrauka neatidaryta demostracijai naudojame pagal nutylejima
if image_file is None:
    image_file = "images/img1.jpg"

# Seamcarver objektas
sc = SeamCarver(image_file, scale_ratio=(scale_ratio/100))

image_in = sc.img
image_out = sc.img

if quality == "Geriausia":
    shrink_image = sc.shrink_image_best
elif quality == "Vidutinė":
    shrink_image = sc.shrink_image_medium
else:
    shrink_image = sc.shrink_image_worst

col11, col12 = st.columns(2)
col11.write("### Originali nuotrauka")
col12.write(f"### Sutraukta nuotrauka ({quality.lower()} kokybė)")

col21, col22 = st.columns(2)
seam_at = col21.slider('Kiek siūlių sutraukti?', 0, sc.get_image_shape()[1]-1, 0)

col31, col32 = st.columns(2)

#draw_seam draw_mode: None, "column", "seam"
if draw_mode_radio == "Siūlė":
    draw_mode = "seam"
elif draw_mode_radio == "Stulpelis":
    draw_mode = "column"
else:
    draw_mode = None

col31.image(sc.draw_seam(seam_at, draw_mode=draw_mode), use_column_width=True)


# TODO 
shrink_by = 200 if seam_at > 200 else seam_at
if not auto_shrink_image:
    if col22.button(f"Panaikinti {shrink_by} siūlių"):
        with st.spinner("Sutraukiama..."):
            image_out = shrink_image(shrink_by)
        st.success("Atlikta!")
else:
    with st.spinner("Sutraukiama..."):
        image_out = shrink_image(shrink_by)
    st.success("Atlikta!")

# Nuotrauka kiekviena karta ja pakeitus yra isaugoma diske
imsave("downloads/seam_img.png", image_out)
col32.image(image_out, use_column_width=True)

st.sidebar.markdown("\n")
st.sidebar.download_button("Atsiųsti sutrauktą nuotrauką", convert_image_for_download("downloads/seam_img.png"), "img_seam.png", "image/png")
