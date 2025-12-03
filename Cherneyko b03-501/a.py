import jetFunctions as j
import spidev
import matplotlib.pyplot as plt
import time as t

j.initSpiAdc()
j.initStepMotorGpio()

try:
    samples = []

    for i in range(220):
        temp = []
        for i in range(4):
            temp.append(j.getAdc())
            t.sleep(0.1)
        samples.append(sum(temp)/len(temp))
        j.stepForward(4)

    j.stepBackward(880)
    
    # plt.plot(samples)
    # plt.show()
    # print(samples)
    with open('text.txt', 'w', encoding='utf-8') as file:
        for i in samples:
            file.write(str(i) +'\n')
finally:
    j.deinitSpiAdc()
    j.deinitStepMotorGpio()