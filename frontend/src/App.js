import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import ApplicationForm from './components/ApplicationForm';
import ResultsDisplay from './components/ResultsDisplay';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (formData) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/evaluate', formData);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while evaluating your application');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎓 US College Admissions Simulator</h1>
        <p>Get an AI-powered evaluation of your college application</p>
      </header>

      <main className="App-main">
        {!result ? (
          <ApplicationForm onSubmit={handleSubmit} loading={loading} error={error} />
        ) : (
          <ResultsDisplay result={result} onReset={handleReset} />
        )}
      </main>

      <footer className="App-footer">
        <p>Note: This is a simulation tool for educational purposes. Results are estimates based on statistical models.</p>
      </footer>
    </div>
  );
}

export default App;
