import streamlit as st
import markovify
import re
import time
from typing import Optional

# Set page config FIRST
st.set_page_config(
    page_title="Text Composer AI",
    page_icon="🎤",
    layout="wide"
)

# Custom CSS styling SECOND
st.markdown("""
<style>
    .main {
        background: linear-gradient(45deg, #1a1a1a, #2a2a2a);
        color: #ffffff;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #333333;
        color: white;
    }
    .generated-box {
       border: 1px solid #4CAF50;
        border-radius: 15px;
        padding: 25px;
        background: #1e1e1e;
        margin-top: 30px;
        color: #e0e0e0;
        font-size: 1.1rem;
        line-height: 1.6;
        box-shadow: 0 4px 20px rgba(76, 175, 80, 0.15);
        transition: all 0.3s ease-in-out;
        word-break: break-word;
    }
    .generated-box:hover {
        box-shadow: 0 6px 25px rgba(76, 175, 80, 0.3);
    }
    .download-btn {
        background: #4CAF50 !important;
        color: white !important;
        border-radius: 5px;
    }
    .header-text {
        font-family: 'Arial Rounded MT Bold', sans-serif;
        color: #4CAF50 !important;
    }
</style>
""", unsafe_allow_html=True)

def detect_content_type(text: str) -> str:
    """Auto-detect content type with improved logic"""
    lines = text.split('\n')
    avg_line_length = sum(len(line) for line in lines) / max(1, len(lines))
    unique_lines = len(set(lines))
    
    # Lyrics detection criteria
    if any([avg_line_length < 60,
            unique_lines/len(lines) < 0.7,
            'verse' in text.lower(),
            'chorus' in text.lower()]):
        return "lyrics"
    return "text"

def clean_content(text: str, content_type: str) -> str:
    """Enhanced content-aware cleaning"""
    # Remove special characters and annotations
    text = re.sub(r'\[.*?\]|\(.*?\)|\{.*?\}|[^a-zA-Z0-9\s.,!?\'"-]', '', text)
    
    if content_type == "lyrics":
        # Preserve line breaks and verse structure
        return '\n'.join([line.strip() for line in text.split('\n') if line.strip()])
    
    # For regular text, create paragraphs
    return '\n\n'.join([' '.join(para.split()) for para in text.split('\n\n')])

def train_model(text: str) -> Optional[markovify.Text]:
    """Robust model training with error handling"""
    try:
        return markovify.Text(
            text,
            state_size=2,
            well_formed=False,
            reject_reg=r'^(.*?)\1{3,}$'  # Reject repeating patterns
        )
    except Exception as e:
        st.error(f"Model training failed: {str(e)}")
        return None

def generate_content(model: markovify.Text, num_lines: int, content_type: str) -> str:
    """Improved content-aware generation"""
    content = []
    line_attempts = 0
    max_attempts = num_lines * 3
    
    while len(content) < num_lines and line_attempts < max_attempts:
        try:
            if content_type == "lyrics":
                line = model.make_short_sentence(80, tries=100)
            else:
                line = model.make_sentence(tries=100)
            
            if line and line not in content:
                content.append(line)
            
            line_attempts += 1
        except:
            break
    
    # Format output based on content type
    if content_type == "lyrics":
        return '\n\n'.join([
            '\n'.join(content[i:i+4]) 
            for i in range(0, len(content), 4)
        ])
    return '\n'.join(content)

# App Header
col1, col2 = st.columns([1, 3])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/4436/4436481.png", width=150)
with col2:
    st.markdown("<h1 class='header-text'>🎵 Smart Content Generator</h1>", unsafe_allow_html=True)
    st.markdown("Transform any text into creative content with AI!")

# File Upload Section
uploaded_file = st.file_uploader("Upload any .txt file", type="txt")
input_text = ""
content_type = "text"

if uploaded_file:
    with st.spinner("Analyzing your content..."):
        try:
            raw_text = uploaded_file.read().decode("utf-8")
            content_type = detect_content_type(raw_text)
            input_text = clean_content(raw_text, content_type)
            
            st.success(f"📄 Detected content type: {content_type.capitalize()}")
            with st.expander("View processed text preview"):
                st.write(input_text[:1000] + ("..." if len(input_text) > 1000 else ""))
                
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")

# Generation Controls
if input_text:
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        num_lines = st.slider(
            "Number of lines to generate", 
            min_value=10, 
            max_value=500, 
            value=100,
            help="Choose between 10 to 500 lines"
        )
    
    with col_b:
        st.markdown("### Generation Options")
        generate_btn = st.button("✨ Create Magic", use_container_width=True)
    
    if generate_btn:
        with st.spinner("Training AI model..."):
            start_time = time.time()
            model = train_model(input_text)
            
            if model:
                progress = st.progress(0)
                status = st.empty()
                
                status.markdown("🚀 Generating content...")
                generated = generate_content(model, num_lines, content_type)
                progress.progress(100)
                
                # Display Results
                st.markdown("---")
                st.markdown(f"### 🎉 Generated {content_type.capitalize()}")
                with st.container():
                    html_generated = generated.replace("\n", "<br>")
                    st.markdown(
                        f'<div class="generated-box">{html_generated}</div>', 
                        unsafe_allow_html=True
                    )
                
                # Download Section
                st.download_button(
                    label="📥 Download Result",
                    data=generated,
                    file_name=f"generated_{content_type}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key="download"
                )
                
                # Performance metrics
                st.caption(f"⚡ Generated {len(generated.splitlines())} lines in "
                          f"{time.time() - start_time:.1f} seconds")
            else:
                st.error("❌ Failed to create model. Please try with more text data.")

# Sidebar Instructions
with st.sidebar:
    st.markdown("## 📖 How to Use")
    st.markdown("""
    1. Upload any .txt file
    2. Let AI detect content type
    3. Choose number of lines (10-500)
    4. Click **Create Magic**
    5. Download your result!
    """)
    st.markdown("---")
    st.markdown("**Supported Content:**")
    st.markdown("- Song lyrics\n- Poetry\n- Stories\n- Articles\n- Any text")
    st.markdown("---")
    st.markdown("Made with 👷🏻‍♂️Engr Danish using Python")

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    Powered by Markov Chains & Streamlit | Generate creative content safely and efficiently
</div>
""", unsafe_allow_html=True)