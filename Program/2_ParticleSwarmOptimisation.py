# Particle Swarm Optimization

import numpy as np

class TrafficIntersection:
    def __init__(self):

        self.arrival_rates = np.array([0.2, 0.15, 0.25, 0.1])

        self.saturation_rate = 0.5

        self.lost_time = 4.0

    def calculate_total_delay(self, green_times):

        total_cycle = np.sum(green_times) + (4 * self.lost_time)
        total_delay = 0.0

        for i in range(len(green_times)):
            g = green_times[i]
            r = total_cycle - g
            q = self.arrival_rates[i]
            s = self.saturation_rate


            if g <= 0 or (g * s) <= (total_cycle * q):

                total_delay += 10000.0
                continue


            delay = (total_cycle * (1 - g / total_cycle)**2) / (2 * (1 - q / s))

            total_delay += delay * q

        return total_delay


class TrafficPSO:
    def __init__(self, num_particles, max_iter, traffic_env):
        self.num_particles = num_particles
        self.max_iter = max_iter
        self.env = traffic_env
        self.dim = 4


        self.min_green = 10.0
        self.max_green = 60.0


        self.w = 0.7
        self.c1 = 1.5
        self.c2 = 1.5


        self.X = np.random.uniform(self.min_green, self.max_green, (num_particles, self.dim))
        self.V = np.random.uniform(-5, 5, (num_particles, self.dim))


        self.P_best = np.copy(self.X)
        self.P_best_scores = np.array([self.env.calculate_total_delay(p) for p in self.X])


        g_best_idx = np.argmin(self.P_best_scores)
        self.G_best = np.copy(self.P_best[g_best_idx])
        self.G_best_score = self.P_best_scores[g_best_idx]

    def optimize(self):
        for it in range(self.max_iter):
            for i in range(self.num_particles):

                r1 = np.random.rand(self.dim)
                r2 = np.random.rand(self.dim)


                self.V[i] = (self.w * self.V[i] +
                             self.c1 * r1 * (self.P_best[i] - self.X[i]) +
                             self.c2 * r2 * (self.G_best - self.X[i]))


                self.X[i] += self.V[i]


                self.X[i] = np.clip(self.X[i], self.min_green, self.max_green)


                current_score = self.env.calculate_total_delay(self.X[i])


                if current_score < self.P_best_scores[i]:
                    self.P_best_scores[i] = current_score
                    self.P_best[i] = np.copy(self.X[i])

                    if current_score < self.G_best_score:
                        self.G_best_score = current_score
                        self.G_best = np.copy(self.X[i])


            if (it + 1) % 10 == 0 or it == 0:
                print(f"Iteration {it+1}/{self.max_iter} -> Current Best Penalty (Delay Value): {self.G_best_score:.4f}")

        return self.G_best, self.G_best_score

if __name__ == "__main__":

    intersection = TrafficIntersection()


    pso_solver = TrafficPSO(num_particles=30, max_iter=50, traffic_env=intersection)
    best_timings, min_delay = pso_solver.optimize()


    print("\n" + "="*40)
    print("OPTIMIZED TRAFFIC MANAGEMENT RESULTS")
    print("="*40)
    for phase, sec in enumerate(best_timings, 1):
        print(f"Phase {phase} (Green Light Duration): {sec:.2f} seconds")
    print(f"Total Intersection Cycle Time: {np.sum(best_timings) + (4 * intersection.lost_time):.2f} seconds")
    print(f"Optimized System Delay Metric: {min_delay:.4f}")
    print("="*40)