import { useState } from 'react';
import './App.css';
import SearchBar from './components/SearchBar';
import LLMResults from './components/LLMResults';

function App() {
  const [category, setCategory] = useState<string | null>(null);
  const [llms, setLlms] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (query: string) => {
    setIsLoading(true);
    setError(null);
    setLlms([]);        // Clear previous results
    setCategory(null);  // Clear previous category

    try {
      const response = await fetch('http://localhost:5000/choose-llm', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const modelNames = data.models.map((model: any) => model.model_name);
      setLlms(modelNames);
      setCategory(data.category);
    } catch (err) {
      console.error('Error fetching LLMs:', err);
      setError('Failed to fetch LLMs. Please try again later.');
    } finally {
      setIsLoading(false);
    }
};


  return (
    <div className="App">
      <h1>Find Your LLM</h1>
      <SearchBar onSearch={handleSearch} />
      {isLoading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <LLMResults llms={llms} category={category} />
    </div>
  );
}

export default App;
