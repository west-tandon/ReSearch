#include <Python.h>

static PyObject *
rsutils_flip_most_significant_bits(PyObject *self, PyObject *args)
{
    PyObject *input_stream, *output_stream;

    if (!PyArg_ParseTuple(args, "OO", &input_stream, &output_stream))
        return NULL;

    int in = PyObject_AsFileDescriptor(input_stream);
    int out = PyObject_AsFileDescriptor(output_stream);

    unsigned char c;
    int n;
    while ((n = read(in, &c, sizeof(c))) != 0) {
        if (n == -1) return NULL;
        c ^= 0x80;
        if (write(out, &c, sizeof(c)) == -1) return NULL;
    }

    if (close(in) == -1) return NULL;
    if (close(out) == -1) return NULL;

    Py_RETURN_NONE;
}

static PyMethodDef SpamMethods[] = {
    {"flip_most_significant_bits",  (PyCFunction)rsutils_flip_most_significant_bits, METH_VARARGS,
    "Flip most significant bits in each byte reading from a file and write to another."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef rsutilsmodule = {
   PyModuleDef_HEAD_INIT,
   "rsutils",   /* name of module */
   NULL, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   SpamMethods
};

PyMODINIT_FUNC
PyInit_rsutils(void)
{
    return PyModule_Create(&rsutilsmodule);
}