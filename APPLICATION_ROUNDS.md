# Application Round Impact on Admissions

## Overview

Application round (ED/EA/REA/RD) **significantly affects admission chances**, often more than any other single factor except recruited athlete status.

## Application Round Types

### 1. **Early Decision (ED)** - BINDING
- **Binding commitment**: Must attend if accepted
- **Deadline**: Usually November 1 or November 15
- **Decision**: Mid-December
- **Can apply to**: Only ONE ED school
- **Acceptance rate boost**: **2-3x higher** than RD

**Schools offering ED:**
- Most private universities: Duke, Penn, Northwestern, Cornell, Dartmouth, Brown, Vanderbilt, etc.
- **NOT offered by**: Harvard, Stanford, MIT, Yale, Princeton, Caltech, all UCs

**Example:**
- Duke RD acceptance rate: 6%
- Duke ED acceptance rate: 18% (3x higher!)

### 2. **Early Decision I & II (ED1/ED2)** - BINDING
- **ED1**: November 1 deadline, December decision
- **ED2**: January 1 deadline, February decision
- **Purpose**: ED2 gives students rejected/deferred from ED1 elsewhere a second chance
- **Acceptance rate boost**: ED1 > ED2 > RD

**Schools offering both ED1 and ED2:**
- Vanderbilt, Emory, NYU, Tufts, Wesleyan, etc.

### 3. **Restrictive Early Action (REA) / Single-Choice Early Action (SCEA)** - NON-BINDING
- **Non-binding**: Can decline if accepted
- **Restriction**: Cannot apply EA/ED to other private schools (can apply to public schools)
- **Deadline**: November 1
- **Decision**: Mid-December
- **Acceptance rate boost**: **1.5-2x higher** than RD

**Schools offering REA/SCEA:**
- Harvard, Stanford, Yale, Princeton, Notre Dame

**Example:**
- Stanford RD acceptance rate: 3.5%
- Stanford REA acceptance rate: 7-8% (2x higher!)

### 4. **Early Action (EA)** - NON-BINDING
- **Non-binding**: Can decline if accepted
- **No restrictions**: Can apply EA to multiple schools
- **Deadline**: November 1
- **Decision**: Mid-December to January
- **Acceptance rate boost**: **1.2-1.5x higher** than RD

**Schools offering EA:**
- MIT, Caltech, UChicago, Georgetown, Boston College, etc.

### 5. **Regular Decision (RD)**
- **Deadline**: Usually January 1-15
- **Decision**: Late March to early April
- **Lowest acceptance rates**
- **Most competitive pool**

### 6. **Rolling Admission**
- **No fixed deadline**: Applications reviewed as received
- **Advantage**: Apply early = better chances (spots fill up)
- **Common at**: State universities, less selective schools

## Acceptance Rate Comparison by Round

| School | ED/REA Rate | RD Rate | Multiplier |
|--------|-------------|---------|------------|
| **Harvard (REA)** | 7.6% | 2.6% | 2.9x |
| **Stanford (REA)** | 7.7% | 2.6% | 3.0x |
| **Yale (REA)** | 10.5% | 3.7% | 2.8x |
| **Princeton (SCEA)** | 13.9% | 3.7% | 3.8x |
| **MIT (EA)** | 4.7% | 2.2% | 2.1x |
| **Penn (ED)** | 14.9% | 4.1% | 3.6x |
| **Duke (ED)** | 17.8% | 4.8% | 3.7x |
| **Northwestern (ED)** | 20.0% | 6.4% | 3.1x |
| **Cornell (ED)** | 19.7% | 7.3% | 2.7x |
| **Brown (ED)** | 13.0% | 3.9% | 3.3x |
| **Dartmouth (ED)** | 15.3% | 5.3% | 2.9x |
| **Vanderbilt (ED1)** | 17.2% | 5.3% | 3.2x |
| **Vanderbilt (ED2)** | 10.3% | 5.3% | 1.9x |
| **UC Berkeley (no ED)** | N/A | 11.3% | 1.0x |
| **UCLA (no ED)** | N/A | 8.6% | 1.0x |

## Why Early Admission Has Higher Acceptance Rates

### 1. **Demonstrated Interest**
- Shows school is your top choice
- Schools want students who will definitely attend (yield protection)

### 2. **Institutional Priorities**
- Fill 40-50% of class through ED/EA
- Lock in high-stats students early
- Secure full-pay students (ED applicants often don't compare financial aid)

### 3. **Less Competition**
- Smaller applicant pool
- Many strong students wait for RD

### 4. **Legacy & Athlete Advantage**
- Most legacies apply ED (where legacy boost is strongest)
- Most recruited athletes apply ED

### 5. **Self-Selection**
- ED applicants tend to be better prepared
- Weaker applicants often wait for RD

## Schools That DON'T Offer Early Decision

### Public Universities (Generally No ED)
- **All UCs**: Berkeley, UCLA, UCSD, UCI, UCSB, UCD, etc.
- **University of Michigan** (EA only)
- **UNC Chapel Hill** (EA only)
- **University of Virginia** (EA only)
- **Georgia Tech** (EA only)

### Top Private Schools Without ED
- **Harvard** (REA only)
- **Stanford** (REA only)
- **Yale** (REA only)
- **Princeton** (SCEA only)
- **MIT** (EA only)
- **Caltech** (EA only)

These schools use REA/EA instead to remain non-binding.

## How to Model Application Round Impact

### Probability Multipliers

```python
def calculate_application_round_boost(application_round, school_data, base_probability):
    """
    Apply multiplier based on application round
    """

    # Check if school offers this round
    if application_round not in school_data["available_rounds"]:
        return base_probability, f"{school_data['name']} does not offer {application_round}"

    # Get multiplier
    multipliers = {
        "ED": 3.0,      # Early Decision: 3x boost
        "ED1": 3.0,     # Early Decision I: 3x boost
        "ED2": 2.0,     # Early Decision II: 2x boost
        "REA": 2.5,     # Restrictive Early Action: 2.5x boost
        "SCEA": 2.5,    # Single-Choice Early Action: 2.5x boost
        "EA": 1.5,      # Early Action: 1.5x boost
        "RD": 1.0,      # Regular Decision: baseline
        "ROLLING": 1.2  # Rolling: slight boost if early
    }

    multiplier = multipliers.get(application_round, 1.0)

    # Apply multiplier
    boosted_probability = base_probability * multiplier

    # Cap at 95% (no guarantee)
    final_probability = min(boosted_probability, 0.95)

    return final_probability, f"{application_round} provides {multiplier}x boost"
```

### School-Specific Round Availability

```python
schools_data = {
    "Harvard University": {
        "available_rounds": ["REA", "RD"],
        "rea_acceptance_rate": 0.076,
        "rd_acceptance_rate": 0.026
    },
    "Stanford University": {
        "available_rounds": ["REA", "RD"],
        "rea_acceptance_rate": 0.077,
        "rd_acceptance_rate": 0.026
    },
    "MIT": {
        "available_rounds": ["EA", "RD"],
        "ea_acceptance_rate": 0.047,
        "rd_acceptance_rate": 0.022
    },
    "Penn": {
        "available_rounds": ["ED", "RD"],
        "ed_acceptance_rate": 0.149,
        "rd_acceptance_rate": 0.041
    },
    "UC Berkeley": {
        "available_rounds": ["RD"],  # No early admission
        "rd_acceptance_rate": 0.113
    },
    "Vanderbilt": {
        "available_rounds": ["ED1", "ED2", "RD"],
        "ed1_acceptance_rate": 0.172,
        "ed2_acceptance_rate": 0.103,
        "rd_acceptance_rate": 0.053
    }
}
```

## Updated Evaluation Logic

```python
def evaluate(self, applicant):
    # ... calculate base scores ...

    # Calculate base probability (without round consideration)
    base_probability = self._calculate_probability(total_score, school_data, applicant)
    # Example: 0.25 (25%)

    # Apply application round boost
    if applicant.application_round in school_data["available_rounds"]:
        if applicant.application_round == "ED" or applicant.application_round == "ED1":
            final_probability = base_probability * 3.0
            boost_explanation = "Early Decision provides 3x boost (binding commitment)"

        elif applicant.application_round == "ED2":
            final_probability = base_probability * 2.0
            boost_explanation = "Early Decision II provides 2x boost"

        elif applicant.application_round in ["REA", "SCEA"]:
            final_probability = base_probability * 2.5
            boost_explanation = "Restrictive Early Action provides 2.5x boost"

        elif applicant.application_round == "EA":
            final_probability = base_probability * 1.5
            boost_explanation = "Early Action provides 1.5x boost"

        elif applicant.application_round == "RD":
            final_probability = base_probability * 1.0
            boost_explanation = "Regular Decision (baseline, no boost)"

        # Cap at 95%
        final_probability = min(final_probability, 0.95)

    else:
        # School doesn't offer this round
        return {
            "error": f"{school_data['name']} does not offer {applicant.application_round}",
            "available_rounds": school_data["available_rounds"]
        }

    # Example: 0.25 * 3.0 = 0.75 (75% with ED boost!)

    return {
        "admission_probability": final_probability,
        "base_probability": base_probability,
        "application_round": applicant.application_round,
        "round_boost": boost_explanation,
        # ... rest of analysis ...
    }
```

## Important Considerations

### 1. **ED is Binding**
- Must withdraw all other applications if accepted
- Financial aid is final (can't compare offers)
- Only apply ED if school is definite #1 choice

### 2. **REA/SCEA Restrictions**
- Cannot apply EA/ED to other private schools
- Can apply to public schools' EA
- Can apply to other schools' RD

### 3. **Financial Aid Concerns**
- ED limits ability to compare financial aid offers
- If need-based aid is critical, consider EA/RD instead
- Can decline ED only if financial aid is insufficient

### 4. **Strategic Considerations**
- **Strong applicant**: Apply REA/EA to reach schools, save ED for slight reach
- **Competitive applicant**: Use ED strategically on realistic reach
- **Need financial aid**: Prefer EA/RD to compare offers

## Example Impact

**Applicant Profile:**
- GPA: 3.85, SAT: 1480, Strong ECs
- Base probability at Penn: 25%

**By Application Round:**
- **ED**: 25% × 3.0 = **75%** (Likely Admit)
- **RD**: 25% × 1.0 = **25%** (Reach)

**Same applicant, 3x better chance with ED!**

## Summary

Application round is **one of the most important factors** in admissions:

- **ED/ED1**: 3x boost (binding)
- **REA/SCEA**: 2.5x boost (non-binding, restricted)
- **ED2**: 2x boost (binding, second chance)
- **EA**: 1.5x boost (non-binding, unrestricted)
- **RD**: 1x (baseline, most competitive)

**Key takeaway**: For top schools, applying early can be the difference between acceptance and rejection.
