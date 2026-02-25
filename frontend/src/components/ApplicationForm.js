import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ApplicationForm({ onSubmit, loading, error }) {
  const [schools, setSchools] = useState([]);
  const [formData, setFormData] = useState({
    region: 'Northeast',
    sex: 'Prefer not to say',
    target_school: '',
    target_major: '',
    gpa: '',
    gpa_trend: 'stable',
    ap_courses: '',
    ap_scores: [],
    sat_score: '',
    toefl_score: '',
    ielts_score: '',
    curriculum_difficulty: 'medium',
    research_experience: '',
    extracurriculars: [],
    competitions: [],
    lor_quality: '3',
    essay_quality: '3'
  });

  const [apScoreInput, setApScoreInput] = useState('');
  const [ecInput, setEcInput] = useState('');
  const [compInput, setCompInput] = useState('');

  useEffect(() => {
    axios.get('http://localhost:8000/schools')
      .then(response => {
        setSchools(response.data);
        if (response.data.length > 0) {
          setFormData(prev => ({ ...prev, target_school: response.data[0] }));
        }
      })
      .catch(err => console.error('Failed to load schools:', err));
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const addApScore = () => {
    const score = parseInt(apScoreInput);
    if (score >= 1 && score <= 5) {
      setFormData(prev => ({
        ...prev,
        ap_scores: [...prev.ap_scores, score]
      }));
      setApScoreInput('');
    }
  };

  const removeApScore = (index) => {
    setFormData(prev => ({
      ...prev,
      ap_scores: prev.ap_scores.filter((_, i) => i !== index)
    }));
  };

  const addExtracurricular = () => {
    if (ecInput.trim()) {
      setFormData(prev => ({
        ...prev,
        extracurriculars: [...prev.extracurriculars, ecInput.trim()]
      }));
      setEcInput('');
    }
  };

  const removeExtracurricular = (index) => {
    setFormData(prev => ({
      ...prev,
      extracurriculars: prev.extracurriculars.filter((_, i) => i !== index)
    }));
  };

  const addCompetition = () => {
    if (compInput.trim()) {
      setFormData(prev => ({
        ...prev,
        competitions: [...prev.competitions, compInput.trim()]
      }));
      setCompInput('');
    }
  };

  const removeCompetition = (index) => {
    setFormData(prev => ({
      ...prev,
      competitions: prev.competitions.filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const submitData = {
      ...formData,
      gpa: parseFloat(formData.gpa),
      ap_courses: parseInt(formData.ap_courses) || 0,
      sat_score: formData.sat_score ? parseInt(formData.sat_score) : null,
      toefl_score: formData.toefl_score ? parseInt(formData.toefl_score) : null,
      ielts_score: formData.ielts_score ? parseFloat(formData.ielts_score) : null,
      lor_quality: parseInt(formData.lor_quality),
      essay_quality: parseInt(formData.essay_quality)
    };

    onSubmit(submitData);
  };

  return (
    <form className="form-container" onSubmit={handleSubmit}>
      {error && <div className="error-message">{error}</div>}

      <div className="form-section">
        <h2>Basic Information</h2>
        <div className="form-row">
          <div className="form-group">
            <label>Region</label>
            <select name="region" value={formData.region} onChange={handleChange} required>
              <option value="Northeast">Northeast</option>
              <option value="Southeast">Southeast</option>
              <option value="Midwest">Midwest</option>
              <option value="Southwest">Southwest</option>
              <option value="West">West</option>
              <option value="International">International</option>
            </select>
          </div>
          <div className="form-group">
            <label>Sex</label>
            <select name="sex" value={formData.sex} onChange={handleChange} required>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
              <option value="Prefer not to say">Prefer not to say</option>
            </select>
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Target School</label>
            <select name="target_school" value={formData.target_school} onChange={handleChange} required>
              {schools.map(school => (
                <option key={school} value={school}>{school}</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Target Major</label>
            <input
              type="text"
              name="target_major"
              value={formData.target_major}
              onChange={handleChange}
              placeholder="e.g., Computer Science"
              required
            />
          </div>
        </div>
      </div>

      <div className="form-section">
        <h2>Academic Metrics</h2>
        <div className="form-row">
          <div className="form-group">
            <label>GPA (0.0 - 4.0)</label>
            <input
              type="number"
              name="gpa"
              value={formData.gpa}
              onChange={handleChange}
              step="0.01"
              min="0"
              max="4"
              required
            />
          </div>
          <div className="form-group">
            <label>GPA Trend</label>
            <select name="gpa_trend" value={formData.gpa_trend} onChange={handleChange} required>
              <option value="upward">Upward</option>
              <option value="stable">Stable</option>
              <option value="downward">Downward</option>
            </select>
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Number of AP Courses</label>
            <input
              type="number"
              name="ap_courses"
              value={formData.ap_courses}
              onChange={handleChange}
              min="0"
              required
            />
          </div>
          <div className="form-group">
            <label>Curriculum Difficulty</label>
            <select name="curriculum_difficulty" value={formData.curriculum_difficulty} onChange={handleChange} required>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="very_high">Very High</option>
            </select>
          </div>
        </div>
        <div className="form-group">
          <label>AP Scores (1-5)</label>
          <div className="dynamic-list">
            <div className="dynamic-list-item">
              <input
                type="number"
                value={apScoreInput}
                onChange={(e) => setApScoreInput(e.target.value)}
                min="1"
                max="5"
                placeholder="Enter AP score"
              />
              <button type="button" className="btn btn-secondary" onClick={addApScore}>Add</button>
            </div>
            {formData.ap_scores.map((score, index) => (
              <div key={index} className="dynamic-list-item">
                <input type="text" value={`AP Score: ${score}`} disabled />
                <button type="button" className="btn btn-remove" onClick={() => removeApScore(index)}>Remove</button>
              </div>
            ))}
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>SAT Score (400-1600)</label>
            <input
              type="number"
              name="sat_score"
              value={formData.sat_score}
              onChange={handleChange}
              min="400"
              max="1600"
              placeholder="Optional"
            />
          </div>
          <div className="form-group">
            <label>TOEFL Score (0-120) or IELTS (0-9)</label>
            <div className="form-row">
              <input
                type="number"
                name="toefl_score"
                value={formData.toefl_score}
                onChange={handleChange}
                min="0"
                max="120"
                placeholder="TOEFL"
              />
              <input
                type="number"
                name="ielts_score"
                value={formData.ielts_score}
                onChange={handleChange}
                step="0.5"
                min="0"
                max="9"
                placeholder="IELTS"
              />
            </div>
          </div>
        </div>
      </div>

      <div className="form-section">
        <h2>Research & Activities</h2>
        <div className="form-group">
          <label>Research Experience</label>
          <textarea
            name="research_experience"
            value={formData.research_experience}
            onChange={handleChange}
            placeholder="Describe your research projects, publications, lab work, etc."
          />
          <small>Include details about publications, conferences, independent projects, or lab work</small>
        </div>
        <div className="form-group">
          <label>Extracurricular Activities</label>
          <div className="dynamic-list">
            <div className="dynamic-list-item">
              <input
                type="text"
                value={ecInput}
                onChange={(e) => setEcInput(e.target.value)}
                placeholder="e.g., President of Debate Club"
              />
              <button type="button" className="btn btn-secondary" onClick={addExtracurricular}>Add</button>
            </div>
            {formData.extracurriculars.map((ec, index) => (
              <div key={index} className="dynamic-list-item">
                <input type="text" value={ec} disabled />
                <button type="button" className="btn btn-remove" onClick={() => removeExtracurricular(index)}>Remove</button>
              </div>
            ))}
          </div>
        </div>
        <div className="form-group">
          <label>Competitions & Awards</label>
          <div className="dynamic-list">
            <div className="dynamic-list-item">
              <input
                type="text"
                value={compInput}
                onChange={(e) => setCompInput(e.target.value)}
                placeholder="e.g., National Merit Scholar"
              />
              <button type="button" className="btn btn-secondary" onClick={addCompetition}>Add</button>
            </div>
            {formData.competitions.map((comp, index) => (
              <div key={index} className="dynamic-list-item">
                <input type="text" value={comp} disabled />
                <button type="button" className="btn btn-remove" onClick={() => removeCompetition(index)}>Remove</button>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="form-section">
        <h2>Application Materials</h2>
        <div className="form-row">
          <div className="form-group">
            <label>Letter of Recommendation Quality (1-5)</label>
            <select name="lor_quality" value={formData.lor_quality} onChange={handleChange} required>
              <option value="1">1 - Weak</option>
              <option value="2">2 - Below Average</option>
              <option value="3">3 - Average</option>
              <option value="4">4 - Strong</option>
              <option value="5">5 - Exceptional</option>
            </select>
          </div>
          <div className="form-group">
            <label>Essay Quality (1-5)</label>
            <select name="essay_quality" value={formData.essay_quality} onChange={handleChange} required>
              <option value="1">1 - Weak</option>
              <option value="2">2 - Below Average</option>
              <option value="3">3 - Average</option>
              <option value="4">4 - Strong</option>
              <option value="5">5 - Exceptional</option>
            </select>
          </div>
        </div>
      </div>

      <div className="submit-section">
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Evaluating...' : 'Evaluate My Application'}
        </button>
      </div>
    </form>
  );
}

export default ApplicationForm;
