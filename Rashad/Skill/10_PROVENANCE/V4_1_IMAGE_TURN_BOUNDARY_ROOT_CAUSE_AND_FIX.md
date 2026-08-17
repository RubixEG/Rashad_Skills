# v4.1 Root Cause — Image Tool Turn Boundary

During the REDF Version 4 acceptance attempt, the image generator returned the cover hero and the assistant turn ended due to tool behavior. The product workflow had not failed analytically; the orchestration lacked a sufficiently explicit resumable handoff rule at the tool boundary.

v4.1 resolves the issue by treating image generation as a persisted sub-state and requiring continuation from the recorded next step.
