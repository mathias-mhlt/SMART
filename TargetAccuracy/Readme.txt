# Dataset Validation Criteria Documentation

**Author:** Ahmed Ayachi  
**Date:** _Generated on: {{TODAY}}_

---

## 📘 Introduction

This document formalizes the data validation criteria implemented in the automated quality checking system. The framework detects four main types of data issues:

- Rare categorical values  
- Pattern mismatches and typos  
- Numerical outliers  
- Feature relationship anomalies  

---

## ✅ Validation Criteria

### 1. Rare Categorical Values

- **Purpose:** Identify infrequently occurring categorical values  
- **Methodology:**  
  A value is considered rare if:

