import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

x = np.array([1, 2, 3, 4, 5])
y = np.array([5, 7, 9, 11, 13])

# We started with 10
ITERATIONS = 100000

# Need to start with something
# We started with 0.1 to find the decreasing cost
# If we start with 1 -> cost increases
# If we start with 0.1 -> cost decreases
LEARNING_RATE = 0.08


def gradient_descent(x, y, iterations=ITERATIONS, learning_rate=LEARNING_RATE):
    """
    Gradient means -> walk downhill step by step to reach global minima
    """
    # we start with some value of m and b to reach global minima
    m_curr = b_curr = 0
    n = len(x)

    cost_history = []
    grad_history = []
    m_history = []
    b_history = []

    for i in range(iterations):
        y_predicted = m_curr * x + b_curr

        # Section 5: "linear_regression.ipynb"
        """
        This computes gradient for y = wx + b
        md: Gradient for weight(m)
        bd: Gradient for bias(b)

        -> How to compute gradient?
        |-------------|----------------------------------|
        | Method		  | Computation                      |
        |-------------|----------------------------------|
        | NumPy       | Manual Computation               |
        | sklearn     | model.coef_ and model.intercept_ |
        | Pytorch			|  loss.backward()                 |
        | TensorFlow  |  GradientTape                    |
        |-------------|----------------------------------|

        -> When to use what?
        |-------------------------|-----------------------|
        | Normal equation         | small datasets        |
        | SVD / least squares     | most libraries        |
        | Gradient descent        | huge datasets         |
        |-------------------------|-----------------------|

        For Linear Regression: gradient descent is actually inferior.
        For linear regression the analytical solution is:

        $\theta = (X^TX)^{-1}X^Ty$

        Computing this requires matrix inversion -> Cost: O(n^3)
        If you have:
        •	10 features → trivial
        •	1000 features → expensive
        •	100k features → basically impossible
        Gradient descent scales much better -> O(n \times iterations)
        So large feature spaces → gradient descent wins.

        For Simple Linear Regression Problem:
          from sklearn.linear_model import LinearRegression
        It uses SVD decomposition, which is:
          •	faster
          •	numerically stable
          •	exact

        |-------------------------|-----------------------|
        | Situation               | Use                   |
        |-------------------------|-----------------------|
        | Small linear regression | Linear algebra        |
        | Many features           | Gradient descent      |
        | Deep learning           | Gradient descent      |
        | Huge datasets           | SGD                   |
        | Real-time updates       | Gradient descent      |
        |-------------------------|-----------------------|
        """
        md = -(2 / n) * np.sum(x * (y - y_predicted))
        bd = -(2 / n) * np.sum(y - y_predicted)

        # Section 5: "linear_regression.ipynb"
        m_curr = m_curr - learning_rate * md
        b_curr = b_curr - learning_rate * bd

        # Our main goal is to decrease the COST i.e MSE (Mean square error)
        # We can also simplify the cost function if using numpy `np.square(y - y_pred).mean()`
        # if we using sklearn we can use `from sklearn.metrics import mean_squared_error; mean_squared_error(y, y_pred)`
        # if we using tensorflow we can use `tf.keras.metrics.mean_squared_error(y, y_pred)`
        # if we using pytorch we can use `torch.nn.functional.mse_loss(y, y_pred)`

        """
        |-------------------------------|----------------------|
        | Scenario							        | Tool                 |
        |-------------------------------|----------------------|
        | Data science / analysis				|	NumPy                |
        | ML pipelines	    						| sklearn              |
        | Deep learning training				|	PyTorch / TensorFlow |
        | Quick scripts									| NumPy                |
        |-------------------------------|----------------------|
        """
        """
        For large datasets the bottleneck is not the math.
        It’s:
        •	memory bandwidth
        •	temporary array allocations
        •	data transfer CPU ↔ GPU
        ------------------------------------------------------
        Q: How to  compute metrics on billions of samples without loading everything into memory? or compute MSE on datasets that don’t fit into RAM?.
        A: Short answer -> Streaming / Chunking / Batching or Streaming MSE
        ------------------------------------------------------
        Large-scale ML pipelines often use:
        •	Apache Spark
        •	Apache Flink
        •	Apache Beam
        All compute metrics using incremental aggregation.
        """
        cost = (1 / n) * np.sum([val**2 for val in (y - y_predicted)])

        # We store the cost history to plot it later
        cost_history.append(cost)
        # Gradient magnitude: combined size of m and b gradients
        grad_history.append(np.sqrt(md**2 + bd**2))
        m_history.append(m_curr)
        b_history.append(b_curr)

        # We print the cost history to see the cost decreasing
        # print(f"m: {m_curr:.4f}, b: {b_curr:.4f}, cost: {cost_history[-1]:.6f}")

    print(f"Final -> m: {m_curr:.4f}, b: {b_curr:.4f}, cost: {cost_history[-1]:.6f}")

    # =====================================================================================
    #
    # - Below Logic is generated using AI to animate to show the working of gradient descent
    #
    # ======================================================================================

    # ── Animation: line gradually fitting the data ─────────────────────────────
    # Sub-sample with log-spacing so the fast early drop gets most of the frames
    # (linear sampling would waste all frames on the flat near-zero tail)
    n_frames = 200
    log_indices = np.unique(
        np.geomspace(1, iterations, n_frames, dtype=int) - 1
    ).tolist()
    frame_indices = [0] + log_indices  # always start from iteration 0

    x_line = np.linspace(x.min() - 0.5, x.max() + 0.5, 200)

    fig, ax = plt.subplots(figsize=(7, 5))
    fig.suptitle("Gradient Descent – Line Converging", fontsize=13, fontweight="bold")

    ax.scatter(x, y, color="steelblue", s=80, zorder=5, label="Actual data")
    (pred_line,) = ax.plot([], [], color="tomato", linewidth=2, label="Predicted line")
    info_text = ax.text(
        0.05,
        0.95,
        "",
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.8),
    )

    ax.set_xlim(x.min() - 0.5, x.max() + 0.5)
    ax.set_ylim(y.min() - 2, y.max() + 2)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="lower right")

    def update(frame_idx):
        i = frame_indices[frame_idx]
        m_f, b_f = m_history[i], b_history[i]
        pred_line.set_data(x_line, m_f * x_line + b_f)
        info_text.set_text(
            f"Iteration : {i:>6}\n"
            f"m         : {m_f:.4f}\n"
            f"b         : {b_f:.4f}\n"
            f"Cost (MSE): {cost_history[i]:.4e}"
        )
        return pred_line, info_text

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(frame_indices),
        interval=30,  # ms between frames
        blit=True,
        repeat=False,
    )

    plt.tight_layout()
    plt.show()

    return ani  # keep reference alive so GC doesn't kill the animation


if __name__ == "__main__":
    _ = gradient_descent(x, y)
