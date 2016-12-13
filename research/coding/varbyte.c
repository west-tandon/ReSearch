#include <Python.c>

static PyObject *
varbyte_encode(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "O", &file))
        return NULL;
    sts = system(command);
    return PyLong_FromLong(sts);
}