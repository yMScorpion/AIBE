import asyncio
import openai

async def test():
    client = openai.AsyncOpenAI(
        api_key="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",
        base_url="https://openrouter.ai/api/v1"
    )
    
    try:
        response = await client.chat.completions.create(
            model="openrouter/auto",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print("Success openrouter/auto")
        
        response = await client.chat.completions.create(
            model="openrouter/free",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print("Success openrouter/free")
    except Exception as e:
        print("Error:", e)

asyncio.run(test())
