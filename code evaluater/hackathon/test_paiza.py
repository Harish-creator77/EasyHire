import httpx
import asyncio

async def test_paiza():
    # step 1: create runner
    url = "https://api.paiza.io/runners/create"
    payload = {
        "source_code": "print('hello from paiza')",
        "language": "python3",
        "input": "",
        "api_key": "guest"
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload)
        data = resp.json()
        runner_id = data.get("id")
        print("Runner ID:", runner_id)
        
        if not runner_id:
            return
            
        # step 2: get details
        await asyncio.sleep(2) # wait for execution
        detail_url = f"https://api.paiza.io/runners/get_details?id={runner_id}&api_key=guest"
        detail_resp = await client.get(detail_url)
        print(detail_resp.json())

if __name__ == "__main__":
    asyncio.run(test_paiza())
