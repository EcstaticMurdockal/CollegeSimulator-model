import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ApplicationFormEnhanced.css';

const API_BASE = 'http://localhost:8000';

// Constants matching backend enums
const GENDER_OPTIONS = [
  'Male',
  'Female',
  'Non-binary',
  'Transgender Male',
  'Transgender Female',
  'Genderqueer/Gender Fluid',
  'Agender',
  'Two-Spirit',
  'Questioning',
  'Prefer not to say',
  'Prefer to self-describe'
];

const APPLICATION_ROUNDS = [
  'Early Decision (ED)',
  'Early Decision I (ED1)',
  'Early Decision II (ED2)',
  'Early Action (EA)',
  'Restrictive Early Action (REA)',
  'Single-Choice Early Action (SCEA)',
  'Regular Decision (RD)',
  'Rolling Admission'
];

const AP_SUBJECTS = [
  // Math & CS
  'AP Calculus AB',
  'AP Calculus BC',
  'AP Statistics',
  'AP Computer Science A',
  'AP Computer Science Principles',
  // Sciences
  'AP Biology',
  'AP Chemistry',
  'AP Physics 1: Algebra-Based',
  'AP Physics 2: Algebra-Based',
  'AP Physics C: Mechanics',
  'AP Physics C: Electricity and Magnetism',
  'AP Environmental Science',
  // English
  'AP English Language and Composition',
  'AP English Literature and Composition',
  // History & Social Sciences
  'AP United States History',
  'AP World History: Modern',
  'AP European History',
  'AP United States Government and Politics',
  'AP Comparative Government and Politics',
  'AP Macroeconomics',
  'AP Microeconomics',
  'AP Psychology',
  'AP Human Geography',
  // World Languages
  'AP Spanish Language and Culture',
  'AP Spanish Literature and Culture',
  'AP French Language and Culture',
  'AP German Language and Culture',
  'AP Italian Language and Culture',
  'AP Chinese Language and Culture',
  'AP Japanese Language and Culture',
  'AP Latin',
  // Arts
  'AP Art History',
  'AP Music Theory',
  'AP Studio Art: 2-D Design',
  'AP Studio Art: 3-D Design',
  'AP Studio Art: Drawing',
  // Capstone
  'AP Seminar',
  'AP Research'
];

const COUNTRIES = [
  'United States', 'China', 'India', 'Canada', 'United Kingdom', 'South Korea',
  'Japan', 'Germany', 'France', 'Australia', 'Singapore', 'Hong Kong',
  'Taiwan', 'Mexico', 'Brazil', 'Russia', 'Italy', 'Spain', 'Netherlands',
  'Switzerland', 'Sweden', 'Norway', 'Denmark', 'Finland', 'Other'
];

const US_STATES = [
  'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
  'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
  'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
  'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
  'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
  'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
  'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
  'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
  'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
  'West Virginia', 'Wisconsin', 'Wyoming', 'Washington DC', 'Puerto Rico'
];

const ETHNICITY_OPTIONS = [
  'Asian',
  'White',
  'Hispanic/Latino',
  'Black/African American',
  'Native American',
  'Pacific Islander',
  'Middle Eastern',
  'Other'
];

function ApplicationFormEnhanced({ onSubmit, loading, error }) {
  const [schools, setSchools] = useState([]);
  const [currentSection, setCurrentSection] = useState(0);

  const [formData, setFormData] = useState({
    // Demographics
    country: 'United States',
    state_province: 'California',
    city: '',
    gender: 'Prefer not to say',
    ethnicity: [],
    first_generation: false,
    legacy_status: false,
    recruited_athlete: false,

    // Target School
    target_school: '',
    target_major: '',
    target_degree: 'Bachelor of Science (BS)',
    application_round: 'Regular Decision (RD)',

    // Socioeconomic
    family_income_bracket: '$75k-$150k',
    fee_waiver: false,

    // High School
    high_school_name: '',
    high_school_type: 'public',
    high_school_ranking: null,
    class_rank: null,
    class_size: null,

    // Academic - GPA
    gpa_unweighted: '',
    gpa_weighted: '',
    gpa_trend: 'stable',
    gpa_by_year: { '9th': 0, '10th': 0, '11th': 0, '12th': 0 },

    // Academic - Test Scores
    sat_score: null,
    sat_math: null,
    sat_ebrw: null,
    act_score: null,
    sat_subject_tests: [],
    toefl_score: null,
    ielts_score: null,
    duolingo_score: null,

    // Academic - Courses
    ap_courses: [],
    honors_courses: 0,
    ib_diploma: false,
    ib_score: null,
    curriculum_difficulty: 'high',

    // Research
    research_experience: '',
    research_publications: [],
    research_presentations: [],
    independent_projects: [],

    // Activities
    extracurriculars: [],
    competitions: [],
    academic_honors: [],
    work_experience: [],
    community_service_hours: 0,
    community_service_description: '',
    summer_activities: [],

    // Application Materials
    lor_quality: 3,
    lor_sources: [],
    essay_quality: 3,
    essay_topics: [],
    supplemental_materials: [],

    // Demonstrated Interest
    campus_visit: false,
    interview_completed: false,
    contacted_admissions: false,
    attended_info_sessions: 0
  });

  // Temporary inputs for dynamic lists
  const [apInput, setApInput] = useState({ subject: AP_SUBJECTS[0], score: 5, year_taken: '12th' });
  const [ecInput, setEcInput] = useState({ activity_name: '', role: '', years_participated: 1, hours_per_week: 5, description: '' });
  const [compInput, setCompInput] = useState({ name: '', level: 'school', award: '', year: '2024' });

  useEffect(() => {
    axios.get(`${API_BASE}/schools`)
      .then(response => {
        setSchools(response.data);
        if (response.data.length > 0) {
          setFormData(prev => ({ ...prev, target_school: response.data[0] }));
        }
      })
      .catch(err => console.error('Failed to load schools:', err));
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleEthnicityChange = (ethnicity) => {
    setFormData(prev => ({
      ...prev,
      ethnicity: prev.ethnicity.includes(ethnicity)
        ? prev.ethnicity.filter(e => e !== ethnicity)
        : [...prev.ethnicity, ethnicity]
    }));
  };

  const addAPCourse = () => {
    if (apInput.subject && apInput.score >= 1 && apInput.score <= 5) {
      setFormData(prev => ({
        ...prev,
        ap_courses: [...prev.ap_courses, { ...apInput }]
      }));
      setApInput({ subject: AP_SUBJECTS[0], score: 5, year_taken: '12th' });
    }
  };

  const removeAPCourse = (index) => {
    setFormData(prev => ({
      ...prev,
      ap_courses: prev.ap_courses.filter((_, i) => i !== index)
    }));
  };

  const addExtracurricular = () => {
    if (ecInput.activity_name && ecInput.role) {
      setFormData(prev => ({
        ...prev,
        extracurriculars: [...prev.extracurriculars, { ...ecInput }]
      }));
      setEcInput({ activity_name: '', role: '', years_participated: 1, hours_per_week: 5, description: '' });
    }
  };

  const removeExtracurricular = (index) => {
    setFormData(prev => ({
      ...prev,
      extracurriculars: prev.extracurriculars.filter((_, i) => i !== index)
    }));
  };

  const addCompetition = () => {
    if (compInput.name && compInput.award) {
      setFormData(prev => ({
        ...prev,
        competitions: [...prev.competitions, { ...compInput }]
      }));
      setCompInput({ name: '', level: 'school', award: '', year: '2024' });
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

    // Auto-fill gpa_by_year if not provided
    const gpaByYear = formData.gpa_by_year['9th'] === 0 ? {
      '9th': parseFloat(formData.gpa_unweighted) || 3.5,
      '10th': parseFloat(formData.gpa_unweighted) || 3.5,
      '11th': parseFloat(formData.gpa_unweighted) || 3.5,
      '12th': parseFloat(formData.gpa_unweighted) || 3.5
    } : formData.gpa_by_year;

    // Convert to backend format
    const submitData = {
      ...formData,
      gpa_unweighted: parseFloat(formData.gpa_unweighted),
      gpa_weighted: formData.gpa_weighted ? parseFloat(formData.gpa_weighted) : null,
      gpa_by_year: gpaByYear,
      class_rank: formData.class_rank ? parseInt(formData.class_rank) : null,
      class_size: formData.class_size ? parseInt(formData.class_size) : null,
      sat_score: formData.sat_score ? parseInt(formData.sat_score) : null,
      sat_math: formData.sat_math ? parseInt(formData.sat_math) : null,
      sat_ebrw: formData.sat_ebrw ? parseInt(formData.sat_ebrw) : null,
      act_score: formData.act_score ? parseInt(formData.act_score) : null,
      toefl_score: formData.toefl_score ? parseInt(formData.toefl_score) : null,
      ielts_score: formData.ielts_score ? parseFloat(formData.ielts_score) : null,
      duolingo_score: formData.duolingo_score ? parseInt(formData.duolingo_score) : null,
      honors_courses: parseInt(formData.honors_courses),
      ib_score: formData.ib_score ? parseInt(formData.ib_score) : null,
      community_service_hours: parseInt(formData.community_service_hours),
      lor_quality: parseInt(formData.lor_quality),
      essay_quality: parseInt(formData.essay_quality),
      attended_info_sessions: parseInt(formData.attended_info_sessions),
      // Ensure required string fields have defaults
      high_school_name: formData.high_school_name || 'Not specified',
      community_service_description: formData.community_service_description || 'None',
      research_experience: formData.research_experience || 'None',
      // Ensure arrays with defaults
      lor_sources: formData.lor_sources.length > 0 ? formData.lor_sources : ['Teacher', 'Counselor'],
      essay_topics: formData.essay_topics.length > 0 ? formData.essay_topics : ['Personal statement'],
      summer_activities: formData.summer_activities.length > 0 ? formData.summer_activities : ['Summer break']
    };

    onSubmit(submitData);
  };

  const sections = [
    'Demographics',
    'Target School',
    'Academic Performance',
    'Test Scores',
    'Courses & Curriculum',
    'Activities & Experience',
    'Application Materials'
  ];

  const nextSection = () => {
    if (currentSection < sections.length - 1) {
      setCurrentSection(currentSection + 1);
      window.scrollTo(0, 0);
    }
  };

  const prevSection = () => {
    if (currentSection > 0) {
      setCurrentSection(currentSection - 1);
      window.scrollTo(0, 0);
    }
  };

  return (
    <div className="form-wrapper">
      <div className="form-progress">
        <div className="progress-bar">
          <div
            className="progress-fill"
            style={{ width: `${((currentSection + 1) / sections.length) * 100}%` }}
          />
        </div>
        <div className="progress-steps">
          {sections.map((section, index) => (
            <div
              key={index}
              className={`progress-step ${index === currentSection ? 'active' : ''} ${index < currentSection ? 'completed' : ''}`}
              onClick={() => setCurrentSection(index)}
            >
              <div className="step-number">{index + 1}</div>
              <div className="step-label">{section}</div>
            </div>
          ))}
        </div>
      </div>

      <form className="form-container-enhanced" onSubmit={handleSubmit}>
        {error && (
          <div className="error-message">
            <strong>Error:</strong>
            <pre style={{ whiteSpace: 'pre-wrap', marginTop: '10px', fontSize: '14px' }}>
              {error}
            </pre>
          </div>
        )}

        {/* Section 0: Demographics */}
        {currentSection === 0 && (
          <div className="form-section">
            <h2>Demographics & Background</h2>

            <div className="form-row">
              <div className="form-group">
                <label>Country *</label>
                <select name="country" value={formData.country} onChange={handleChange} required>
                  {COUNTRIES.map(country => (
                    <option key={country} value={country}>{country}</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>State/Province *</label>
                {formData.country === 'United States' ? (
                  <select name="state_province" value={formData.state_province} onChange={handleChange} required>
                    {US_STATES.map(state => (
                      <option key={state} value={state}>{state}</option>
                    ))}
                  </select>
                ) : (
                  <input
                    type="text"
                    name="state_province"
                    value={formData.state_province}
                    onChange={handleChange}
                    placeholder="Enter state/province"
                    required
                  />
                )}
              </div>
            </div>

            <div className="form-group">
              <label>City *</label>
              <input
                type="text"
                name="city"
                value={formData.city}
                onChange={handleChange}
                placeholder="Enter your city"
                required
              />
            </div>

            <div className="form-group">
              <label>Gender *</label>
              <select name="gender" value={formData.gender} onChange={handleChange} required>
                {GENDER_OPTIONS.map(gender => (
                  <option key={gender} value={gender}>{gender}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Ethnicity (Select all that apply)</label>
              <div className="checkbox-group">
                {ETHNICITY_OPTIONS.map(ethnicity => (
                  <label key={ethnicity} className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={formData.ethnicity.includes(ethnicity)}
                      onChange={() => handleEthnicityChange(ethnicity)}
                    />
                    {ethnicity}
                  </label>
                ))}
              </div>
            </div>

            <div className="form-row">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="first_generation"
                  checked={formData.first_generation}
                  onChange={handleChange}
                />
                First-generation college student
              </label>
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="legacy_status"
                  checked={formData.legacy_status}
                  onChange={handleChange}
                />
                Legacy (parent/sibling attended)
              </label>
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="recruited_athlete"
                  checked={formData.recruited_athlete}
                  onChange={handleChange}
                />
                Recruited athlete
              </label>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Family Income Bracket</label>
                <select name="family_income_bracket" value={formData.family_income_bracket} onChange={handleChange}>
                  <option value="<$30k">&lt;$30k</option>
                  <option value="$30k-$75k">$30k-$75k</option>
                  <option value="$75k-$150k">$75k-$150k</option>
                  <option value="$150k-$250k">$150k-$250k</option>
                  <option value=">$250k">&gt;$250k</option>
                </select>
              </div>
              <div className="form-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    name="fee_waiver"
                    checked={formData.fee_waiver}
                    onChange={handleChange}
                  />
                  Application fee waiver
                </label>
              </div>
            </div>
          </div>
        )}

        {/* Section 1: Target School */}
        {currentSection === 1 && (
          <div className="form-section">
            <h2>Target School & Application</h2>

            <div className="form-group">
              <label>Target School *</label>
              <select name="target_school" value={formData.target_school} onChange={handleChange} required>
                {schools.map(school => (
                  <option key={school} value={school}>{school}</option>
                ))}
              </select>
              <small>{schools.length} universities available</small>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Target Major *</label>
                <input
                  type="text"
                  name="target_major"
                  value={formData.target_major}
                  onChange={handleChange}
                  placeholder="e.g., Computer Science"
                  required
                />
              </div>
              <div className="form-group">
                <label>Target Degree *</label>
                <select name="target_degree" value={formData.target_degree} onChange={handleChange} required>
                  <option value="Bachelor of Arts (BA)">Bachelor of Arts (BA)</option>
                  <option value="Bachelor of Science (BS)">Bachelor of Science (BS)</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label>Application Round *</label>
              <select name="application_round" value={formData.application_round} onChange={handleChange} required>
                {APPLICATION_ROUNDS.map(round => (
                  <option key={round} value={round}>{round}</option>
                ))}
              </select>
              <small>Early Decision is binding. Early Action is non-binding.</small>
            </div>
          </div>
        )}

        {/* Section 2: Academic Performance */}
        {currentSection === 2 && (
          <div className="form-section">
            <h2>Academic Performance</h2>

            <h3>High School Information</h3>
            <div className="form-row">
              <div className="form-group">
                <label>High School Name *</label>
                <input
                  type="text"
                  name="high_school_name"
                  value={formData.high_school_name}
                  onChange={handleChange}
                  placeholder="Enter your high school name"
                  required
                />
              </div>
              <div className="form-group">
                <label>High School Type *</label>
                <select name="high_school_type" value={formData.high_school_type} onChange={handleChange} required>
                  <option value="public">Public</option>
                  <option value="private">Private</option>
                  <option value="charter">Charter</option>
                  <option value="international">International</option>
                  <option value="homeschool">Homeschool</option>
                </select>
              </div>
            </div>

            <h3>GPA</h3>
            <div className="form-row">
              <div className="form-group">
                <label>Unweighted GPA (0.0-4.0) *</label>
                <input
                  type="number"
                  name="gpa_unweighted"
                  value={formData.gpa_unweighted}
                  onChange={handleChange}
                  step="0.01"
                  min="0"
                  max="4"
                  required
                />
              </div>
              <div className="form-group">
                <label>Weighted GPA (optional)</label>
                <input
                  type="number"
                  name="gpa_weighted"
                  value={formData.gpa_weighted}
                  onChange={handleChange}
                  step="0.01"
                  min="0"
                  max="5"
                />
              </div>
            </div>

            <div className="form-group">
              <label>GPA Trend *</label>
              <select name="gpa_trend" value={formData.gpa_trend} onChange={handleChange} required>
                <option value="upward">Upward (improving over time)</option>
                <option value="stable">Stable (consistent)</option>
                <option value="downward">Downward (declining)</option>
              </select>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Class Rank (optional)</label>
                <input
                  type="number"
                  name="class_rank"
                  value={formData.class_rank || ''}
                  onChange={handleChange}
                  min="1"
                  placeholder="e.g., 5"
                />
              </div>
              <div className="form-group">
                <label>Class Size (optional)</label>
                <input
                  type="number"
                  name="class_size"
                  value={formData.class_size || ''}
                  onChange={handleChange}
                  min="1"
                  placeholder="e.g., 500"
                />
              </div>
            </div>
          </div>
        )}

        {/* Section 3: Test Scores */}
        {currentSection === 3 && (
          <div className="form-section">
            <h2>Standardized Test Scores</h2>

            <h3>SAT</h3>
            <div className="form-row">
              <div className="form-group">
                <label>SAT Total (400-1600)</label>
                <input
                  type="number"
                  name="sat_score"
                  value={formData.sat_score || ''}
                  onChange={handleChange}
                  min="400"
                  max="1600"
                  placeholder="Optional"
                />
              </div>
              <div className="form-group">
                <label>SAT Math (200-800)</label>
                <input
                  type="number"
                  name="sat_math"
                  value={formData.sat_math || ''}
                  onChange={handleChange}
                  min="200"
                  max="800"
                  placeholder="Optional"
                />
              </div>
              <div className="form-group">
                <label>SAT EBRW (200-800)</label>
                <input
                  type="number"
                  name="sat_ebrw"
                  value={formData.sat_ebrw || ''}
                  onChange={handleChange}
                  min="200"
                  max="800"
                  placeholder="Optional"
                />
              </div>
            </div>

            <h3>ACT</h3>
            <div className="form-group">
              <label>ACT Composite (1-36)</label>
              <input
                type="number"
                name="act_score"
                value={formData.act_score || ''}
                onChange={handleChange}
                min="1"
                max="36"
                placeholder="Optional"
              />
            </div>

            <h3>English Proficiency (for international students)</h3>
            <div className="form-row">
              <div className="form-group">
                <label>TOEFL (0-120)</label>
                <input
                  type="number"
                  name="toefl_score"
                  value={formData.toefl_score || ''}
                  onChange={handleChange}
                  min="0"
                  max="120"
                  placeholder="Optional"
                />
              </div>
              <div className="form-group">
                <label>IELTS (0-9)</label>
                <input
                  type="number"
                  name="ielts_score"
                  value={formData.ielts_score || ''}
                  onChange={handleChange}
                  step="0.5"
                  min="0"
                  max="9"
                  placeholder="Optional"
                />
              </div>
              <div className="form-group">
                <label>Duolingo (10-160)</label>
                <input
                  type="number"
                  name="duolingo_score"
                  value={formData.duolingo_score || ''}
                  onChange={handleChange}
                  min="10"
                  max="160"
                  placeholder="Optional"
                />
              </div>
            </div>
          </div>
        )}

        {/* Section 4: Courses & Curriculum */}
        {currentSection === 4 && (
          <div className="form-section">
            <h2>Courses & Curriculum</h2>

            <div className="form-group">
              <label>Curriculum Difficulty *</label>
              <select name="curriculum_difficulty" value={formData.curriculum_difficulty} onChange={handleChange} required>
                <option value="low">Low - Regular courses</option>
                <option value="medium">Medium - Some honors/AP</option>
                <option value="high">High - Mostly honors/AP</option>
                <option value="very_high">Very High - Maximum rigor</option>
              </select>
            </div>

            <h3>AP Courses</h3>
            <div className="form-group">
              <label>Add AP Course</label>
              <div className="ap-input-row">
                <select
                  value={apInput.subject}
                  onChange={(e) => setApInput({ ...apInput, subject: e.target.value })}
                  className="ap-subject-select"
                >
                  {AP_SUBJECTS.map(subject => (
                    <option key={subject} value={subject}>{subject}</option>
                  ))}
                </select>
                <select
                  value={apInput.score}
                  onChange={(e) => setApInput({ ...apInput, score: parseInt(e.target.value) })}
                  className="ap-score-select"
                >
                  <option value="5">5</option>
                  <option value="4">4</option>
                  <option value="3">3</option>
                  <option value="2">2</option>
                  <option value="1">1</option>
                </select>
                <select
                  value={apInput.year_taken}
                  onChange={(e) => setApInput({ ...apInput, year_taken: e.target.value })}
                  className="ap-year-select"
                >
                  <option value="9th">9th</option>
                  <option value="10th">10th</option>
                  <option value="11th">11th</option>
                  <option value="12th">12th</option>
                </select>
                <button type="button" className="btn btn-secondary" onClick={addAPCourse}>
                  Add
                </button>
              </div>
              <div className="ap-list">
                {formData.ap_courses.map((ap, index) => (
                  <div key={index} className="ap-item">
                    <span>{ap.subject} - Score: {ap.score} ({ap.year_taken})</span>
                    <button type="button" className="btn btn-remove" onClick={() => removeAPCourse(index)}>
                      Remove
                    </button>
                  </div>
                ))}
              </div>
              <small>{formData.ap_courses.length} AP courses added</small>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Honors Courses</label>
                <input
                  type="number"
                  name="honors_courses"
                  value={formData.honors_courses}
                  onChange={handleChange}
                  min="0"
                />
              </div>
              <div className="form-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    name="ib_diploma"
                    checked={formData.ib_diploma}
                    onChange={handleChange}
                  />
                  IB Diploma Candidate
                </label>
              </div>
              {formData.ib_diploma && (
                <div className="form-group">
                  <label>IB Score (24-45)</label>
                  <input
                    type="number"
                    name="ib_score"
                    value={formData.ib_score || ''}
                    onChange={handleChange}
                    min="24"
                    max="45"
                  />
                </div>
              )}
            </div>
          </div>
        )}

        {/* Section 5: Activities & Experience */}
        {currentSection === 5 && (
          <div className="form-section">
            <h2>Activities & Experience</h2>

            <div className="form-group">
              <label>Research Experience</label>
              <textarea
                name="research_experience"
                value={formData.research_experience}
                onChange={handleChange}
                placeholder="Describe research projects, publications, lab work, independent studies..."
                rows="4"
              />
            </div>

            <h3>Extracurricular Activities</h3>
            <div className="form-group">
              <label>Add Activity</label>
              <div className="ec-input-grid">
                <input
                  type="text"
                  value={ecInput.activity_name}
                  onChange={(e) => setEcInput({ ...ecInput, activity_name: e.target.value })}
                  placeholder="Activity name"
                />
                <input
                  type="text"
                  value={ecInput.role}
                  onChange={(e) => setEcInput({ ...ecInput, role: e.target.value })}
                  placeholder="Your role"
                />
                <input
                  type="number"
                  value={ecInput.years_participated}
                  onChange={(e) => setEcInput({ ...ecInput, years_participated: parseFloat(e.target.value) })}
                  placeholder="Years"
                  min="0"
                  max="4"
                  step="0.5"
                />
                <input
                  type="number"
                  value={ecInput.hours_per_week}
                  onChange={(e) => setEcInput({ ...ecInput, hours_per_week: parseInt(e.target.value) })}
                  placeholder="Hours/week"
                  min="0"
                />
                <textarea
                  value={ecInput.description}
                  onChange={(e) => setEcInput({ ...ecInput, description: e.target.value })}
                  placeholder="Description"
                  rows="2"
                />
                <button type="button" className="btn btn-secondary" onClick={addExtracurricular}>
                  Add Activity
                </button>
              </div>
              <div className="ec-list">
                {formData.extracurriculars.map((ec, index) => (
                  <div key={index} className="ec-item">
                    <strong>{ec.activity_name}</strong> - {ec.role}
                    <br />
                    <small>{ec.years_participated} years, {ec.hours_per_week} hrs/week</small>
                    <br />
                    <small>{ec.description}</small>
                    <button type="button" className="btn btn-remove" onClick={() => removeExtracurricular(index)}>
                      Remove
                    </button>
                  </div>
                ))}
              </div>
            </div>

            <h3>Competitions & Awards</h3>
            <div className="form-group">
              <label>Add Competition/Award</label>
              <div className="comp-input-grid">
                <input
                  type="text"
                  value={compInput.name}
                  onChange={(e) => setCompInput({ ...compInput, name: e.target.value })}
                  placeholder="Competition name"
                />
                <select
                  value={compInput.level}
                  onChange={(e) => setCompInput({ ...compInput, level: e.target.value })}
                >
                  <option value="school">School</option>
                  <option value="regional">Regional</option>
                  <option value="state">State</option>
                  <option value="national">National</option>
                  <option value="international">International</option>
                </select>
                <input
                  type="text"
                  value={compInput.award}
                  onChange={(e) => setCompInput({ ...compInput, award: e.target.value })}
                  placeholder="Award/placement"
                />
                <input
                  type="text"
                  value={compInput.year}
                  onChange={(e) => setCompInput({ ...compInput, year: e.target.value })}
                  placeholder="Year"
                />
                <button type="button" className="btn btn-secondary" onClick={addCompetition}>
                  Add
                </button>
              </div>
              <div className="comp-list">
                {formData.competitions.map((comp, index) => (
                  <div key={index} className="comp-item">
                    <strong>{comp.name}</strong> ({comp.level}) - {comp.award} ({comp.year})
                    <button type="button" className="btn btn-remove" onClick={() => removeCompetition(index)}>
                      Remove
                    </button>
                  </div>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label>Work Experience (optional)</label>
              <textarea
                name="work_experience_text"
                value={formData.work_experience.join('\n')}
                onChange={(e) => setFormData(prev => ({
                  ...prev,
                  work_experience: e.target.value.split('\n').filter(line => line.trim())
                }))}
                placeholder="Describe any paid work, internships, or jobs (one per line)..."
                rows="3"
              />
            </div>

            <h3>Community Service</h3>
            <div className="form-row">
              <div className="form-group">
                <label>Community Service Hours *</label>
                <input
                  type="number"
                  name="community_service_hours"
                  value={formData.community_service_hours}
                  onChange={handleChange}
                  min="0"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label>Community Service Description *</label>
              <textarea
                name="community_service_description"
                value={formData.community_service_description}
                onChange={handleChange}
                placeholder="Describe your community service activities..."
                rows="3"
                required
              />
            </div>

            <div className="form-group">
              <label>Summer Activities</label>
              <textarea
                name="summer_activities_text"
                value={formData.summer_activities.join('\n')}
                onChange={(e) => setFormData(prev => ({
                  ...prev,
                  summer_activities: e.target.value.split('\n').filter(line => line.trim())
                }))}
                placeholder="Describe summer programs, camps, courses, travel (one per line)..."
                rows="3"
              />
            </div>
          </div>
        )}

        {/* Section 6: Application Materials */}
        {currentSection === 6 && (
          <div className="form-section">
            <h2>Application Materials</h2>

            <div className="form-row">
              <div className="form-group">
                <label>Letter of Recommendation Quality (1-5) *</label>
                <select name="lor_quality" value={formData.lor_quality} onChange={handleChange} required>
                  <option value="1">1 - Weak</option>
                  <option value="2">2 - Below Average</option>
                  <option value="3">3 - Average</option>
                  <option value="4">4 - Strong</option>
                  <option value="5">5 - Exceptional</option>
                </select>
              </div>
              <div className="form-group">
                <label>Essay Quality (1-5) *</label>
                <select name="essay_quality" value={formData.essay_quality} onChange={handleChange} required>
                  <option value="1">1 - Weak</option>
                  <option value="2">2 - Below Average</option>
                  <option value="3">3 - Average</option>
                  <option value="4">4 - Strong</option>
                  <option value="5">5 - Exceptional</option>
                </select>
              </div>
            </div>

            <h3>Demonstrated Interest</h3>
            <div className="form-row">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="campus_visit"
                  checked={formData.campus_visit}
                  onChange={handleChange}
                />
                Visited campus
              </label>
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="interview_completed"
                  checked={formData.interview_completed}
                  onChange={handleChange}
                />
                Completed interview
              </label>
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="contacted_admissions"
                  checked={formData.contacted_admissions}
                  onChange={handleChange}
                />
                Contacted admissions office
              </label>
            </div>

            <div className="form-group">
              <label>Info Sessions Attended</label>
              <input
                type="number"
                name="attended_info_sessions"
                value={formData.attended_info_sessions}
                onChange={handleChange}
                min="0"
              />
            </div>
          </div>
        )}

        {/* Navigation buttons */}
        <div className="form-navigation">
          {currentSection > 0 && (
            <button type="button" className="btn btn-secondary" onClick={prevSection}>
              Previous
            </button>
          )}
          {currentSection < sections.length - 1 ? (
            <button type="button" className="btn btn-primary" onClick={nextSection}>
              Next
            </button>
          ) : (
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Evaluating...' : 'Submit Application'}
            </button>
          )}
        </div>
      </form>
    </div>
  );
}

export default ApplicationFormEnhanced;
