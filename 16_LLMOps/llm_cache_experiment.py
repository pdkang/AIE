import time
import uuid
from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache
from langchain_huggingface import HuggingFaceEndpoint
import os
import getpass

# Set up environment variables
# Uncomment and use these lines if running interactively
# os.environ["HF_TOKEN"] = getpass.getpass("HF Token Key:")
# os.environ["LANGCHAIN_PROJECT"] = f"LLM Cache Experiment - {uuid.uuid4().hex[0:8]}"
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = getpass.getpass("LangChain API Key:")

# For this experiment, we'll use a HuggingFace endpoint
# Replace with your actual endpoint URL
HF_ENDPOINT_URL = "https://dcrebqe18cydo729.us-east-1.aws.endpoints.huggingface.cloud"

def setup_llm():
    """Set up and return the LLM."""
    return HuggingFaceEndpoint(
        endpoint_url=HF_ENDPOINT_URL,
        task="text-generation",
        max_new_tokens=128,
        top_k=10,
        top_p=0.95,
        typical_p=0.95,
        temperature=0.01,
        repetition_penalty=1.03,
    )

def run_experiment(llm, queries, use_cache=False):
    """Run experiment with or without cache."""
    if use_cache:
        set_llm_cache(InMemoryCache())
    else:
        set_llm_cache(None)  # Disable cache
    
    results = []
    
    for query in queries:
        start_time = time.perf_counter()
        response = llm.invoke(query)
        end_time = time.perf_counter()
        
        results.append({
            "query": query,
            "time": end_time - start_time,
            "response": response
        })
    
    return results

def main():
    # Set up test queries - we'll use the same query multiple times to test caching
    queries = [
        "What is machine learning?",
        "Explain the concept of neural networks.",
        "What is machine learning?",  # Repeated query to test cache
        "Explain the concept of neural networks.",  # Repeated query to test cache
        "What is machine learning?",  # Repeated again
    ]
    
    llm = setup_llm()
    
    print("Running experiment WITHOUT cache...")
    no_cache_results = run_experiment(llm, queries, use_cache=False)
    
    print("\nRunning experiment WITH cache...")
    cache_results = run_experiment(llm, queries, use_cache=True)
    
    # Print results
    print("\n===== RESULTS =====")
    print("\nWITHOUT CACHE:")
    for i, result in enumerate(no_cache_results):
        print(f"Query {i+1}: '{result['query'][:30]}...' - Time: {result['time']:.4f}s")
    
    print("\nWITH CACHE:")
    for i, result in enumerate(cache_results):
        print(f"Query {i+1}: '{result['query'][:30]}...' - Time: {result['time']:.4f}s")
    
    # Calculate and print statistics
    no_cache_avg = sum(r["time"] for r in no_cache_results) / len(no_cache_results)
    cache_avg = sum(r["time"] for r in cache_results) / len(cache_results)
    
    # Calculate cache hit statistics
    first_occurrence_times = {}
    cache_hit_times = []
    cache_miss_times = []
    
    for result in cache_results:
        query = result["query"]
        if query not in first_occurrence_times:
            first_occurrence_times[query] = result["time"]
            cache_miss_times.append(result["time"])
        else:
            cache_hit_times.append(result["time"])
    
    cache_hit_avg = sum(cache_hit_times) / len(cache_hit_times) if cache_hit_times else 0
    cache_miss_avg = sum(cache_miss_times) / len(cache_miss_times) if cache_miss_times else 0
    
    print("\n===== STATISTICS =====")
    print(f"Average time WITHOUT cache: {no_cache_avg:.4f}s")
    print(f"Average time WITH cache: {cache_avg:.4f}s")
    print(f"Average time for cache HITS: {cache_hit_avg:.4f}s")
    print(f"Average time for cache MISSES: {cache_miss_avg:.4f}s")
    print(f"Speed improvement for cache hits: {(cache_miss_avg/cache_hit_avg):.2f}x faster")
    
    # Verify response consistency
    print("\n===== RESPONSE CONSISTENCY =====")
    for i in range(len(queries)):
        if i > 0 and queries[i] == queries[i-1]:
            if cache_results[i]["response"] == cache_results[i-1]["response"]:
                print(f"Query {i+1}: Responses match for repeated query (GOOD)")
            else:
                print(f"Query {i+1}: Responses differ for repeated query (UNEXPECTED)")

if __name__ == "__main__":
    main() 