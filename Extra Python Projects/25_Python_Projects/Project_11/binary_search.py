import streamlit as st
import time

def naive_search(l, target):
    for i in range(len(l)):
        if l[i] == target:
            return i
    return -1

def binary_search(l, target, low=None, high=None):
    if low is None:
        low = 0
    if high is None:
        high = len(l) - 1

    if high < low:
        return -1

    midpoint = (low + high) // 2

    if l[midpoint] == target:
        return midpoint
    elif target < l[midpoint]:
        return binary_search(l, target, low, midpoint - 1)
    else:
        return binary_search(l, target, midpoint + 1, high)

@st.cache_data
def generate_sorted_list():
    return list(range(-30000, 30001))

st.set_page_config(page_title="Binary vs Naive Search", layout="centered")
st.title("🔍 Binary vs Naive Search Comparison")
st.markdown("Search for a number between **-30,000 to 30,000** using both methods at once.")


sorted_list = generate_sorted_list()


st.subheader("🎯 Enter the number you want to search")
col1, col2 = st.columns(2)
with col1:
    target = st.slider("Select a number", -30000, 30000, 0)
with col2:
    manual_input = st.number_input("Or type a number", value=target, step=1)
    target = manual_input  


if st.button("🔎 Search Now"):
    # Naive search
    start_naive = time.time()
    index_naive = naive_search(sorted_list, target)
    end_naive = time.time()
    time_naive = end_naive - start_naive

    # Binary search
    start_binary = time.time()
    index_binary = binary_search(sorted_list, target)
    end_binary = time.time()
    time_binary = end_binary - start_binary

    # Results
    st.subheader("🔁 Search Results")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🐢 Naive Search")
        if index_naive != -1:
            st.success(f"Found `{target}` at index `{index_naive}`")
        else:
            st.error("Not found.")
        st.info(f"⏱️ Time: `{time_naive:.6f}` seconds")

    with col2:
        st.markdown("### ⚡ Binary Search")
        if index_binary != -1:
            st.success(f"Found `{target}` at index `{index_binary}`")
        else:
            st.error("Not found.")
        st.info(f"⏱️ Time: `{time_binary:.6f}` seconds")
