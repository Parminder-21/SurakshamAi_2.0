"""
LLM Client — supports OpenAI, Azure OpenAI, Google Gemini, and Groq.
Configured via LLM_PROVIDER env variable.

Recommended free option: LLM_PROVIDER=groq, LLM_MODEL=llama-3.3-70b-versatile
"""
from app.config import settings


async def get_llm_response(prompt: str, system_prompt: str = "") -> str:
    provider = settings.llm_provider.lower()

    if provider == "openai":
        return await _openai_response(prompt, system_prompt)
    elif provider == "azure":
        return await _azure_response(prompt, system_prompt)
    elif provider == "gemini":
        return await _gemini_response(prompt, system_prompt)
    elif provider == "groq":
        return await _groq_response(prompt, system_prompt)
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")


async def _groq_response(prompt: str, system_prompt: str) -> str:
    """
    Groq — free tier, very fast inference.
    Models: llama-3.3-70b-versatile, llama-3.1-8b-instant, mixtral-8x7b-32768
    """
    from openai import AsyncOpenAI

    client = AsyncOpenAI(
        api_key=settings.groq_api_key,
        base_url="https://api.groq.com/openai/v1",
    )
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model=settings.llm_model,
        messages=messages,
        temperature=0.1,
        max_tokens=1024,
    )
    return response.choices[0].message.content or ""


async def _gemini_response(prompt: str, system_prompt: str) -> str:
    import google.generativeai as genai

    genai.configure(api_key=settings.google_api_key)
    model = genai.GenerativeModel(
        model_name=settings.llm_model,
        system_instruction=system_prompt if system_prompt else None,
        generation_config={"temperature": 0.1, "max_output_tokens": 1024},
    )
    response = await model.generate_content_async(prompt)
    return response.text or ""


async def _openai_response(prompt: str, system_prompt: str) -> str:
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model=settings.llm_model,
        messages=messages,
        temperature=0.1,
        max_tokens=1024,
    )
    return response.choices[0].message.content or ""


async def _azure_response(prompt: str, system_prompt: str) -> str:
    from openai import AsyncAzureOpenAI

    client = AsyncAzureOpenAI(
        api_key=settings.azure_openai_api_key,
        azure_endpoint=settings.azure_openai_endpoint,
        api_version="2024-02-01",
    )
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model=settings.llm_model,
        messages=messages,
        temperature=0.1,
        max_tokens=1024,
    )
    return response.choices[0].message.content or ""


async def _gemini_response(prompt: str, system_prompt: str) -> str:
    """
    Uses google-generativeai SDK with gemini-1.5-pro (best for Gemini Pro plan).
    Supports system instructions natively.
    """
    import google.generativeai as genai

    genai.configure(api_key=settings.google_api_key)

    # gemini-1.5-pro supports system_instruction natively
    model = genai.GenerativeModel(
        model_name=settings.llm_model,
        system_instruction=system_prompt if system_prompt else None,
        generation_config={
            "temperature": 0.1,        # Low temp for consistent fraud detection
            "max_output_tokens": 1024,
            "response_mime_type": "text/plain",
        },
    )

    response = await model.generate_content_async(prompt)
    return response.text or ""


async def _openai_response(prompt: str, system_prompt: str) -> str:
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model=settings.llm_model,
        messages=messages,
        temperature=0.1,
        max_tokens=1024,
    )
    return response.choices[0].message.content or ""


async def _azure_response(prompt: str, system_prompt: str) -> str:
    from openai import AsyncAzureOpenAI

    client = AsyncAzureOpenAI(
        api_key=settings.azure_openai_api_key,
        azure_endpoint=settings.azure_openai_endpoint,
        api_version="2024-02-01",
    )
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model=settings.llm_model,
        messages=messages,
        temperature=0.1,
        max_tokens=1024,
    )
    return response.choices[0].message.content or ""
