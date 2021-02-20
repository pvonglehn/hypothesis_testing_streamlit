import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
import streamlit as st

header = '''# Hypothesis testing

## Type I and Type II error tradeoff '''

st.markdown(header)

x = np.linspace(0,10,10000)

mu_0 = st.sidebar.slider(r"theta_0",0.0,10.0,6.0,0.1)
mu_A = st.sidebar.slider(r"theta_A",0.0,10.0,3.0,0.1)

y_0 = norm(mu_0).pdf(x)
y_A = norm(mu_A).pdf(x)

alpha = st.sidebar.slider(r"alpha",0.0,0.2,value=0.05,step=0.01)
q_alpha = norm(mu_0).ppf(alpha)
beta = 1 - norm(mu_A).cdf(q_alpha)
_ = st.sidebar.text(f"beta = {beta:.4f}")

fig, ax = plt.subplots()
ax.plot(x,y_0,color='black')
ax.plot(x,y_A,color='black')
ax.get_yaxis().set_visible(False)

x_type_two = list(filter(lambda a: a > q_alpha,x))
x_type_one = list(filter(lambda a: a <= q_alpha,x))
n_x_type_two = len(x_type_two)
n_x_type_one = len(x_type_one)
ax.fill_between(x_type_two, y_A[-n_x_type_two:], 0, alpha = 0.5, label="Type II error")
ax.fill_between(x_type_one, y_0[:n_x_type_one], 0, alpha = 0.5, label="Type I error")
plt.legend()

st.write(fig)