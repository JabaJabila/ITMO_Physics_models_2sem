'''
Made by Andreev Artem Ruslanovich group# M3114
'''

import matplotlib.pyplot as plt
from math import sqrt, sin, cos, atan, log
import pygame
pygame.init()

# Initial data (variant#3)
r = 2
R = 5
V_0 = 8e6
L = 13

# Constants for electron
m = 9.1e-31
q = 1.6e-19

# Tranlate to SI
r /= 100
R /= 100
L /= 100


n = 100

# Flight calculations
def estimate(L, V_0, R, r, q, m, U):
	dt = L / V_0 / n
	T = [0]
	V_y = [0]
	a_y = [0]
	x = [0]
	y = [(R - r) / 2]
	i = 0
	crash = False
	while (not (x[i] >= L) and not (y[i] <= 0)):
		i += 1
		a_y.append((U * q) / (log(R / r) * (r + y[i - 1]) * m))
		V_y.append(V_y[i - 1] + a_y[i] * dt)
		T.append(T[i - 1] + dt)
		x.append(x[i - 1] + V_0 * dt)
		y.append(y[i - 1] - V_y[i] * dt - (a_y[i] * (dt ** 2)) / 2)
		if (y[i] <= 0):
			crash = True

	V_end = sqrt(V_0 ** 2 + V_y[len(V_y) - 1] ** 2)
	return T, a_y, x, V_y, y, V_end, crash

# Search for minimum voltage
min = 0
max = 1000
while ((max - min) > 0.0011):
	mid = min + (max - min) / 2
	mid = round(mid, 3)
	T, a_y, x, V_y, y, V_end, crash = estimate(L, V_0, R, r, q, m, mid)
	if crash:
		max = mid
	else:
		min = mid

U_min = max
U = U_min

T, a_y, x, V_y, y, V_end, crash = estimate(L, V_0, R, r, q, m, U)
t = T[len(T) - 1]

# Plotting
def build_plots(x, y, T, V_y, a_y):

	plots = [["График y(x)", x, y, "x, м", "y, м"], 
	         ["График V_y(t)", T, V_y, "t, c", "V_y, м/с"], 
	         ["График a_y(t)", T[1:], a_y[1:], "t, c", "a, м/с^2"], 
	         ["График y(t)", T, y, "t, c", "y, м"]]

	fig, ax = plt.subplots(2, 2, figsize=(15, 10))
	axs = [ax[i, j] for i in range(2) for j in range(2)]
	plt.subplots_adjust(hspace=0.3)

	for i in range(4):
	    axs[i].grid(True)
	    axs[i].set_xlabel(plots[i][3])
	    axs[i].set_ylabel(plots[i][4])
	    axs[i].set_xlim([plots[i][1][0], plots[i][1][len(plots[i][1]) - 1]])
	    axs[i].set_title(plots[i][0])
	    axs[i].plot(plots[i][1], plots[i][2], color='red')

	plt.show()

# Window configuration
win = pygame.display.set_mode([1500, 900])
pygame.display.set_caption('Моделирование №2')
clock = pygame.time.Clock()
fps = 60
pygame.display.flip()

pygame.draw.line(win, (255, 255, 255), (100, 100), (1400, 100), 3)
pygame.draw.line(win, (255, 255, 255), (100, 400), (1400, 400), 3)

font1 = pygame.font.SysFont('serif', 32)
font2 = pygame.font.SysFont('serif', 28)
text11 = font1.render(("Минимальная разность потенциалов, при которой электрон не успеет вылететь"), 1, (255, 255, 255)) 
text12 = font1.render(("из конденсатора = " + str(U_min) + " В"), 1, (255, 255, 255))
text2 = font1.render(("Текущая разность потенциалов = " + str(U) + " В"), 1, (255, 255, 255))
text3 = font1.render(("Время полёта = " + str(t) + " с"), 1, (255, 255, 255))
text4 = font1.render(("Конечная скорость = " + str(round(V_end, 3)) + " м/с"), 1, (255, 255, 255))
text5 = font2.render("Запустить электрон", 2, (0, 0, 0))
text6 = font2.render("Посторить графики", 2, (0, 0, 0))
text7 = font1.render("Задать разность потенциалов:", 1, (255, 255, 255))

button1 = pygame.Rect(1100, 600, 300, 80)
button2 = pygame.Rect(1100, 720, 300, 80)
input_box = pygame.Rect(100, 770, 400, 50)
pygame.draw.rect(win, (255, 255, 255), button1)
pygame.draw.rect(win, (255, 255, 255), button2)
pygame.draw.rect(win, (255, 255, 255), input_box)

win.blit(text11, (100, 430))
win.blit(text12, (100, 470))
win.blit(text2, (100, 550))
win.blit(text3, (100, 610))
win.blit(text4, (100, 670))
win.blit(text5, (1132, 622))
win.blit(text6, (1132, 742))
win.blit(text7, (100, 730))
text = ""

# Flight vizalization
def flying(x, y, crash):
	flag = True
	for i in range(8): # Pre- phase
		pygame.draw.circle(win, (0, 255, 0), (-4 + i * 13, 250), 7)
		pygame.display.update()
		clock.tick(fps)
		pygame.draw.circle(win, (0, 0, 0), (-4 + i * 13, 250), 7)

	for i in range(len(y)):
		
		if (i == len(y) - 1 and crash):
			for j in range(7, 12): # If crashes
				flag = False
				pygame.draw.circle(win, (255, 0, 0), (100 + int(x[i] * 10000), 400 - int(y[i] * 10000)), j)
				pygame.display.update()
				clock.tick(fps // 4)
			pygame.draw.circle(win, (0, 0, 0), (100 + int(x[i] * 10000), 400 - int(y[i] * 10000)), 11)
		else:
			pygame.draw.circle(win, (0, 255, 0), (100 + int(x[i] * 10000), 400 - int(y[i] * 10000)), 7)
			pygame.display.update()
			clock.tick(fps)
			pygame.draw.circle(win, (0, 0, 0), (100 + int(x[i] * 10000), 400 - int(y[i] * 10000)), 7)

		pygame.draw.line(win, (255, 255, 255), (100, 100), (1400, 100), 3)
		pygame.draw.line(win, (255, 255, 255), (100, 400), (1400, 400), 3)

	if flag: # If flights through
		for i in range(10):
			pygame.draw.line(win, (255, 255, 255), (100, 100), (1400, 100), 3)
			pygame.draw.line(win, (255, 255, 255), (100, 400), (1400, 400), 3)
			pygame.draw.circle(win, (0, 255, 0), (int((100 + (x[len(x) - 1] * 10000) + cos(atan(V_y[len(V_y) - 1]/V_0))*(i + 1) * 13)), int((400 - (y[len(y) - 1] * 10000)
							   + sin(atan(V_y[len(V_y) - 1]/V_0))*(i + 1) * 13))), 7)
			pygame.display.update()
			clock.tick(fps)
			pygame.draw.circle(win, (0, 0, 0), (int((100 + (x[len(x) - 1] * 10000) + cos(atan(V_y[len(V_y) - 1]/V_0))*(i + 1) * 13)), int((400 - int(y[len(y) - 1] * 10000)
							   + sin(atan(V_y[len(V_y) - 1]/V_0))*(i + 1) * 13))), 8)


while True: # Infinite loop

	input_box = pygame.Rect(100, 770, 400, 50)
	pygame.draw.rect(win, (255, 255, 255), button1)
	pygame.draw.rect(win, (255, 255, 255), button2)

	win.blit(text5, (1132, 622))
	win.blit(text6, (1132, 742))

	clock.tick(fps)
	pygame.display.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

		if event.type == pygame.MOUSEBUTTONDOWN: # if "Запустить электрон" pressed
				if button1.collidepoint(event.pos):
					pygame.draw.rect(win, (170, 170, 170), button1)
					win.blit(text5, (1132, 622))
					pygame.draw.rect(win, (170, 170, 170), button2)
					win.blit(text6, (1132, 742))
					flying(x, y, crash)

				if button2.collidepoint(event.pos): # if "Построить графики" pressed
					pygame.draw.rect(win, (170, 170, 170), button2)
					win.blit(text6, (1132, 742))
					pygame.draw.rect(win, (170, 170, 170), button1)
					win.blit(text5, (1132, 622))
					clock.tick(fps)
					pygame.display.update()

					clock.tick(fps)
					pygame.display.update()
					build_plots(x, y, T, V_y, a_y)

		if event.type == pygame.KEYDOWN: # textfield
			if event.key == pygame.K_RETURN:
				pygame.draw.rect(win, (255, 255, 255), input_box)
				try:
					text = float(text)
					if (text >= 0 and text <= 1000):
						U = round(text, 3)
						T, a_y, x, V_y, y, V_end, crash = estimate(L, V_0, R, r, q, m, U)
						text2 = font1.render(("Текущая разность потенциалов = " + str(U) + " В"), 1, (255, 255, 255))
						text3 = font1.render(("Время полёта = " + str(T[len(T) - 1]) + " с"), 1, (255, 255, 255))
						text4 = font1.render(("Конечная скорость = " + str(round(V_end, 3)) + " м/с"), 1, (255, 255, 255))
						pygame.draw.rect(win, (0, 0, 0), (100, 550, 600, 40))
						pygame.draw.rect(win, (0, 0, 0), (100, 610, 600, 40))
						pygame.draw.rect(win, (0, 0, 0), (100, 670, 600, 40))
						win.blit(text2, (100, 550))
						win.blit(text3, (100, 610))
						win.blit(text4, (100, 670))
						clock.tick(fps)
						pygame.display.update()
					text = ""
				except:
					text = ""

			elif event.key == pygame.K_BACKSPACE:
				pygame.draw.rect(win, (255, 255, 255), input_box)
				text = text[:-1]
			else:
				text += event.unicode

			txt_surface = font2.render(text, True, (0, 0, 0))
			win.blit(txt_surface, (input_box.x+5, input_box.y+8))

		pygame.event.clear()