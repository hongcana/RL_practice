import numpy as np
import matplotlib.pyplot as plt

# inplace 방식 구현

threshold = 0.0001
gamma = 0.9
p_left = 0.5
V = {"L1": 0.0, "L2":0.0}
trace_V = [list(V.values())]
cnt = 0

while True:

    t = p_left * (-1 + gamma * V['L1']) + (1-p_left) * (1 + gamma * V['L2'])
    delta = abs(t - V['L1'])
    V['L1'] = t # 갱신됨

    t = p_left * (0 + gamma * V['L1']) + (1-p_left) * (-1 + gamma * V['L2'])

    delta = max(delta, abs(t - V['L2']))
    V['L2'] = t

    cnt += 1

    trace_V.append(list(V.values()))
    print(['V_'+str(cnt)+'('+state+')='+str(np.round(value, 3)) for state, value in V.items()])

    if delta < threshold:
        break

trace_V = np.array(trace_V).T

v1 = -2.25
v2 = -2.75

plt.figure(figsize=(8, 6))
plt.plot(trace_V[0], color='blue', label='$V_k(L1)$')
plt.plot(trace_V[1], color='orange', label='$V_k(L2)$')
plt.hlines(y=v1, xmin=0, xmax=cnt, color='blue', linestyle=':', label='$v_{\pi}(L1)$')
plt.hlines(y=v2, xmin=0, xmax=cnt, color='orange', linestyle=':', label='$v_{\pi}(L2)$')
plt.xlabel('iteration (k)')
plt.ylabel('state-value')
plt.suptitle('Iterative Policy Evaluation', fontsize=20)
plt.title('$\gamma='+str(gamma) + ', \pi='+str([p_left, 1-p_left])+'$', loc='left')
plt.grid()
plt.legend()
plt.show()


