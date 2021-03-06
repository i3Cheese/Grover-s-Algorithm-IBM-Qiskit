#!/usr/bin/env python
# coding: utf-8

# # Алгоритм Гровера

# Сегодня мы рассмотрим алгоритм Гровера и то, как его можно использовать для решения задач неструктурированного поиска. Затем мы реализуем квантовый алгоритм с помощью Qiskit и запустим его на квантовом симуляторе и реальном устройстве. 
# 

# ## 1. Введение <a id='introduction'></a>
# 
# Вы, наверное, слышали, что одним из многих преимуществ квантового компьютера над классическим компьютером является его превосходство в скорости поиска в неупорядоченных базах данных. Алгоритм Гровера демонстрирует эту возможность. Этот алгоритм может квадратично ускорить задачу неструктурированного поиска, но его использование выходит за рамки этого; он может служить общим приемом или подпрограммой для получения квадратичных улучшений времени выполнения для множества других алгоритмов. Это называется трюком с усилением амплитуды.

# ### Неструктурированный/неупорядоченный поиск
# 
# Предположим, вам дан большой список из $N$ элементов. Среди этих элементов есть всего один элемент с уникальным свойством, которое мы и хотим найти; назовем его победителем $w$. Давайте для визуализации и простоты мы будем думайть о каждом элементе в списке как о прямоугольнике определенного цвета. Скажем, все элементы в списке серые, кроме победителя $w$, который окрашен в фиолетовый цвет.
# 
# ![image1](images/grover_list.png)
# 
# Чтобы найти фиолетовый прямоугольник - *отмеченный элемент* - с помощью классических методов вычислений, нужно будет проверить в среднем $N/2$ этих полей, а в худшем случае - все $N$ из них. Однако на квантовом компьютере мы можем найти отмеченный элемент примерно за $\sqrt{N}$ шагов с помощью алгоритма Гровера с "усилением амплитуды". Квадратичное ускорение действительно существенно экономит время при поиске отмеченных элементов в длинных списках. Кроме того, алгоритм не использует внутреннюю структуру списка, что делает его *универсальным,* поэтому он сразу обеспечивает квадратичное квантовое ускорение для многих классических задач.

# ### Создание оракула
# 
# Для примера примем, что наша «база данных» состоит из всех возможных вычислительных базисных состояний, в которых могут находиться наши кубиты. Например, если у нас есть 3 кубита, наш список - это состояния $|000\rangle, |001\rangle, \dots |111\rangle$ (т.е. состояния $|0\rangle \rightarrow |7\rangle$).
# 
# Алгоритм Гровера находит оракулы, которые добавляют отрицательную фазу к состояниям решения. Т.е. для любого состояния $|x\rangle$ в вычислительном базисе: 
# 
# $$
# U_\omega|x\rangle = \bigg\{
# \begin{aligned}
# \phantom{-}|x\rangle \quad \text{if} \; x \neq \omega \\
# -|x\rangle \quad \text{if} \; x = \omega \\
# \end{aligned}
# $$
# 
# Такой оракул будет диагональной матрицей, где запись, соответствующая отмеченному элементу, будет иметь отрицательную фазу. Например, если у нас есть три кубита и $\omega =\text{101}$, у нашего оракула будет матрица следующего вида:
# 
# $$
# U_\omega = 
# \begin{bmatrix}
# 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
# 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\
# 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\
# 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\
# 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\
# 0 & 0 & 0 & 0 & 0 & -1 & 0 & 0 \\
# 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\
# 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 \\
# \end{bmatrix}
# \begin{aligned}
# \\
# \\
# \\
# \\
# \\
# \\
# \leftarrow \omega = \text{101}\\
# \\
# \\
# \\
# \end{aligned}
# $$
# 
# 
# Что делает алгоритм Гровера настолько мощным, так это то, насколько легко преобразовать задачу в оракул такой формы. Есть много вычислительных задач, для которых трудно найти решение, но относительно легко проверить решение. 

# ### Амплитудное усиление
# 
# Итак, как же работает алгоритм? Прежде чем посмотреть на список элементов, мы понятия не имеем, где находится наш отмеченный элемент. Следовательно, любое предположение о его местонахождении ничуть не хуже любого другого, которое может быть выражено в терминах суперпозиции: $|s \rangle = \frac{1}{\sqrt{N}} \sum_{x = 0}^{N -1} | x\rangle.$
# 
# Если бы в этот момент мы должны были измерить в стандартном базисе $\{|x\rangle \} $, то эта суперпозиция сколлапсирует, согласно квантовому закону, в любое из базисных состояний с той же вероятностью $\frac{1}{N}=\frac{1}{2^n}$. Следовательно, наши шансы угадать правильное значение $w$, равны $1$ в $ 2 ^ n $, как и следовало ожидать. Следовательно, в среднем нам нужно будет сделать приблизительно $N/2 = 2^{n-1}$ попыток, чтобы угадать правильный элемент.
# 
# Начнем процедуру, называемую усилением амплитуды, с помощью которой квантовый компьютер значительно увеличивает эту вероятность. Нам потребуется всего 3 довольно простых шага. Эта процедура расширяет (усиливает) амплитуду отмеченного элемента, что уменьшает амплитуду других элементов, так что измерение конечного состояния даст нам (вернет) правильный элемент с высокой достоверностью.
# 
# Этот алгоритм имеет красивую геометрическую интерпретацию в терминах двух отражений, которые генерируют вращение в двухмерной плоскости. Нам нужно учитывать только два особых состояния: победитель $|w\rangle$ и равномерная суперпозиция $|s\rangle$. Эти два вектора покрывают двумерную плоскость в векторном пространстве $\mathbb{C}^ N.$ Они не перпендикулярны, потому что $|w\rangle$ также встречается в суперпозиции с амплитудой $N^{-1/2}$.
# Однако мы можем ввести дополнительное состояние $|s'\rangle$, которое находится в промежутке этих двух векторов, перпендикулярном $|w\rangle $ и получается из $|s\rangle$ удалением $|w\rangle$ и масштабированием.
# 
# 
# **Шаг 1**: Процедура усиления амплитуды начинается с суперпозиции $| s \rangle$, которая легко получается из $| s \rangle = H^{\otimes n} | 0 \rangle^n$.
# 
# ![image2](images/grover_step1.jpg)
# 
# Левый рисунок соответствует двумерной плоскости, натянутой на перпендикулярные векторы $|w\rangle$ and $|s'\rangle$, что позволяет выразить начальное состояние как $|s\rangle = \sin \theta | w \rangle + \cos \theta | s' \rangle,$, где $\theta = \arcsin \langle s | w \rangle = \arcsin \frac{1}{\sqrt{N}}$. Правый график представляет собой гистограмму амплитуд состояния $| s \rangle$.
# 
# **Шаг 2**: Применим отражение оракула $U_f$ к состоянию $|s\rangle$.
# 
# ![image3](images/grover_step2.jpg)
# 
# Геометрически это соответствует отражению состояния $|s\rangle$ относительно $|s'\rangle$. Это преобразование означает, что амплитуда перед состоянием $|w\rangle$ становится отрицательной, что, в свою очередь, означает, что средняя амплитуда (обозначенная пунктирной линией) была понижена.
# 
# **Шаг 3**: Теперь мы применим дополнительное отражение ($U_s$) относительно состояния $|s\rangle$: $U_s = 2|s\rangle\langle s| - \mathbb{1}$. Это преобразование отображает состояние в $U_s U_f| s \rangle$ и завершает преобразование.
# 
# ![image4](images/grover_step3.jpg)
# 
# Два отражения всегда соответствуют вращению. Преобразование $U_s U_f$ поворачивает начальное состояние $|s\rangle$ ближе к победителю $|w\rangle$. Действие отражения $U_s$ на гистограмме амплитуды можно понимать как отражение около средней амплитуды. Поскольку средняя амплитуда была понижена первым отражением, это преобразование увеличивает отрицательную амплитуду $|w\rangle$ примерно в три раза по сравнению с исходным значением, в то время как остальные амплитуды уменьшаются. Затем мы переходим к **Шагу 2**, чтобы повторить отражением. Эта процедура будет повторяться несколько раз, чтобы определить победителя.
# 
# После $ t $ шагов мы окажемся в состоянии $|\psi_t\rangle$ where: $| \psi_t \rangle = (U_s U_f)^t  | s \rangle.$
# 
# Сколько раз нам нужно применить вращение? Оказывается, достаточно примерно $\sqrt{N}$ вращений. Это становится ясно, если посмотреть на амплитуды состояния $| \psi \rangle$. Мы видим, что амплитуда $| w \rangle$  линейно растет с количеством применений $\sim t N^{-1/2}$. Однако, поскольку мы имеем дело с амплитудами, а не с вероятностями, размерность векторного пространства входит как квадратный корень. Следовательно, в этой процедуре усиливается амплитуда, а не только вероятность.
# 
# В случае, когда существует несколько решений, $M$, можно показать, что примерно $\sqrt{(N/M)}$ вращений будет достаточно.
# 
# 
# ![image5](images/grover_circuit_high_level.png)

# ## 2. Пример: 2 кубита <a id='2qubits'></a>
# 
# Рассмотрим случай алгоритма Гровера для $N= 4$, который реализован с помощью 2 кубитов. В этом конкретном случае требуется только <b> один поворот </b>, чтобы повернуть начальное состояние $|s\rangle$ до победителя $|w\rangle$ [3]:
# 
# <ol>
#     <li>
#         Следуя приведенному выше описанию, в случае $N=4$ имеем угол
# 
# $$\theta = \arcsin \frac{1}{2} = \frac{\pi}{6}.$$
# 
# </li>
# <li>
#         После $t$ шагов, мы имеем  $$(U_s U_\omega)^t  | s \rangle = \sin \theta_t | \omega \rangle + \cos \theta_t | s' \rangle ,$$где $$\theta_t = (2t+1)\theta.$$
# 
# </li>
# <li>
#    
#     Чтобы получить $| \omega \rangle$ нам нужен угол $\theta_t = \frac{\pi}{2}$, который с $\theta=\frac{\pi}{6}$, приведенным выше, приводит к $t=1$. Это означает, что после поворота $t=1$ наш искомый элемент найден. 
#  
# </li>
# </ol>
# 
# Теперь рассмотрим пример с использованием конкретного оракула.
# 
# #### Оракул для  $\lvert \omega \rangle = \lvert 11 \rangle$
# Давайте посмотрим на случай $\lvert w \rangle = \lvert 11 \rangle$. Оракул $U_\omega$ в этом случае действует следующим образом:
# 
# $$U_\omega | s \rangle = U_\omega \frac{1}{2}\left( |00\rangle + |01\rangle + |10\rangle + |11\rangle \right) = \frac{1}{2}\left( |00\rangle + |01\rangle + |10\rangle - |11\rangle \right).$$
# 
# или в матричном представлении:
# 
# $$
# U_\omega = 
# \begin{bmatrix}
# 1 & 0 & 0 & 0 \\
# 0 & 1 & 0 & 0 \\
# 0 & 0 & 1 & 0 \\
# 0 & 0 & 0 & -1 \\
# \end{bmatrix}
# $$
# 
# который вы можете распознать как управляемый Z-вентиль (CZ gate). Таким образом, в этом примере наш оракул - это просто CZ gate:
# 
# ![image6](images/grover_circuit_2qbuits_oracle_11.svg)
# 
# #### Отражение $U_s$
# 
# Для завершения схемы нам необходимо реализовать дополнительное отражение $U_s = 2|s\rangle\langle s| - \mathbb{1}$. Поскольку это отражение относительно $|s\rangle$, мы хотим добавить отрицательную фазу к каждому состоянию, ортогональному к $|s\rangle$. 
# 
# Один из способов сделать это - использовать операцию, которая преобразует состояние $|s\rangle \rightarrow |0\rangle$, которое (как мы видим) является вентилем Адамара, применяемым к каждому кубиту:
# 
# $$H^{\otimes n}|s\rangle = |0\rangle$$
# 
# Затем мы применяем схему, которая добавляет отрицательную фазу к состояниям, ортогональным $|0\rangle$:
# 
# $$U_0 \frac{1}{2}\left( \lvert 00 \rangle + \lvert 01 \rangle + \lvert 10 \rangle + \lvert 11 \rangle \right) = \frac{1}{2}\left( \lvert 00 \rangle - \lvert 01 \rangle - \lvert 10 \rangle - \lvert 11 \rangle \right)$$
# 
# т.е. знаки каждого состояния меняются местами, кроме $\lvert 00 \rangle$. Как легко проверить, одним из способов реализации $U_0$ является следующая схема:
# 
# ![Circuit for reflection around |0>](images/grover_circuit_2qbuits_reflection_0.svg)
# 
# Наконец, мы выполняем операцию, которая преобразует состояние $|0\rangle \rightarrow |s\rangle$ (снова вентиль Адамара):
# 
# $$H^{\otimes n}U_0 H^{\otimes n} = U_s$$
# 
# Полная схема для $ U_s $ выглядит так:
# 
# ![Circuit for reflection around |s>](images/grover_circuit_2qbuits_reflection.svg)
# 
# 
# #### Полная схема для $\lvert w \rangle = |11\rangle$
# Поскольку в частном случае $N=4$ требуется только одно вращение, мы можем объединить вышеуказанные компоненты, чтобы построить полную схему алгоритма Гровера для случая $\lvert w \rangle = |11\rangle$:
# 
# ![image10](images/grover_circuit_2qubits_full_11.svg)
# 
# ### 2.1 Реализация с помощью Qiskit 
# 
# Теперь мы реализуем алгоритм Гровера для указанного выше случая двух кубитов для $\lvert w \rangle = |11\rangle$.

# In[16]:


#initialization
import matplotlib.pyplot as plt
import numpy as np

# importing Qiskit
from qiskit import IBMQ, Aer, assemble, transpile
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.providers.ibmq import least_busy

# import basic plot tools
from qiskit.visualization import plot_histogram


# Начнем с подготовки квантовой схемы с двумя кубитами:

# In[17]:


n = 2
grover_circuit = QuantumCircuit(n)


# Затем нам просто нужно выписать команды для схемы, изображенной выше. Сначала нам нужно инициализировать состояние $|s\rangle$. Давайте создадим общую функцию (для любого количества кубитов), чтобы мы могли использовать ее и потом: 

# In[18]:


def initialize_s(qc, qubits):
    """Apply a H-gate to 'qubits' in qc"""
    for q in qubits:
        qc.h(q)
    return qc


# In[19]:


grover_circuit = initialize_s(grover_circuit, [0,1])
grover_circuit.draw()


# Применим оракул для $|w\rangle = |11\rangle$. Этот оракул относится к 2 кубитам:

# In[20]:


grover_circuit.cz(0,1) # Oracle
grover_circuit.draw()


# <span id="general_diffuser"></span>Теперь мы хотим применить диффузионный оператор ($ U_s $). Как и в случае со схемой, которая инициализирует $|s\rangle$, мы создадим общий оператор (для любого количества кубитов), чтобы мы могли использовать его позже в других задачах. 

# In[21]:


# Diffusion operator (U_s)
grover_circuit.h([0,1])
grover_circuit.z([0,1])
grover_circuit.cz(0,1)
grover_circuit.h([0,1])
grover_circuit.draw()


# Это наша законченная схема.

# ### 2.1.1 Эксперимент с использованием симулятора <a id='2qubits-simulation'></a>
# 
# Запустим схему в симуляции. Во-первых, мы можем проверить, что у нас на выходе есть правильный вектор состояний:

# In[22]:


sv_sim = Aer.get_backend('statevector_simulator')
qobj = assemble(grover_circuit)
result = sv_sim.run(qobj).result()
statevec = result.get_statevector()
from qiskit_textbook.tools import vector2latex
vector2latex(statevec, pretext="|\\psi\\rangle =")


# Как и ожидалось, амплитуда каждого состояния, отличного от $|11\rangle$, равна 0, это означает, что у нас есть 100% шанс измерить $|11\rangle$:

# In[23]:


grover_circuit.measure_all()

qasm_sim = Aer.get_backend('qasm_simulator')
qobj = assemble(grover_circuit)
result = qasm_sim.run(qobj).result()
counts = result.get_counts()
plot_histogram(counts)


# ### 2.1.2 Эксперимент с помощью реального квантового устройства <a id='2qubits-device'></a>
# 
# Мы можем запустить схему на реальном устройстве.

# In[33]:


# Load IBM Q account and get the least busy backend device
from qiskit import IBMQ
IBMQ.load_account()


# In[34]:


provider = IBMQ.get_provider(hub='ibm-q')
for backend in provider.backends():
    print(backend)


# In[35]:


real_device = provider.get_backend('ibmq_belem')


# In[36]:


# Run our circuit on the least busy backend. Monitor the execution of the job in the queue
from qiskit.tools.monitor import job_monitor
transpiled_grover_circuit = transpile(grover_circuit, real_device, optimization_level=3)
qobj = assemble(transpiled_grover_circuit)
job = real_device.run(qobj)
job_monitor(job, interval=2)


# In[37]:


# Get the results from the computation
results = job.result()
answer = results.get_counts(grover_circuit)
plot_histogram(answer)


# 
# Подтверждаем, что в большинстве случаев измеряется состояние $|11\rangle$. Остальные результаты связаны с ошибками квантовых вычислений.

# In[ ]:




