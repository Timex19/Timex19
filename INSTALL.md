# Add the design to your GitHub profile

1. Open the `Timex19/Timex19` repository.
2. Replace its root `README.md` with this folder's `README.md`.
3. Copy the complete `assets` folder into the repository root, beside `README.md`.
4. Commit the README and assets together, then check your profile.

The artwork uses relative paths, so the README and assets must stay together. The supplied ZIP contains the correct folder structure.

The local preview approximates GitHub's layout. Its badge images are locally generated stand-ins for Shields.io; actual badge rendering and the optional statistics card depend on their external services.

To edit the custom artwork or regenerate the README, modify `build-profile.py` and run `python docs/github-profile/build-profile.py` from this workspace. The preview uses the existing client development dependencies and Microsoft Edge: `node docs/github-profile/preview-profile.cjs`.
