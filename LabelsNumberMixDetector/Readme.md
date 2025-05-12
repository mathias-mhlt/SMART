# Heart Disease Data Analysis

This dataset contains information on patients and their likelihood of heart disease. The dataset includes the following columns:

| Column         | Description                              |
|----------------|------------------------------------------|
| **Age**        | Age of the patient                       |
| **Sex**        | Sex of the patient (M: Male, F: Female)  |
| **ChestPainType** | Type of chest pain (ATA, NAP, ASY)      |
| **RestingBP**  | Resting blood pressure                   |
| **Cholesterol**| Serum cholesterol level                  |
| **FastingBS**  | Fasting blood sugar (0 = normal, 1 = above normal) |
| **RestingECG** | Resting electrocardiogram results        |
| **MaxHR**      | Maximum heart rate achieved              |
| **ExerciseAngina** | Exercise-induced angina (Y: Yes, N: No) |
| **Oldpeak**    | Depression induced by exercise           |
| **ST_Slope**   | Slope of the peak exercise ST segment    |
| **HeartDisease** | Presence of heart disease (1: Yes, 0: No) |

## Sample Data:

| Age | Sex | ChestPainType | RestingBP | Cholesterol | FastingBS | RestingECG | MaxHR | ExerciseAngina | Oldpeak | ST_Slope | HeartDisease |
|-----|-----|---------------|-----------|-------------|-----------|------------|-------|----------------|---------|----------|--------------|
| 49  | F   | NAP           | 160       | 180         | 0         | Normal     | 156   | N              | 1       | Flat     | 1            |
| 37  | M   | ATA           | 130       | 283         | 0         | ST         | 98    | N              | 0       | Up       | 0            |
| 48  | F   | ASY           | 138       | 214         | 0         | Normal     | 108   | Y              | 1.5     | Flat     | 1            |
| 54  | M   | NAP           | 150       | 195         | 0         | Normal     | 122   | N              | 0       | Up       | 0            |
| 39  | M   | NAP           | 120       | 339         | 0         | Normal     | 170   | N              | 0       | Up       | 0            |
| 45  | F   | ATA           | 130       | 237         | 0         | Normal     | 170   | N              | 0       | Up       | 0            |
| 54  | M   | ATA           | 110       | 208         | 0         | Normal     | 142   | N              | 0       | Up       | 0            |
| 37  | M   | ASY           | 140       | 207         | 0         | Normal     | 130   | Y              | 1.5     | Flat     | 1            |

## Analysis Result:

- **Column 'Age'** has 20.00% wrongly attributed.
- **Result**: 1 (This is because the value is still within the acceptable range of the age interval).
- **Note**: The value is considered 1 if it falls within the "ok" interval (else it would be 0).
