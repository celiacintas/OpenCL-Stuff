/*kernel by celita for implementing the Verhulst model.
Fractal and Chaos - Chapter 5 - Iterative Feedback Processes and Chaos. */

__kernel void verhulst(global float* alpha, global float* xd, global float* output)
{
    float temp;
    int idx = get_local_id(0)+get_local_size(0)*get_group_id(0);
    temp = xd[0];
    int i;
    for(i=0;i<=idx;i++)
    {
        temp = alpha[0]*temp*(1-temp);
    }
    output[idx] = temp;
}

