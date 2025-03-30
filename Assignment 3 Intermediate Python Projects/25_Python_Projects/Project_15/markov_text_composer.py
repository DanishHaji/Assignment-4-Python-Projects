import markovify # type: ignore

def train_markov_model(text_file):
    """Train a Markov chain model using the provided text file."""

    try:
        with open(text_file, "r", encoding="utf-8") as file:
            text = file.read()

        # Build the Markov model
        text_model = markovify.Text(text, state_size=2)

        return text_model
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return None
    
def generate_text(model, num_sentences=5):
    """Generate text based on the trained Markov model."""
    generate_text = [model.make_sentence() for _ in range(num_sentences)]
    return "\n".join(filter(None, generate_text)) # Remove None values

if __name__ == "__main__":
    text_file = "walker.txt"

    model = train_markov_model(text_file)

    if model:
        print("\n🎶 Generated Text 🎶\n")
        print(generate_text(model))
