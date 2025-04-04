import streamlit as st

# Set page title
st.set_page_config(page_title="My First Website", page_icon=":guardsman:", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "About", "Contact"])

# Home page
if page == "Home":
    st.title("Welcome to My First Website! :wave:")
    st.write("This is a simple website built with Streamlit.")

elif page == "About":
    st.title("About Me :book:")
    st.write("Hi! I'm a budding developer learning Streamlit.")
    st.markdown("""
    - 🔥 **Fast Development**
    - 🎨 **Easy UI**
    - 🚀 **Deploy Anywhere**
    """)
elif page == "Contact":
    st.title("Contact Me :envelope:")
    st.write("Feel free to reach out!")
    st.text_input("Your Name")
    st.text_input("Your Email")
    st.text_area("Your Message")
    if st.button("Send"):
        st.success("Message sent!")
    
st.write("🌍 Made with Danish haji using Streamlit")