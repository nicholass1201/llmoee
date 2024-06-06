# llama 한국어 모델 로컬에 다운 
from transformers import LlamaForCausalLM, LlamaTokenizer

tokenizer = LlamaTokenizer.from_pretrained("beomi/llama-2-ko-7b")
model = LlamaForCausalLM.from_pretrained("beomi/llama-2-ko-7b")
