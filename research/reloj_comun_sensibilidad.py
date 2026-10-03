"""Population sensitivity for the shared-noisy-clock counterexample.

All quantities are variance units of the same synthetic timing offset.
This is a design calculator, not a fitted model of cameras or people.
"""

import argparse
import json
import math


def artifact_covariance(drive_variance, clock_variance):
    if clock_variance == 0:
        return 0.0
    return drive_variance * clock_variance / (drive_variance + clock_variance)


def artifact_correlation(drive_variance, clock_variance, hand_variance):
    common = artifact_covariance(drive_variance, clock_variance)
    return common / (common + hand_variance)


def maximum_clock_variance_for_target(target, drive_variance, hand_variance):
    common_limit = hand_variance * target / (1 - target)
    if common_limit >= drive_variance:
        return math.inf
    return drive_variance * common_limit / (drive_variance - common_limit)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--drive-variance", type=float, default=1.0)
    parser.add_argument("--hand-variance", type=float, default=0.09)
    parser.add_argument("--target-artifact-correlation", type=float, default=0.1)
    args = parser.parse_args()
    if args.drive_variance <= 0 or args.hand_variance <= 0:
        parser.error("variances must be positive")
    if not 0 < args.target_artifact_correlation < 1:
        parser.error("target correlation must lie strictly between zero and one")

    ceiling = maximum_clock_variance_for_target(
        args.target_artifact_correlation, args.drive_variance, args.hand_variance
    )
    example_clock_variances = [0.0, 0.01, 0.05, 0.25, 1.0]
    report = {
        "scope": "synthetic_population_linear_residual_model_not_camera_or_human_data",
        "drive_variance": args.drive_variance,
        "hand_variance_each": args.hand_variance,
        "target_artifact_correlation": args.target_artifact_correlation,
        "maximum_clock_variance_for_target": ceiling if math.isfinite(ceiling) else None,
        "maximum_clock_sd_for_target": math.sqrt(ceiling) if math.isfinite(ceiling) else None,
        "sweep": [
            {
                "clock_variance": value,
                "artifact_covariance": artifact_covariance(args.drive_variance, value),
                "artifact_correlation": artifact_correlation(args.drive_variance, value, args.hand_variance),
            }
            for value in example_clock_variances
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
