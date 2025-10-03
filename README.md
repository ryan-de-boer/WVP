# WVP
Tools that allow extraction of a WV matrix from a WVP matrix, so you can transform geometry correctly if all you have is a WVP from vertex shader inputs.

__Q:__ Can you extract a world (or world-view) matrix from a World-View-Projection matrix? Some apps might only provide a WVP matrix to vertex shader inputs. If you intercept them you can't transform geometry into world space. Tranforming using the WVP matrix leads to geometry that has been distorted from the projection matrix. I need the world (or world-view) matrix so I can transform geometry without distortion.

__A:__ Yes you can extract the world-view matrix from a World-View-Projection matrix. The key is guessing the projection matrix, and multiplying the WVP matrix by the inverse projection matrix. One way of guessing the projection matrix is by parameterizing the matrix, transforming a 1x1x1 cube by the WVP*P^-1, and checking how close the 1x1x1 cube edges are - is it still 1x1x1 or has it been distorted? You can do a simple coarse search to find the parameters with the least error, or use an algorithm like Nelder-Mead to do a more refined search.
