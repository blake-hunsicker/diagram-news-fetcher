import config
import os
import openai

openai.api_key = config.openai_secret_key

# openai.File.create(
#   file=open("output-Supreme Court foster parents.jsonl"),
#   purpose='answers'
# )

print(openai.File.list())

# openai.File('file-Cj6YEBVN52oAqIsQBpdu0LhB').delete()

answer = openai.Answer.create(
  search_model="davinci", 
  model="babbage", 
  question="Can you explain this to me?", 
  file="file-n3kw53gnUpE36P3aNFyvfqFz", 
  examples_context="The first reported Asian giant hornet of 2021 in the United States was found dead near Seattle by a Washington state resident in early June. The dead insect, nicknamed the “murder hornet,” found in Marysville, Washington, was dried out and emerged earlier than usual, so it may have been an “old hornet from a previous season that wasn’t discovered until now,” said Sven Spichiger, managing entomologist for the Washington State Department of Agriculture, during a press conference.", 
  examples=[["Give me the gist:", "Asian giant hornets have appeared early this year. The insect was found in Washington state in early June."],["What happened?", "Murder hornets are appearing earlier than normal this year. One was found in Washington state in early June."]], 
  temperature=0.8,
  max_rerank=10,
  max_tokens=50,
  stop=["\n", "<|endoftext|>"]
)

print(answer)