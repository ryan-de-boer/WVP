# WVP
Tools that allow extraction of a WV matrix from a WVP matrix, so you can transform geometry correctly if all you have is a WVP from vertex shader inputs.

__Q:__ Can you extract a world (or world-view) matrix from a World-View-Projection matrix? Some apps might only provide a WVP matrix to vertex shader inputs. If you intercept them you can't transform geometry into world space. Tranforming using the WVP matrix leads to geometry that has been distorted from the projection matrix. I need the world (or world-view) matrix so I can transform geometry without distortion.

__A:__ Yes you can extract the world-view matrix from a World-View-Projection matrix. The key is guessing the projection matrix, and multiplying the WVP matrix by the inverse projection matrix. One way of guessing the projection matrix is by parameterizing the matrix, transforming a 1x1x1 cube by the WVP*P^-1, and checking how close the 1x1x1 cube edges are - is it still 1x1x1 or has it been distorted? You can do a simple coarse search to find the parameters with the least error, or use an algorithm like Nelder-Mead to do a more refined search.

Here is an example app that displays two cubes like BZTuts 10. I have stored an archive of the original webpage in case it ever goes down: [![BzTuts10_archive.7z](archive/BzTuts10_archive.7z)](https://github.com/ryan-de-boer/WVP/raw/refs/heads/main/archive/BzTuts10_archive.7z)
![BZ Tuts 10](images/BZTuts10_example.jpg)

Here is showing PIX displaying the second cubes WVP matrix (row major). PIX (or renderdoc) is useful to understand the WVP matrix if you app supports it.
![PIX](images/PIX.jpg)

Here is showing exported the geometry using just local coordinates (no transform). Both cubes are on top of each other at the origin. If you don't have much geometry you could manually move them in place - eg a tree might just have 2 meshes one for the trunk, one for the leaves. But if your working on a car game, its possible the car has 100 meshes - too many to manually place.
![Local coordinates](images/local.jpg)

Here is showing the distortion that takes place if you use the WVP matrix. The two cubes appear squashed. It is this squashing behaviour we want to stop.
![WVP transform](images/wvp.jpg)

This is the result of exporting the scene using our estimated WV matrix. You can see the cubes are not distorted - yey.
![WV transform](images/wv.jpg)
