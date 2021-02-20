import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
import streamlit as st

header = r'''# *$\alpha$*  and *$\beta$* Tradeoff  in Hypothesis Testing'''

st.markdown(header)

mu_0 = 1
mu_A = 0
stddev = 0.3

dist_0 = norm(mu_0, stddev)
dist_A = norm(mu_A, stddev)

x_min = mu_A - 3*stddev
x_max = mu_0 + 3*stddev
x = np.linspace(x_min,x_max,10000)

y_0 = dist_0.pdf(x)
y_A = dist_A.pdf(x)

_ = st.sidebar.text(f"Mu_0 = {mu_0}")
_ = st.sidebar.text(f"Mu_A = {mu_A}")
_ = st.sidebar.text(f"standard deviation = {stddev}")
alpha = st.sidebar.slider(r"alpha",0.0,0.2,value=0.05,step=0.01)
q_alpha = dist_0.ppf(alpha)
beta = 1 - dist_A.cdf(q_alpha)
_ = st.sidebar.text(f"Beta = {beta:.4f}")
_ = st.sidebar.text(f"Power = {1 - beta:.4f}")


fig, ax = plt.subplots(figsize=(12,6))
ax.plot(x,y_0,color='black')
ax.annotate("null hypothesis",(mu_0 - 0.7*stddev,max(y_0) / 2))
ax.plot(x,y_A,color='black')
ax.annotate("alternative hypothesis",(mu_A - stddev,max(y_A) / 2))
ax.get_yaxis().set_visible(False)

x_type_two = list(filter(lambda a: a > q_alpha,x))
x_type_one = list(filter(lambda a: a <= q_alpha,x))
n_x_type_two = len(x_type_two)
n_x_type_one = len(x_type_one)
ax.fill_between(x_type_two, y_A[-n_x_type_two:], 0, alpha = 0.5, label=r"$\beta$")
ax.fill_between(x_type_one, y_0[:n_x_type_one], 0, alpha = 0.5, label=r"$\alpha$")
plt.legend()

st.write(fig)

explanation = r'''*$\alpha$*, also known as the significance level, is the probability of committing a type I error - rejecting the null hypothesis when it is true.    

*$\beta$* is the probability of committing a type II error - failing to reject the null hypothesis when it is false.   

By playing around with the sliders on the left you can see that choosing the significance level involves a tradeoff between *$\alpha$* and *$\beta$* as reducing one will
cause an increase in the other.

In this example the null hypothesis is that the data comes from a normal distribution with mean 1. The alternative hypothesis is that the mean is 0.'''

st.markdown(explanation)