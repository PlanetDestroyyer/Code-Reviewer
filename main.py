from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.llms import Ollama
import nest_asyncio
import uvicorn

nest_asyncio.apply()

app = FastAPI()

class FunctionInput(BaseModel):
    code: str
    language: str


llm = Ollama(model='llama3')

@app.post("/analyze_function")
async def analyze_function(input: FunctionInput):
    prompt = f"""
    {input.code}

    Analyze the function in programming language {input.language}
    Provide detailed information about it
    Identify and fix any possible bugs
    Optimize the code if possible
    give me list of global variable used in the function in list format

    Please provide as many as at least 30 possible different test cases in array format to test this function. Each test case should be a tuple containing two elements: the input array and the target sum. Also, provide a small function to run all 100 test cases.

    Example format for test cases:
    [
        (input, output),
        (input, output),
        ...
    ]
    """

    try:
        response = llm(prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
