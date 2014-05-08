__kernel void mandelbrot(global char* i_buffer)
{
	int row = get_local_id(1) + get_local_size(1)*get_group_id(1);
    int col = get_local_id(0) + get_local_size(0)*get_group_id(0);
    int idx = row * 1024 + col;

    float x0 = ((float)col / 1024) * 3.5f - 2.5f;
    float y0 = ((float)row / 1024) * 3.5f - 1.75f;
    float x = 0.0f;
	float y = 0.0f;
	int iter = 0;
	float xtemp;
	while((x * x + y * y <= 4.0f) && (iter < idx))
	{ 
		xtemp = x * x - y * y + x0;
		y = 2.0f * x * y + y0;
		x = xtemp;
		iter++;
	}

	int color = iter * 5;
	if (color >= 256) color = 0;
	i_buffer[idx] = color;
}


    