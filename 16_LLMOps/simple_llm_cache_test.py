import time
from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache
from langchain_core.language_models.llms import LLM
from typing import Any, List, Optional

class MockLLM(LLM):
    """A mock LLM that simulates response generation with a delay."""
    
    def __init__(self, response_delay: float = 1.0):
        """Initialize with configurable delay."""
        super().__init__()
        self.response_delay = response_delay
        self.call_count = 0
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs: Any) -> str:
        """Simulate LLM call with a delay."""
        self.call_count += 1
        # Simulate processing time
        time.sleep(self.response_delay)
        return f"Response to: {prompt} (Call #{self.call_count})"
    
    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "mock_llm"

def run_cache_experiment():
    """Run a simple experiment to test LLM caching."""
    # Create our mock LLM with a 1-second delay
    llm = MockLLM(response_delay=1.0)
    
    # Define test queries - with repetitions to test cache
    queries = [
        "What is machine learning?",
        "Explain neural networks.",
        "What is machine learning?",  # Repeated to test cache
        "What is machine learning?",  # Repeated again
        "Explain neural networks.",   # Repeated to test cache
    ]
    
    print("===== WITHOUT CACHE =====")
    # First run without cache
    set_llm_cache(None)  # Ensure cache is disabled
    
    for i, query in enumerate(queries):
        start_time = time.perf_counter()
        response = llm.invoke(query)
        end_time = time.perf_counter()
        
        print(f"Query {i+1}: '{query}'")
        print(f"Response: {response}")
        print(f"Time: {end_time - start_time:.4f} seconds")
        print("-" * 50)
    
    # Reset call counter
    llm.call_count = 0
    
    print("\n===== WITH CACHE =====")
    # Now run with cache enabled
    set_llm_cache(InMemoryCache())
    
    for i, query in enumerate(queries):
        start_time = time.perf_counter()
        response = llm.invoke(query)
        end_time = time.perf_counter()
        
        print(f"Query {i+1}: '{query}'")
        print(f"Response: {response}")
        print(f"Time: {end_time - start_time:.4f} seconds")
        print("-" * 50)
    
    # Print cache statistics
    print("\n===== CACHE STATISTICS =====")
    print(f"Total queries: {len(queries)}")
    print(f"Unique queries: {len(set(queries))}")
    print(f"Actual LLM calls made: {llm.call_count}")
    print(f"Queries served from cache: {len(queries) - llm.call_count}")

if __name__ == "__main__":
    run_cache_experiment() 