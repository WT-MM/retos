"""Script to check GPR joint positions in MuJoCo."""

import argparse

import numpy as np

from retos.configs import GPR_CONFIG, Cfg
from retos.mujoco.replay import run_mujoco_orientation, run_mujoco_positions

SAVED_POSITIONS_PATH = "gpr_lr_legs.npy"
SAVED_ORIENTATIONS_PATH = "imu_log.npy"

if __name__ == "__main__":
    assert isinstance(GPR_CONFIG["config"], Cfg)
    assert isinstance(GPR_CONFIG["path"], str)

    parser = argparse.ArgumentParser()
    parser.add_argument("--pos", action="store_true", help="Replay positions")
    parser.add_argument("--ori", action="store_true", help="Replay orientations")
    args = parser.parse_args()

    if args.pos:
        positions = np.load(SAVED_POSITIONS_PATH)
        positions = positions[400:]  # skip the first 100

        print(f"Loaded positions: {positions}")

        # Real to sim mapping
        signs = np.array([-1, 1, 1, -1, 1, -1, 1, 1, -1, 1])

        sim_positions = np.deg2rad(positions)

        sim_positions = sim_positions * signs[None, :]

        run_mujoco_positions(GPR_CONFIG["path"], GPR_CONFIG["config"].sim, sim_positions, timescale=0.1)

    if args.ori:
        orientations = np.load(SAVED_ORIENTATIONS_PATH)

        # orientations = np.array([[0, 0, 0]]*1000)

        signs = np.array([-1, -1, -1])

        sim_orientations = np.deg2rad(orientations)

        sim_orientations = sim_orientations * signs[None, :]

        run_mujoco_orientation(GPR_CONFIG["path"], GPR_CONFIG["config"].sim, sim_orientations, timescale=10)
