import matplotlib.pyplot as plt

distances = [1, 2, 3, 4, 5]
accuracy = [100, 100, 75, 50, 25]

plt.plot(distances, accuracy, marker='o')
plt.title('Taxa de Acerto x Distância')
plt.xlabel('Distância (m)')
plt.ylabel('Taxa de Acerto (%)')
plt.xticks(distances)
plt.ylim(0, 110)
plt.grid()
plt.show()