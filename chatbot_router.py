from parts_similarity_tool import run_parts_similarity


class Chatbot:

    def __init__(self):
        pass

    def detect_similarity_request(self, query):
        keywords = ["similar parts", "find similar", "part similarity"]

        return any(k in query.lower() for k in keywords)

    def ask(self, query, uploaded_file=None):

        # If user asks similarity
        if self.detect_similarity_request(query):

            if uploaded_file is None:
                return "📂 Please upload a CSV file containing Parts data."

            try:
                output = run_parts_similarity(uploaded_file)

                return f"""
✅ Similar parts generated successfully.

Output file:
{output}
"""
            except Exception as e:
                return f"❌ Error processing file: {str(e)}"

        return "🤖 Normal chatbot response here."
