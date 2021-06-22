import config
import openai

openai.api_key = config.openai_secret_key

response = openai.Completion.create(
  engine="davinci",
  prompt="",
  temperature=0.8,
  max_tokens=120,
  top_p=1.0,
  frequency_penalty=0.9,
  presence_penalty=0.9
)

print(response)