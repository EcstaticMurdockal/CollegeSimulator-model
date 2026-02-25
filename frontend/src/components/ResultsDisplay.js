import React from 'react';

function ResultsDisplay({ result, onReset }) {
  const getDecisionClass = (decision) => {
    const decisionMap = {
      'Likely Admit': 'decision-likely',
      'Possible': 'decision-possible',
      'Reach': 'decision-reach',
      'Unlikely': 'decision-unlikely'
    };
    return decisionMap[decision] || 'decision-reach';
  };

  return (
    <div className="results-container">
      <div className="results-header">
        <div className={`decision-badge ${getDecisionClass(result.decision)}`}>
          {result.decision}
        </div>
        <div className="probability">
          {(result.admission_probability * 100).toFixed(1)}%
        </div>
        <p style={{ color: '#666', fontSize: '1.1rem' }}>Estimated Admission Probability</p>
      </div>

      <div className="results-section">
        <h3>Analysis</h3>
        <ul className="reasoning-list">
          {result.reasoning.map((reason, index) => (
            <li key={index}>{reason}</li>
          ))}
        </ul>
      </div>

      {result.strengths.length > 0 && (
        <div className="results-section">
          <h3>Your Strengths</h3>
          <ul className="strengths-list">
            {result.strengths.map((strength, index) => (
              <li key={index}>✓ {strength}</li>
            ))}
          </ul>
        </div>
      )}

      {result.weaknesses.length > 0 && (
        <div className="results-section">
          <h3>Areas for Improvement</h3>
          <ul className="weaknesses-list">
            {result.weaknesses.map((weakness, index) => (
              <li key={index}>⚠ {weakness}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="results-section">
        <h3>Score Breakdown</h3>
        <div className="score-breakdown">
          <div className="score-item">
            <div className="score-label">Academic</div>
            <div className="score-value">{result.score_breakdown.academic}</div>
          </div>
          <div className="score-item">
            <div className="score-label">Extracurricular</div>
            <div className="score-value">{result.score_breakdown.extracurricular}</div>
          </div>
          <div className="score-item">
            <div className="score-label">Application</div>
            <div className="score-value">{result.score_breakdown.application}</div>
          </div>
          <div className="score-item">
            <div className="score-label">Demographic</div>
            <div className="score-value">{result.score_breakdown.demographic}</div>
          </div>
          <div className="score-item">
            <div className="score-label">Total</div>
            <div className="score-value">{result.score_breakdown.total}</div>
          </div>
        </div>
      </div>

      {result.ml_info && (
        <div className="results-section">
          <h3>ML Prediction Details</h3>
          <div style={{ background: '#f0f8ff', padding: '15px', borderRadius: '8px', borderLeft: '4px solid #2196F3' }}>
            <p><strong>Method:</strong> {result.ml_info.method === 'hybrid' ? 'Hybrid (ML + Rule-based)' : 'Rule-based Only'}</p>
            {result.ml_info.ml_available && (
              <>
                <p><strong>ML Probability:</strong> {(result.ml_info.ml_probability * 100).toFixed(1)}%</p>
                <p><strong>Rule-based Probability:</strong> {(result.ml_info.rule_based_probability * 100).toFixed(1)}%</p>
              </>
            )}
            <p style={{ fontSize: '0.9rem', color: '#666', marginTop: '10px' }}>
              {result.ml_info.note}
            </p>
          </div>
        </div>
      )}

      <div className="reset-section">
        <button className="btn btn-primary" onClick={onReset}>
          Evaluate Another Application
        </button>
      </div>
    </div>
  );
}

export default ResultsDisplay;
