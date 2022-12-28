import os, sys
import time, random


distribution = {
    'U': {
        'fileName': 'Uniform',
        'generator': (lambda m,v: (random.random() - 0.5) * v + m)
    },
    'G': {
        'fileName': 'Gaussian',
        'generator': (lambda m,v: random.gauss(m, v))
    },
}

try:
    numPoints, distType, xData, yData = sys.argv[1:]
    
    numPoints = int(numPoints)
    assert(distType in ['U', 'G'])

    xm, xw = map(float, xData.split(','))
    ym, yw = map(float, yData.split(','))

except:
    print("Invalid parameters passed !")
    exit()


timestamp = str(time.time())
points = [(str(distribution[distType]['generator'](xm, xw)), str(distribution[distType]['generator'](ym, yw))) for i in range(numPoints)]

with open(f"Input/{distribution[distType]['fileName']}_{timestamp}.txt", 'w') as F:
    for p in points:
        F.write(','.join(p) + '\n')
