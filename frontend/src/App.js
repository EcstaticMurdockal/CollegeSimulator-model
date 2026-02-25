import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import ApplicationFormEnhanced from './components/ApplicationFormEnhanced';
import ResultsDisplay from './components/ResultsDisplay';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (formData) => {
    setLoading(true);
    setError(null);
    setResult(null);

    // Log the data being sent for debugging
    console.log('Submitting data:', JSON.stringify(formData, null, 2));

    try {
      const response = await axios.post('http://localhost:8000/evaluate', formData);
      setResult(response.data);
    } catch (err) {
      console.error('Full error object:', err);
      console.error('Error response:', err.response);
      console.error('Error details:', err.response?.data);

      // Handle validation errors from FastAPI
      if (err.response?.data?.detail) {
        const detail = err.response.data.detail;

        // If detail is an array of validation errors
        if (Array.isArray(detail)) {
          const errorMessages = detail.map(error => {
            const field = error.loc ? error.loc.join(' -> ') : 'Unknown field';
            return `${field}: ${error.msg}`;
          }).join('\n');
          setError(`Validation errors:\n${errorMessages}`);
        }
        // If detail is a string
        else if (typeof detail === 'string') {
          setError(detail);
        }
        // If detail is an object
        else {
          setError(JSON.stringify(detail, null, 2));
        }
      } else if (err.response?.status) {
        setError(`Server error (${err.response.status}): ${err.response.statusText || 'Unknown error'}\n\nPlease check the browser console for details.`);
      } else if (err.request) {
        setError('No response from server. Please make sure the backend is running on http://localhost:8000');
      } else {
        setError(`Error: ${err.message}\n\nPlease check the browser console for details.`);
      }
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
        <h1>🎓 US College Admissions Simulator - Enhanced</h1>
        <p>Get an ML-powered evaluation of your college application</p>
        <p className="subtitle">100 Top Universities • 11 Gender Options • 38 AP Subjects • ML Predictions</p>
      </header>

      <main className="App-main">
        {!result ? (
          <ApplicationFormEnhanced onSubmit={handleSubmit} loading={loading} error={error} />
        ) : (
          <ResultsDisplay result={result} onReset={handleReset} />
        )}
      </main>

      <footer className="App-footer">
        <p>Note: This is a simulation tool for educational purposes. Results are estimates based on ML models and statistical analysis.</p>
      </footer>
    </div>
  );
}

export default App;
