interface LLMResultsProps {
  llms: string[];
  category: string | null;
}

function LLMResults({ llms, category }: LLMResultsProps) {
  return (
    <div>
      {category && <h2>Category: {category}</h2>}
      <h3>Top {llms.length} LLMs:</h3>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {llms.map((llm, index) => (
          <li key={index} style={{ marginBottom: '10px' }}>{llm}</li>
        ))}
      </ul>
    </div>
  );
}

export default LLMResults;
