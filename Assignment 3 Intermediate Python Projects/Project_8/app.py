import streamlit as st

def calculate_bmi(weight, height):
    return weight / (height ** 2)

# Streamlit UI
st.title("BMI Calculator 💪")

st.write("Calculate your Body Mass Index (BMI): ")

# User inputs
weight = st.number_input("Enter your weight in (kg):", min_value=1.0, step=0.1)
height = st.number_input("Enter your height in (m):", min_value=0.5, step=0.01)


if st.button("Calculate BMI"):
    if weight and height:
        bmi = calculate_bmi(weight, height)
        st.success(f"Your BMI is: {bmi:.2f}")

        # BMI classification
        if bmi < 18.5:
            st.warning("You are underweight.")
        elif 18.5 <= bmi < 24.9:
            st.success("You have a normal wight.")
        elif 25 <= bmi < 29.9:
            st.warning("You are overweight.")
        else:
            st.error("You are obese.")
    else:
        st.error("Please enter valid weight and height values.")

st.write("Developed by Danish Haji.")
