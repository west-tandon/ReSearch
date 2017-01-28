#include <Python.h>
#include <sys/stat.h>

static const int BUFFER_SIZE = 1024 * 1024;

off_t file_size(int fd)
{
    struct stat buffer;
    int status;
    status = fstat(fd, &buffer);
    if (status == -1) exit(errno);
    return buffer.st_size;
}

char* readable_fs(double size, char *buf) {
    int i = 0;
    const char* units[] = {"B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"};
    while (size > 1024) {
        size /= 1024;
        i++;
    }
    sprintf(buf, "%.*f %s", i, size, units[i]);
    return buf;
}

void log_process(off_t processed_bytes, off_t total_bytes)
{
    char processed[10], total[10];
    readable_fs(processed_bytes, processed);
    readable_fs(total_bytes, total);
    fprintf(stderr, "Processed %s/%s, %ld%%\n", processed, total, (100 * processed_bytes) / total_bytes);
}

static PyObject *
research_c_utils_flip_most_significant_bits(PyObject *self, PyObject *args)
{
    PyObject *input_stream, *output_stream;

    if (!PyArg_ParseTuple(args, "OO", &input_stream, &output_stream))
        return NULL;

    int in = PyObject_AsFileDescriptor(input_stream);
    int out = PyObject_AsFileDescriptor(output_stream);

    off_t total_bytes = file_size(in);
    off_t processed_bytes = 0;

    time_t start, current;
    start = time(NULL);

    unsigned char buffer[BUFFER_SIZE];
    int n;
    while ((n = read(in, buffer, BUFFER_SIZE)) != 0) {
        if (n == -1) return NULL;
        processed_bytes += n;
        int i;
        for (i = 0; i < n; i++) buffer[i] ^= 0x80;
        if (write(out, buffer, n) == -1) return NULL;
        current = time(NULL);
        if (current != start) {
            start = current;
            log_process(processed_bytes, total_bytes);
        }
    }

    if (close(in) == -1) return NULL;
    if (close(out) == -1) return NULL;

    log_process(processed_bytes, total_bytes);

    Py_RETURN_NONE;
}

static PyMethodDef SpamMethods[] = {
    {"flip_most_significant_bits",  (PyCFunction)research_c_utils_flip_most_significant_bits, METH_VARARGS,
    "Flip most significant bits in each byte reading from a file and write to another."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef research_c_utilsmodule = {
   PyModuleDef_HEAD_INIT,
   "research_c_utils",   /* name of module */
   NULL, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   SpamMethods
};

PyMODINIT_FUNC
PyInit_research_c_utils(void)
{
    return PyModule_Create(&research_c_utilsmodule);
}