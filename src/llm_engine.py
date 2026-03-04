from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def generate_response(user_text):
    """
    Generates a Telugu response using GPT-4o.
    """
    client = OpenAI()
    
    system_prompt = (
        "You are a helpful assistant that speaks Telugu. "
        "Always respond in clear, natural Telugu. Keep responses concise."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"LLM error: {str(e)}"

if __name__ == "__main__":
    # Test (requires API key)
    # print(generate_response("తెలంగాణ రాజధాని ఏది?"))
    pass
