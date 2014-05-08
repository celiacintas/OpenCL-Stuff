#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pyopencl as cl
import numpy as np
import pylab

class CL:
    def __init__(self):
        self.ctx = cl.create_some_context()
        self.queue = cl.CommandQueue(self.ctx)

    def loadProgram(self, filename):
        #read in the OpenCL source file as a string
        f = open(filename, 'r')
        fstr = "".join(f.readlines())
        print fstr
        self.program = cl.Program(self.ctx, fstr).build()

    def mandelbrot(self):
        mf = cl.mem_flags
        self.z = np.zeros((1024, 1024), np.uint8)
        self.z_buff = cl.Buffer(self.ctx, mf.READ_WRITE, self.z.nbytes)

    def execute(self):
        #program_name>.<kernel_name>( <command_queue>, <Global_work_size>,
        #       <Local_work_size>, <Parameters_to_kernel.....> )
        self.program.mandelbrot(self.queue, self.z.shape, None,
                                self.z_buff)
        cl.enqueue_copy(self.queue, self.z, self.z_buff)
        print ":D"


if __name__ == "__main__":
    my_mandelbrot = CL()
    my_mandelbrot.loadProgram("mandelbrot.cl")
    my_mandelbrot.mandelbrot()
    my_mandelbrot.execute()

    pylab.imshow(my_mandelbrot.z)
    pylab.imsave('/tmp/save.png', my_mandelbrot.z)
    pylab.title("Mandelbrot with PyOpenCL")
    pylab.show()