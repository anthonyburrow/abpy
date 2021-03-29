import numpy as np
from mypytools.math.multigauss import MultiGauss


con_colors = ['#bdbdbd', '#595959', '#1f1f1f', 'k']


def draw_contours(
        axis, gmm, xbounds, ybounds, which=(0, 1), con_density=400, alpha=0.7):
    """Draw 2D (filled) contours on axis with 1-, 2-, 3-sigma levels"""
    assert len(which) == 2

    con0 = np.linspace(*xbounds, con_density)
    con1 = np.linspace(*ybounds, con_density)

    n_components = gmm.means_.shape[0]
    for i in range(n_components):
        mu = gmm.means_[i]
        cov = gmm.covariances_[i]
        gauss = MultiGauss(mu, cov)

        con_in = np.array((con0, con1)).T
        z_con = gauss.proj_pdf(con_in, which=which, ravel=False)

        sig = 1 / np.sqrt(gauss.cov_inv[which[0], which[0]])
        sig_point = mu.copy()

        z_levels = []
        for level in range(3):
            sig_point[which[0]] += sig

            z_level = gauss.pdf(sig_point)
            z_levels.append(z_level)
        z_levels = list(reversed(z_levels))
        z_levels.append(1.1)

        for j in range(3):
            axis.contourf(con0, con1, z_con, levels=[z_levels[j], 1.5],
                          colors=[con_colors[j], 'k'], alpha=alpha,
                          antialiased=True, zorder=j - 3)


def draw_3sig_contour(
        axis, gmm, xbounds, ybounds, which=(0, 1), con_density=400):
    """Draw 2D (filled) contours on axis with 1-, 2-, 3-sigma levels"""
    assert len(which) == 2

    con0 = np.linspace(*xbounds, con_density)
    con1 = np.linspace(*ybounds, con_density)

    n_components = gmm.means_.shape[0]
    for i in range(n_components):
        mu = gmm.means_[i]
        cov = gmm.covariances_[i]
        gauss = MultiGauss(mu, cov)

        con_in = np.array((con0, con1)).T
        z_con = gauss.proj_pdf(con_in, which=which, ravel=False)

        sig = 1 / np.sqrt(gauss.cov_inv[which[0], which[0]])
        sig_point = mu.copy()
        sig_point[which[0]] += 3 * sig
        z_level = gauss.pdf(sig_point)

        axis.contour(con0, con1, z_con, levels=[z_level, 100],
                     colors='k', antialiased=True)
