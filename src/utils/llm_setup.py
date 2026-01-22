import os
from altair import Config
from llama_cpp import Llama
from langchain_huggingface import HuggingFaceEmbeddings
from src.utils.config import LLMConfig, EmbeddingConfig, ChromaConfig
import torch

llm_cfg = LLMConfig()
emb_cfg = EmbeddingConfig()
chroma_cfg = ChromaConfig()

class LLMManager:
    def __init__(self):
        self.llm = None
        self.model = None
        self.tokenizer = None
        self.use_real_llm = False
        self._init_llm()

    def _init_llm(self):
        """Initialize llama-cpp or fallback to transformers."""
        try:
            if os.path.isfile(llm_cfg.model_path):
                print(f"Loading llama-cpp model: {llm_cfg.model_path}")
                self.llm = Llama(
                    model_path=llm_cfg.model_path,
                    n_gpu_layers=llm_cfg.n_gpu_layers,
                    n_ctx=llm_cfg.n_ctx,
                    verbose=False
                )
                self.use_real_llm = True
                print("llama-cpp model loaded successfully")
                return

            print(f"Model not found at {Config.LLM_MODEL_PATH}, using transformers fallback")
            self._init_transformers()

        except Exception as e:
            print(f"Error loading llama-cpp: {e}")
            print("Falling back to transformers...")
            self._init_transformers()

    def _init_transformers(self):
        """Initialize transformers fallback model."""
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer

            model_name = Config.SETTINGS.get(
                "TRANSFORMERS_FALLBACK_MODEL",
                "TinyLlama/TinyLlama-1.1b-chat-v1.0"
            )

            print(f"Loading transformers model: {model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                device_map="auto",
                torch_dtype=torch.float16
            )
            self.use_real_llm = True
            print("Transformers model loaded successfully")

        except Exception as e:
            print(f"Failed to load transformers fallback: {e}")
            self.use_real_llm = False

    def generate(self, prompt):
        """Generate text using llama-cpp or transformers."""
        if not self.use_real_llm:
            raise RuntimeError("No LLM backend available")

        if self.llm:
            return self._generate_llama_cpp(prompt)

        if self.model:
            return self._generate_transformers(prompt)

        raise RuntimeError("LLM backend not initialized")

    def _generate_llama_cpp(self, prompt):
        try:
            print("Generating with llama-cpp...")
            response = self.llm(
                prompt,
                max_tokens=llm_cfg.max_tokens,
                temperature=llm_cfg.temperature,
                top_k=llm_cfg.top_k,
                top_p=llm_cfg.top_p,
                # stop=["Human:", "Assistant:"]
            )
            return response["choices"][0]["text"].strip()

        except Exception as e:
            print(f"llama-cpp generation failed: {e}")
            raise

    def _generate_transformers(self, prompt):
        try:
            print("Generating with transformers...")
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=1024
            )
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=Config.SETTINGS.get("LLM_MAX_TOKENS", 512),
                    temperature=Config.SETTINGS.get("LLM_TEMPERATURE", 0.5),
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Remove prompt echo
            if response.startswith(prompt):
                response = response[len(prompt):].strip()

            return response

        except Exception as e:
            print(f"Transformers generation failed: {e}")
            raise

# llm = Llama(
#     model_path=llm_cfg.model_path,
#     temperature=llm_cfg.temperature,
#     max_tokens=llm_cfg.max_tokens,
#     n_ctx=llm_cfg.n_ctx,
#     n_gpu_layers=llm_cfg.n_gpu_layers,
#     top_k=llm_cfg.top_k,
#     top_p=llm_cfg.top_p,
#     verbose=False,
# )

embeddings_model = HuggingFaceEmbeddings(model_name=emb_cfg.model_name)
