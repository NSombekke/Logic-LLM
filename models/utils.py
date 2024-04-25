import backoff  # for exponential backoff
import openai
import os
import asyncio
from typing import Any

from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer


# Backoff decorator -> Retry function when RateLimitError is raised
@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def completions_with_backoff(**kwargs):
    return openai.Completion.create(**kwargs)


@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def chat_completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)


async def dispatch_openai_chat_requests(
    messages_list: list[list[dict[str, Any]]],
    model: str,
    temperature: float,
    max_tokens: int,
    top_p: float,
    stop_words: list[str],
) -> list[str]:
    """Dispatches requests to OpenAI API asynchronously.

    Args:
        messages_list: List of messages to be sent to OpenAI ChatCompletion API.
        model: OpenAI model to use.
        temperature: Temperature to use for the model.
        max_tokens: Maximum number of tokens to generate.
        top_p: Top p to use for the model.
        stop_words: List of words to stop the model from generating.
    Returns:
        List of responses from OpenAI API.
    """
    async_responses = [
        openai.ChatCompletion.acreate(
            model=model,
            messages=x,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stop=stop_words,
        )
        for x in messages_list
    ]
    return await asyncio.gather(*async_responses)


async def dispatch_openai_prompt_requests(
    messages_list: list[list[dict[str, Any]]],
    model: str,
    temperature: float,
    max_tokens: int,
    top_p: float,
    stop_words: list[str],
) -> list[str]:
    async_responses = [
        openai.Completion.acreate(
            model=model,
            prompt=x,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=stop_words,
        )
        for x in messages_list
    ]
    return await asyncio.gather(*async_responses)


class OpenAIModel:
    def __init__(self, API_KEY, model_name, stop_words, max_new_tokens) -> None:
        openai.api_key = API_KEY
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens
        self.stop_words = stop_words

    # used for chat-gpt and gpt-4
    def chat_generate(self, input_string, temperature=0.0):
        response = chat_completions_with_backoff(
            model=self.model_name,
            messages=[{"role": "user", "content": input_string}],
            max_tokens=self.max_new_tokens,
            temperature=temperature,
            top_p=1.0,
            stop=self.stop_words,
        )
        generated_text = response["choices"][0]["message"]["content"].strip()
        return generated_text

    # used for text/code-davinci
    def prompt_generate(self, input_string, temperature=0.0):
        response = completions_with_backoff(
            model=self.model_name,
            prompt=input_string,
            max_tokens=self.max_new_tokens,
            temperature=temperature,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=self.stop_words,
        )
        generated_text = response["choices"][0]["text"].strip()
        return generated_text

    def generate(self, input_string, temperature=0.0):
        if self.model_name in [
            "text-davinci-002",
            "code-davinci-002",
            "text-davinci-003",
        ]:
            return self.prompt_generate(input_string, temperature)
        elif self.model_name in ["gpt-4", "gpt-3.5-turbo"]:
            return self.chat_generate(input_string, temperature)
        else:
            raise Exception("Model name not recognized")

    def batch_chat_generate(self, messages_list, temperature=0.0):
        open_ai_messages_list = []
        for message in messages_list:
            open_ai_messages_list.append([{"role": "user", "content": message}])
        predictions = asyncio.run(
            dispatch_openai_chat_requests(
                open_ai_messages_list,
                self.model_name,
                temperature,
                self.max_new_tokens,
                1.0,
                self.stop_words,
            )
        )
        return [x["choices"][0]["message"]["content"].strip() for x in predictions]

    def batch_prompt_generate(self, prompt_list, temperature=0.0):
        predictions = asyncio.run(
            dispatch_openai_prompt_requests(
                prompt_list,
                self.model_name,
                temperature,
                self.max_new_tokens,
                1.0,
                self.stop_words,
            )
        )
        return [x["choices"][0]["text"].strip() for x in predictions]

    def batch_generate(self, messages_list, temperature=0.0):
        if self.model_name in [
            "text-davinci-002",
            "code-davinci-002",
            "text-davinci-003",
        ]:
            return self.batch_prompt_generate(messages_list, temperature)
        elif self.model_name in ["gpt-4", "gpt-3.5-turbo"]:
            return self.batch_chat_generate(messages_list, temperature)
        else:
            raise Exception("Model name not recognized")

    def generate_insertion(self, input_string, suffix, temperature=0.0):
        response = completions_with_backoff(
            model=self.model_name,
            prompt=input_string,
            suffix=suffix,
            temperature=temperature,
            max_tokens=self.max_new_tokens,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        generated_text = response["choices"][0]["text"].strip()
        return generated_text


class HuggingFaceModel:
    def __init__(
        self, API_KEY, model_name, stop_words, max_new_tokens, temperature=0.0
    ) -> None:
        self.api_key = API_KEY
        self.model_name = model_name

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name, device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, device_map="auto"
        )

        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            token=self.api_key,
            max_new_tokens=max_new_tokens,
            top_p=1.0,
            device_map="auto",
            do_sample=False,
            return_full_text=False,
        )

    def generate(self, input_string):
        if self.model_name in [
            "meta-llama/Meta-Llama-3-8B",
            "meta-llama/Meta-Llama-3-70B",
            "mistralai/Mixtral-8x7B-v0.1",
            "mistralai/Mixtral-8x22B-v0.1",
        ]:
            return self.prompt_generate(input_string)
        elif self.model_name in [
            "meta-llama/Meta-Llama-3-8B-Instruct",
            "meta-llama/Meta-Llama-3-70B-Instruct",
            "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "mistralai/Mixtral-8x22B-Instruct-v0.1",
        ]:
            return self.chat_generate(input_string)
        else:
            raise Exception("Model name not recognized")

    def chat_generate(self, input_string):
        message = [{"role": "user", "content": input_string}]
        inputs = self.pipe.tokenizer.apply_chat_template(
            message, tokenize=False, add_generation_prompt=True
        )
        response = self.pipe(
            inputs,
        )
        generated_text = response[0]["generated_text"].strip()
        return generated_text

    def prompt_generate(self, input_string):
        response = self.pipe(
            input_string,
        )
        generated_text = response[0]["generated_text"].strip()
        return generated_text

    def batch_generate(self, input_string):
        if self.model_name in [
            "meta-llama/Meta-Llama-3-8B",
            "meta-llama/Meta-Llama-3-70B",
            "mistralai/Mixtral-8x7B-v0.1",
            "mistralai/Mixtral-8x22B-v0.1",
        ]:
            return self.batch_prompt_generate(input_string)
        elif self.model_name in [
            "meta-llama/Meta-Llama-3-8B-Instruct",
            "meta-llama/Meta-Llama-3-70B-Instruct",
            "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "mistralai/Mixtral-8x22B-Instruct-v0.1",
        ]:
            return self.batch_chat_generate(input_string)
        else:
            raise Exception("Model name not recognized")

    def batch_chat_generate(self, input_strings):
        inputs_list = []
        for input_string in input_strings:
            message = [{"role": "user", "content": input_string}]
            inputs = self.pipe.tokenizer.apply_chat_template(
                message, tokenize=False, add_generation_prompt=True
            )
            inputs_list.append(inputs)
        responses = self.pipe(
            inputs_list,
        )
        generated_text = [response["generated_text"].strip() for response in responses]
        return generated_text

    def batch_prompt_generate(self, input_strings):
        responses = self.pipe(
            input_strings,
        )
        generated_text = [response["generated_text"].strip() for response in responses]
        return generated_text
