from math import asin, sin, cos, sqrt, degrees, atan, radians
import pygame

pygame.init()
pygame.display.init()

R_moon = 1738000
M_moon = 7.36e22
M_cargo = 200
M_ship = 2000
M_fuel = 4000
V_fuel = 3660
a_max = 29.43
G = 6.67430e-11
X_sh = 0
Y_sh = R_moon

X_0st = -64000
H_st = 42000
flag = False

class Orbital_Station():
    def __init__(self):
        self.x = X_0st
        self.h = R_moon + H_st
        self.phi = asin(self.x / self.h)
        self.y = self.h * cos(self.phi)
        self.speed = sqrt(G * M_moon / self.h)
        self.vx = self.speed * cos(self.phi)
        self.vy = -1 * self.speed * sin(self.phi)
        self.w = self.speed / self.h

    def fly(self, time):
        self.phi += self.w * time
        self.x = self.h * sin(self.phi)
        self.y = self.h * cos(self.phi)
        self.vx = self.speed * cos(self.phi)
        self.vy = -1 * self.speed * sin(self.phi)


class Rocket():
    def __init__(self):
        self.x = X_sh
        self.y = Y_sh
        self.max_a = a_max
        self.m = M_ship + M_fuel + M_cargo
        self.m_fuel = M_fuel
        self.V_fuel = V_fuel
        self.V_x = 0
        self.V_y = 0
        self.phi = 0
        self.alpha = 0
        self.a_x = 0
        self.a_y = 0
        self.g = G * M_moon / (R_moon ** 2)

    def fly(self, alpha, d_m, time):
        self.alpha = radians(alpha)
        global flag
        for i in range(int(time * 10)):
            if (self.m_fuel <= 0):
                if (not flag):
                    print("out of fuel!!!")
                    flag = True
                d_m = 0
            self.phi = atan(self.x / self.y)
            self.g = G * M_moon / (self.x ** 2 + self.y ** 2)
            self.m_fuel -= (d_m / 10)
            self.m -= (d_m / 10)
            self.a_y = (d_m * self.V_fuel * cos(self.alpha) - self.m * self.g * cos(self.phi)) / (self.m)
            self.a_x = (d_m * self.V_fuel * sin(self.alpha) - self.m * self.g * sin(self.phi)) / (self.m)
            if (sqrt(self.a_y ** 2 + self.a_x ** 2) >= a_max):
                print("overload!!!")
                # return False
            self.V_y += self.a_y * 0.1
            self.V_x += self.a_x * 0.1
            self.y += self.V_y * 0.1 + self.a_y * (0.1 ** 2) / 2
            self.x += self.V_x * 0.1 + self.a_x * (0.1 ** 2) / 2
            if (self.y ** 2 + self.x ** 2 <= R_moon ** 2):
                self.a_y = 0
                self.V_y = 0
                print("crash!!!")
                return False
        return True

    def autopilot(self, time, o_st):
        self.alpha = atan((o_st.x - self.x) / (o_st.y - self.y))
        if (o_st.y - self.y) > 0:
            self.alpha = atan((o_st.x - self.x) / (o_st.y - self.y))
        elif (o_st.x - self.x) > 0:
            if (o_st.x - self.x) == 0:
                self.alpha = radians(90)
            else:
                self.alpha = radians(90) + atan((self.y - o_st.y) / (o_st.x - self.x))
        else:
            if (self.x - rocket.x) == 0:
                self.alpha = radians(-90)
            else:
                self.alpha = radians(-90) - atan((self.y - o_st.y) / (self.x - rocket.x))

        d = sqrt((rocket.x - o_st.x) ** 2 + (rocket.y - o_st.y) ** 2)
        self.fly(time, d / 3000)            


if __name__ == "__main__":
    win = pygame.display.set_mode([1600, 500])
    pygame.display.set_caption('Моделирование №1')
    clock = pygame.time.Clock()
    fps = 60
    o_st = Orbital_Station()
    rocket = Rocket()
    pygame.draw.circle(win, (255, 255, 255), (300, 6485), 6185)
    pygame.draw.rect(win, (0, 255, 0), pygame.Rect(297, 298, 6, 4), 3)
    pygame.draw.rect(win, (0, 255, 0), pygame.Rect(297, 298, 6, 4), 3)
            
    pygame.draw.circle(win, (255, 255, 0), (300 + int(o_st.x) // 281, (6485 - int(o_st.y) // 281)), 3)
    pygame.draw.circle(win, (255, 0, 0), (300 + int(rocket.x) // 281, (6485 - int(rocket.y) // 281)), 3)
    time = 0

    while (True):
        pygame.draw.circle(win, (255, 255, 0), (300 + int(o_st.x) // 281, (6485 - int(o_st.y) // 281)), 3)
        pygame.draw.circle(win, (255, 0, 0), (300 + int(rocket.x) // 281, (6485 - int(rocket.y) // 281)), 3)
        clock.tick(fps)
        pygame.display.update()
        print("V_x = " + str(round(rocket.V_x, 1)) + " м/с\tV_y = " + str(round(rocket.V_y, 1)) + 
              " м/с\tx = " + str(round(rocket.x, 1)) + " м\ty = " + str(round(rocket.y, 1)) + " м")
        command = input()       # angle[degrees], fuel consumption per second[kilograms], time[seconds] 
        command = list(map(int, command.split()))
        time = command[2]

        while(time > 0):

            pygame.draw.circle(win, (255, 255, 0), (300 + int(o_st.x) // 281, (6485 - int(o_st.y) // 281)), 3)
            pygame.draw.circle(win, (255, 0, 0), (300 + int(rocket.x) // 281, (6485 - int(rocket.y) // 281)), 3)

            clock.tick(fps)
            pygame.display.update()

            pygame.draw.circle(win, (0, 0, 0), (300 + int(o_st.x) // 281, (6485 - int(o_st.y) // 281)), 3)
            pygame.draw.circle(win, (0, 0, 0), (300 + int(rocket.x) // 281, (6485 - int(rocket.y) // 281)), 3)

            pygame.draw.circle(win, (255, 255, 255), (300, 6485), 6185)
            pygame.draw.rect(win, (0, 255, 0), pygame.Rect(297, 298, 6, 4), 3)

            o_st.fly(0.1)
            rocket.fly(command[0], command[1], 0.1)
            if (sqrt((rocket.x - o_st.x) ** 2 + (rocket.y - o_st.y) ** 2) <= 50 and abs(rocket.V_x - o_st.V_x) + abs(rocket.V_y - o_st.V_y) <= 0.1):
                print("Успешная состыковка!")
                rocket.m -= M_cargo
            time -= 0.1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()