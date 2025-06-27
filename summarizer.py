from transformers import pipeline

class Summarizer:
    def __init__(self):
        # Using a T5-small model for summarization, suitable for local execution.
        # You might need to download this model the first time it's used.
        self.summarizer_pipeline = pipeline("summarization", model="t5-small")

    def generate_summary(self, text: str, max_length: int = 150, min_length: int = 30) -> str:
        """Generates a concise summary of the given text."""
        # LLMs have context window limits. For long transcripts, you might need
        # to chunk the text and summarize each chunk, then summarize the summaries.
        # For simplicity, this example assumes the input text fits.
        if not text.strip():
            return "No content to summarize."
        try:
            summary = self.summarizer_pipeline(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )[0]['summary_text']
            return summary
        except Exception as e:
            return f"Error generating summary: {e}"