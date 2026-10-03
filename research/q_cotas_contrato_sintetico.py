"""Arithmetic contrast of two Q error bounds; no camera or human measurements."""

from math import sqrt


def main():
    observed_lengths = (1.0, 0.001)
    point_error_max = (0.0005, 0.0005, 0.0005)
    edge_errors = tuple(a + b for a, b in zip(point_error_max, point_error_max[1:]))
    e = sum(edge_errors)
    observed_arc = sum(observed_lengths)
    assert observed_arc > e
    direct_worst = min(1.0, (2 / sqrt(3) + 1) * e / (observed_arc - e))
    assert 0 < direct_worst < 0.00432
    assert observed_lengths[1] <= edge_errors[1]
    angular_v0 = 1.0  # A 90-degree-or-worse uncertain segment forces sin(alpha)=1.
    assert angular_v0 > 200 * direct_worst
    print(f"E={e:.6f} m; Lhat={observed_arc:.6f} m; "
          f"B_pos_worst={direct_worst:.9f}; B_angular_v0={angular_v0:.1f}")


if __name__ == "__main__":
    main()
