import asyncio
from evaluator import CodeEvaluator

async def run_test():
    ev = CodeEvaluator()
    code = """
import sys
data = sys.stdin.read().split()
if data:
    a, b = int(data[0]), int(data[1])
    print(a + b)
"""
    tests = [
        {"input": "2 3", "expected": "5"}
    ]
    
    print("Fetching runtimes...")
    await ev.get_runtimes()
    print("Python version:", ev.runtimes.get("python"))
    
    res = await ev.evaluate("python", code, tests)
    import json
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    asyncio.run(run_test())
