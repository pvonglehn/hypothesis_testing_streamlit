"""
## Hypothesis testing alpha vs beta tradeoff

This app explores the tradeoff between alpha and beta in hypothesis testing.

Author: [Patrick von Glehn](https://www.linkedin.com/in/patrickvonglehn)\n
Source: [Github](https://github.com/pvonglehn/hypothesis_testing_streamlit)
"""

import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
import streamlit as st

def get_distributions(mu_0, mu_A, stddev):
    """Get distribution objects"""

    dist_0 = norm(mu_0, stddev)
    dist_A = norm(mu_A, stddev)

    return dist_0, dist_A

def get_parameters(dist_0, dist_A):
    """Get statistical parameters and properties alpha, q_alpha and beta"""

    alpha = st.slider(r"alpha",0.0,0.2,value=0.05,step=0.001)
    q_alpha = dist_0.ppf(1 - alpha)
    beta = 1 - dist_A.cdf(q_alpha)

    return alpha, q_alpha, beta

def make_figure(dist_0, dist_A, stddev, q_alpha):
    """Create matplotlib figure"""

    mu_0 = dist_0.mean()
    mu_A = dist_A.mean()

    # get the points to plot for null and alternative distributions
    x_min = mu_A + 3*stddev
    x_max = mu_0 - 3*stddev
    x = np.linspace(x_min,x_max,10000)
    y_0 = dist_0.pdf(x)
    y_A = dist_A.pdf(x)

    # plot null and alternative distributions
    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot(x,y_0,color='black')
    ax.annotate("null hypothesis",(mu_0 - 0.7*stddev,max(y_0) / 2))
    ax.plot(x,y_A,color='black')
    ax.annotate("alternative hypothesis",(mu_A - stddev,max(y_A) / 2))
    
    # plot the areas under the curves
    x_beta = list(filter(lambda a: a < q_alpha,x))
    x_alpha = list(filter(lambda a: a >= q_alpha,x))
    n_x_beta = len(x_beta)
    n_x_alpha = len(x_alpha)
    ax.fill_between(x_beta, y_A[-n_x_beta:], 0, alpha = 0.5, label=r"$\beta$")
    ax.fill_between(x_alpha, y_0[:n_x_alpha], 0, alpha = 0.5, label=r"$\alpha$")

    ax.axvline(q_alpha,color='black',linestyle="--",label="q_alpha")

    plt.legend()
    ax.get_yaxis().set_visible(False)

    st.pyplot(fig)

def plot_sidebar(mu_A, mu_0, stddev, beta, alpha):
    """Plot sidebar stats"""

    for s in [
        f"Mu_0 = {mu_0}",
        f"Mu_A = {mu_A}",
        f"standard deviation = {stddev}",
        f"Alpha = {alpha:.4f}",
        f"Beta = {beta:.4f}",
        f"Power = {1 - beta:.4f}"]:

        st.sidebar.text(s)

st.set_page_config(layout="wide")

mu_0 = 0
mu_A = 1
stddev = 0.3

header = r'''# *$\alpha$*  and *$\beta$* Tradeoff  in Hypothesis Testing'''
st.markdown(header)

dist_0, dist_A = get_distributions(mu_0, mu_A, stddev)
alpha, q_alpha, beta = get_parameters(dist_0, dist_A)

make_figure(dist_0, dist_A, stddev, q_alpha)
plot_sidebar(mu_A, mu_0, stddev, beta, alpha)


explanation = rf'''$\alpha$, also known as the significance level, is the probability of committing a type I error - 
rejecting the null hypothesis when it is true.    

$\beta$ is the probability of committing a type II error - failing to reject the null hypothesis when it is false. 

By playing around with the slider you can see that choosing the significance level involves a tradeoff 
between $\alpha$ and $\beta$ as reducing one will
cause an increase in the other.

In this example the null hypothesis is that the data comes from a normal distribution with mean {mu_0} and standard deviation {stddev}. 
The alternative hypothesis is that the mean is {mu_A}.'''
st.markdown(explanation)

