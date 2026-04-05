import httpx
import asyncio

class CodeEvaluator:
    def __init__(self):
        self.runtimes = {
            "python": "python3",
            "javascript": "javascript",
            "cpp": "cpp",
            "java": "java",
            "go": "go",
            "rust": "rust"
        }

    async def get_runtimes(self):
        return self.runtimes

    async def _execute_single(self, client, language, code, test_input):
        """Execute a single test case using the free Paiza API"""
        paiza_lang = self.runtimes.get(language, language)
        
        url_create = "https://api.paiza.io/runners/create"
        payload = {
            "source_code": code,
            "language": paiza_lang,
            "input": test_input,
            "api_key": "guest"
        }
        
        try:
            resp = await client.post(url_create, json=payload)
            data = resp.json()
            runner_id = data.get("id")
            if not runner_id:
                return {"stdout": "", "stderr": f"Paiza API Error: {data.get('error', 'Failed to create runner')}"}
                
            # Poll for completion (max 5 seconds)
            detail_url = f"https://api.paiza.io/runners/get_details?id={runner_id}&api_key=guest"
            for _ in range(15): 
                await asyncio.sleep(0.5)
                detail_resp = await client.get(detail_url)
                res = detail_resp.json()
                
                if res.get("status") == "completed":
                    # Combine compile errors and runtime errors
                    stderr = res.get("stderr", "") or ""
                    build_stderr = res.get("build_stderr", "") or ""
                    
                    full_error = stderr
                    if build_stderr:
                        full_error = build_stderr + "\n" + full_error
                        
                    return {
                        "stdout": (res.get("stdout") or "").strip() + "\n",
                        "stderr": full_error.strip()
                    }
            
            return {"stdout": "", "stderr": "Error: Timeout waiting for paiza.io execution"}
        except Exception as e:
            return {"stdout": "", "stderr": f"Connection Error: {str(e)}"}

    async def evaluate(self, language: str, code: str, tests: list):
        """
        Evaluate code against a list of test cases in parallel using Paiza API.
        """
        results = []
        async with httpx.AsyncClient(timeout=10.0) as client:
            tasks = [self._execute_single(client, language, code, t["input"]) for t in tests]
            outputs = await asyncio.gather(*tasks)

        for idx, (out, test) in enumerate(zip(outputs, tests)):
            actual_stdout = out.get("stdout", "").strip()
            stderr = out.get("stderr", "").strip()
            expected = test.get("expected", "").strip()
            
            passed = (actual_stdout == expected) and (not stderr)
            
            results.append({
                "test_case": idx + 1,
                "input": test["input"],
                "expected": expected,
                "actual": actual_stdout,
                "error": stderr,
                "passed": passed
            })

        total_passed = sum(1 for r in results if r["passed"])
        return {
            "status": "Success" if total_passed == len(tests) else "Failed",
            "score": f"{total_passed}/{len(tests)}",
            "details": results
        }
