# summarize.py

from transformers import pipeline

def generate_summary(text):
    """
    Summarizes extracted text using a transformer model.
    """

    if not text or len(text.strip()) == 0:
        return "No text found to summarize."

    # Initialize summarizer
    summarizer = pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6",   # lightweight summarization model
        device=-1
    )

    # Transformers accept max ~1024 tokens → split long text
    max_len = 700
    chunks = []

    words = text.split()
    for i in range(0, len(words), max_len):
        chunk = " ".join(words[i: i + max_len])
        chunks.append(chunk)

    summaries = []

    for chunk in chunks:
        summary = summarizer(
            chunk,
            max_length=130,
            min_length=40,
            do_sample=False
        )[0]['summary_text']

        summaries.append(summary)

    # Combine all summaries
    final_summary = "\n".join(summaries)

    return final_summary


# Test the function (run only when executed directly)
if __name__ == "__main__":
    sample_text = """
    Artificial intelligence (AI) refers to the simulation of human intelligence 
    in machines that are programmed to think like humans and mimic their actions. 
    AI can be applied to various industries including healthcare, finance, 
    education, transportation, and more.
    """

    print(generate_summary(sample_text))
