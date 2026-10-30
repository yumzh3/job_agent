from dotenv import load_dotenv
import anthropic

load_dotenv()                      # reads .env into environment variables
client = anthropic.Anthropic()     # finds ANTHROPIC_API_KEY automatically

response = client.messages.create(
    model="claude-haiku-5-5",      # cheapest model, fine for testing
    max_tokens=100,                # caps the length of the reply
    messages=[{"role": "user", "content": "Say hello in one sentence."}],
)

print(response.content[0].text)    # the reply text
print(response.usage)              # tokens in and out, which is what you pay for