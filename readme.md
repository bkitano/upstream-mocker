https://gist.github.com/takuma7/44f9ecb028ff00e2132e

If you linearly interpolate the mouse movements, you don't need to use the screen recorder at all.

1. Make all the mock screens at each stage
    1. Original screen, mouse is anywhere
    2. Dark screen with popup, mouse still on original button
    3. Dark screen with popup, mouse at video starting position (first_frame)

Then linearly interpolate the scenes between 1-2 and 2-3. You'll need 
1. mocks from each scene without the cursor present.
2. mocks from each scene with the starting cursor positions.