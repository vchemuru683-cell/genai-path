"""llm_chat.py — talk to an LLM from your terminal (Phase 1 deliverable).

Usage:
  python llm_chat.py "Explain a hash map in two sentences." --model gpt-4o-mini --system "You are a terse senior engineer."
"""
import argparse
import sys
import time

from dotenv import load_dotenv
from openai import BadRequestError, OpenAI

load_dotenv()  # Reads OPENAI_API_KEY from .env.


def chat(prompt, model, system=None, temperature=None, max_tokens=1024):
    client = OpenAI()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    kwargs = {
        "model": model,
        "max_completion_tokens": max_tokens,
        "messages": messages,
    }
    if temperature is not None:
        try:
            return client.chat.completions.create(**kwargs, temperature=temperature)
        except BadRequestError as e:
            # Retry only if temperature caused the rejection.
            if e.param != "temperature":
                raise
            print(f"[note] API rejected temperature: {e.message}", file=sys.stderr)
    return client.chat.completions.create(**kwargs)


def main():
    ap = argparse.ArgumentParser(description="Send one prompt to OpenAI.")
    ap.add_argument("prompt")
    ap.add_argument("--model", default="gpt-4o-mini")
    ap.add_argument("--system", help="system prompt: persona and rules")
    ap.add_argument("--temperature", type=float, help="randomness (0 to 2), where supported")
    ap.add_argument("--max-tokens", type=int, default=1024,
                    help="maximum completion tokens, including any reasoning tokens")
    a = ap.parse_args()
    if a.max_tokens < 1:
        ap.error("--max-tokens must be positive")
    if a.temperature is not None and not 0 <= a.temperature <= 2:
        ap.error("--temperature must be between 0 and 2")

    start = time.perf_counter()
    msg = chat(a.prompt, a.model, a.system, a.temperature, a.max_tokens)
    secs = time.perf_counter() - start

    choice = msg.choices[0]
    print(choice.message.content or choice.message.refusal or "", flush=True)
    if not choice.message.content and not choice.message.refusal:
        print("[note] No answer text returned.", file=sys.stderr)
        if choice.finish_reason == "length":
            print("[note] Token budget exhausted; increase --max-tokens to allow room for reasoning and an answer.", file=sys.stderr)
    u = msg.usage
    if u:
        print(f"\n[{a.model} · {u.prompt_tokens} in / {u.completion_tokens} out · "
              f"{secs:.1f}s · stop: {choice.finish_reason}]", file=sys.stderr)


if __name__ == "__main__":
    main()
