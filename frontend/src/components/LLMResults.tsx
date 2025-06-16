interface LLMResultsProps {
  llms: string[];
}

function LLMResults({ llms }: LLMResultsProps) {
  return (
    <div>
      <h2>Top 3 LLMs:</h2>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {llms.map((llm, index) => (
          <li key={index} style={{ marginBottom: '10px' }}>{llm}</li>
        ))}
      </ul>
    </div>
  );
}

export default LLMResults;
