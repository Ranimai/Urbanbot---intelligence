# 📝 Intelligence Instruction Layer
# Build structured LLM prompt



def build_prompt(user_question, context_data=None):

    base_prompt = f"""
You are UrbanBot AI Assistant.

Answer clearly and professionally.

User Question:
{user_question}
"""

    if context_data is not None:
        base_prompt += f"\n\nDatabase Context:\n{context_data}"

    return base_prompt



