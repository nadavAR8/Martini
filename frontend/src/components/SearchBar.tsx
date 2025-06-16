import { useState } from 'react';

interface SearchBarProps {
  onSearch: (query: string) => void;
}

function SearchBar({ onSearch }: SearchBarProps) {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() !== '') {
      onSearch(inputValue);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
      <input
        type="text"
        placeholder="Type here..."
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        style={{ padding: '10px', fontSize: '16px', width: '300px' }}
      />
      <button type="submit" style={{ padding: '10px 20px', fontSize: '16px', marginLeft: '10px' }}>
        Submit
      </button>
    </form>
  );
}

export default SearchBar;
