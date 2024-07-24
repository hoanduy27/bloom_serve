import torch 
from transformers import BloomForCausalLM, AutoTokenizer, GenerationConfig

MAX_LEN = 2048

class BloomInferencer:
  def __init__(self, model, tokenizer):
    self.model = model
    self.tokenizer = tokenizer
    # self.model.to("cuda")

  def generate_token(self, inputs):
    with torch.no_grad():
      outputs = self.model(**inputs)

      logits = outputs.logits
      
      last_logits = logits[0, -1, :]
      
      next_token_id = last_logits.argmax()

      token_logprob = torch.nn.functional.log_softmax(
        last_logits
      ).max()

      return next_token_id, outputs.past_key_values, token_logprob

  def __call__(self, prompt: str, uses_kv=True):
    inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")

    if not uses_kv:
      outputs = self.model.generate(
          inputs['input_ids'],
          generation_config=GenerationConfig(max_new_tokens=MAX_LEN)
      )
      
      # A lil cheat here
      generated_tokens = self.tokenizer.decode(outputs[0])[
        len(prompt):-len(self.tokenizer.eos_token)
      ]

      yield generated_tokens.strip(), None

    else:
      generated_tokens = ""
      next_inputs = inputs

      sequence_logprob = 0

      for _ in range(MAX_LEN):
          next_token_id, past_key_values, token_logprob = self.generate_token(next_inputs)

          sequence_logprob += token_logprob.item()

          if next_token_id == self.tokenizer.eos_token_id:
              break

          next_inputs = {
              "input_ids": next_token_id.reshape((1, 1)),
              "attention_mask": torch.cat(
                  [next_inputs["attention_mask"], torch.tensor([[1]], device="cuda")],
                  dim=1),
              "past_key_values": past_key_values,
          }

          next_token = self.tokenizer.decode(next_token_id)
          generated_tokens += next_token

          yield generated_tokens.strip(), sequence_logprob
          
  @classmethod 
  def from_pretrained(cls, model_name_or_path):
    model = BloomForCausalLM.from_pretrained(model_name_or_path)
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    return cls(model, tokenizer)
    # return generated_tokens.strip()

# print(f"{sum(durations_s)} s")
