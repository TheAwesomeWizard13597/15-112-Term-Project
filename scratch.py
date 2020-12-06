# 1. Assign these values from your Autolab gradebook:
hwAvg      = 97.8
collabAvg  = 100
quizAvg    = 91.3
midtermAvg = 91.2

# 2. Then pick these values based on your expected grades:
final = midtermAvg         # the default if you do not opt-in to take the final
tp = 75                    # your tp3 grade.  You can try different values...
passedParticipation = True # Set this to False if needed

# 3. Then run this to see your standard (non-AMG) grade computation:
divisor = 0.9 if passedParticipation else 1.0
grade = (0.10*quizAvg +
         0.15*hwAvg +
         0.20*collabAvg +
         0.15*midtermAvg +
         0.20*tp +
         0.10*final) / divisor

print(f'Standard (non-AMG) grade: {round(grade, 1)}')

if (grade < 70):
    print('Please recompute using the AMG grade computation.')
    print('See syllabus for details.')