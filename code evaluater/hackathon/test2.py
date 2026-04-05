import httpx
import asyncio

async def main():
    payload = {
        "language": "python",
        "version": "3.10.0",
        "files": [{"content": "print('hello')"}],
        "stdin": "",
        "compile_timeout": 5000,
        "run_timeout": 5000,
    }
    async with httpx.AsyncClient() as c:
        res = await c.post("https://emkc.org/api/v2/piston/execute", json=payload)
        print(res.status_code, res.text)

if __name__ == "__main__":
    asyncio.run(main())
