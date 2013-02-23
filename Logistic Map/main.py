# Ian Johnson.
# http://documen.tician.de/pyopencl/
#
# celita changes in buffers, data and parameters
# for implementation of the logistic map
#

import pyopencl as cl
import numpy
import pylab
import argparse


class CL:
    def __init__(self):
        self.ctx = cl.create_some_context()
        self.queue = cl.CommandQueue(self.ctx)

    def loadProgram(self, filename):
        #read in the OpenCL source file as a string
        f = open(filename, 'r')
        fstr = "".join(f.readlines())
        print fstr
        #create the program
        self.program = cl.Program(self.ctx, fstr).build()

    def logisticMap(self, alpha=0.9, xd=0.2):
        mf = cl.mem_flags

        #initialize client side (CPU) arrays
        self.alpha = numpy.float32(alpha)
        self.xd = numpy.float32(xd)
        self.output = numpy.zeros(100, numpy.float32)
        #create OpenCL buffers
        self.alpha_buf = cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR,
                                   hostbuf=self.alpha)
        self.xd_buf = cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR,
                                self.xd.nbytes, hostbuf=self.xd)
        self.dest_buf = cl.Buffer(self.ctx, mf.READ_WRITE, self.output.nbytes)

    def execute(self):
        #program_name>.<kernel_name>( <command_queue>, <Global_work_size>,
        #       <Local_work_size>, <Parameters_to_kernel.....> )
        self.program.verhulst(self.queue, self.output.shape, (50,),
                              self.alpha_buf, self.xd_buf, self.dest_buf)
        cl.enqueue_copy(self.queue, self.output, self.dest_buf)
        print "alpha: ", self.alpha
        print "xn: ", self.xd
        print "results: ", self.output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
                                     'Logistic Map with control parameter')
    parser.add_argument("--alpha", dest="alpha", default=0.9, 
                        help='This option is used to set the alpha')
    args = parser.parse_args()
    alphaIn = args.alpha

    myLogisticMap = CL()
    myLogisticMap.loadProgram("verhulst.cl")
    myLogisticMap.logisticMap(alpha=alphaIn)
    myLogisticMap.execute()

    pylab.plot(myLogisticMap.output, 'ro-')
    pylab.ylim(0, 1)
    pylab.text(40, 0.2, r'$\alpha = %f$' % (myLogisticMap.alpha))
    pylab.title("Successive Iterations of the logistic Map")
    pylab.show()
