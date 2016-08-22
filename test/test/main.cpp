#ifdef _DEBUG
#undef _DEBUG
#include <Python.h>
#define _DEBUG
#else
#include <Python.h>
#endif

static PyObject* random(PyObject* self, PyObject* args)
{
	/* initialize random seed: */
	srand(time(NULL));
	int random = rand() % 10;
	PyObject * python_val = Py_BuildValue("i", random);
	return python_val;
}

PyMODINIT_FUNC initmy_math(void)
{
	static PyMethodDef methods[] = {
		{ "random", random, METH_NOARGS,
		"Generate random number betweeen 0-9" },
		{ NULL, NULL, 0, NULL }
	};

	PyObject *m = Py_InitModule("my_math", methods);
}