import streamlit as st
import markovify
import re

def clean_text(text):
    """
    Remove unwanted characters (e.g., [Chorus], (Verse)) and normalize spaces.
    
    Args:
        text (str): Raw input text.
    
    Returns:
        str: Cleaned and preprocessed text.
    """
    text = re.sub(r'\[.*?\]|\(.*?\)', '', text)  # Remove [Chorus], (Verse), etc.
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

def train_markov_model(text, state_size=2):
    """
    Train a Markov model on the given text.
    
    Args:
        text (str): Cleaned input text.
        state_size (int): Complexity of the Markov chain.
    
    Returns:
        markovify.Text or None: A trained Markov model or None if training fails.
    """
    try:
        return markovify.Text(text, state_size=state_size)
    except Exception as e:
        st.error(f"❌ Error: {str(e)}. Could not build Markov model. Ensure your input text is long enough.")
        return None

def generate_text(model, num_sentences=5):
    """
    Generate sentences using the trained Markov model.
    
    Args:
        model (markovify.Text): A trained Markov model.
        num_sentences (int): Number of sentences to generate.
    
    Returns:
        str: Generated text or an error message if generation fails.
    """
    sentences = []
    for _ in range(num_sentences * 2):  # Try extra times to get valid sentences
        sentence = model.make_sentence(tries=100, max_overlap_ratio=0.7)  # Allow more randomness
        if sentence:
            sentences.append(sentence)
        if len(sentences) >= num_sentences:
            break
    return "\n".join(sentences) if sentences else "⚠ Could not generate lyrics. Please try a longer input text."

# Streamlit App
st.title("🎵 Enhanced Lyrics Composer with Markov Chains")
st.markdown("Upload a `.txt` file or paste lyrics to generate AI-powered song lyrics!")

# Input Method
input_method = st.radio("Input method:", ["Upload a .txt file", "Paste Lyrics"])

text = ""
if input_method == "Upload a .txt file":
    uploaded_file = st.file_uploader("Choose a .txt file", type="txt")
    if uploaded_file:
        with st.spinner("Processing your input..."):
            try:
                text = clean_text(uploaded_file.read().decode("utf-8"))
                st.write("✅ Uploaded Text Preview:", text[:500])  # Show cleaned preview
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
else:
    text = st.text_area("Paste Lyrics Here (e.g., song lyrics, poem):", height=200)
    text = clean_text(text)
    st.write("✅ Pasted Text Preview:", text[:500])  # Show cleaned preview

if text:
    # Model Settings
    col1, col2 = st.columns(2)
    with col1:
        state_size = st.slider("Markov Chain Complexity:", 1, 4, 2)
    with col2:
        num_sentences = st.slider("Number of Lines:", 1, 20, 5)

    model = train_markov_model(text, state_size)

    if model and st.button("Generate Lyrics"):
        generated_lyrics = generate_text(model, num_sentences)
        st.subheader("🎤 Generated Lyrics:")
        st.text(generated_lyrics)

        # Download Button (only if lyrics exist)
        if generated_lyrics and "⚠" not in generated_lyrics:
            st.download_button(
                "Download Lyrics",
                generated_lyrics,
                file_name="generated_lyrics.txt",
                mime="text/plain"
            )
else:
    st.warning("⚠ Please upload a file or paste lyrics first!")
