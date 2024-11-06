# localhost address - http://localhost:8501
#!streamlit run app.py & npx localtunnel --port 8501
# core package
import streamlit as st
import numpy as np
import os
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
import cv2

#for QR Code
import qrcode
qr = qrcode.QRCode(version =1 ,
                   error_correction = qrcode.constants.ERROR_CORRECT_L,
                   box_size=10,
                   border=14)


from PIL import Image
#function to load image
def load_image(img):
    im = Image.open(img)
    return im

#application
def main():
    menu = ["Home","DecodeQR","About"]

    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.subheader("Home")
        # Text Input
        with st.form(key='myqr_form'):
            raw_text = st.text_area("Text Here")
            submit_button = st.form_submit_button("Generate")
        #Layout
        if submit_button:
            col1,col2 = st.columns(2)

            with col1:
                #Add Data
                qr.add_data(raw_text)
                #Generate
                qr.make(fit=True)
                img = qr.make_image(fill_color='black',back_color="white")

                # Filename
                img_filename = 'generate_image_{}.png'.format(timestr)
                path_for_images = os.path.join('image_folder',img_filename)
                img.save(path_for_images)
         
                final_img = load_image(path_for_images)
                st.image(final_img)

            with col2:
                st.info("Original Text")
                st.write(raw_text)
        
    elif choice == "DecodeQR":
        st.subheader("Decode QR")

        image_file = st.file_uploader("Upload Image",type=['jpg','png','jpeg'])
        #Method 1 : Display image
        if image_file is not None:
            #img = load_image(image_file)
            #st.image(img)
            
            # Method 2 : Using opencv
            file_bytes = np.asarray(bytearray(image_file.read()),dtype=np.uint8)
            opencv_image = cv2.imdecode(file_bytes,1)



            c1,c2 = st.columns(2)
            with c1:
                st.image(opencv_image)
            with c2:
                st.info("Decoded QR code")
                det = cv2.QRCodeDetector()
                retval,points,straight_qrcode = det.detectAndDecode(opencv_image)

                #retval is for text
                st.write(retval)
                #st.write(points)
                #st.write(straight_qrcode)

    else:
        st.subheader("About This Project")
        st.header("Python Project")
        st.subheader("Created By -:\n1. Vikas Rajak \n2. Dasmat Hansda \n3. Prince Kumar")
        st.write("We are Students of K22DH  We have Created this Project Using Streamlit, It is an open source app framework in Python language. It helps us create web apps for data science and machine learning in a short time. ")
        st.write("This Project was Submitted to -:\nMr. Bhupinder Singh")


if __name__ == '__main__' :
    main()
