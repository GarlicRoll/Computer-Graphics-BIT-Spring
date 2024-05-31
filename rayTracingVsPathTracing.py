import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import time
import threading
import tkinter as tk

from vertexShader import vertex_shader
from rayTracingFragmentShader import ray_tracing_fragment_shader
from pathTracingFragmentShader import path_tracing_fragment_shader

def create_shader_program(vertex_src, fragment_src):
    vertex_shader = compileShader(vertex_src, GL_VERTEX_SHADER)
    fragment_shader = compileShader(fragment_src, GL_FRAGMENT_SHADER)
    shader = compileProgram(vertex_shader, fragment_shader)
    return shader


def start_tkinter_app(sphere_center):
    def update_position(event):
        sphere_center[0] = x_slider.get()
        sphere_center[1] = y_slider.get()
        sphere_center[2] = z_slider.get()

    root = tk.Tk()
    root.title("Sphere Position")

    x_slider = tk.Scale(root, from_=-2.0, to=2.0, resolution=0.01, orient='horizontal', label='X',
                        command=update_position)
    x_slider.pack(fill='x')
    y_slider = tk.Scale(root, from_=-2.0, to=2.0, resolution=0.01, orient='horizontal', label='Y',
                        command=update_position)
    y_slider.pack(fill='x')
    z_slider = tk.Scale(root, from_=-2.0, to=2.0, resolution=0.01, orient='horizontal', label='Z',
                        command=update_position)
    z_slider.pack(fill='x')

    root.mainloop()


def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 800, "Ray Tracing vs Path Tracing", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    vertices = np.array([
        -1.0, -1.0, 0.0,
        1.0, -1.0, 0.0,
        1.0, 1.0, 0.0,
        -1.0, 1.0, 0.0,
    ], dtype=np.float32)

    indices = np.array([
        0, 1, 2,
        2, 3, 0,
    ], dtype=np.uint32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    ray_tracing_shader = create_shader_program(vertex_shader, ray_tracing_fragment_shader)
    path_tracing_shader = create_shader_program(vertex_shader, path_tracing_fragment_shader)

    start_time = time.time()
    fps_counter = 0
    fps_time = time.time()
    current_shader = ray_tracing_shader
    technique_name = "Ray Tracing"
    swap_interval = 5  # Swap every 5 seconds

    sphere_center = [0.0, 0.0, 0.0]

    # Start the Tkinter GUI in a separate thread
    threading.Thread(target=start_tkinter_app, args=(sphere_center,), daemon=True).start()

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(current_shader)
        sphere_center_loc = glGetUniformLocation(current_shader, "sphereCenter")
        glUniform3f(sphere_center_loc, *sphere_center)

        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)

        fps_counter += 1
        current_time = time.time()

        if current_time - fps_time >= 1.0:
            fps = fps_counter / (current_time - fps_time)
            fps_time = current_time
            fps_counter = 0
            glfw.set_window_title(window, f"{technique_name} - FPS: {fps:.2f}")

        if current_time - start_time >= swap_interval:
            start_time = current_time
            if current_shader == ray_tracing_shader:
                current_shader = path_tracing_shader
                technique_name = "Path Tracing"
            else:
                current_shader = ray_tracing_shader
                technique_name = "Ray Tracing"

    glDeleteVertexArrays(1, vao)
    glDeleteBuffers(1, vbo)
    glDeleteBuffers(1, ebo)

    glfw.terminate()


if __name__ == "__main__":
    main()
