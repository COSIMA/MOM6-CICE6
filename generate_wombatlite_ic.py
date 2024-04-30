# Copyright 2023 ACCESS-NRI and contributors. See the top-level COPYRIGHT file for details.
# SPDX-License-Identifier: Apache-2.0

# =========================================================================================
# Generate constant initial conditions for WOMBATlite using grid from a provided file
#
# To run:
#   python generate_wombatlite_ic.py --grid-filename=<path-to-grid-file>
#       --variable-name=<variable-name> --ic-filename=<path-to-output-file>
#
# For more information, run `python generate_wombatlite_ic.py -h`
#
# Contact:
#   Dougie Squire <dougal.squire@anu.edu.au>
#
# Dependencies:
#   argparse, xarray
# =========================================================================================

import os
import subprocess
import xarray as xr


def is_git_repo():
    """
    Return True/False depending on whether or not the current directory is a git repo.
    """

    return subprocess.call(
        ['git', '-C', '.', 'status'],
        stderr=subprocess.STDOUT,
        stdout = open(os.devnull, 'w')
    ) == 0

def git_info():
    """
    Return the git repo origin url, relative path to this file, and latest commit hash.
    """

    url = subprocess.check_output(
        ["git", "remote", "get-url", "origin"]
    ).decode('ascii').strip()
    top_level_dir = subprocess.check_output(
        ['git', 'rev-parse', '--show-toplevel']
    ).decode('ascii').strip()
    rel_path = os.path.relpath(__file__, top_level_dir)
    hash = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD']
    ).decode('ascii').strip()

    return url, rel_path, hash

def main():
    parser = argparse.ArgumentParser(
        description="Generate constant initial conditions for WOMBATlite using grid from provided file."
    )

    parser.add_argument(
        "--grid-filename",
        required=True,
        help="The path to a file containing a variable to copy the grid from.",
    )

    parser.add_argument(
        "--variable-name",
        required=True,
        help="The name of the variable to copy the grid from.",
    )

    parser.add_argument(
        "--ic-filename",
        required=True,
        help="The path to the initial condition file to be outputted.",
    )

    args = parser.parse_args()
    grid_filename = args.grid_filename
    variable_name = args.variable_name
    ic_filename = args.ic_filename

    # Add some info about how the file was generated
    runcmd = (
        f"python3 {__file__} --grid-filename={os.path.abspath(grid_filename)} "
        f"--variable-name={variable_name} --ic-filename={os.path.abspath(ic_filename)}"
    )

    if is_git_repo():
        url, rel_path, hash = git_info()
        prepend = f"Created using commit {hash} of {rel_path} in {url}: "
    else:
        prepend = "Created using: "

    global_attrs = {"history": prepend + runcmd}

    # Generate the initial conditions
    init_vars = {
        "phy": (0.01e-6, "mol kg-1"),
        "zoo": (0.01e-6, "mol kg-1"),
        "det": (0.01e-6, "mol kg-1"),
        "caco3": (0.01e-6, "mol kg-1"),
        "det_sediment": (0.0, "mol m-2"),
        "caco3_sediment": (0.0, "mol m-2"),
    }

    xr.set_options(keep_attrs=True)
    template = xr.open_dataset(
        grid_filename,
        decode_cf=False,
        decode_times=False,
    )[variable_name].compute()
    ds = {}
    for name, (const, units) in init_vars.items():
        da = 0 * template + const
        da.attrs["units"] = units
        da.attrs["long_name"] = name
        ds[name] = da
    ds = xr.Dataset(ds)
    ds.attrs = global_attrs

    ds.to_netcdf(ic_filename)

if __name__ == "__main__":
    import argparse

    main()
